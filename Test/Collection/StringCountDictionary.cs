namespace Robust.Core.Collection
{
	using System.Collections.Concurrent;

	/// <summary>
	/// 문자열 갯수 측정
	/// </summary>
	public sealed class StringCountDictionary
	{
		private readonly ConcurrentDictionary<string, ulong> dict = new();

		/// <summary>
		/// 데이터 삭제
		/// </summary>
		/// <param name="str">삭제할 문자열</param>
		/// <returns>
		/// 실제 내부 자료 구조에 문자열 삭제 여부
		/// </returns>
		public bool Remove(string str)
		{
			if(string.IsNullOrWhiteSpace(str))
				return false;

			if(!this.dict.TryGetValue(str, out var idx))
				return false;

			this.dict[str] = --idx;

			if(idx < 1)
			{
				this.dict.TryRemove(str, out _);
				return true;
			}

			return false;
		}

		/// <summary>
		/// 추가
		/// </summary>
		/// <param name="str">추가할 문자열</param>
		/// <returns>처음 추가 여부 </returns>
		public bool Add(string str)
		{
			if(string.IsNullOrWhiteSpace(str))
				return false;

			if(!this.dict.TryGetValue(str, out var value))
			{
				this.dict[str] = 1;
				return true;
			}

			this.dict[str] = value + 1;
			return false;
		}

		public List<string> GetStringList()
		{
			return [.. this.dict.Keys];
		}

		public bool Contains(string str)
		{
			return this.dict.ContainsKey(str);
		}

		public void Clear()
		{
			this.dict.Clear();
		}

		public ulong GetCount(string str)
		{
			if(!Contains(str))
				return 0ul;

			this.dict.TryGetValue(str, out var count);
			return count;
		}

		public IEnumerable<string> GetOver(ulong count)
		{
			foreach(var i in this.dict)
			{
				if(i.Value > count)
					yield return i.Key;
			}
		}
	}
}