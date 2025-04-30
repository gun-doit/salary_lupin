namespace Robust.Core.Collection
{
	/// <summary>
	/// <seealso cref="ConcurrentRoundRobinQueue"/>의 기능 테스트
	/// </summary>
	[TestClass]
	public sealed class ConcurrentRoundRobinQueueTest
	{
		[TestMethod]
		public void 동시성입출력테스트()
		{
			var sut = new ConcurrentRoundRobinQueue<int, int>();

			for(var i = 0; i < 500; ++i)
			{
				Assert.IsTrue(sut.TryEnqueue(0, i));
				Assert.IsTrue(sut.TryEnqueue(1, i));
			}

			var count = 0;
			for(var i = 0; i < 1000; ++i)
			{
				Assert.IsTrue(sut.TryDequeue(out var pair));
				if(pair.Key == 0) count++;
			}

			if(count > 501)
			{
				var str = $"Failure: Count({count})";
				Log.ErrorCaller(str);
			}

			for(var i = 0; i < 10; ++i)
			{
				Assert.IsTrue(sut.TryEnqueue(1, 0));
			}
		}
	}
}