<template>
  <q-page class="q-pa-md">
    <!-- 页面标题 -->
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="q-ma-none">关于系统</h4>
        <p class="text-grey-6 q-ma-none">风控XML管理平台系统信息</p>
      </div>
    </div>

    <!-- 系统信息卡片 -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6 q-mb-md">系统信息</div>
        <div class="row q-gutter-md">
          <div class="col-12 col-md-6">
            <q-list>
              <q-item>
                <q-item-section>
                  <q-item-label>系统名称</q-item-label>
                  <q-item-label caption>风控XML管理平台</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item-label>版本号</q-item-label>
                  <q-item-label caption>v1.0.0</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item-label>技术栈</q-item-label>
                  <q-item-label caption>Vue 3 + TypeScript + Quasar + FastAPI</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
          <div class="col-12 col-md-6">
            <q-list>
              <q-item>
                <q-item-section>
                  <q-item-label>开发团队</q-item-label>
                  <q-item-label caption>CTP开发团队</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item-label>最后更新</q-item-label>
                  <q-item-label caption>{{ lastUpdate }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item-label>系统状态</q-item-label>
                  <q-item-label caption>
                    <q-badge color="positive" label="运行正常" />
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- 功能模块 -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6 q-mb-md">功能模块</div>
        <div class="row q-gutter-md">
          <div class="col-12 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="computer" size="2rem" color="primary" />
                  <div class="text-subtitle2 q-mt-sm">机器管理</div>
                  <div class="text-caption text-grey-6">管理交易服务器和配置</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="settings" size="2rem" color="secondary" />
                  <div class="text-subtitle2 q-mt-sm">XML配置</div>
                  <div class="text-caption text-grey-6">可视化XML配置管理</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="history" size="2rem" color="accent" />
                  <div class="text-subtitle2 q-mt-sm">操作日志</div>
                  <div class="text-caption text-grey-6">系统操作记录查询</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="person" size="2rem" color="positive" />
                  <div class="text-subtitle2 q-mt-sm">用户管理</div>
                  <div class="text-caption text-grey-6">用户权限和角色管理</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- 联系方式 -->
    <q-card>
      <q-card-section>
        <div class="text-h6 q-mb-md">联系方式</div>
        <div class="row q-gutter-md">
          <div class="col-12 col-md-6">
            <q-list>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="email" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>技术支持</q-item-label>
                  <q-item-label caption>support@ctp.com</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="phone" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>联系电话</q-item-label>
                  <q-item-label caption>400-123-4567</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
          <div class="col-12 col-md-6">
            <q-list>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="location_on" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>公司地址</q-item-label>
                  <q-item-label caption>北京市朝阳区金融街</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="web" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>官方网站</q-item-label>
                  <q-item-label caption>www.ctp.com</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const lastUpdate = computed(() => {
  return new Date().toLocaleDateString('zh-CN');
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}
</style>

