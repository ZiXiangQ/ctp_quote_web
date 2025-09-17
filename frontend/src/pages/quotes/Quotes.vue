<template>
  <q-page class="quotes-page">
      <!-- 左侧合约订阅区域 -->
      <div class="left-sidebar">
        <!-- 页面标题和状态 -->
        <div class="sidebar-header">
          <div class="title-section">
            <h2 class="page-title">
              <img src="/ctp-logo.svg" alt="CTP Logo" class="title-logo">
              实时行情
            </h2>
            <div class="status-indicator">
              <q-icon name="fiber_manual_record" :color="isConnected ? 'positive' : 'negative'" size="8px" />
              <span class="status-text">{{ isConnected ? 'WebSocket已连接' : 'WebSocket未连接' }}</span>
            </div>
            <div class="ctp-status">
              <q-icon name="fiber_manual_record" :color="isCTPConnected ? 'positive' : 'negative'" size="8px" />
              <span class="status-text">{{ isCTPConnected ? 'CTP已连接' : 'CTP未连接' }}</span>
              <span v-if="isCTPLoggedIn" class="login-status">(已登录)</span>
            </div>
            <div v-if="isConnected && updateStats.totalUpdates > 0" class="update-stats">
              更新: {{ updateStats.totalUpdates }} | 频率: {{ updateStats.updatesPerSecond }}/s
            </div>
          </div>
        </div>

        <!-- 合约订阅区域 -->
        <div class="subscription-section">
          <div class="section-title">
            <q-icon name="insights" />
            合约订阅
          </div>

          <!-- CTP连接控制 -->
          <div class="ctp-controls">
            <q-btn
              v-if="!isCTPConnected"
              color="positive"
              icon="link"
              label="连接CTP"
              :loading="operationStatus.connecting"
              :disable="operationStatus.connecting"
              class="full-width"
              @click="connectCTP"
            />
            <q-btn
              v-else
              color="negative"
              icon="link_off"
              label="断开CTP"
              :loading="operationStatus.disconnecting"
              :disable="operationStatus.disconnecting"
              class="full-width"
              @click="disconnectCTP"
            />
          </div>

          <!-- 订阅输入 -->
          <div class="subscribe-input">
            <q-input
              v-model="newInstrumentId"
              label="合约代码"
              placeholder="例如: rb2501, cu2501"
              outlined
              dense
              :disable="!canSubscribe"
              @keyup.enter="subscribeNewInstrument"
            >
              <template #prepend>
                <q-icon name="add" />
              </template>
              <template #append>
                <q-btn
                  flat
                  dense
                  icon="send"
                  color="primary"
                  :disable="!newInstrumentId.trim() || !canSubscribe"
                  :loading="operationStatus.subscribing"
                  @click="subscribeNewInstrument"
                />
              </template>
            </q-input>
          </div>

          <!-- 已订阅列表 -->
          <div class="subscribed-list">
            <div class="list-header">
              <span>已订阅 ({{ subscribedInstruments.length }})</span>
              <q-btn
                flat
                dense
                icon="refresh"
                size="sm"
                color="primary"
                @click="refresh"
              >
                <q-tooltip>刷新</q-tooltip>
              </q-btn>
            </div>
            <div class="instrument-chips">
              <q-chip
                v-for="instrument in subscribedInstruments"
                :key="instrument"
                removable
                color="primary"
                text-color="white"
                class="instrument-chip"
                @remove="removeFromWatchlist(instrument)"
              >
                {{ instrument }}
              </q-chip>
              <div v-if="subscribedInstruments.length === 0" class="empty-state">
                暂无订阅合约
              </div>
            </div>
          </div>
        </div>

        <!-- 消息显示区域 -->
        <div class="message-section">
          <q-banner
            v-if="errorMessage"
            class="bg-negative text-white"
            rounded
          >
            <template #avatar>
              <q-icon name="error" />
            </template>
            {{ errorMessage }}
          </q-banner>
          <q-banner
            v-if="successMessage"
            class="bg-positive text-white"
            rounded
          >
            <template #avatar>
              <q-icon name="check_circle" />
            </template>
            {{ successMessage }}
          </q-banner>
        </div>
      </div>
      <!-- 右侧行情展示区域 -->
      <div class="right-content">
        <MarketTable
          :rows="rows"
          :loading="loading"
          :subscribed-instruments="subscribedInstruments"
          :operation-status="operationStatus"
          :can-subscribe="canSubscribe"
          :can-unsubscribe="canUnsubscribe"
          @subscribe="addToWatchlist"
          @unsubscribe="removeFromWatchlist"
        />
      </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import {
  connectSocket,
  getSocket,
  isSocketConnected,
  getConnectionStatus
} from "../../services/socket";
import { ctpAPI } from "../../services/api";
import MarketTable from "./component/marketTable.vue";

const loading = ref(false);
const rows = ref([]);
const isConnected = ref(false);
const subscribedInstruments = ref([]);
const newInstrumentId = ref("");
const updateQueue = ref([]);
const isUpdating = ref(false);
const updateStats = ref({
  totalUpdates: 0,
  lastUpdateTime: 0,
  updatesPerSecond: 0
});
const connectionInfo = ref({
  connected: false,
  connecting: false,
  socketId: null
});

// CTP状态管理
const ctpStatus = ref({
  connected: false,
  loggedIn: false,
  subscribedInstruments: [],
  lastUpdate: null
});

// 操作状态
const operationStatus = ref({
  subscribing: false,
  unsubscribing: false,
  connecting: false,
  disconnecting: false
});

// 错误信息
const errorMessage = ref("");
const successMessage = ref("");

// 计算属性
const isCTPConnected = computed(() => ctpStatus.value.connected);
const isCTPLoggedIn = computed(() => ctpStatus.value.loggedIn);
const canSubscribe = computed(() =>
  isCTPConnected.value &&
  isCTPLoggedIn.value &&
  !operationStatus.value.subscribing
);
const canUnsubscribe = computed(() =>
  isCTPConnected.value &&
  isCTPLoggedIn.value &&
  !operationStatus.value.unsubscribing
);

// 显示消息
function showMessage (message, type = "info") {
  if (type === "error") {
    errorMessage.value = message;
    window.setTimeout(() => { errorMessage.value = ""; }, 5000);
  } else if (type === "success") {
    successMessage.value = message;
    window.setTimeout(() => { successMessage.value = ""; }, 3000);
  }
}


async function addToWatchlist (row) {
  if (!canSubscribe.value) {
    showMessage("CTP未连接或未登录，无法订阅", "error");
    return;
  }

  operationStatus.value.subscribing = true;
  try {
    const result = await ctpAPI.subscribe(row.instrumentId);
    if (result.ok) {
      if (!subscribedInstruments.value.includes(row.instrumentId)) {
        subscribedInstruments.value.push(row.instrumentId);
      }
      showMessage(`成功订阅合约 ${row.instrumentId}`, "success");
      // 更新CTP状态
      await updateCTPStatus();
    } else {
      showMessage(`订阅失败: ${result.error || "未知错误"}`, "error");
    }
  } catch (error) {
    console.error("Error subscribing instrument:", error);
    showMessage(`订阅失败: ${error.message}`, "error");
  } finally {
    operationStatus.value.subscribing = false;
  }
}

async function removeFromWatchlist (instrumentId) {
  if (!canUnsubscribe.value) {
    showMessage("CTP未连接或未登录，无法取消订阅", "error");
    return;
  }

  operationStatus.value.unsubscribing = true;
  try {
    const result = await ctpAPI.unsubscribe(instrumentId);
    if (result.ok) {
      const index = subscribedInstruments.value.indexOf(instrumentId);
      if (index > -1) {
        subscribedInstruments.value.splice(index, 1);
      }
      showMessage(`成功取消订阅合约 ${instrumentId}`, "success");
      // 更新CTP状态
      await updateCTPStatus();
    } else {
      showMessage(`取消订阅失败: ${result.error || "未知错误"}`, "error");
    }
  } catch (error) {
    console.error("Error unsubscribing instrument:", error);
    showMessage(`取消订阅失败: ${error.message}`, "error");
  } finally {
    operationStatus.value.unsubscribing = false;
  }
}

async function subscribeNewInstrument () {
  if (!newInstrumentId.value.trim()) return;

  if (!canSubscribe.value) {
    showMessage("CTP未连接或未登录，无法订阅", "error");
    return;
  }

  const instrumentId = newInstrumentId.value.trim();

  // 检查是否已经订阅
  if (subscribedInstruments.value.includes(instrumentId)) {
    showMessage(`合约 ${instrumentId} 已经订阅`, "error");
    return;
  }

  operationStatus.value.subscribing = true;
  try {
    const result = await ctpAPI.subscribe(instrumentId);
    if (result.ok) {
      subscribedInstruments.value.push(instrumentId);
      newInstrumentId.value = "";
      showMessage(`成功订阅合约 ${instrumentId}`, "success");
      // 更新CTP状态
      await updateCTPStatus();
    } else {
      showMessage(`订阅失败: ${result.error || "未知错误"}`, "error");
    }
  } catch (error) {
    console.error("Error subscribing instrument:", error);
    showMessage(`订阅失败: ${error.message}`, "error");
  } finally {
    operationStatus.value.subscribing = false;
  }
}


// CTP状态管理函数
async function updateCTPStatus () {
  try {
    const status = await ctpAPI.getStatus();
    if (status) {
      ctpStatus.value = { ...ctpStatus.value, ...status };
      ctpStatus.value.lastUpdate = new Date().toISOString();

      // 同步订阅列表
      if (status.subscribedInstruments) {
        subscribedInstruments.value = status.subscribedInstruments;
      }
    }
  } catch (error) {
    console.error("Failed to update CTP status:", error);
  }
}

// CTP连接管理
async function connectCTP () {
  if (operationStatus.value.connecting) return;

  operationStatus.value.connecting = true;
  try {
    const result = await ctpAPI.connect();
    if (result.success) {
      showMessage("CTP连接成功", "success");
      await updateCTPStatus();
    } else {
      showMessage(`CTP连接失败: ${result.message || "未知错误"}`, "error");
    }
  } catch (error) {
    console.error("Error connecting CTP:", error);
    showMessage(`CTP连接失败: ${error.message}`, "error");
  } finally {
    operationStatus.value.connecting = false;
  }
}

async function disconnectCTP () {
  if (operationStatus.value.disconnecting) return;

  operationStatus.value.disconnecting = true;
  try {
    const result = await ctpAPI.disconnect();
    if (result.success) {
      showMessage("CTP断开连接成功", "success");
      await updateCTPStatus();
    } else {
      showMessage(`CTP断开连接失败: ${result.message || "未知错误"}`, "error");
    }
  } catch (error) {
    console.error("Error disconnecting CTP:", error);
    showMessage(`CTP断开连接失败: ${error.message}`, "error");
  } finally {
    operationStatus.value.disconnecting = false;
  }
}


function upsertRow (quote) {
  // 更新统计信息
  updateStats.value.totalUpdates++;
  const now = Date.now();
  if (updateStats.value.lastUpdateTime > 0) {
    const timeDiff = now - updateStats.value.lastUpdateTime;
    if (timeDiff > 0) {
      updateStats.value.updatesPerSecond = Math.round(1000 / timeDiff);
    }
  }
  updateStats.value.lastUpdateTime = now;

  // 添加到更新队列
  updateQueue.value.push(quote);

  // 如果正在更新，直接返回
  if (isUpdating.value) return;

  // 启动批量更新
  processUpdateQueue();
}

function processUpdateQueue () {
  if (updateQueue.value.length === 0) return;

  isUpdating.value = true;

  // 使用 setTimeout 确保在下一个事件循环中执行
  window.setTimeout(() => {
    const updates = [...updateQueue.value];
    updateQueue.value = [];

    // 批量处理更新
    updates.forEach(quote => {
      const idx = rows.value.findIndex(
        (r) => r.instrumentId === quote.instrumentId
      );

      if (idx >= 0) {
        // 直接更新现有行
        const existingRow = rows.value[idx];
        const updatedRow = { ...existingRow, ...quote };

        // 添加更新时间戳用于动画
        updatedRow._lastUpdate = Date.now();

        // 直接替换数组元素
        rows.value.splice(idx, 1, updatedRow);
      } else {
        // 新行添加更新时间戳
        quote._lastUpdate = Date.now();
        rows.value.unshift(quote);
      }
    });

    isUpdating.value = false;

    // 如果队列中还有新的更新，继续处理
    if (updateQueue.value.length > 0) {
      processUpdateQueue();
    }
  }, 0);
}

let socket;

onMounted(async () => {
  try {
    loading.value = true;

    // 初始化CTP状态
    await updateCTPStatus();

    // 加载订阅列表
    try {
      const subscriptions = await ctpAPI.getSubscriptions();
      subscribedInstruments.value = subscriptions || [];
    } catch (error) {
      console.warn("Failed to load subscriptions:", error);
      subscribedInstruments.value = [];
    }

    // 检查是否已有连接
    if (isSocketConnected()) {
      console.log("Reusing existing WebSocket connection");
      socket = getSocket();
    } else {
      // 创建新连接
      socket = connectSocket();
    }

    if (socket) {
      // 添加事件监听器
      socket.on("quote", upsertRow);
      socket.on("connect", () => {
        isConnected.value = true;
        console.log("WebSocket connected in Quotes page");
      });
      socket.on("disconnect", () => {
        isConnected.value = false;
        console.log("WebSocket disconnected in Quotes page");
      });
      socket.on("server_info", (data) => {
        console.log("Server info:", data);
      });

      // 更新连接状态
      const status = getConnectionStatus();
      isConnected.value = status.connected;
      connectionInfo.value = status;
    }

    // 如果已订阅合约，获取初始行情数据
    if (subscribedInstruments.value.length > 0) {
      try {
        const quotes = await ctpAPI.getQuotes(subscribedInstruments.value);
        if (quotes && Array.isArray(quotes)) {
          quotes.forEach(quote => {
            upsertRow(quote);
          });
        }
      } catch (error) {
        console.warn("Failed to load initial quotes:", error);
      }
    }

    showMessage("页面初始化完成", "success");
  } catch (error) {
    console.error("Initialization error:", error);
    isConnected.value = false;
    showMessage(`初始化失败: ${error.message}`, "error");
  } finally {
    loading.value = false;
  }
});

onBeforeUnmount(() => {
  const s = getSocket();
  if (s) {
    // 移除事件监听器
    s.off("quote", upsertRow);
    s.off("connect");
    s.off("disconnect");
    s.off("server_info");
    console.log("Cleaned up WebSocket event listeners");
  }
});

async function refresh () {
  try {
    loading.value = true;

    // 刷新订阅列表
    const subscriptions = await ctpAPI.getSubscriptions();
    subscribedInstruments.value = subscriptions || [];

    // 更新CTP状态
    await updateCTPStatus();

    // 刷新行情数据
    if (subscribedInstruments.value.length > 0) {
      const quotes = await ctpAPI.getQuotes(subscribedInstruments.value);
      if (quotes && Array.isArray(quotes)) {
        // 更新行情数据
        quotes.forEach(quote => {
          upsertRow(quote);
        });
      }
    }

    showMessage("刷新成功", "success");
  } catch (error) {
    console.error("Error refreshing data:", error);
    showMessage(`刷新失败: ${error.message}`, "error");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.quotes-page {
  display: flex;
  background-color: #f5f5f5;
  height: 90%;
  width: 100%;
  overflow: hidden;
}

/* 左侧边栏 - 固定400px宽度 */
.left-sidebar {
  width: 400px;
  background: white;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  flex-shrink: 0; /* 防止收缩 */
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  background: #fafafa;
  flex: 1;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1976d2;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-logo {
  width: 20px;
  height: 20px;
  border-radius: 4px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #666;
}

.status-text {
  font-weight: 500;
}

.ctp-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #666;
}

.login-status {
  font-size: 10px;
  color: #4caf50;
  font-weight: 600;
}

.update-stats {
  font-size: 10px;
  color: #666;
}

/* 订阅区域 */
.subscription-section {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  flex-shrink: 0;
}

.ctp-controls {
  margin-bottom: 12px;
  flex-shrink: 0;
}

.subscribe-input {
  margin-bottom: 12px;
  flex-shrink: 0;
}

.subscribed-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #666;
  flex-shrink: 0;
}

.instrument-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  overflow-y: auto;
  flex: 1;
}

.instrument-chip {
  font-size: 11px;
}

.empty-state {
  color: #999;
  font-size: 12px;
  text-align: center;
  padding: 16px;
  font-style: italic;
}

/* 右侧内容区 - 自适应填满剩余空间 */
.right-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f5f5f5;
  min-width: 0; /* 确保flex项目可以收缩 */
}



/* 响应式设计 - 全屏适配 */
@media (max-width: 1400px) {
  .left-sidebar {
    width: 350px;
  }
}

@media (max-width: 1200px) {
  .left-sidebar {
    width: 320px;
  }
}

@media (max-width: 1024px) {
  .left-sidebar {
    width: 300px;
  }

  .page-title {
    font-size: 16px;
  }

  .title-logo {
    width: 18px;
    height: 18px;
  }
}

@media (max-width: 768px) {
  .page-layout {
    flex-direction: column;
    height: 100%;
  }

  .left-sidebar {
    width: 100%;
    height: 200px;
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
    flex-shrink: 0;
  }

  .sidebar-header {
    padding: 12px;
  }

  .subscription-section {
    padding: 12px;
    gap: 8px;
  }


  .instrument-chips {
    max-height: 80px;
  }

  .page-title {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .left-sidebar {
    height: 180px;
  }

  .sidebar-header {
    padding: 8px;
  }

  .subscription-section {
    padding: 8px;
    gap: 6px;
  }

  .page-title {
    font-size: 14px;
  }

  .title-logo {
    width: 16px;
    height: 16px;
  }

  .section-title {
    font-size: 12px;
  }

  .instrument-chip {
    font-size: 10px;
  }
}

/* 深色主题适配 - 全屏设计 */
.body--dark .quotes-page {
  background-color: #121212;
}

.body--dark .page-layout {
  background-color: #121212;
}

.body--dark .left-sidebar {
  background: #1e1e1e;
  border-color: #333;
}

.body--dark .right-content {
  background: #121212;
}


.body--dark .sidebar-header {
  background: #2a2a2a;
  border-color: #333;
}

.body--dark .page-title {
  color: #26a69a;
}

.body--dark .section-title {
  color: #e0e0e0;
}

.body--dark .status-text,
.body--dark .update-stats {
  color: #aaa;
}

.body--dark .list-header {
  color: #ccc;
}

.body--dark .empty-state {
  color: #666;
}


/* 消息区域样式 */
.message-section {
  padding: 8px 16px;
  flex-shrink: 0;
}

.message-section .q-banner {
  margin-bottom: 8px;
  font-size: 12px;
}

.message-section .q-banner:last-child {
  margin-bottom: 0;
}
</style>
