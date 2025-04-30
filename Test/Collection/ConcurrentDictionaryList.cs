namespace Robust.Core.Collection
{
	/// <summary>
	/// <seealso cref="DictionaryList"/>의 기능 ThreadSafe
	/// </summary>
	/// <typeparam name="TKey"></typeparam>
	/// <typeparam name="TValue"></typeparam>
	public sealed class ConcurrentDictionaryList<TKey, TValue> : DictionaryList<TKey, TValue> where TValue : class
	{
		private readonly RWLock rwlock = new();

		public override void Set(List<TKey> keyList, List<TValue> valueList)
		{
			using(this.rwlock.WriterLock)
			{
				base.Set(keyList, valueList);
			}
		}

		public override TValue TryGet(TKey key)
		{
			using(this.rwlock.ReaderLock)
			{
				return base.TryGet(key);
			}
		}

		public override List<TValue> GetList()
		{
			using(this.rwlock.ReaderLock)
			{
				return base.GetList();
			}
		}

		public override void Clear()
		{
			using(this.rwlock.WriterLock)
			{
				base.Clear();
			}
		}

		public override bool Update(TKey key, TValue value)
		{
			using(this.rwlock.WriterLock)
			{
				return base.Update(key, value);
			}
		}

		public override void Remove(TKey key)
		{
			using(this.rwlock.WriterLock)
			{
				base.Remove(key);
			}
		}
	}
}