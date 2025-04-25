# UdpReactor
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\UdpReactor.cs
네임스페이스 : Robust.Core.Net

>  UDP 소켓 리엑터 패턴
	

## Class Declaration
```csharp
public sealed class UdpReactor
```

## Methods
### ThreadStart
```csharp
private void ThreadStart()
```

### Add
```csharp
public void Add(UdpEventHandler handler)
```
** Parameters **
- handler (UdpEventHandler)

### GetEventHandler
```csharp
private UdpEventHandler GetEventHandler(Socket sock)
```
** Parameters **
- sock (Socket)

### Loop
>  이벤트 루프  <br/>
		 1분마다 활성화된 소캣을 감지하며, 읽기 작업만 처리함
		
```csharp
private void Loop()
```

### Start
```csharp
public void Start()
```

### Stop
```csharp
public void Stop()
```

### Join
```csharp
private void Join()
```

### Abort
```csharp
public void Abort()
```
