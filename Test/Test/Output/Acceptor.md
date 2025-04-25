# Acceptor
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\Acceptor.cs
네임스페이스 : Robust.Core.Net

>  Reactor 패턴을 사용한 비동기 서버 소켓
	

## Class Declaration
```csharp
public sealed class Acceptor<EventHandler> : ReactorEventHandler where EventHandler : ReactorEventHandler, new()
```

## Constructor
```csharp

		public Acceptor(Reactor reactor) : base(reactor, null)
		{
			this.Reactor = reactor;
		}

```

## Methods
### Listen
>  서버 소켓을생성하고 지정된 포트에서 연결 요청을 대기
		
```csharp
public void Listen(int port)
```
** Parameters **
- port (int)

### OnRead
>  새로운 클라이언트 연결 수락
		
```csharp
public override void OnRead()
```

### OnCommand
```csharp
public override void OnCommand(string command)
```
** Parameters **
- command (string)

### Close
>  서버 소켓 종료
		
```csharp
public void Close()
```
