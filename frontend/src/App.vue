<!--
 * @Author: qiuzx
 * @Date: 2025-09-09 22:01:13
 * @LastEditors: qiuzx
 * @Description: 风控XML管理平台主应用
-->
<script setup lang="ts">
import { useRoute } from "vue-router";

const $route = useRoute();
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <!-- 顶部头部 - 64px高度 -->
    <q-header elevated class="bg-primary text-white" style="height: 64px;">
      <q-toolbar style="height: 64px;">
        <q-toolbar-title class="text-h6">
          风控XML管理平台
        </q-toolbar-title>
        <q-btn flat round dense icon="account_circle">
          <q-tooltip>用户设置</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <!-- 左侧导航栏 - 固定200px宽度 -->
    <div class="sidebar">
      <q-list>
        <q-item-label header class="text-grey-8">
          系统管理
        </q-item-label>

        <q-item v-ripple clickable to="/machine-management" class="q-mx-sm"
          :class="{ 'bg-primary text-white': $route.path === '/machine-management' }">
          <q-item-section avatar>
            <q-icon name="computer" />
          </q-item-section>
          <q-item-section>
            <q-item-label>机器管理</q-item-label>
          </q-item-section>
        </q-item>

        <q-item v-ripple clickable to="/xml-config" class="q-mx-sm"
          :class="{ 'bg-primary text-white': $route.path === '/xml-config' }">
          <q-item-section avatar>
            <q-icon name="settings" />
          </q-item-section>
          <q-item-section>
            <q-item-label>XML配置</q-item-label>
          </q-item-section>
        </q-item>

        <q-item v-ripple clickable to="/operation-logs" class="q-mx-sm"
          :class="{ 'bg-primary text-white': $route.path === '/operation-logs' }">
          <q-item-section avatar>
            <q-icon name="history" />
          </q-item-section>
          <q-item-section>
            <q-item-label>操作日志</q-item-label>
          </q-item-section>
        </q-item>



        <q-separator class="q-my-md" />

        <q-item-label header class="text-grey-8">
          用户设置
        </q-item-label>

        <q-item v-ripple clickable to="/user-management" class="q-mx-sm"
          :class="{ 'bg-primary text-white': $route.path === '/user-management' }">
          <q-item-section avatar>
            <q-icon name="person" />
          </q-item-section>
          <q-item-section>
            <q-item-label>用户管理</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>

    <!-- 主内容区域 -->
    <q-page-container style="margin-left: 200px; margin-top: 0;">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 64px;
  left: 0;
  width: 200px;
  height: calc(100vh - 64px);
  background-color: var(--q-surface);
  border-right: 1px solid#cdcccc;
  z-index: 1000;
  overflow-y: auto;
}

.q-item {
  border-radius: 8px;
  margin: 4px 8px;
}

.q-item--active {
  background-color: var(--q-primary);
  color: white;
}

.q-item--active .q-icon {
  color: white;
}

/* 主内容区域样式 */
.q-page-container {
  margin-left: 200px;
  margin-top: 0;
}

/* 响应式处理 */
@media (max-width: 1024px) {
  .q-page-container {
    margin-left: 0;
  }

  .sidebar {
    display: none;
  }
}
</style>
