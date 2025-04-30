namespace Robust.Core.Collection
{
	[TestClass]
	public sealed class DictionaryListTest
	{
		private readonly List<int> keyList =
		[
			50,
			51,
			52,
			53,
			54,
			55,
			56,
			57,
			58,
			59
		];

		private readonly List<string> valueList =
		[
			"500",
			"501",
			"502",
			"503",
			"504",
			"505",
			"506",
			"507",
			"508",
			"509"
		];

		[TestMethod]
		public void 기능검증()
		{
			var dictList = new DictionaryList<int, string>();

			for(var i = 0; i < 10; i++)
			{
				Assert.IsTrue(dictList.Update(i + 100, (i + 1000).ToString()));
				Assert.AreEqual((i + 1000).ToString(), dictList.TryGet(i + 100));
			}

			dictList.Set(this.keyList, this.valueList);

			for(var i = 0; i < 10; i++)
			{
				Assert.AreEqual((i + 500).ToString(), dictList.TryGet(i + 50));
			}

			var convertKeyToListToArray = dictList.GetKeyList().ToArray();

			for(var i = 0; i < convertKeyToListToArray.Length; i++)
			{
				Assert.AreEqual(this.keyList[i], convertKeyToListToArray[i]);
			}

			var getValueToListToArray = dictList.GetList().ToArray();

			for(var i = 0; i < getValueToListToArray.Length; i++)
			{
				Assert.AreEqual(this.valueList[i], getValueToListToArray[i]);
			}

			dictList.Remove(55);

			var getValueToList = dictList.GetList();
			Assert.AreEqual(9, getValueToList.Count);

			var list = this.valueList.Except(getValueToList);
			Assert.AreEqual("505", list.First());

			dictList.Dispose();

			getValueToList = dictList.GetList();
			Assert.AreEqual(0, getValueToList.Count);
		}
	}
}