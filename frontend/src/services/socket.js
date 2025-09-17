/*
 * @Author: qiuzx
 * @Date: 2025-09-09 22:27:21
 * @LastEditors: qiuzx
 * @Description: CTP行情WebSocket服务
 */
import { io } from "socket.io-client";
import { ctpAPI } from "./api.js";

function getBackendUrl() {
  return localStorage.getItem("backendUrl") || "http://172.18.141.52:5005";
}

let socket = null;
let isConnecting = false;
let ctpStatus = {
  connected: false,
  loggedIn: false,
  subscribedInstruments: []
};

export function connectSocket() {
  // 如果已经连接或正在连接，直接返回现有连接
  if (socket && socket.connected) {
    console.log("WebSocket already connected, reusing existing connection");
    return socket;
  }

  if (isConnecting) {
    console.log("WebSocket connection in progress, waiting...");
    return socket;
  }

  // 如果存在旧连接，先断开
  if (socket) {
    console.log("Disconnecting existing WebSocket connection");
    socket.disconnect();
    socket = null;
  }

  const url = getBackendUrl();
  console.log("Creating new WebSocket connection:", url);
  isConnecting = true;
  socket = io(url, {
    transports: ["websocket", "polling"],
    reconnection: true,
    reconnectionAttempts: 3,
    reconnectionDelay: 2000,
    reconnectionDelayMax: 5000,
    timeout: 20000,
    forceNew: false, // 不强制创建新连接
    multiplex: true
  });

  socket.on("connect", () => {
    console.log("WebSocket connected successfully");
    isConnecting = false;
    ctpStatus.connected = true;
    fetchCTPStatus();
  });

  socket.on("disconnect", (reason) => {
    console.log("WebSocket disconnected:", reason);
    isConnecting = false;
    ctpStatus.connected = false;
  });

  socket.on("connect_error", (error) => {
    console.error("WebSocket connection error:", error);
    isConnecting = false;
    ctpStatus.connected = false;
  });

  socket.on("reconnect", (attemptNumber) => {
    console.log("WebSocket reconnected after", attemptNumber, "attempts");
    ctpStatus.connected = true;
  });

  socket.on("reconnect_error", (error) => {
    console.error("WebSocket reconnection error:", error);
  });

  socket.on("reconnect_failed", () => {
    console.error("WebSocket reconnection failed");
    ctpStatus.connected = false;
  });

  socket.on("quote", (data) => {
    console.log("Received quote:", data);
  });

  return socket;
}

export function getSocket() {
  return socket;
}

export function disconnectSocket() {
  if (socket) {
    console.log("Manually disconnecting WebSocket");
    socket.disconnect();
    socket = null;
    isConnecting = false;
    ctpStatus.connected = false;
  }
}

export function isSocketConnected() {
  return socket && socket.connected;
}

export function getConnectionStatus() {
  return {
    connected: socket ? socket.connected : false,
    connecting: isConnecting,
    socketId: socket ? socket.id : null
  };
}

export function getCTPStatus() {
  return ctpStatus;
}

// 使用新的API服务
export async function fetchCTPStatus() {
  try {
    const data = await ctpAPI.getStatus();
    ctpStatus = { ...ctpStatus, ...data };
    return data;
  } catch (error) {
    console.error("Failed to fetch CTP status:", error);
    return null;
  }
}

export async function connectCTP() {
  try {
    const data = await ctpAPI.connect();
    if (data.success) {
      await fetchCTPStatus();
    }
    return data;
  } catch (error) {
    console.error("Failed to connect CTP:", error);
    return { success: false, message: error.message };
  }
}

export async function disconnectCTP() {
  try {
    const data = await ctpAPI.disconnect();
    if (data.success) {
      await fetchCTPStatus();
    }
    return data;
  } catch (error) {
    console.error("Failed to disconnect CTP:", error);
    return { success: false, message: error.message };
  }
}

export async function subscribeInstrument(instrumentId) {
  try {
    const data = await ctpAPI.subscribe(instrumentId);
    if (data.ok) {
      await fetchCTPStatus();
    }
    return data;
  } catch (error) {
    console.error("Failed to subscribe instrument:", error);
    return { ok: false, error: error.message };
  }
}

export async function unsubscribeInstrument(instrumentId) {
  try {
    const data = await ctpAPI.unsubscribe(instrumentId);
    if (data.ok) {
      await fetchCTPStatus();
    }
    return data;
  } catch (error) {
    console.error("Failed to unsubscribe instrument:", error);
    return { ok: false, error: error.message };
  }
}

export async function getSubscriptions() {
  try {
    const data = await ctpAPI.getSubscriptions();
    return data;
  } catch (error) {
    console.error("Failed to get subscriptions:", error);
    return [];
  }
}
