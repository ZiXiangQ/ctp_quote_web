<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="q-ma-none">合约配置管理</h4>
        <p class="text-grey-6 q-ma-none">管理特定合约的风险控制配置</p>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="添加合约配置"
          @click="showAddDialog = true"
        />
      </div>
    </div>

    <!-- 合约配置列表 -->
    <q-card>
      <q-table
        :rows="instrumentConfigs"
        :columns="columns"
        row-key="id"
        :loading="loading"
        :pagination="pagination"
        @request="onRequest"
        binary-state-sort
      >
        <template #body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              color="primary"
              icon="edit"
              size="sm"
              @click="editInstrumentConfig(props.row)"
            >
              <q-tooltip>编辑</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              color="negative"
              icon="delete"
              size="sm"
              @click="deleteInstrumentConfig(props.row)"
            >
              <q-tooltip>删除</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- 添加/编辑合约配置对话框 -->
    <q-dialog v-model="showAddDialog" persistent>
      <q-card style="min-width: 700px">
        <q-card-section>
          <div class="text-h6">
            {{ editingConfig ? '编辑合约配置' : '添加合约配置' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form class="q-gutter-md" @submit="saveInstrumentConfig">
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="configForm.instrument_id"
                  label="合约代码"
                  :rules="[val => !!val || '请输入合约代码']"
                  outlined
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="configForm.max_qty_per_order"
                  label="每单最大数量"
                  type="number"
                  outlined
                  :rules="[val => val > 0 || '必须大于0']"
                />
              </div>
            </div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="configForm.max_qty_per_day"
                  label="每日最大数量"
                  type="number"
                  outlined
                  :rules="[val => val > 0 || '必须大于0']"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="configForm.max_net_position"
                  label="最大净持仓"
                  type="number"
                  outlined
                />
              </div>
            </div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="configForm.bid_limit_percent"
                  label="买价限制百分比(%)"
                  type="number"
                  outlined
                  :rules="[val => val >= 0 || '必须大于等于0']"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="configForm.ask_limit_percent"
                  label="卖价限制百分比(%)"
                  type="number"
                  outlined
                  :rules="[val => val >= 0 || '必须大于等于0']"
                />
              </div>
            </div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="configForm.bid_limit_value"
                  label="买价限制值"
                  type="number"
                  outlined
                  :rules="[val => val >= 0 || '必须大于等于0']"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="configForm.ask_limit_value"
                  label="卖价限制值"
                  type="number"
                  outlined
                  :rules="[val => val >= 0 || '必须大于等于0']"
                />
              </div>
            </div>
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" @click="closeDialog" />
          <q-btn color="primary" label="保存" @click="saveInstrumentConfig" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- 删除确认对话框 -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">确认删除</div>
        </q-card-section>

        <q-card-section>
          确定要删除合约 "{{ deletingConfig?.instrument_id }}" 的配置吗？此操作不可撤销。
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" @click="showDeleteDialog = false" />
          <q-btn color="negative" label="删除" @click="confirmDelete" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { httpClient } from "../services/api";
import { useQuasar } from "quasar";
import { onMounted, reactive, ref } from "vue";
import { useRoute } from "vue-router";

interface InstrumentConfig {
  id: number
  instrument_id: string
  max_qty_per_order: number
  max_qty_per_day: number
  max_net_position: number
  bid_limit_percent: number
  ask_limit_percent: number
  bid_limit_value: number
  ask_limit_value: number
  created_at: string
  updated_at: string
}

const route = useRoute();
const $q = useQuasar();

const instrumentConfigs = ref<InstrumentConfig[]>([]);
const loading = ref(false);
const showAddDialog = ref(false);
const showDeleteDialog = ref(false);
const editingConfig = ref<InstrumentConfig | null>(null);
const deletingConfig = ref<InstrumentConfig | null>(null);

const configForm = reactive({
  instrument_id: "",
  max_qty_per_order: 50,
  max_qty_per_day: 400,
  max_net_position: 50,
  bid_limit_percent: 200,
  ask_limit_percent: 200,
  bid_limit_value: 10000,
  ask_limit_value: 10000
});

const columns = [
  {
    name: "instrument_id",
    required: true,
    label: "合约代码",
    align: "left",
    field: "instrument_id",
    sortable: true
  },
  {
    name: "max_qty_per_order",
    label: "每单最大数量",
    align: "center",
    field: "max_qty_per_order",
    sortable: true
  },
  {
    name: "max_qty_per_day",
    label: "每日最大数量",
    align: "center",
    field: "max_qty_per_day",
    sortable: true
  },
  {
    name: "max_net_position",
    label: "最大净持仓",
    align: "center",
    field: "max_net_position",
    sortable: true
  },
  {
    name: "bid_limit_percent",
    label: "买价限制(%)",
    align: "center",
    field: "bid_limit_percent",
    sortable: true
  },
  {
    name: "ask_limit_percent",
    label: "卖价限制(%)",
    align: "center",
    field: "ask_limit_percent",
    sortable: true
  },
  {
    name: "created_at",
    label: "创建时间",
    align: "center",
    field: "created_at",
    format: (val: string) => new Date(val).toLocaleString(),
    sortable: true
  },
  {
    name: "actions",
    label: "操作",
    align: "center",
    field: "actions"
  }
];

const pagination = ref({
  sortBy: "instrument_id",
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
});

async function loadInstrumentConfigs() {
  const machineId = route.params.machineId;
  const versionId = route.params.versionId;
  
  try {
    loading.value = true;
    const response = await httpClient.get(`/v1/machines/${machineId}/versions/${versionId}/instrument-configs`);
    instrumentConfigs.value = response.data.data || [];
    pagination.value.rowsNumber = instrumentConfigs.value.length;
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "加载合约配置失败"
    });
  } finally {
    loading.value = false;
  }
}

function onRequest(props: any) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;
  pagination.value.page = page;
  pagination.value.rowsPerPage = rowsPerPage;
  pagination.value.sortBy = sortBy;
  pagination.value.descending = descending;
  loadInstrumentConfigs();
}

function editInstrumentConfig(config: InstrumentConfig) {
  editingConfig.value = config;
  configForm.instrument_id = config.instrument_id;
  configForm.max_qty_per_order = config.max_qty_per_order;
  configForm.max_qty_per_day = config.max_qty_per_day;
  configForm.max_net_position = config.max_net_position;
  configForm.bid_limit_percent = config.bid_limit_percent;
  configForm.ask_limit_percent = config.ask_limit_percent;
  configForm.bid_limit_value = config.bid_limit_value;
  configForm.ask_limit_value = config.ask_limit_value;
  showAddDialog.value = true;
}

function deleteInstrumentConfig(config: InstrumentConfig) {
  deletingConfig.value = config;
  showDeleteDialog.value = true;
}

async function saveInstrumentConfig() {
  const machineId = route.params.machineId;
  const versionId = route.params.versionId;
  
  try {
    if (editingConfig.value) {
      // 更新合约配置
      await httpClient.put(`/v1/machines/${machineId}/versions/${versionId}/instrument-configs/${editingConfig.value.id}`, configForm);
      $q.notify({
        type: "positive",
        message: "合约配置更新成功"
      });
    } else {
      // 创建合约配置
      await httpClient.post(`/v1/machines/${machineId}/versions/${versionId}/instrument-configs`, configForm);
      $q.notify({
        type: "positive",
        message: "合约配置创建成功"
      });
    }
    closeDialog();
    loadInstrumentConfigs();
  } catch (error) {
    $q.notify({
      type: "negative",
      message: editingConfig.value ? "更新失败" : "创建失败"
    });
  }
}

async function confirmDelete() {
  if (!deletingConfig.value) return;
  
  const machineId = route.params.machineId;
  const versionId = route.params.versionId;
  
  try {
    await httpClient.delete(`/v1/machines/${machineId}/versions/${versionId}/instrument-configs/${deletingConfig.value.id}`);
    $q.notify({
      type: "positive",
      message: "合约配置删除成功"
    });
    showDeleteDialog.value = false;
    loadInstrumentConfigs();
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "删除失败"
    });
  }
}

function closeDialog() {
  showAddDialog.value = false;
  editingConfig.value = null;
  configForm.instrument_id = "";
  configForm.max_qty_per_order = 50;
  configForm.max_qty_per_day = 400;
  configForm.max_net_position = 50;
  configForm.bid_limit_percent = 200;
  configForm.ask_limit_percent = 200;
  configForm.bid_limit_value = 10000;
  configForm.ask_limit_value = 10000;
}

onMounted(() => {
  loadInstrumentConfigs();
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}
</style>
