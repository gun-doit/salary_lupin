# AsyncSocketAuto
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\AsyncSocketAuto.cs
네임스페이스 : Robust.Core.Net

## Class Declaration
```csharp
public sealed class AsyncSocketAuto
```

## Methods
### ConnectAsync
```csharp
public void ConnectAsync(string host, int port)
```
** Parameters **
- host (string)
- port (int)

### OnConnect
```csharp
public void OnConnect(IAsyncResult ar)
```
** Parameters **
- ar (IAsyncResult)

### ReConnectStart
```csharp
private void ReConnectStart()
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

### Close
```csharp
public void Close()
```

### SocketClose
```csharp
public void SocketClose()
```

### RecvStart
```csharp
private void RecvStart()
```

### ReceiveCallback
```csharp
private void ReceiveCallback(IAsyncResult ar)
```
** Parameters **
- ar (IAsyncResult)

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

### ToString
```csharp
public override string ToString()
```
