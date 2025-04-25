# AsyncBaseSocket
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\AsyncBaseSocket.cs
네임스페이스 : Robust.Core.Net

>  비동기 소켓 기본 클래스
	

## Class Declaration
```csharp
public class AsyncBaseSocket
```

## Methods
### Shutdown
```csharp
public void Shutdown(SocketShutdown how)
```
** Parameters **
- how (SocketShutdown)

### GracefulClose
```csharp
public void GracefulClose()
```

### SetBufferSize
```csharp
public void SetBufferSize(int bufferSize)
```
** Parameters **
- bufferSize (int)

### BufferStatusString
```csharp
public string BufferStatusString()
```

### Send
```csharp
public int Send(byte[] buf)
```
** Parameters **
- buf (byte[])

### Send
```csharp
public int Send(byte[] buf, int size)
```
** Parameters **
- buf (byte[])
- size (int)

### Send
```csharp
public int Send(byte[] buf, int size, SocketFlags flag, out SocketError errCode)
```
** Parameters **
- buf (byte[])
- size (int)
- flag (SocketFlags)
- errCode (SocketError)

### Send
```csharp
public int Send(byte[] buf, int offset, int size)
```
** Parameters **
- buf (byte[])
- offset (int)
- size (int)

### Send
```csharp
public int Send(byte[] buf, int sentSize, int dataLeft, SocketFlags socketFlags, out SocketError errorCode)
```
** Parameters **
- buf (byte[])
- sentSize (int)
- dataLeft (int)
- socketFlags (SocketFlags)
- errorCode (SocketError)

### ToString
```csharp
public override string ToString()
```
