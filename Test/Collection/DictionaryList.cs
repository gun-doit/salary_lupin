namespace Robust.Core.Collection
{
	using System.Collections;
	using System.ComponentModel;

	/// <summary>
	/// 킷 값을 이용하여 빠르게 데이터를 찾을 수 있는 정렬 가능한 바인딩 리스트(List에 Dict를 연동)
	/// </summary>
	public class DictionaryList<TKey, TValue> : IDisposable, IEnumerable<TValue> where TValue : class
	{
		private readonly Dictionary<TKey, int> dict = [];

		/// <summary>
		/// 바인딩 리스트, UI에서 정렬을 바꾸면 안됨
		/// </summary>
		public BindingList<TValue> List = [];

		public bool RaiseListChangedEvents
		{
			get => this.List.RaiseListChangedEvents;
			set => this.List.RaiseListChangedEvents = value;
		}

		public int Count => this.List.Count;

		public int DataCount => this.dict.Count;

		// indexer support
		public TValue this[TKey key]
		{
			get => TryGet(key);
			set => Update(key, value);
		}

		public TValue TryGetIdx(int idx)
		{
			return this.List[idx];
		}

		public void Dispose()
		{
			Dispose(true);
			GC.SuppressFinalize(this);
		}

		protected virtual void Dispose(bool disposing)
		{
			if(disposing)
				Clear();
		}

		public List<TValue> ToList()
		{
			return [.. this.List];
		}

		public IEnumerator GetEnumerator()
		{
			return this.List.GetEnumerator();
		}

		IEnumerator<TValue> IEnumerable<TValue>.GetEnumerator()
		{
			return this.List.GetEnumerator();
		}

		public virtual void Set(List<TKey> keyList, List<TValue> valueList)
		{
			Clear();

			if(keyList.Count != valueList.Count)
			{
				Log.Error("keyList.Count({0:N0}) != valueList.Count({1:N0})", keyList.Count, valueList.Count);
				return;
			}

			for(var i = 0; i < keyList.Count; i++)
			{
				this.List.Add(valueList[i]);
				this.dict.Add(keyList[i], this.List.Count - 1);
			}
		}

		public IEnumerable<TKey> GetKeyStream()
		{
			return this.dict.Keys;
		}

		public List<TKey> GetKeyList()
		{
			return [.. this.dict.Keys];
		}

		public virtual TValue TryGet(TKey key)
		{
			try
			{
				if(Equals(key, default(TKey)))
					return default;

				if(this.dict.TryGetValue(key, out var pos))
					return this.List[pos];

				return default;
			}
			catch(Exception ex)
			{
				Log.Error(ex);
			}

			return default;
		}

		public virtual List<TValue> GetList()
		{
			var newItem = new List<TValue>(this.List);
			return newItem;
		}

		public virtual void Clear()
		{
			this.dict.Clear();
			this.List.Clear();
		}

		public virtual bool Update(TKey key, TValue value)
		{
			if(this.dict.TryGetValue(key, out var pos))
			{
				this.List[pos] = value;
			}
			else
			{
				this.List.Add(value);
				this.dict.Add(key, this.List.Count - 1);
			}

			return true;
		}

		public virtual void Remove(TKey key)
		{
			if(this.dict.TryGetValue(key, out var pos))
			{
				this.dict.Remove(key);
				this.List.RemoveAt(pos);

				Set([.. this.dict.Keys], [.. this.List]);
			}
		}

		public virtual void ResetBindings()
		{
			this.List.ResetBindings();
		}

		public virtual void ResetItem(int pos)
		{
			this.List.ResetItem(pos);
		}

		public void ResetItemByKey(TKey key)
		{
			if(this.dict.TryGetValue(key, out var pos))
				this.List.ResetItem(pos);
		}
	}
}