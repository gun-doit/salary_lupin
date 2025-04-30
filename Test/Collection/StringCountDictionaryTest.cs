namespace Robust.Core.Collection
{
	/// <summary>
	/// <seealso cref="StringCountDictionary"/> 의 기능 테스트
	/// </summary>
	[TestClass]
	public sealed class StringCountDictionaryTest
	{
		private readonly StringCountDictionary sut = new();

		[TestMethod]
		public void StringCountTest()
		{
			var testStr = "ZX";

			Assert.IsTrue(this.sut.Add(testStr));
			Assert.IsFalse(this.sut.Add(testStr));
			Assert.IsFalse(this.sut.Remove(testStr));
			Assert.IsTrue(this.sut.Remove(testStr));
		}
	}
}