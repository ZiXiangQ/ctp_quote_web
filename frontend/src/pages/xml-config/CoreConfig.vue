<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="q-ma-none">
          核心配置编辑
        </h4>
        <p class="text-grey-6 q-ma-none">
          配置文件路径和系统参数
        </p>
      </div>
      <div class="col-auto">
        <q-btn color="secondary" icon="save" label="保存" :loading="saving" @click="saveConfig" />
        <q-btn flat icon="arrow_back" label="返回" class="q-ml-sm" @click="goBack" />
      </div>
    </div>

    <div class="row q-gutter-md">
      <!-- 文件路径配置 -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">
              文件路径配置
            </div>

            <!-- 合约文件路径 -->
            <div class="q-mb-md">
              <div class="text-subtitle2 q-mb-sm">
                合约文件路径
              </div>
              <div v-for="(path, index) in config.instrument_file_paths" :key="index" class="row q-gutter-sm q-mb-sm">
                <div class="col">
                  <q-input v-model="config.instrument_file_paths[index]" outlined dense />
                </div>
                <div class="col-auto">
                  <q-btn flat round color="negative" icon="remove" size="sm" @click="removeInstrumentPath(index)" />
                </div>
              </div>
              <q-btn flat color="primary" icon="add" label="添加路径" size="sm" @click="addInstrumentPath" />
            </div>

            <!-- 手续费文件 -->
            <q-input v-model="config.instrument_fee_file" label="手续费文件" outlined class="q-mb-md" />

            <!-- 虚拟合约文件 -->
            <q-input v-model="config.virtual_instrument_file" label="虚拟合约文件" outlined class="q-mb-md" />

            <!-- 持仓文件 -->
            <q-input v-model="config.position_file" label="持仓文件" outlined class="q-mb-md" />

            <!-- 成交文件 -->
            <q-input v-model="config.trade_file" label="成交文件" outlined class="q-mb-md" />

            <!-- 订单文件 -->
            <q-input v-model="config.order_file" label="订单文件" outlined />
          </q-card-section>
        </q-card>
      </div>

      <!-- 系统参数配置 -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">
              系统参数配置
            </div>

            <!-- 布尔配置 -->
            <div class="q-mb-md">
              <q-checkbox v-model="config.ignore_instruments_without_config" label="忽略无配置的合约" />
            </div>
            <div class="q-mb-md">
              <q-checkbox v-model="config.ignore_duplicate_instruments" label="忽略重复合约" />
            </div>
            <div class="q-mb-md">
              <q-checkbox v-model="config.keep_cffex_gfex_in_night_trading" label="夜盘保留中金所和广期所合约" />
            </div>

            <!-- 数值配置 -->
            <q-input v-model.number="config.arbi_check_interval" label="套利检查间隔(秒)" type="number" outlined
              class="q-mb-md" :rules="[val => val > 0 || '必须大于0']" />

            <q-input v-model.number="config.max_order_per_sec" label="每秒最大订单数" type="number" outlined class="q-mb-md"
              :rules="[val => val > 0 || '必须大于0']" />

            <!-- 比例值配置 -->
            <div class="q-mb-md">
              <div class="text-subtitle2 q-mb-sm">
                比例值
              </div>
              <div v-for="(value, index) in config.ratio_values" :key="index" class="row q-gutter-sm q-mb-sm">
                <div class="col">
                  <q-input v-model.number="config.ratio_values[index]" type="number" outlined dense />
                </div>
                <div class="col-auto">
                  <q-btn flat round color="negative" icon="remove" size="sm" @click="removeRatioValue(index)" />
                </div>
              </div>
              <q-btn flat color="primary" icon="add" label="添加比例值" size="sm" @click="addRatioValue" />
            </div>
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

interface CoreConfig {
  instrument_file_paths: string[]
  instrument_fee_file: string
  virtual_instrument_file: string
  position_file: string
  trade_file: string
  order_file: string
  ignore_instruments_without_config: boolean
  ignore_duplicate_instruments: boolean
  keep_cffex_gfex_in_night_trading: boolean
  arbi_check_interval: number
  max_order_per_sec: number
  ratio_values: number[]
}

const route = useRoute();
const router = useRouter();
const $q = useQuasar();

const saving = ref(false);

const config = reactive<CoreConfig>({
  instrument_file_paths: [],
  instrument_fee_file: "",
  virtual_instrument_file: "",
  position_file: "",
  trade_file: "",
  order_file: "",
  ignore_instruments_without_config: true,
  ignore_duplicate_instruments: true,
  keep_cffex_gfex_in_night_trading: true,
  arbi_check_interval: 5,
  max_order_per_sec: 80,
  ratio_values: []
});

async function loadConfig() {
  const machineId = route.params.machineId;
  const versionId = route.params.versionId;

  try {
    const response = await api.get(`/v1/machines/${machineId}/versions/${versionId}/core`);
    const data = response.data.data;

    if (data) {
      Object.assign(config, {
        instrument_file_paths: data.instrument_file_paths || [],
        instrument_fee_file: data.instrument_fee_file || "",
        virtual_instrument_file: data.virtual_instrument_file || "",
        position_file: data.position_file || "",
        trade_file: data.trade_file || "",
        order_file: data.order_file || "",
        ignore_instruments_without_config: data.ignore_instruments_without_config ?? true,
        ignore_duplicate_instruments: data.ignore_duplicate_instruments ?? true,
        keep_cffex_gfex_in_night_trading: data.keep_cffex_gfex_in_night_trading ?? true,
        arbi_check_interval: data.arbi_check_interval ?? 5,
        max_order_per_sec: data.max_order_per_sec ?? 80,
        ratio_values: data.ratio_values || []
      });
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
    await api.put(`/v1/machines/${machineId}/versions/${versionId}/core`, config);
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

function addInstrumentPath() {
  config.instrument_file_paths.push("");
}

function removeInstrumentPath(index: number) {
  config.instrument_file_paths.splice(index, 1);
}

function addRatioValue() {
  config.ratio_values.push(100000);
}

function removeRatioValue(index: number) {
  config.ratio_values.splice(index, 1);
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
