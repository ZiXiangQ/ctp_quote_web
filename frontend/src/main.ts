/*
 * @Author: qiuzx
 * @Date: 2025-01-18
 * @Description: 应用入口文件 - TypeScript版本
 */

import { createPinia } from "pinia";
import { Quasar } from "quasar";
import { createApp } from "vue";

// 导入Quasar图标和字体
import "@quasar/extras/fontawesome-v6/fontawesome-v6.css";
import "@quasar/extras/material-icons/material-icons.css";

// 导入Quasar样式
import "quasar/src/css/index.sass";

// 导入应用组件和路由
import App from "./App.vue";
import router from "./router/index";

// 导入样式
import "./style.css";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(Quasar, {
  plugins: {} // 导入Quasar插件
});

app.mount("#app");
