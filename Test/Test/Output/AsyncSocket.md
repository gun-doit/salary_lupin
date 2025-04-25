# AsyncSocket
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\AsyncSocket.cs
네임스페이스 : Robust.Core.Net

>  비동기 소켓 추상 클래스  <br/>
	 비동기 데이터 수신 메서드를 지원한다.
	

## Class Declaration
```csharp
public abstract class AsyncSocket : AsyncBaseSocket
```

## Methods
### OnRecv
```csharp
protected abstract void OnRecv(Archive recvBuf, int readLen);
```
** Parameters **
- recvBuf (Archive)
- readLen (int)

### OnClose
```csharp
protected abstract void OnClose();
```

### OnException
```csharp
protected abstract void OnException(Exception ex);
```
** Parameters **
- ex (Exception)

### Connect
>  소켓 연결
		
```csharp
public bool Connect(string host, int port)
```
** Parameters **
- host (string)
- port (int)

### SockClose
```csharp
public void SockClose()
```

### RecvStart
>  비동기적으로 데이터 수신  <br/>
		 읽기 작업이 완료됐을 때 콜백 함수가 호출됨  <br/>
		 연결이 계속 유지된다면 다시 비동기적으로 데이터를 수신함
		
```csharp
public void RecvStart()
```

### ReceiveCallback
```csharp
private void ReceiveCallback(IAsyncResult ar)
```
** Parameters **
- ar (IAsyncResult)
