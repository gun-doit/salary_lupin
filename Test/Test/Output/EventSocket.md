# EventSocket
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\EventSocket.cs
네임스페이스 : Robust.Core.Net

>  이벤트 소켓  <br/>
	 AsyncBaseSocket 클래스를 상속받으며 소켓 연결, 데이터 수신 이벤트를 제공한다.
	

## Class Declaration
```csharp
public sealed class EventSocket : AsyncBaseSocket
```

## Constructor
```csharp

		public EventSocket()
		{
			this.Sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
		}

```

## Methods
### ConnectAsync
>  비동기적으로 연결  <br/>
		 성공적으로 연결이 되면 OnConnect 콜백함수를 호출한다.
		
```csharp
public void ConnectAsync(string host, int port)
```
** Parameters **
- host (string)
- port (int)

### ConnectAsyncProcess
```csharp
private void ConnectAsyncProcess(string host, int port)
```
** Parameters **
- host (string)
- port (int)

### OnConnect
>  연결된 소켓으로부터 데이터를 수신할 준비를 하며 ConnectionEvent 이벤트를 호출한다.
		
```csharp
private void OnConnect(IAsyncResult ar)
```
** Parameters **
- ar (IAsyncResult)

### Close
```csharp
public void Close()
```

### SendBlocking
>  블로킹 방식으로 데이터 송신
		
```csharp
public int SendBlocking(byte[] bytes)
```
** Parameters **
- bytes (byte[])

### RecvStart
>  데이터를 수신하면 ReceiveCallback 콜백함수를 호출한다.
		
```csharp
private void RecvStart()
```

### ReceiveCallback
>  수신된 데이터와 함께 이벤트를 발생시키고, 다시 비동기적으로 데이터를 수신한다.
		
```csharp
private void ReceiveCallback(IAsyncResult ar)
```
** Parameters **
- ar (IAsyncResult)
