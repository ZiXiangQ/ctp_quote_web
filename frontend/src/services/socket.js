/*
 * @Author: qiuzx
 * @Date: 2025-09-09 22:27:21
 * @LastEditors: qiuzx
 * @Description: description
 */
import { io } from 'socket.io-client'

function getBackendUrl() {
  return localStorage.getItem('backendUrl') || 'http://127.0.0.1:5005'
}

let socket

export function connectSocket() {
  const url = getBackendUrl()
  socket = io(url, { transports: ['websocket'], reconnection: true })
  return socket
}

export function getSocket() {
  return socket
}
