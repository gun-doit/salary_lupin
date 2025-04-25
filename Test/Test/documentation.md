Namespace: Robust.Core.Collection
Class: ConcurrentDictionaryList
  Method: Set
    Parameter: keyList (List<TKey>)
    Parameter: valueList (List<TValue>)
  Method: TryGet
    Parameter: key (TKey)
  Method: GetList
  Method: Clear
  Method: Update
    Parameter: key (TKey)
    Parameter: value (TValue)
  Method: Remove
    Parameter: key (TKey)
Namespace: Robust.Core.Collection
Class: ConcurrentHashSet
  Method: Add
    Parameter: item (T)
  Method: AddRange
    Parameter: collection (IEnumerable<T>)
  Method: Clear
  Method: Contains
    Parameter: item (T)
  Method: Remove
    Parameter: item (T)
  Method: ToStringList
  Method: Any
  Method: Set
    Parameter: collection (IEnumerable<T>)
  Method: ToArray
  Method: GetEnumerator
  Method: GetEnumerator
Comment: // to use lock free
Namespace: Robust.Core.Collection
Class: ConcurrentList
  Method: GetEnumerator
  Method: GetEnumerator
  Method: GetEnumerator
  Method: Add
    Parameter: item (T)
  Method: Add
    Parameter: collection (IEnumerable<T>)
  Method: TryAdd
    Parameter: item (T)
  Method: Clear
  Method: Contains
    Parameter: item (T)
  Method: Sort
  Method: Sort
    Parameter: comparer (IComparer<T>)
  Method: Sort
    Parameter: comparison (Comparison<T>)
  Method: CopyTo
    Parameter: array (T[])
    Parameter: arrayIndex (int)
  Method: Remove
    Parameter: item (T)
  Method: IndexOf
    Parameter: item (T)
  Method: Insert
    Parameter: index (int)
    Parameter: item (T)
  Method: RemoveAt
    Parameter: index (int)
  Method: ShallowClone
  Method: Exists
    Parameter: match (Predicate<T>)
  Method: Set
    Parameter: collection (IEnumerable<T>)
Namespace: Robust.Core.Collection
Class: ConcurrentRoundRobinQueue
  Method: TryEnqueue
    Parameter: key (TKey)
    Parameter: value (TValue)
  Method: TryDequeue
    Parameter: pair (KeyValuePair<TKey, TValue>)
Namespace: Robust.Core.Collection
Class: ConcurrentRoundRobinQueueTest
  Method: 동시성입출력테스트
Namespace: Robust.Core.Collection
Class: ConcurrentSortedSet
  Method: Add
    Parameter: value (T)
  Method: AddRange
    Parameter: collection (IEnumerable<T>)
  Method: Remove
    Parameter: value (T)
  Method: Any
  Method: ToStringList
  Method: Clear
Namespace: Robust.Core.Collection
Class: DictionaryList
  Method: TryGetIdx
    Parameter: idx (int)
  Method: Dispose
  Method: Dispose
    Parameter: disposing (bool)
  Method: ToList
  Method: GetEnumerator
  Method: GetEnumerator
  Method: Set
    Parameter: keyList (List<TKey>)
    Parameter: valueList (List<TValue>)
  Method: GetKeyStream
  Method: GetKeyList
  Method: TryGet
    Parameter: key (TKey)
  Method: GetList
  Method: Clear
  Method: Update
    Parameter: key (TKey)
    Parameter: value (TValue)
  Method: Remove
    Parameter: key (TKey)
  Method: ResetBindings
  Method: ResetItem
    Parameter: pos (int)
  Method: ResetItemByKey
    Parameter: key (TKey)
Comment: // indexer support
Namespace: Robust.Core.Collection
Class: DictionaryListTest
  Method: 기능검증
Namespace: Robust.Core.Collection
Class: StringCountDictionary
  Method: Remove
    Parameter: str (string)
  Method: Add
    Parameter: str (string)
  Method: GetStringList
  Method: Contains
    Parameter: str (string)
  Method: Clear
  Method: GetCount
    Parameter: str (string)
  Method: GetOver
    Parameter: count (ulong)
Namespace: Robust.Core.Collection
Class: StringCountDictionaryTest
  Method: StringCountTest