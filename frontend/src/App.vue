<!--
 * @Author: qiuzx
 * @Date: 2025-09-09 22:01:13
 * @LastEditors: qiuzx
 * @Description: description
-->
<script setup>
import { ref } from "vue";
import { useQuasar } from "quasar";

const leftDrawerOpen = ref(true);
const $q = useQuasar();

// 主题切换函数
const toggleTheme = () => {
  $q.dark.toggle();
};

</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-toolbar-title class="text-left">
          CTP 行情终端
        </q-toolbar-title>
        <q-btn flat dense round :icon="$q.dark.isActive ? 'light_mode' : 'dark_mode'" class="q-ml-auto"
          @click="toggleTheme">
          <q-tooltip>切换主题</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" :width="220" bordered :breakpoint="0" overlay
    @click="leftDrawerOpen = false">
      <q-list padding>
        <q-item v-ripple clickable to="/quotes" exact>
          <q-item-section avatar>
            <q-icon name="insights" />
          </q-item-section>
          <q-item-section>行情</q-item-section>
        </q-item>
        <q-separator class="q-my-sm" />
        <q-item v-ripple clickable to="/about">
          <q-item-section avatar>
            <q-icon name="info" />
          </q-item-section>
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
/* 确保应用占满整个屏幕 */
.q-layout {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
}

.q-page-container {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

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
