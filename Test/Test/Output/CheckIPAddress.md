# CheckIPAddress
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\CheckIPAddress.cs
네임스페이스 : Robust.Core.Net

>  IP Address 범위 비교용 클래스
	

## Class Declaration
```csharp
public class CheckIPAddress
```

## Constructor
```csharp

		public CheckIPAddress(string fileName, FileType type)
		{
			switch(type)
			{
				case FileType.KoreaIPv4List:
					this.ranges = GetIpv4KoreaList(fileName);
					break;
			}

			if(this.ranges == null || this.ranges.Length < 1)
				Log.Error("파일 타입이 적용되지 않았습니다. 확인이 필요합니다.");

			Array.Sort(this.ranges);
			Log.Notice($"{this.ranges.Length}개의 한국 IP Address 가 등록됨");
		}

```

## Methods
### GetIpv4KoreaList
>  파일에 적힌 IP를 읽어서 IPv4Range 배열 생성
		
```csharp
private static IPv4Range[] GetIpv4KoreaList(string fileName)
```
** Parameters **
- fileName (string)

### Search
>  맨 앞에서부터 해당하는 범위의 IPv4Range를 반환
		
```csharp
private IPv4Range Search(IPAddress item)
```
** Parameters **
- item (IPAddress)

### Contain
```csharp
private bool Contain(IPAddress item)
```
** Parameters **
- item (IPAddress)

### Contain
>  범위에 포함하는지 공인 IP인지 확인
		
```csharp
public bool Contain(string publicIp)
```
** Parameters **
- publicIp (string)

### GetIp
```csharp
public static string GetIp(string addr)
```
** Parameters **
- addr (string)
