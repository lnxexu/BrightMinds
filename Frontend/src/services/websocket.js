class WebSocketService {
  constructor() {
    this.ws = null;
  }

  connect() {
    this.ws = new WebSocket("ws://your-server-address:port/ws");

    this.ws.onopen = () => {
      console.log("WebSocket Connected");
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    this.ws.onclose = () => {
      console.log("WebSocket connection closed");
      // Optional: Implement reconnection logic
      setTimeout(() => this.connect(), 5000);
    };

    this.ws.onmessage = (event) => {
      // Handle incoming messages
      console.log("Received:", event.data);
    };
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
}

export default new WebSocketService();
