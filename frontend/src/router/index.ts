/*
 * @Author: qiuzx
 * @Date: 2025-01-18
 * @Description: 路由配置 - TypeScript版本
 */

import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/machine-management"
  },
  {
    path: "/machine-management",
    name: "MachineManagement",
    component: () => import("../pages/machine-management/MachineManagement.vue")
  },
  {
    path: "/xml-config",
    name: "XMLConfig",
    component: () => import("../pages/xml-config/XMLConfig.vue")
  },
  {
    path: "/operation-logs",
    name: "OperationLogs",
    component: () => import("../pages/operation-logs/OperationLogs.vue")
  },
  {
    path: "/user-management",
    name: "UserManagement",
    component: () => import("../pages/user-management/UserManagement.vue")
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
