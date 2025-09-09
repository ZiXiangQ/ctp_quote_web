<template>
  <q-page padding>
    <div class="text-h5 q-mb-md">订阅合约</div>

    <q-form @submit.prevent="onSubmit" class="q-gutter-md" style="max-width: 560px;">
      <q-input v-model="instrumentId" label="合约代码，如 IF2409" dense outlined />

      <div class="row items-center q-gutter-sm">
        <q-btn label="订阅" color="primary" type="submit" :loading="submitting" />
        <q-btn label="清空" flat color="grey" @click="instrumentId = ''" />
      </div>
    </q-form>

    <div class="q-mt-lg">
      <div class="text-subtitle1 q-mb-sm">已订阅</div>
      <q-chip v-for="id in subscribed" :key="id" color="primary" text-color="white" icon="insights" class="q-mr-sm q-mb-sm">
        {{ id }}
      </q-chip>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

function getBackendUrl() {
  return localStorage.getItem('backendUrl') || 'http://127.0.0.1:5000'
}

const instrumentId = ref('')
const subscribed = ref([])
const submitting = ref(false)

onMounted(async () => {
  const { data } = await axios.get(getBackendUrl() + '/api/subscriptions')
  subscribed.value = data
})

async function onSubmit() {
  if (!instrumentId.value) return
  submitting.value = true
  try {
    await axios.post(getBackendUrl() + '/api/subscribe', { instrumentId: instrumentId.value })
    if (!subscribed.value.includes(instrumentId.value)) {
      subscribed.value.push(instrumentId.value)
    }
  } finally {
    submitting.value = false
  }
}
</script>
