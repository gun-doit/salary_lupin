# UdpEventHandler
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\UdpEventHandler.cs
네임스페이스 : Robust.Core.Net

>  UDP 소켓 이벤트 핸들러
	

## Class Declaration
```csharp
public sealed class UdpEventHandler
```

## Constructor
```csharp

		public UdpEventHandler(string srcHost, int srcPort, string multicastHost)
		{
			Connect(srcHost, srcPort, multicastHost);
		}

```

## Methods
### Connect
>  주어진 멀티케스트 그룹에 바인딩
		
```csharp
private void Connect(string srcHost, int srcPort, string multicastHost)
```
** Parameters **
- srcHost (string)
- srcPort (int)
- multicastHost (string)

### OnRead
>  지정된 soruceEndPoint로부터 데이터를 수신  <br/>
		 수신한 버퍼를 복사하여 DataReceive 이벤트를 호출함과 동시에 전달
		
```csharp
internal void OnRead()
```

### Close
>  해당 소캣을 멀티케스트 그룹에서 제외시키고 Close
		
```csharp
public void Close()
```

### ToString
```csharp
public override string ToString()
```
