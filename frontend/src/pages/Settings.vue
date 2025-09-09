<template>
  <q-page padding>
    <div class="text-h5 q-mb-md">设置</div>

    <q-list bordered padding style="max-width: 640px">
      <q-item>
        <q-item-section>
          <q-input v-model="backendUrl" label="后端服务地址" outlined dense placeholder="http://127.0.0.1:5000" />
        </q-item-section>
        <q-item-section side>
          <q-btn label="保存" color="primary" @click="save" />
        </q-item-section>
      </q-item>

      <q-item tag="label" v-ripple>
        <q-item-section>
          <q-item-label>深色模式</q-item-label>
          <q-item-label caption>切换界面为深色风格</q-item-label>
        </q-item-section>
        <q-item-section side top>
          <q-toggle v-model="isDark" color="primary" @update:model-value="toggleDark" />
        </q-item-section>
      </q-item>
    </q-list>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Dark } from 'quasar'

const backendUrl = ref('')
const isDark = ref(Dark.isActive)

onMounted(() => {
  backendUrl.value = localStorage.getItem('backendUrl') || 'http://127.0.0.1:5000'
})

function save() {
  localStorage.setItem('backendUrl', backendUrl.value)
}

function toggleDark(val) {
  Dark.set(val)
}
</script>
