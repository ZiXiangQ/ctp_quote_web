/*
 * @Author: qiuzx
 * @Date: 2025-09-09 22:17:58
 * @LastEditors: qiuzx
 * @Description: description
 */
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", redirect: "/quotes" },
  {
    path: "/quotes",
    name: "quotes",
    component: () => import("../pages/quotes/Quotes.vue")
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../pages/About.vue")
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
