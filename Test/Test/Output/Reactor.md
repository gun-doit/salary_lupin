# Reactor
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\Reactor.cs
네임스페이스 : Robust.Core.Net

## Class Declaration
```csharp
public sealed class Reactor
```

## Constructor
```csharp

		public Reactor()
		{
			var internalSocket = CreateInternalSocket();
			this.cmdClientSock = internalSocket[0];
			this.cmdServerSock = internalSocket[1];
		}

```

## Methods
### Add
```csharp
public void Add(ReactorEventHandler handler)
```
** Parameters **
- handler (ReactorEventHandler)

### Wake
```csharp
public void Wake()
```

### Remove
```csharp
public void Remove(ReactorEventHandler handler)
```
** Parameters **
- handler (ReactorEventHandler)

### ThreadMain
```csharp
private void ThreadMain()
```

### GetReadList
```csharp
private List<Socket> GetReadList()
```

### GetWriteList
```csharp
private List<Socket> GetWriteList()
```

### Loop
>  TimeoutMicroSec동안 대기하며 읽기/쓰기 소캣을 탐지  <br/>
		 존재하지 않으면 OnTimeout 이벤트 발생  <br/>
		 둘 중 하나라도 존재하면 읽기는 OnRecvCommand/OnRead, 쓰기를 OnWrite 이벤트를 발생
		
```csharp
private void Loop()
```

### OnRecvCommand
```csharp
private void OnRecvCommand(string cmdString, Socket sock)
```
** Parameters **
- cmdString (string)
- sock (Socket)

### GetEventHandler
>  해당 소캣에 등록된 핸들러를 반환
		
```csharp
private ReactorEventHandler GetEventHandler(Socket sock)
```
** Parameters **
- sock (Socket)

### Start
```csharp
public void Start()
```

### CreateInternalSocket
>  내부적으로 서로 연결된 client socket과 server socket을 반환
		
```csharp
private static Socket[] CreateInternalSocket()
```

### Stop
```csharp
public void Stop()
```

### SendCommand
>  명령어를 client socket에 전송
		
```csharp
public void SendCommand(string cmd)
```
** Parameters **
- cmd (string)

### Join
```csharp
private void Join()
```

### Abort
```csharp
public void Abort()
```
