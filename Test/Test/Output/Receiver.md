# Receiver
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\Receiver.cs
네임스페이스 : Robust.Core.Net

>  리엑터 패턴 이벤트 수신기
	

## Class Declaration
```csharp
public class Receiver : ReactorEventHandler
```

## Constructor
```csharp

		public Receiver()
		{
		}

```
```csharp

		public Receiver(Reactor reactor, Socket sock)
			: base(reactor, sock)
		{
		}

```

## Methods
### OnRead
```csharp
public override void OnRead()
```

### OnClose
```csharp
protected void OnClose()
```

### OnCommand
```csharp
public override void OnCommand(string command)
```
** Parameters **
- command (string)
