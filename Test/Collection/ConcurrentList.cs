namespace Robust.Core.Collection
{
	using System.Collections;

	/// <summary>
	/// 동시성과 순서을 보장하는 리스트(성능이 다소 아쉬움)
	/// 순서에 상관없으면 <see cref="ConcurrentBag.cs"/>, 인덱서 접근이 필요없다면 <see cref="ConcurrentHashSet.cs"> 사용 요망
	/// </summary>
	/// <typeparam name="T"></typeparam>
	public class ConcurrentList<T> : IList<T>
	{
		private readonly List<T> items = [];
		private readonly RWLock rwLock = new();

		public ConcurrentList(IEnumerable<T> collection = null)
		{
			Add(collection);
		}

		public List<T>.Enumerator GetEnumerator()
		{
			return this.items.GetEnumerator();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			return GetEnumerator();
		}

		IEnumerator<T> IEnumerable<T>.GetEnumerator()
		{
			return GetEnumerator();
		}

		public void Add(T item)
		{
			if(Equals(default(T), item))
				return;

			using(this.rwLock.WriterLock)
			{
				this.items.Add(item);
			}
		}

		/// <summary>
		/// Add in an enumerable of items.
		/// </summary>
		/// <param name="collection"></param>
		public void Add(IEnumerable<T> collection)
		{
			if(collection == null)
				return;

			using(this.rwLock.WriterLock)
			{
				this.items.AddRange(collection.Where(arg => !Equals(default(T), arg)));
			}
		}

		public bool TryAdd(T item)
		{
			if(Equals(default(T), item))
				return false;

			using(this.rwLock.WriterLock)
			{
				this.items.Add(item);
				return true;
			}
		}

		public void Clear()
		{
			using(this.rwLock.WriterLock)
			{
				this.items.Clear();
			}
		}

		public bool Contains(T item)
		{
			using(this.rwLock.ReaderLock)
			{
				return this.items.Contains(item);
			}
		}

		public void Sort()
		{
			using(this.rwLock.WriterLock)
			{
				this.items.Sort();
			}
		}

		public void Sort(IComparer<T> comparer)
		{
			using(this.rwLock.WriterLock)
			{
				this.items.Sort(comparer);
			}
		}

		public void Sort(Comparison<T> comparison)
		{
			using(this.rwLock.WriterLock)
			{
				this.items.Sort(comparison);
			}
		}

		/// <summary>
		/// 배열로 해당 데이터 복사
		/// </summary>
		/// <param name="array"></param>
		/// <param name="arrayIndex"></param>
		/// <exception cref="ArgumentNullException"></exception>
		/// <exception cref="ArgumentOutOfRangeException"></exception>
		/// <exception cref="ArgumentException"></exception>
		public void CopyTo(T[] array, int arrayIndex)
		{
			if(array == null)
				throw new ArgumentNullException(nameof(array));
			else if(arrayIndex < 0)
				throw new ArgumentOutOfRangeException(nameof(arrayIndex), "arrayIndex는 0보다 작을 수 없습니다.");
			else if(array.Length - arrayIndex < this.items.Count)
				throw new ArgumentException("대상 배열에 요소를 복사할 충분한 공간이 없습니다.", nameof(array));

			using(this.rwLock.WriterLock)
			{
				try
				{
					this.items.CopyTo(array, arrayIndex);
				}
				catch(Exception ex)
				{
					Log.Error(ex);
				}
			}
		}

		public bool Remove(T item)
		{
			using(this.rwLock.WriterLock)
			{
				return this.items.Remove(item);
			}
		}

		public int Count
		{
			get
			{
				using(this.rwLock.ReaderLock)
				{
					return this.items.Count;
				}
			}
		}

		public bool IsReadOnly => false;

		public int IndexOf(T item)
		{
			using(this.rwLock.ReaderLock)
			{
				return this.items.IndexOf(item);
			}
		}

		public void Insert(int index, T item)
		{
			using(this.rwLock.WriterLock)
			{
				this.items.Insert(index, item);
			}
		}

		public void RemoveAt(int index)
		{
			using(this.rwLock.WriterLock)
			{
				this.items.RemoveAt(index);
			}
		}

		public T this[int index]
		{
			get
			{
				using(this.rwLock.ReaderLock)
				{
					return this.items[index];
				}
			}

			set
			{
				using(this.rwLock.WriterLock)
				{
					this.items[index] = value;
				}
			}
		}

		/// <summary>
		/// Returns a new copy of all items in the <see cref="List{T}" />.
		/// </summary>
		/// <returns></returns>
		public List<T> ShallowClone()
		{
			using(this.rwLock.ReaderLock)
			{
				return [.. this.items];
			}
		}

		public bool Exists(Predicate<T> match)
		{
			using(this.rwLock.ReaderLock)
			{
				return this.items.Exists(match);
			}
		}

		/// <summary>
		/// 인자 스트림으로 해당 컬렉션을 설정
		/// </summary>
		/// <param name="collection"></param>
		public void Set(IEnumerable<T> collection)
		{
			using(this.rwLock.WriterLock)
			{
				Clear();
				foreach(var i in collection)
				{
					Add(i);
				}
			}
		}
	}
}