<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="q-ma-none">
          风险配置编辑
        </h4>
        <p class="text-grey-6 q-ma-none">
          配置价格限制、数量限制和持仓限制
        </p>
      </div>
      <div class="col-auto">
        <q-btn color="secondary" icon="save" label="保存" :loading="saving" @click="saveConfig" />
        <q-btn flat icon="arrow_back" label="返回" class="q-ml-sm" @click="goBack" />
      </div>
    </div>

    <div class="row q-gutter-md">
      <!-- 价格限制配置 -->
      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">
              价格限制配置
            </div>

            <q-checkbox v-model="config.check_cross_order" label="检查交叉订单" class="q-mb-md" />

            <q-input v-model.number="config.bid_limit_percent" label="买价限制百分比(%)" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.bid_limit_value" label="买价限制值" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.ask_limit_percent" label="卖价限制百分比(%)" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.ask_limit_value" label="卖价限制值" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.ask_limit_up_percent" label="卖价上涨限制百分比(%)" type="number" outlined
              class="q-mb-md" :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.ask_limit_down_percent" label="卖价下跌限制百分比(%)" type="number" outlined
              :rules="[val => val >= 0 || '必须大于等于0']" />
          </q-card-section>
        </q-card>
      </div>

      <!-- 数量限制配置 -->
      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">
              数量限制配置
            </div>

            <q-input v-model.number="config.max_qty_per_order" label="每单最大数量" type="number" outlined class="q-mb-md"
              :rules="[val => val > 0 || '必须大于0']" />

            <q-input v-model.number="config.max_qty_per_day" label="每日最大数量" type="number" outlined class="q-mb-md"
              :rules="[val => val > 0 || '必须大于0']" />

            <q-input v-model.number="config.max_qty_per_sec" label="每秒最大数量" type="number" outlined
              :rules="[val => val > 0 || '必须大于0']" />
          </q-card-section>
        </q-card>
      </div>

      <!-- 持仓限制配置 -->
      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">
              持仓限制配置
            </div>

            <q-select v-model="config.position_method" :options="positionMethodOptions" label="持仓方法" outlined
              class="q-mb-md" />

            <q-input v-model.number="config.min_net_position" label="最小净持仓" type="number" outlined class="q-mb-md" />

            <q-input v-model.number="config.max_net_position" label="最大净持仓" type="number" outlined class="q-mb-md" />

            <q-input v-model.number="config.max_self_trade_count" label="最大自成交次数" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_cancel_count" label="最大撤单次数" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_soft_cancel_count" label="最大软撤单次数" type="number" outlined
              class="q-mb-md" :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_ioc_cancel_count" label="最大IOC撤单次数" type="number" outlined
              class="q-mb-md" :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_soft_ioc_cancel_count" label="最大软IOC撤单次数" type="number" outlined
              class="q-mb-md" :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_message_amount" label="最大消息数量" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_soft_message_amount" label="最大软消息数量" type="number" outlined
              class="q-mb-md" :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_trade_count" label="最大成交次数" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_soft_trade_count" label="最大软成交次数" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_open_count" label="最大开仓次数" type="number" outlined class="q-mb-md"
              :rules="[val => val >= 0 || '必须大于等于0']" />

            <q-input v-model.number="config.max_soft_open_count" label="最大软开仓次数" type="number" outlined
              :rules="[val => val >= 0 || '必须大于等于0']" />
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { api } from "@/services/api";
import { useQuasar } from "quasar";
import { onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

interface RiskConfig {
  check_cross_order: boolean
  bid_limit_percent: number
  bid_limit_value: number
  ask_limit_percent: number
  ask_limit_value: number
  ask_limit_up_percent: number
  ask_limit_down_percent: number
  max_qty_per_order: number
  max_qty_per_day: number
  max_qty_per_sec: number
  position_method: string
  min_net_position: number
  max_net_position: number
  max_self_trade_count: number
  max_cancel_count: number
  max_soft_cancel_count: number
  max_ioc_cancel_count: number
  max_soft_ioc_cancel_count: number
  max_message_amount: number
  max_soft_message_amount: number
  max_trade_count: number
  max_soft_trade_count: number
  max_open_count: number
  max_soft_open_count: number
}

const route = useRoute();
const router = useRouter();
const $q = useQuasar();

const saving = ref(false);

const positionMethodOptions = [
  { label: "CLOSE", value: "CLOSE" },
  { label: "CLOSE_YESTERDAY", value: "CLOSE_YESTERDAY" },
  { label: "CLOSE_TODAY", value: "CLOSE_TODAY" }
];

const config = reactive<RiskConfig>({
  check_cross_order: true,
  bid_limit_percent: 200,
  bid_limit_value: 10000,
  ask_limit_percent: 200,
  ask_limit_value: 10000,
  ask_limit_up_percent: 80,
  ask_limit_down_percent: 80,
  max_qty_per_order: 50,
  max_qty_per_day: 400,
  max_qty_per_sec: 2000,
  position_method: "CLOSE",
  min_net_position: -50,
  max_net_position: 50,
  max_self_trade_count: 20,
  max_cancel_count: 300,
  max_soft_cancel_count: 350,
  max_ioc_cancel_count: 10000,
  max_soft_ioc_cancel_count: 9999,
  max_message_amount: 17900,
  max_soft_message_amount: 17800,
  max_trade_count: 500,
  max_soft_trade_count: 499,
  max_open_count: 200,
  max_soft_open_count: 199
});

async function loadConfig() {
  const machineId = route.params.machineId;
  const versionId = route.params.versionId;

  try {
    const response = await api.get(`/v1/machines/${machineId}/versions/${versionId}/default-risk`);
    const data = response.data.data;

    if (data) {
      Object.assign(config, data);
    }
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "加载配置失败"
    });
  }
}

async function saveConfig() {
  const machineId = route.params.machineId;
  const versionId = route.params.versionId;

  try {
    saving.value = true;
    await api.put(`/v1/machines/${machineId}/versions/${versionId}/default-risk`, config);
    $q.notify({
      type: "positive",
      message: "配置保存成功"
    });
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "配置保存失败"
    });
  } finally {
    saving.value = false;
  }
}

function goBack() {
  router.back();
}

onMounted(() => {
  loadConfig();
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}
</style>
