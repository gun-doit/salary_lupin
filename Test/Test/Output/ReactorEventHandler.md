# ReactorEventHandler
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\ReactorEventHandler.cs
네임스페이스 : Robust.Core.Net

>  리엑터 패턴 이벤트 핸들러
	

## Class Declaration
```csharp
public abstract class ReactorEventHandler
```

## Constructor
```csharp

		protected ReactorEventHandler()
		{
		}

```
```csharp

		protected ReactorEventHandler(Reactor reactor, Socket sock)
		{
			this.Reactor = reactor;
			this.Socket = sock;
		}

```

## Methods
### OnRead
```csharp
public abstract void OnRead();
```

### OnCommand
```csharp
public abstract void OnCommand(string command);
```
** Parameters **
- command (string)

### OnTimeout
```csharp
public virtual void OnTimeout()
```

### OnWrite
>  논블로킹 쓰기 작업
		
```csharp
public void OnWrite()
```

### SetStatus
```csharp
protected void SetStatus(string status)
```
** Parameters **
- status (string)

### Notify
```csharp
public void Notify(int ID, object Data)
```
** Parameters **
- ID (int)
- Data (object)

### OnStatusChanged
```csharp
protected virtual void OnStatusChanged(StatusChangedEventArgs e)
```
** Parameters **
- e (StatusChangedEventArgs)

### SendUTF8
```csharp
public int SendUTF8(string str)
```
** Parameters **
- str (string)

### Send
```csharp
public int Send(byte[] buf)
```
** Parameters **
- buf (byte[])
