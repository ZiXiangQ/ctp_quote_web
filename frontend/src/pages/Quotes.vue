<template>
  <q-page padding>
    <div class="row items-center q-mb-md">
      <div class="text-h5">实时行情</div>
      <q-space />
      <q-btn color="primary" icon="refresh" label="刷新" flat @click="refresh" />
    </div>

    <q-table
      :rows="rows"
      :columns="columns"
      row-key="instrumentId"
      flat bordered
      :loading="loading"
      :pagination="{ rowsPerPage: 15 }"
    >
      <template #body-cell-lastPrice="props">
        <q-td :props="props">
          <span :class="priceClass(props.row.change)">{{ props.row.lastPrice }}</span>
        </q-td>
      </template>
      <template #body-cell-changePercent="props">
        <q-td :props="props">
          <q-badge :color="props.row.change >= 0 ? 'positive' : 'negative'">
            {{ props.row.changePercent }}%
          </q-badge>
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { connectSocket, getSocket } from '../services/socket'

const loading = ref(false)
const rows = ref([])

const columns = [
  { name: 'instrumentId', label: '合约', field: 'instrumentId', align: 'left', sortable: true },
  { name: 'lastPrice', label: '最新', field: 'lastPrice', align: 'right', sortable: true },
  { name: 'change', label: '涨跌', field: 'change', align: 'right', sortable: true },
  { name: 'changePercent', label: '涨跌幅', field: 'changePercent', align: 'right', sortable: true },
]

function priceClass(delta) {
  if (delta > 0) return 'text-positive'
  if (delta < 0) return 'text-negative'
  return ''
}

function upsertRow(quote) {
  const idx = rows.value.findIndex(r => r.instrumentId === quote.instrumentId)
  if (idx >= 0) {
    rows.value[idx] = { ...rows.value[idx], ...quote }
    rows.value = [...rows.value]
  } else {
    rows.value = [quote, ...rows.value]
  }
}

let socket

onMounted(() => {
  socket = connectSocket()
  socket.on('quote', upsertRow)
})

onBeforeUnmount(() => {
  const s = getSocket()
  if (s) {
    s.off('quote', upsertRow)
  }
})

function refresh() {
  // 未来可调用后端刷新或重新订阅
}
</script>
