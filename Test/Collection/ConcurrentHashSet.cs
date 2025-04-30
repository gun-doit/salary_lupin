namespace Robust.Core.Collection
{
	using System.Collections;
	using System.Collections.Concurrent;

	/// <summary>
	/// 동시성을 보장하는 HashSet<T>
	/// </summary>
	/// <typeparam name="T"></typeparam>
	public sealed class ConcurrentHashSet<T> : IEnumerable<T>
	{
		private readonly ConcurrentDictionary<T, bool> dict = new(); // to use lock free

		public bool Add(T item)
		{
			return this.dict.TryAdd(item, true);
		}

		public void AddRange(IEnumerable<T> collection)
		{
			collection.ForEach(x => Add(x));
		}

		public void Clear()
		{
			this.dict.Clear();
		}

		public bool Contains(T item)
		{
			return this.dict.ContainsKey(item);
		}

		public bool Remove(T item)
		{
			return this.dict.TryRemove(item, out _);
		}

		public int Count => this.dict.Count;

		public string ToStringList()
		{
			return this.dict.ToStringList();
		}

		public bool Any()
		{
			return this.Count > 0;
		}

		public void Set(IEnumerable<T> collection)
		{
			Clear();
			AddRange(collection);
		}

		public T[] ToArray()
		{
			return [.. this.dict.Keys];
		}

		public IEnumerator<T> GetEnumerator()
		{
			return this.dict.Keys.GetEnumerator();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			return this.dict.Keys.GetEnumerator();
		}
	}
}