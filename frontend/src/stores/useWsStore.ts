// src/stores/useWsStore.ts
import type { WsEventHandler } from "@/services/websocket";
import { createSimpleWS, SimpleWS } from "@/services/websocket";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useWsStore = defineStore("ws", () => {
  // 单例 SimpleWS
  const url = localStorage.getItem("backendUrl") || "ws://127.0.0.1:5004/ws";
  const client: SimpleWS = createSimpleWS(url);

  // state
  const connected = ref<boolean>(false);
  const connecting = ref<boolean>(false);
  const readyState = ref<number>(WebSocket.CLOSED);
  const subscribedInstruments = ref<string[]>([]);
  const lastQuote = ref<any | null>(null);

  // computed aggregate
  const status = computed(() => ({
    connected: connected.value,
    connecting: connecting.value,
    readyState: readyState.value,
    url
  }));

  // wire client events to pins
  client.on("open", () => {
    connected.value = true;
    connecting.value = false;
    readyState.value = WebSocket.OPEN;
    client.emit("status", status.value);
  });
  client.on("close", () => {
    connected.value = false;
    connecting.value = false;
    readyState.value = WebSocket.CLOSED;
    client.emit("status", status.value);
  });
  client.on("reconnect", () => {
    connecting.value = true;
  });
  client.on("message", (msg: any) => {
    // generic messages
    // if msg has type 'quote' it will be emitted separately below
    // For safety, update lastQuote if it's quote-like
    if (msg && msg.instrumentId) lastQuote.value = msg;
  });
  client.on("quote", (data: any) => {
    lastQuote.value = data;
  });

  // API exposed by store
  function connect() {
    connecting.value = true;
    client.connect();
  }

  function close() {
    client.close();
  }

  function send(msg: any) {
    client.send(msg);
  }

  function on(ev: string, handler: WsEventHandler) {
    client.on(ev, handler);
  }

  function off(ev: string, handler?: WsEventHandler) {
    client.off(ev, handler);
  }

  // subscribe/unsubscribe (local and remote calling ctpAPI is still kept in your page code)
  function addLocalSubscription(instrumentId: string) {
    if (!subscribedInstruments.value.includes(instrumentId)) {
      subscribedInstruments.value.push(instrumentId);
    }
  }
  function removeLocalSubscription(instrumentId: string) {
    const idx = subscribedInstruments.value.indexOf(instrumentId);
    if (idx >= 0) subscribedInstruments.value.splice(idx, 1);
  }
  function setLocalSubscriptions(list: string[]) {
    subscribedInstruments.value = Array.isArray(list) ? [...list] : [];
  }

  return {
    // state
    connected,
    connecting,
    readyState,
    subscribedInstruments,
    lastQuote,
    status,

    // methods
    connect,
    close,
    send,
    on,
    off,
    addLocalSubscription,
    removeLocalSubscription,
    setLocalSubscriptions
  };
});
