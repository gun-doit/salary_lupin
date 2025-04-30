namespace Robust.Core.Collection
{
	/// <summary>
	/// 동시성을 지원하는 SortedSet
	/// </summary>
	/// <typeparam name="T"></typeparam>
	public sealed class ConcurrentSortedSet<T>
	{
		private readonly RWLock rwLock = new();
		private readonly SortedSet<T> set = [];

		public int Count => this.set.Count;

		public bool Add(T value)
		{
			using(this.rwLock.WriterLock)
			{
				var ret = this.set.Add(value);
				return ret;
			}
		}

		public void AddRange(IEnumerable<T> collection)
		{
			collection.ForEach(x => Add(x));
		}

		public bool Remove(T value)
		{
			using(this.rwLock.WriterLock)
			{
				var ret = this.set.Remove(value);
				return ret;
			}
		}

		public bool Any()
		{
			using(this.rwLock.ReaderLock)
			{
				return this.set.Count != 0;
			}
		}

		public string ToStringList()
		{
			using(this.rwLock.ReaderLock)
			{
				return this.set.ToStringList();
			}
		}

		public void Clear()
		{
			using(this.rwLock.WriterLock)
			{
				this.set.Clear();
			}
		}
	}
}