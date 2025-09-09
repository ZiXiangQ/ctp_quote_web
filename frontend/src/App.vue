<script setup>
import { ref } from 'vue'

const leftDrawerOpen = ref(true)
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-toolbar-title>CTP 行情终端</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above :width="220" bordered>
      <q-list padding>
        <q-item clickable v-ripple to="/quotes" exact>
          <q-item-section avatar><q-icon name="insights" /></q-item-section>
          <q-item-section>行情</q-item-section>
        </q-item>
        <q-item clickable v-ripple to="/subscribe">
          <q-item-section avatar><q-icon name="playlist_add" /></q-item-section>
          <q-item-section>订阅</q-item-section>
        </q-item>
        <q-item clickable v-ripple to="/settings">
          <q-item-section avatar><q-icon name="settings" /></q-item-section>
          <q-item-section>设置</q-item-section>
        </q-item>
        <q-separator class="q-my-sm" />
        <q-item clickable v-ripple to="/about">
          <q-item-section avatar><q-icon name="info" /></q-item-section>
          <q-item-section>关于</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
