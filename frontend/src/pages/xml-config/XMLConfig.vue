<template>
  <q-page class="q-pa-md">
    <!-- 机器选择 -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row items-center q-gutter-sm">
          <div class="col-auto">
            <q-select v-model="selectedMachine" :options="machineOptions" dense label="选择机器" outlined
              style="min-width: 300px;" @update:model-value="loadConfig" />
          </div>
          <div class="col flex items-center justify-end">
            <q-btn color="secondary" icon="upload" label="导入XML" class="q-mr-sm" @click="showImportDialog = true" />
            <q-btn color="primary" icon="download" label="导出XML" @click="exportXML" />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- 配置类型 + 右侧预览 -->
    <div class="row q-gutter-md">
      <div class="col-auto">
        <q-card style="width: 800px;">
          <q-tabs v-model="activeTab" dense class="text-grey" active-color="primary" indicator-color="primary"
            align="justify" narrow-indicator>
            <q-tab name="core" label="核心配置" />
            <q-tab name="risk" label="风险配置" />

            <q-tab name="instrument" label="合约配置" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="activeTab" class="q-pa-md" animated>
            <!-- 核心配置 -->
            <q-tab-panel name="core">
              <div class="row q-gutter-md">
                <div class="col-6">
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-h6 q-mb-md">
                        文件路径配置
                      </div>

                      <div class="q-mb-md">
                        <div class="text-subtitle2 q-mb-sm">
                          合约文件路径
                        </div>
                        <div v-for="(path, index) in coreConfig.instrument_file_paths" :key="index"
                          class="row q-gutter-sm q-mb-sm">
                          <div class="col">
                            <q-input v-model="coreConfig.instrument_file_paths[index]" outlined dense />
                          </div>
                          <div class="col-auto">
                            <q-btn flat round color="negative" icon="remove" size="sm"
                              @click="removeInstrumentPath(index)" />
                          </div>
                        </div>
                        <q-btn flat color="primary" icon="add" label="添加路径" size="sm" @click="addInstrumentPath" />
                      </div>

                      <q-input v-model="coreConfig.instrument_fee_file" label="手续费文件" outlined class="q-mb-md" />

                      <q-input v-model="coreConfig.virtual_instrument_file" label="虚拟合约文件" outlined class="q-mb-md" />

                      <q-input v-model="coreConfig.position_file" label="持仓文件" outlined class="q-mb-md" />

                      <q-input v-model="coreConfig.trade_file" label="成交文件" outlined class="q-mb-md" />

                      <q-input v-model="coreConfig.order_file" label="订单文件" outlined />
                    </q-card-section>
                  </q-card>
                </div>

                <div class="col-5">
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-h6 q-mb-md">
                        系统参数配置
                      </div>

                      <q-checkbox v-model="coreConfig.ignore_instruments_without_config" label="忽略无配置的合约"
                        class="q-mb-md" />

                      <q-checkbox v-model="coreConfig.ignore_duplicate_instruments" label="忽略重复合约" class="q-mb-md" />

                      <q-checkbox v-model="coreConfig.keep_cffex_gfex_in_night_trading" label="夜盘保留中金所和广期所合约"
                        class="q-mb-md" />

                      <q-input v-model.number="coreConfig.arbi_check_interval" label="套利检查间隔(秒)" type="number" outlined
                        class="q-mb-md" />

                      <q-input v-model.number="coreConfig.max_order_per_sec" label="每秒最大订单数" type="number" outlined
                        class="q-mb-md" />

                      <div class="q-mb-md">
                        <div class="text-subtitle2 q-mb-sm">
                          比例值
                        </div>
                        <div v-for="(value, index) in coreConfig.ratio_values" :key="index"
                          class="row q-gutter-sm q-mb-sm">
                          <div class="col">
                            <q-input v-model.number="coreConfig.ratio_values[index]" type="number" outlined dense />
                          </div>
                          <div class="col-auto">
                            <q-btn flat round color="negative" icon="remove" size="sm"
                              @click="removeRatioValue(index)" />
                          </div>
                        </div>
                        <q-btn flat color="primary" icon="add" label="添加比例值" size="sm" @click="addRatioValue" />
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
              </div>
            </q-tab-panel>

            <!-- 风险配置 -->
            <q-tab-panel name="risk">
              <div class="row q-gutter-md">
                <div class="col-4 col-md-4">
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-h6 q-mb-md">
                        价格限制
                      </div>
                      <q-checkbox v-model="riskConfig.check_cross_order" label="检查交叉订单" class="q-mb-md" />
                      <q-input v-model.number="riskConfig.bid_limit_percent" label="买价限制百分比(%)" type="number" outlined
                        class="q-mb-md" />
                      <q-input v-model.number="riskConfig.bid_limit_value" label="买价限制值" type="number" outlined
                        class="q-mb-md" />
                      <q-input v-model.number="riskConfig.ask_limit_percent" label="卖价限制百分比(%)" type="number" outlined
                        class="q-mb-md" />
                      <q-input v-model.number="riskConfig.ask_limit_value" label="卖价限制值" type="number" outlined
                        class="q-mb-md" />
                      <q-input v-model.number="riskConfig.ask_limit_up_percent" label="卖价上涨限制百分比(%)" type="number"
                        outlined class="q-mb-md" />
                      <q-input v-model.number="riskConfig.ask_limit_down_percent" label="卖价下跌限制百分比(%)" type="number"
                        outlined />
                    </q-card-section>
                  </q-card>
                </div>

                <div class="col-4 col-md-4">
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-h6 q-mb-md">
                        数量限制
                      </div>

                      <q-input v-model.number="riskConfig.max_qty_per_order" label="每单最大数量" type="number" outlined
                        class="q-mb-md" />

                      <q-input v-model.number="riskConfig.max_qty_per_day" label="每日最大数量" type="number" outlined
                        class="q-mb-md" />

                      <q-input v-model.number="riskConfig.max_qty_per_sec" label="每秒最大数量" type="number" outlined />
                    </q-card-section>
                  </q-card>
                </div>

                <div class="col-3 col-md-3">
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-h6 q-mb-md">
                        持仓限制
                      </div>

                      <q-select v-model="riskConfig.position_method" :options="positionMethodOptions" label="持仓方法"
                        outlined class="q-mb-md" />

                      <q-input v-model.number="riskConfig.min_net_position" label="最小净持仓" type="number" outlined
                        class="q-mb-md" />

                      <q-input v-model.number="riskConfig.max_net_position" label="最大净持仓" type="number" outlined
                        class="q-mb-md" />

                      <q-input v-model.number="riskConfig.max_self_trade_count" label="最大自成交次数" type="number" outlined
                        class="q-mb-md" />

                      <q-input v-model.number="riskConfig.max_cancel_count" label="最大撤单次数" type="number" outlined
                        class="q-mb-md" />

                      <q-input v-model.number="riskConfig.max_trade_count" label="最大成交次数" type="number" outlined />
                    </q-card-section>
                  </q-card>
                </div>
              </div>
            </q-tab-panel>



            <!-- 合约配置 -->
            <q-tab-panel name="instrument">
              <div class="row q-mb-md">
                <div class="col">
                  <h6>合约配置列表</h6>
                </div>
                <div class="col-auto">
                  <q-btn color="primary" icon="add" label="添加合约配置" @click="showInstrumentConfigDialog = true" />
                </div>
              </div>

              <q-table :rows="instrumentConfigs" :columns="instrumentConfigColumns" row-key="id" :loading="loading">
                <template #body-cell-actions="props">
                  <q-td :props="props">
                    <q-btn flat round color="primary" icon="edit" size="sm" @click="editInstrumentConfig(props.row)">
                      <q-tooltip>编辑</q-tooltip>
                    </q-btn>
                    <q-btn flat round color="negative" icon="delete" size="sm"
                      @click="deleteInstrumentConfig(props.row)">
                      <q-tooltip>删除</q-tooltip>
                    </q-btn>
                  </q-td>
                </template>
              </q-table>
            </q-tab-panel>
          </q-tab-panels>

          <!-- 保存按钮 -->
          <q-card-actions align="right" class="q-pa-md">
            <q-btn color="primary" icon="save" label="保存配置" :loading="saving" @click="saveConfig" />
          </q-card-actions>
        </q-card>
      </div>

      <!-- 右侧 XML 预览 -->
      <div class="col">
        <q-card flat bordered class="xml-preview-card">
          <q-card-section class="row items-center justify-between">
            <div class="text-h6">
              XML预览
            </div>
            <div class="row items-center">
              <q-toggle v-model="wrapXml" size="sm" left-label label="自动换行" class="q-mr-md" />
              <q-btn flat round icon="content_copy" @click="copyXml">
                <q-tooltip>复制</q-tooltip>
              </q-btn>
              <q-btn flat round icon="download" class="q-ml-sm" @click="downloadXml">
                <q-tooltip>下载</q-tooltip>
              </q-btn>
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section class="q-pa-none">
            <div class="xml-code" :class="{ wrap: wrapXml }">
              <pre><code ref="xmlCodeEl" class="language-xml">{{ xmlPreview }}</code></pre>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- 导入XML对话框 -->
    <q-dialog v-model="showImportDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">
            导入XML配置
          </div>
        </q-card-section>

        <q-card-section>
          <q-file v-model="importFile" label="选择XML文件" accept=".xml" outlined />
          <div class="q-mt-md text-caption text-grey-6">
            支持导入RiskManager格式的XML配置文件
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" @click="showImportDialog = false" />
          <q-btn color="primary" label="导入" :disable="!importFile" :loading="importing" @click="importXML" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { useQuasar } from "quasar";
import { computed, nextTick, onMounted, reactive, ref, watch } from "vue";

const $q = useQuasar();

const activeTab = ref("core");
const loading = ref(false);
const saving = ref(false);
const importing = ref(false);
const showImportDialog = ref(false);

const showInstrumentConfigDialog = ref(false);
const importFile = ref(null);
const selectedMachine = ref(null);

// 右侧预览控制
const wrapXml = ref(true);
const xmlCodeEl = ref<HTMLElement | null>(null);

// 机器选项
const machineOptions = ref([
  { label: "trading-server-01", value: 1 },
  { label: "trading-server-02", value: 2 },
  { label: "trading-server-03", value: 3 }
]);

// 核心配置
const coreConfig = reactive({
  instrument_file_paths: ["/data/instruments/instrument.csv"],
  instrument_fee_file: "/data/fees/fee.csv",
  virtual_instrument_file: "/data/virtual/virtual.csv",
  position_file: "/data/positions/position.csv",
  trade_file: "/data/trades/trade.csv",
  order_file: "/data/orders/order.csv",
  ignore_instruments_without_config: true,
  ignore_duplicate_instruments: true,
  keep_cffex_gfex_in_night_trading: true,
  arbi_check_interval: 5,
  max_order_per_sec: 80,
  ratio_values: [100000, 200000, 500000]
});

// 风险配置
const riskConfig = reactive({
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
  max_trade_count: 500
});



// 合约配置
const instrumentConfigs = ref([
  {
    id: 1,
    instrument_id: "rb2501",
    max_qty_per_order: 100,
    max_qty_per_day: 800,
    max_net_position: 100,
    bid_limit_percent: 300,
    ask_limit_percent: 300
  }
]);

const instrumentConfigColumns = [
  { name: "instrument_id", label: "合约代码", field: "instrument_id", align: "left" },
  { name: "max_qty_per_order", label: "每单最大数量", field: "max_qty_per_order", align: "center" },
  { name: "max_qty_per_day", label: "每日最大数量", field: "max_qty_per_day", align: "center" },
  { name: "max_net_position", label: "最大净持仓", field: "max_net_position", align: "center" },
  { name: "actions", label: "操作", field: "actions", align: "center" }
];

const positionMethodOptions = [
  { label: "CLOSE", value: "CLOSE" },
  { label: "CLOSE_YESTERDAY", value: "CLOSE_YESTERDAY" },
  { label: "CLOSE_TODAY", value: "CLOSE_TODAY" }
];

function loadConfig() {
  // 加载配置逻辑
  console.log("Loading config for machine:", selectedMachine.value);
}

function addInstrumentPath() {
  coreConfig.instrument_file_paths.push("");
}

function removeInstrumentPath(index: number) {
  coreConfig.instrument_file_paths.splice(index, 1);
}

function addRatioValue() {
  coreConfig.ratio_values.push(100000);
}

function removeRatioValue(index: number) {
  coreConfig.ratio_values.splice(index, 1);
}

function saveConfig() {
  saving.value = true;
  // 模拟保存
  setTimeout(() => {
    saving.value = false;
    $q.notify({
      type: "positive",
      message: "配置保存成功"
    });
  }, 1000);
}

function importXML() {
  if (!importFile.value) return;

  importing.value = true;
  // 模拟导入
  setTimeout(() => {
    importing.value = false;
    showImportDialog.value = false;
    $q.notify({
      type: "positive",
      message: "XML导入成功"
    });
  }, 2000);
}

function exportXML() {
  $q.notify({
    type: "positive",
    message: "XML导出成功"
  });
}

// 生成 XML 预览（示例格式，可按后端实际需要调整）
const xmlPreview = computed(() => {
  const indent = (level: number) => "  ".repeat(level);
  const esc = (v: string | number | boolean) => String(v).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  const core = coreConfig;
  const risk = riskConfig;

  const coreXml = [
    `${indent(1)}<CoreConfig>`,
    `${indent(2)}<InstrumentFilePaths>`,
    ...core.instrument_file_paths.map(p => `${indent(3)}<Path>${esc(p)}</Path>`),
    `${indent(2)}</InstrumentFilePaths>`,
    `${indent(2)}<InstrumentFeeFile>${esc(core.instrument_fee_file)}</InstrumentFeeFile>`,
    `${indent(2)}<VirtualInstrumentFile>${esc(core.virtual_instrument_file)}</VirtualInstrumentFile>`,
    `${indent(2)}<PositionFile>${esc(core.position_file)}</PositionFile>`,
    `${indent(2)}<TradeFile>${esc(core.trade_file)}</TradeFile>`,
    `${indent(2)}<OrderFile>${esc(core.order_file)}</OrderFile>`,
    `${indent(2)}<IgnoreInstrumentsWithoutConfig>${core.ignore_instruments_without_config}</IgnoreInstrumentsWithoutConfig>`,
    `${indent(2)}<IgnoreDuplicateInstruments>${core.ignore_duplicate_instruments}</IgnoreDuplicateInstruments>`,
    `${indent(2)}<KeepCffexGfexInNight>${core.keep_cffex_gfex_in_night_trading}</KeepCffexGfexInNight>`,
    `${indent(2)}<ArbiCheckInterval>${core.arbi_check_interval}</ArbiCheckInterval>`,
    `${indent(2)}<MaxOrderPerSec>${core.max_order_per_sec}</MaxOrderPerSec>`,
    `${indent(2)}<RatioValues>`,
    ...core.ratio_values.map(v => `${indent(3)}<Value>${esc(v)}</Value>`),
    `${indent(2)}</RatioValues>`,
    `${indent(1)}</CoreConfig>`
  ].join("\n");

  const riskXml = [
    `${indent(1)}<RiskConfig>`,
    `${indent(2)}<CheckCrossOrder>${risk.check_cross_order}</CheckCrossOrder>`,
    `${indent(2)}<BidLimitPercent>${risk.bid_limit_percent}</BidLimitPercent>`,
    `${indent(2)}<BidLimitValue>${risk.bid_limit_value}</BidLimitValue>`,
    `${indent(2)}<AskLimitPercent>${risk.ask_limit_percent}</AskLimitPercent>`,
    `${indent(2)}<AskLimitValue>${risk.ask_limit_value}</AskLimitValue>`,
    `${indent(2)}<AskLimitUpPercent>${risk.ask_limit_up_percent}</AskLimitUpPercent>`,
    `${indent(2)}<AskLimitDownPercent>${risk.ask_limit_down_percent}</AskLimitDownPercent>`,
    `${indent(2)}<MaxQtyPerOrder>${risk.max_qty_per_order}</MaxQtyPerOrder>`,
    `${indent(2)}<MaxQtyPerDay>${risk.max_qty_per_day}</MaxQtyPerDay>`,
    `${indent(2)}<MaxQtyPerSec>${risk.max_qty_per_sec}</MaxQtyPerSec>`,
    `${indent(2)}<PositionMethod>${risk.position_method}</PositionMethod>`,
    `${indent(2)}<MinNetPosition>${risk.min_net_position}</MinNetPosition>`,
    `${indent(2)}<MaxNetPosition>${risk.max_net_position}</MaxNetPosition>`,
    `${indent(2)}<MaxSelfTradeCount>${risk.max_self_trade_count}</MaxSelfTradeCount>`,
    `${indent(2)}<MaxCancelCount>${risk.max_cancel_count}</MaxCancelCount>`,
    `${indent(2)}<MaxTradeCount>${risk.max_trade_count}</MaxTradeCount>`,
    `${indent(1)}</RiskConfig>`
  ].join("\n");



  const instrumentsXml = [
    `${indent(1)}<InstrumentConfigs>`,
    ...instrumentConfigs.value.map(i => [
      `${indent(2)}<InstrumentConfig>`,
      `${indent(3)}<InstrumentId>${esc(i.instrument_id)}</InstrumentId>`,
      `${indent(3)}<MaxQtyPerOrder>${i.max_qty_per_order}</MaxQtyPerOrder>`,
      `${indent(3)}<MaxQtyPerDay>${i.max_qty_per_day}</MaxQtyPerDay>`,
      `${indent(3)}<MaxNetPosition>${i.max_net_position}</MaxNetPosition>`,
      `${indent(2)}</InstrumentConfig>`
    ].join("\n")),
    `${indent(1)}</InstrumentConfigs>`
  ].join("\n");

  return [
    `<?xml version="1.0" encoding="UTF-8"?>`,
    `<RiskManagerConfig>`,
    coreXml,
    riskXml,
    instrumentsXml,
    `</RiskManagerConfig>`
  ].join("\n");
});

function copyXml() {
  navigator.clipboard.writeText(xmlPreview.value).then(() => {
    $q.notify({ type: "positive", message: "XML已复制到剪贴板" });
  });
}

function downloadXml() {
  const blob = new Blob([xmlPreview.value], { type: "application/xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "risk_manager_config.xml";
  a.click();
  URL.revokeObjectURL(url);
}

// highlight.js render
function highlightXml() {
  const hljs = (window as any).hljs;
  if (xmlCodeEl.value && hljs && typeof hljs.highlightElement === "function") {
    hljs.highlightElement(xmlCodeEl.value);
  }
}

watch(xmlPreview, async () => {
  await nextTick();
  highlightXml();
});

onMounted(() => {
  highlightXml();
});




function editInstrumentConfig(config: any) {
  // 编辑合约配置逻辑
  console.log("Edit instrument config:", config);
}

function deleteInstrumentConfig(config: any) {
  $q.dialog({
    title: "确认删除",
    message: `确定要删除合约 "${config.instrument_id}" 的配置吗？`,
    cancel: true,
    persistent: true
  }).onOk(() => {
    const index = instrumentConfigs.value.findIndex(c => c.id === config.id);
    if (index > -1) {
      instrumentConfigs.value.splice(index, 1);
      $q.notify({
        type: "positive",
        message: "合约配置删除成功"
      });
    }
  });
}

onMounted(() => {
  // 初始化
  selectedMachine.value = machineOptions.value[0];
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}

.xml-preview-card {
  max-height: calc(100vh - 180px);
  overflow: auto;
}

.xml-code pre {
  margin: 0;
  white-space: pre;
}

.xml-code.wrap pre {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
