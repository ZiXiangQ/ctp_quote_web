// src/services/websocket.ts
/* Simple WebSocket client with heartbeat, auto-reconnect and event emitter */
export type WsEventHandler = (...args: any[]) => void;

export class SimpleWS {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectDelay = 5000; // 增加重连延迟到5秒
  private reconnectTimer: number | null = null;
  private heartbeatInterval = 30000; // 增加心跳间隔到30秒
  private heartbeatTimer: number | null = null;
  private pingTimeoutTimer: number | null = null;
  private eventMap = new Map<string, WsEventHandler[]>();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5; // 最大重连次数
  public status = {
    connected: false,
    connecting: false,
    readyState: WebSocket.CLOSED,
    url: ""
  };

  constructor(url: string) {
    this.url = url;
    this.status.url = url;
  }

  connect() {
    // 防止重复连接
    if (this.status.connecting || this.status.connected) {
      console.log("WebSocket already connecting or connected");
      return;
    }

    this.clearReconnectTimer();
    this.status.connecting = true;
    this.reconnectAttempts++;

    try {
      this.ws = new WebSocket(this.url);
      this.status.readyState = WebSocket.CONNECTING;
      this.emit("status", { ...this.status });
      this.ws.onopen = () => this.handleOpen();
      this.ws.onmessage = (ev) => this.handleMessage(ev);
      this.ws.onclose = (ev) => this.handleClose(ev);
      this.ws.onerror = (ev) => this.handleError(ev);
    } catch (err) {
      this.status.connecting = false;
      this.scheduleReconnect();
      console.error("WebSocket connect error", err);
    }
  }

  private handleOpen() {
    this.status = { connected: true, connecting: false, readyState: WebSocket.OPEN, url: this.url };
    this.reconnectAttempts = 0; // 重置重连次数
    this.emit("open");
    this.emit("status", { ...this.status });
    this.startHeartbeat();
    console.log("WebSocket connected successfully");
  }

  private handleMessage(ev: MessageEvent) {
    // Try parse JSON, else pass raw
    let parsed: any = null;
    try {
      parsed = JSON.parse(ev.data);
    } catch {
      // raw
    }

    if (parsed && parsed.type === "pong") {
      // pong response
      this.clearPingTimeout();
      console.log("Received pong");
      return;
    }

    // emit generic message and type-based
    this.emit("message", parsed ?? ev.data);
    if (parsed && parsed.type) {
      this.emit(parsed.type, parsed.data ?? parsed);
    }
  }

  private handleClose(ev: CloseEvent) {
    this.status = { connected: false, connecting: false, readyState: WebSocket.CLOSED, url: this.url };
    this.emit("close", ev);
    this.emit("status", { ...this.status });
    this.stopHeartbeat();

    // 只有在达到最大重连次数时才停止重连
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.scheduleReconnect();
    } else {
      console.warn("Max reconnect attempts reached, stopping reconnection");
    }
  }

  private handleError(ev: Event) {
    this.emit("error", ev);
    // let onclose handle the reconnect path
  }

  send(obj: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const payload = typeof obj === "string" ? obj : JSON.stringify(obj);
      this.ws.send(payload);
      return true;
    } else {
      this.emit("warn", "ws-not-open");
      return false;
    }
  }

  close() {
    this.clearReconnectTimer();
    this.stopHeartbeat();
    if (this.ws) {
      try { this.ws.close(); } catch { }
      this.ws = null;
    }
    this.status = { connected: false, connecting: false, readyState: WebSocket.CLOSED, url: this.url };
    this.emit("status", { ...this.status });
    console.log("WebSocket closed");
  }

  // Heartbeat: send ping and expect pong
  private startHeartbeat() {
    this.stopHeartbeat();
    console.log(`Starting heartbeat with ${this.heartbeatInterval}ms interval`);

    this.heartbeatTimer = window.setInterval(() => {
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;

      try {
        this.send({ type: "ping" });
        console.log("Sent ping");

        // set a ping timeout - if not cleared by pong in time, force close to trigger reconnect
        this.clearPingTimeout();
        this.pingTimeoutTimer = window.setTimeout(() => {
          console.warn("Ping timeout - closing socket to trigger reconnect");
          this.ws?.close();
        }, this.heartbeatInterval); // use same interval for simplicity
      } catch (err) {
        console.error("Heartbeat send error", err);
      }
    }, this.heartbeatInterval);
  }

  private stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
      console.log("Heartbeat stopped");
    }
    this.clearPingTimeout();
  }

  private clearPingTimeout() {
    if (this.pingTimeoutTimer) {
      clearTimeout(this.pingTimeoutTimer);
      this.pingTimeoutTimer = null;
    }
  }

  // Reconnect
  private scheduleReconnect() {
    if (this.reconnectTimer != null) return;

    console.log(`Scheduling reconnect in ${this.reconnectDelay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    this.reconnectTimer = window.setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
      this.emit("reconnect");
    }, this.reconnectDelay);
  }

  private clearReconnectTimer() {
    if (this.reconnectTimer != null) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }

  // event emitter
  on(ev: string, handler: WsEventHandler) {
    const arr = this.eventMap.get(ev) ?? [];
    arr.push(handler);
    this.eventMap.set(ev, arr);
  }

  off(ev: string, handler?: WsEventHandler) {
    if (!handler) { this.eventMap.delete(ev); return; }
    const arr = this.eventMap.get(ev) ?? [];
    const idx = arr.indexOf(handler);
    if (idx >= 0) arr.splice(idx, 1);
    if (arr.length === 0) this.eventMap.delete(ev);
    else this.eventMap.set(ev, arr);
  }

  emit(ev: string, ...args: any[]) {
    const arr = this.eventMap.get(ev) ?? [];
    for (const h of arr) {
      try { h(...args); } catch (e) { console.error("ws handler error", e); }
    }
  }
}

/* Export a singleton factory helper (you can change URL via param) */
export const createSimpleWS = (url?: string) => new SimpleWS(url ?? (localStorage.getItem("backendUrl") || "ws://127.0.0.1:5004/ws"));
