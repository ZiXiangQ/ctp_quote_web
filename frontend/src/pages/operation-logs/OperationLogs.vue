<template>
  <q-page class="q-pa-md">
    <!-- 筛选条件 -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="col-auto" style="width: 150px;">
            <q-select v-model="filters.operation_type" :options="operationTypeOptions" label="操作类型" outlined
              clearable />
          </div>
          <div class="col-auto" style="width: 150px;">
            <q-input v-model="filters.start_date" label="开始日期" type="date" outlined />
          </div>
          <div class="col-auto" style="width: 150px;">
            <q-input v-model="filters.end_date" label="结束日期" type="date" outlined />
          </div>
          <div class="col-auto" style="width: 150px;">
            <q-input v-model="filters.operator" label="操作者" outlined clearable />
          </div>
          <div class="col-auto">
            <q-btn color="primary" icon="search" label="搜索" @click="applyFilters" />
          </div>
          <div class="col-auto">
            <q-btn color="secondary" icon="clear" label="清空" @click="clearFilters" />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- 日志列表 -->
    <q-card>
      <q-table :rows="filteredLogs" :columns="columns" row-key="id" :loading="loading" :pagination="pagination"
        binary-state-sort @request="onRequest">
        <template #body-cell-operation_type="props">
          <q-td :props="props">
            <q-badge :color="getOperationTypeColor(props.value)" :label="getOperationTypeLabel(props.value)" />
          </q-td>
        </template>

        <template #body-cell-log_level="props">
          <q-td :props="props">
            <q-badge :color="getLogLevelColor(props.value)" :label="props.value.toUpperCase()" />
          </q-td>
        </template>

        <template #body-cell-created_at="props">
          <q-td :props="props">
            {{ formatDateTime(props.value) }}
          </q-td>
        </template>

        <template #body-cell-operation_details="props">
          <q-td :props="props">
            <q-btn flat round color="primary" icon="info" size="sm" @click="showDetails(props.value)">
              <q-tooltip>查看详情</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- 详情对话框 -->
    <q-dialog v-model="showDetailsDialog" persistent>
      <q-card style="min-width: 600px; max-width: 800px">
        <q-card-section>
          <div class="text-h6">
            操作详情
          </div>
        </q-card-section>

        <q-card-section>
          <div class="q-gutter-md">
            <div class="row">
              <div class="col-3 text-weight-medium">
                操作类型:
              </div>
              <div class="col-9">
                {{ selectedLog?.operation_type }}
              </div>
            </div>
            <div class="row">
              <div class="col-3 text-weight-medium">
                操作者:
              </div>
              <div class="col-9">
                {{ selectedLog?.operator }}
              </div>
            </div>

            <div class="row">
              <div class="col-3 text-weight-medium">
                时间:
              </div>
              <div class="col-9">
                {{ formatDateTime(selectedLog?.created_at) }}
              </div>
            </div>

            <div class="row">
              <div class="col-3 text-weight-medium">
                操作详情:
              </div>
              <div class="col-9">
                <pre class="text-caption bg-grey-2 q-pa-md rounded-borders">{{
                  JSON.stringify(selectedLog?.operation_details, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="关闭" @click="showDetailsDialog = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { useQuasar } from "quasar";
import { onMounted, reactive, ref } from "vue";

interface OperationLog {
  id: number;
  machine_id: number;
  machine_name: string;
  version_id?: number;
  operation_type: string;
  operation_details: any;
  operator: string;
  log_level: string;
  created_at: string;
}

const $q = useQuasar();

const logs = ref<OperationLog[]>([]);
const filteredLogs = ref<OperationLog[]>([]);
const loading = ref(false);
const showDetailsDialog = ref(false);
const selectedLog = ref<OperationLog | null>(null);

const filters = reactive({
  operation_type: null,

  start_date: "",
  end_date: "",
  operator: "",
  log_level: null
});

const operationTypeOptions = [
  { label: "创建", value: "create" },
  { label: "更新", value: "update" },
  { label: "删除", value: "delete" },
  { label: "导入", value: "import" },
  { label: "导出", value: "export" },
  { label: "启动", value: "start" },
  { label: "停止", value: "stop" },
  { label: "重启", value: "restart" }
];





const columns = [
  {
    name: "created_at",
    required: true,
    label: "时间",
    align: "left",
    field: "created_at",
    sortable: true
  },
  {
    name: "operation_type",
    label: "操作类型",
    align: "center",
    field: "operation_type",
    sortable: true
  },
  {
    name: "operator",
    label: "操作者",
    align: "center",
    field: "operator",
    sortable: true
  },
  {
    name: "change_summary",
    label: "修改内容",
    align: "left",
    field: (row: any) => summarizeChange(row),
    sortable: false
  },

  {
    name: "operation_details",
    label: "详情",
    align: "center",
    field: "operation_details"
  }
];

const pagination = ref({
  sortBy: "created_at",
  descending: true,
  page: 1,
  rowsPerPage: 20,
  rowsNumber: 0
});

function getOperationTypeColor(type: string) {
  switch (type) {
    case "create": return "positive";
    case "update": return "primary";
    case "delete": return "negative";
    case "import": return "info";
    case "export": return "warning";
    case "start": return "positive";
    case "stop": return "negative";
    case "restart": return "warning";
    default: return "grey";
  }
}

function getOperationTypeLabel(type: string) {
  switch (type) {
    case "create": return "创建";
    case "update": return "更新";
    case "delete": return "删除";
    case "import": return "导入";
    case "export": return "导出";
    case "start": return "启动";
    case "stop": return "停止";
    case "restart": return "重启";
    default: return "未知";
  }
}

function getLogLevelColor(level: string) {
  switch (level) {
    case "info": return "info";
    case "warning": return "warning";
    case "error": return "negative";
    case "debug": return "grey";
    default: return "grey";
  }
}

function formatDateTime(dateTime: string) {
  return new Date(dateTime).toLocaleString();
}

function summarizeChange(row: any) {
  const d = row.operation_details;
  if (!d) return "";
  try {
    return JSON.stringify(d);
  } catch (e) {
    return String(d);
  }
}

function loadLogs() {
  // 模拟数据
  const mockLogs: OperationLog[] = [
    {
      id: 1,
      machine_id: 1,
      machine_name: "trading-server-01",
      version_id: 1,
      operation_type: "create",
      operation_details: { action: "创建机器", name: "trading-server-01", ip: "192.168.1.100" },
      operator: "admin",
      log_level: "info",
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      machine_id: 1,
      machine_name: "trading-server-01",
      version_id: 1,
      operation_type: "import",
      operation_details: { action: "导入XML配置", file: "riskManager.xml", size: "2.5KB" },
      operator: "admin",
      log_level: "info",
      created_at: new Date(Date.now() - 3600000).toISOString()
    },
    {
      id: 3,
      machine_id: 2,
      machine_name: "trading-server-02",
      version_id: 2,
      operation_type: "start",
      operation_details: { action: "启动机器", status: "success" },
      operator: "operator1",
      log_level: "info",
      created_at: new Date(Date.now() - 7200000).toISOString()
    },
    {
      id: 4,
      machine_id: 1,
      machine_name: "trading-server-01",
      version_id: 1,
      operation_type: "update",
      operation_details: { action: "更新风险配置", field: "max_qty_per_order", old_value: 50, new_value: 100 },
      operator: "admin",
      log_level: "warning",
      created_at: new Date(Date.now() - 10800000).toISOString()
    },
    {
      id: 5,
      machine_id: 3,
      machine_name: "trading-server-03",
      version_id: 1,
      operation_type: "delete",
      operation_details: { action: "删除用户配置", user_id: "user001" },
      operator: "admin",
      log_level: "error",
      created_at: new Date(Date.now() - 14400000).toISOString()
    }
  ];

  logs.value = mockLogs;
  filteredLogs.value = mockLogs;
  pagination.value.rowsNumber = mockLogs.length;
}

function applyFilters() {
  let filtered = logs.value;

  if (filters.operation_type) {
    filtered = filtered.filter(log => log.operation_type === filters.operation_type);
  }



  if (filters.operator) {
    filtered = filtered.filter(log =>
      log.operator.toLowerCase().includes(filters.operator.toLowerCase())
    );
  }



  if (filters.start_date) {
    const startDate = new Date(filters.start_date);
    filtered = filtered.filter(log => new Date(log.created_at) >= startDate);
  }

  if (filters.end_date) {
    const endDate = new Date(filters.end_date);
    endDate.setHours(23, 59, 59, 999); // 设置为当天的最后一刻
    filtered = filtered.filter(log => new Date(log.created_at) <= endDate);
  }

  filteredLogs.value = filtered;
  pagination.value.rowsNumber = filtered.length;
}

function clearFilters() {
  filters.operation_type = null;

  filters.start_date = "";
  filters.end_date = "";
  filters.operator = "";

  filteredLogs.value = logs.value;
  pagination.value.rowsNumber = logs.value.length;
}

function onRequest(props: any) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;
  pagination.value.page = page;
  pagination.value.rowsPerPage = rowsPerPage;
  pagination.value.sortBy = sortBy;
  pagination.value.descending = descending;
  loadLogs();
}

function showDetails(details: any) {
  // 找到对应的日志记录
  const log = filteredLogs.value.find(l => l.operation_details === details);
  selectedLog.value = log || null;
  showDetailsDialog.value = true;
}

onMounted(() => {
  loadLogs();
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}

pre {
  background-color: var(--q-surface-variant);
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
  max-height: 300px;
}
</style>
