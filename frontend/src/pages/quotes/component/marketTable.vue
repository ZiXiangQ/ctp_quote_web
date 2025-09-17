<template>
  <div class="table-section">
    <q-table :rows="rows" :columns="columns" row-key="instrumentId" flat bordered :loading="loading"
      :pagination="{ rowsPerPage: 20 }" class="quotes-table" :rows-per-page-options="[10, 20, 50, 100]"
      binary-state-sort :grid="$q.screen.lt.md">
      <template #body-cell-instrumentId="props">
        <q-td :props="props">
          <div class="instrument-cell">
            <div class="instrument-id">
              {{ props.value }}
            </div>
            <div class="instrument-name">
              {{ getInstrumentName(props.value) }}
            </div>
          </div>
        </q-td>
      </template>

      <template #body-cell-lastPrice="props">
        <q-td :props="props">
          <span :key="props.row._lastUpdate"
            :class="[priceClass(props.row.change), 'price-text', { 'price-updated': isRecentlyUpdated(props.row) }]">
            {{ formatPrice(props.value) }}
          </span>
        </q-td>
      </template>

      <template #body-cell-change="props">
        <q-td :props="props">
          <span :key="props.row._lastUpdate"
            :class="[priceClass(props.value), 'change-text', { 'price-updated': isRecentlyUpdated(props.row) }]">
            {{ formatPrice(props.value) }}
          </span>
        </q-td>
      </template>

      <template #body-cell-changePercent="props">
        <q-td :props="props">
          <q-badge :color="props.row.change >= 0 ? 'positive' : 'negative'" class="percent-badge">
            {{ formatPercent(props.value) }}%
          </q-badge>
        </q-td>
      </template>

      <template #body-cell-volume="props">
        <q-td :props="props">
          <span class="volume-text">{{ formatVolume(props.value) }}</span>
        </q-td>
      </template>

      <template #body-cell-actions="props">
        <q-td :props="props">
          <div class="action-buttons">
            <q-btn v-if="!isSubscribed(props.row.instrumentId)" size="sm" color="primary" icon="add" flat round
              :disable="!canSubscribe" :loading="operationStatus.subscribing" @click="$emit('subscribe', props.row)">
              <q-tooltip>{{ canSubscribe ? '订阅行情' : 'CTP未连接' }}</q-tooltip>
            </q-btn>
            <q-btn v-else size="sm" color="negative" icon="remove" flat round :disable="!canUnsubscribe"
              :loading="operationStatus.unsubscribing" @click="$emit('unsubscribe', props.row.instrumentId)">
              <q-tooltip>{{ canUnsubscribe ? '取消订阅' : 'CTP未连接' }}</q-tooltip>
            </q-btn>
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script setup>

// Props定义
const props = defineProps({
  rows: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  subscribedInstruments: {
    type: Array,
    default: () => []
  },
  operationStatus: {
    type: Object,
    default: () => ({
      subscribing: false,
      unsubscribing: false
    })
  },
  canSubscribe: {
    type: Boolean,
    default: false
  },
  canUnsubscribe: {
    type: Boolean,
    default: false
  }
});

// Emits定义
defineEmits(["subscribe", "unsubscribe"]);

// 表格列定义
const columns = [
  {
    name: "instrumentId",
    label: "合约",
    field: "instrumentId",
    align: "left",
    sortable: true,
    style: "min-width: 120px"
  },
  {
    name: "lastPrice",
    label: "最新价",
    field: "lastPrice",
    align: "right",
    sortable: true,
    style: "min-width: 100px"
  },
  {
    name: "change",
    label: "涨跌",
    field: "change",
    align: "right",
    sortable: true,
    style: "min-width: 100px"
  },
  {
    name: "changePercent",
    label: "涨跌幅",
    field: "changePercent",
    align: "right",
    sortable: true,
    style: "min-width: 100px"
  },
  {
    name: "volume",
    label: "成交量",
    field: "volume",
    align: "right",
    sortable: true,
    style: "min-width: 100px"
  },
  {
    name: "actions",
    label: "操作",
    field: "actions",
    align: "center",
    sortable: false,
    style: "min-width: 80px"
  }
];

// 工具函数
function priceClass(delta) {
  if (delta > 0) return "text-positive";
  if (delta < 0) return "text-negative";
  return "";
}

function formatPrice(price) {
  if (!price) return "--";
  return Number(price).toFixed(2);
}

function formatPercent(percent) {
  if (!percent) return "--";
  return Number(percent).toFixed(2);
}

function formatVolume(volume) {
  if (!volume) return "--";
  if (volume >= 10000) {
    return (volume / 10000).toFixed(1) + "万";
  }
  return volume.toString();
}

function getInstrumentName(instrumentId) {
  const nameMap = {
    "rb2501": "螺纹钢主力",
    "hc2501": "热卷主力",
    "i2501": "铁矿石主力",
    "j2501": "焦炭主力",
    "jm2501": "焦煤主力",
    "cu2501": "沪铜主力",
    "al2501": "沪铝主力",
    "zn2501": "沪锌主力"
  };
  return nameMap[instrumentId] || "未知合约";
}

function isSubscribed(instrumentId) {
  return props.subscribedInstruments.includes(instrumentId);
}

function isRecentlyUpdated(row) {
  if (!row._lastUpdate) return false;
  const now = Date.now();
  const timeDiff = now - row._lastUpdate;
  return timeDiff < 1000; // 1秒内更新的数据
}
</script>

<style scoped>
.table-section {
  flex: 1;
  padding: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.quotes-table {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.instrument-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.instrument-id {
  font-weight: 600;
  font-size: 14px;
  color: #1976d2;
}

.instrument-name {
  font-size: 11px;
  color: #666;
}

.price-text,
.change-text {
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
}

.price-updated {
  animation: priceFlash 0.5s ease-in-out;
}

@keyframes priceFlash {
  0% {
    background-color: transparent;
  }

  50% {
    background-color: rgba(25, 118, 210, 0.1);
  }

  100% {
    background-color: transparent;
  }
}

.percent-badge {
  font-size: 11px;
  font-weight: 600;
}

.volume-text {
  font-size: 13px;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 4px;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .table-section {
    padding: 8px;
  }

  .instrument-id {
    font-size: 13px;
  }

  .instrument-name {
    font-size: 10px;
  }

  .price-text,
  .change-text {
    font-size: 13px;
  }
}

/* 深色主题支持 */
.body--dark .quotes-table {
  background: #1e1e1e;
  color: #e0e0e0;
}

.body--dark .instrument-id {
  color: #64b5f6;
}

.body--dark .instrument-name {
  color: #aaa;
}

.body--dark .volume-text {
  color: #aaa;
}
</style>
