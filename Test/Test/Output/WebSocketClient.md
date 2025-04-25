# WebSocketClient
Path: D:\Src\VS2024\RobustCommonLibrary\Core\Net\WebSocketClient.cs
네임스페이스 : Robust.Core.Net

>  웹소켓 사용
	

## Class Declaration
```csharp
public class WebSocketClient
```

## Constructor
```csharp

		protected WebSocketClient(string uri)
		{
			this.websock = new ClientWebSocket();
			this.websock.Options.KeepAliveInterval = TimeSpan.FromSeconds(20);

			this.uri = new Uri(uri);
			this.cancellationToken = this.cancellationTokenSource.Token;
		}

```

## Methods
### Create
>  Creates a new instance.
		
```csharp
public static WebSocketClient Create(string uri)
```
** Parameters **
- uri (string)
> The URI of the WebSocket server.

### Connect
>  Connects to the WebSocket server.
		
```csharp
public WebSocketClient Connect()
```

### SendMessage
>  Send a message to the WebSocket server.
		
```csharp
public void SendMessage(string message)
```
** Parameters **
- message (string)
> The message to send

### Close
```csharp
public void Close()
```

### SendMessageAsync
```csharp
private async Task SendMessageAsync(string message)
```
** Parameters **
- message (string)

### ConnectAsync
```csharp
private async Task ConnectAsync()
```

### StartListen
```csharp
private async Task StartListen()
```

### CallOnMessage
```csharp
private void CallOnMessage(string str)
```
** Parameters **
- str (string)

### CallOnDisconnected
```csharp
private void CallOnDisconnected(string messageOverride)
```
** Parameters **
- messageOverride (string)

### CallOnConnected
```csharp
private void CallOnConnected()
```
