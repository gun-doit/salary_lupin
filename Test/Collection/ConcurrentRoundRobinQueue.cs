namespace Robust.Core.Collection
{
	/// <summary>
	/// 동시성을 보장하는 라운드로빈 큐
	/// </summary>
	/// <typeparam name="TKey"></typeparam>
	/// <typeparam name="TValue"></typeparam>
	public sealed class ConcurrentRoundRobinQueue<TKey, TValue>
	{
		private readonly Dictionary<TKey, Queue<TValue>> keyValueDict = [];
		private readonly List<TKey> keyList = [];

		private int idx;
		private readonly Lock lockObject = new();

		public int Count
		{
			get
			{
				var count = 0;

				foreach(var d in this.keyValueDict)
				{
					count += d.Value.Count;
				}

				return count;
			}
		}

		/// <summary>
		/// 해당 키로 값을 큐에 추가합니다.
		/// </summary>
		/// <param name="key">키</param>
		/// <param name="value">추가할 값</param>
		/// <returns>성공 여부</returns>
		public bool TryEnqueue(TKey key, TValue value)
		{
			lock(this.lockObject)
			{
				if(this.keyValueDict.Count == int.MaxValue)
					return false;

				if(!this.keyValueDict.TryGetValue(key, out var queue))
				{
					queue = new Queue<TValue>();

					this.keyList.Add(key);
					this.keyValueDict.Add(key, queue);
				}

				if(queue.Count == int.MaxValue)
					return false;

				queue.Enqueue(value);
				return true;
			}
		}

		/// <summary>
		/// 라운드로빈 방식으로 값을 큐에서 가져옵니다.
		/// </summary>
		/// <param name="pair">가져온 키-값 페어</param>
		/// <returns>성공 여부</returns>
		public bool TryDequeue(out KeyValuePair<TKey, TValue> pair)
		{
			lock(this.lockObject)
			{
				var keyCount = this.keyList.Count;
				for(var i = 0; i < keyCount; ++i)
				{
					var idx = (this.idx + i) % keyCount;
					var key = this.keyList[idx];

					if(!this.keyValueDict.TryGetValue(key, out var queue))
						continue;

					if(queue.Count == 0)
						continue;

					var value = queue.Dequeue();
					if(queue.Count < 1)
					{
						this.keyList.RemoveAt(idx);
						this.keyValueDict.Remove(key);
						idx--;
					}

					pair = new KeyValuePair<TKey, TValue>(key, value);
					this.idx = idx + 1;
					return true;
				}

				pair = new KeyValuePair<TKey, TValue>();
				return false;
			}
		}
	}
}