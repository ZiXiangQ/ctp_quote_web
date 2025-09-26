<template>
  <q-page class="q-pa-sm">
    <div class="row row-spacing">
      <div class="col-4 col-sm-4">
        <q-input v-model="searchText" label="搜索机器名称" outlined clearable dense @input="filterMachines">
          <template #prepend>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>
      <div class="col-8 flex items-center justify-end">
        <q-btn color="primary" icon="add" label="添加机器" @click="showAddDialog = true" />
      </div>
    </div>

    <!-- 机器列表 -->
    <q-table :rows="filteredMachines" :columns="columns" row-key="id" :loading="loading" :pagination="pagination"
      binary-state-sort @request="onRequest">
      <template #body-cell-xml_config="props">
        <q-td :props="props">
          <q-btn flat round color="primary" icon="settings" size="sm" @click="manageConfig(props.row)">
            <q-tooltip>管理XML配置</q-tooltip>
          </q-btn>
        </q-td>
      </template>
      <template #body-cell-actions="props">
        <q-td :props="props">
          <q-btn flat round color="primary" icon="edit" size="sm" @click="editMachine(props.row)">
            <q-tooltip>编辑</q-tooltip>
          </q-btn>
          <q-btn flat round color="negative" icon="delete" size="sm" @click="deleteMachine(props.row)">
            <q-tooltip>删除</q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>

    <!-- 添加/编辑机器对话框 -->
    <q-dialog v-model="showAddDialog" persistent>
      <q-card style="width: 400px">
        <q-card-section>
          <div class="text-h6">
            {{ editingMachine ? '编辑机器' : '添加机器' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form class="q-gutter-md" @submit="saveMachine">
            <div class="col">
              <q-input v-model="machineForm.name" label="机器名称" :rules="[val => !!val || '请输入机器名称']" outlined />
              <q-input v-model="machineForm.description" label="描述" outlined />
              <q-select v-model="machineForm.xmlFileName" :options="xmlOptions" label="关联XML文件" outlined dense />
            </div>
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" @click="closeDialog" />
          <q-btn color="primary" label="保存" @click="saveMachine" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- 删除确认对话框 -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">
            确认删除
          </div>
        </q-card-section>

        <q-card-section>
          确定要删除机器 "{{ deletingMachine?.name }}" 吗？此操作不可撤销。
        </q-card-section>

        <q-card-actions align="right">
          <q-btn color="negative" label="删除" @click="confirmDelete" />
          <q-btn flat label="取消" @click="showDeleteDialog = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { useQuasar } from "quasar";
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

interface Machine {
  id: number;
  name: string;
  description: string;
  xml_file_name?: string;
  created_at: string;
  updated_at: string;
}

const router = useRouter();
const $q = useQuasar();

const machines = ref<Machine[]>([]);
const filteredMachines = ref<Machine[]>([]);
const loading = ref(false);
const showAddDialog = ref(false);
const showDeleteDialog = ref(false);
const editingMachine = ref<Machine | null>(null);
const deletingMachine = ref<Machine | null>(null);
const searchText = ref("");
const xmlOptions = ref<string[]>(["riskManager.xml", "default.xml", "prod.xml"]);

const machineForm = reactive({
  name: "",
  description: "",
  xmlFileName: ""
});


const columns = [
  {
    name: "name",
    required: true,
    label: "机器名称",
    align: "left" as const,
    field: "name",
    sortable: true
  },
  {
    name: "description",
    label: "描述",
    align: "left" as const,
    field: "description",
    sortable: true
  },
  {
    name: "xml_config",
    label: "关联XML配置",
    align: "center" as const,
    field: "xml_config"
  },
  {
    name: "created_at",
    label: "创建时间",
    align: "center" as const,
    field: "created_at",
    format: (val: string) => new Date(val).toLocaleString(),
    sortable: true
  },
  {
    name: "updated_at",
    label: "更新时间",
    align: "center" as const,
    field: "updated_at",
    format: (val: string) => new Date(val).toLocaleString(),
    sortable: true
  },
  {
    name: "actions",
    label: "操作",
    align: "center" as const,
    field: "actions"
  }
];

const pagination = ref({
  sortBy: "name",
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
});


function loadMachines() {
  // 模拟数据
  const mockMachines: Machine[] = [
    {
      id: 1,
      name: "trading-server-01",
      description: "主交易服务器",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    },
    {
      id: 2,
      name: "trading-server-02",
      description: "备用交易服务器",
      created_at: new Date(Date.now() - 86400000).toISOString(),
      updated_at: new Date(Date.now() - 86400000).toISOString()
    },
    {
      id: 3,
      name: "trading-server-03",
      description: "测试交易服务器",
      created_at: new Date(Date.now() - 172800000).toISOString(),
      updated_at: new Date(Date.now() - 172800000).toISOString()
    }
  ];

  machines.value = mockMachines;
  filteredMachines.value = mockMachines;
  pagination.value.rowsNumber = mockMachines.length;
}

function filterMachines() {
  let filtered = machines.value;

  if (searchText.value) {
    filtered = filtered.filter(machine =>
      machine.name.toLowerCase().includes(searchText.value.toLowerCase())
    );
  }

  filteredMachines.value = filtered;
  pagination.value.rowsNumber = filtered.length;
}

function onRequest(props: any) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;
  pagination.value.page = page;
  pagination.value.rowsPerPage = rowsPerPage;
  pagination.value.sortBy = sortBy;
  pagination.value.descending = descending;
  loadMachines();
}

function editMachine(machine: Machine) {
  editingMachine.value = machine;
  machineForm.name = machine.name;
  machineForm.description = machine.description || "";
  machineForm.xmlFileName = machine.xml_file_name || "";
  showAddDialog.value = true;
}

function manageConfig(machine: Machine) {
  router.push(`/xml-config?machineId=${machine.id}`);
}

function onXmlSelected(file: File | File[] | null) {
  if (Array.isArray(file)) {
    machineForm.xmlFile = file[0] || null;
  } else {
    machineForm.xmlFile = file as File | null;
  }
  machineForm.xmlFileName = machineForm.xmlFile ? machineForm.xmlFile.name : "";
}


function deleteMachine(machine: Machine) {
  deletingMachine.value = machine;
  showDeleteDialog.value = true;
}

function saveMachine() {
  if (editingMachine.value) {
    // 更新机器
    editingMachine.value.name = machineForm.name;
    editingMachine.value.description = machineForm.description;
    editingMachine.value.xml_file_name = machineForm.xmlFileName;
    $q.notify({
      type: "positive",
      message: "机器更新成功"
    });
  } else {
    // 创建机器
    const newMachine: Machine = {
      id: Date.now(),
      name: machineForm.name,
      description: machineForm.description,
      xml_file_name: machineForm.xmlFileName,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    machines.value.push(newMachine);
    $q.notify({
      type: "positive",
      message: "机器创建成功"
    });
  }
  closeDialog();
  filterMachines();
}

function confirmDelete() {
  if (!deletingMachine.value) return;

  const index = machines.value.findIndex(m => m.id === deletingMachine.value!.id);
  if (index > -1) {
    machines.value.splice(index, 1);
    $q.notify({
      type: "positive",
      message: "机器删除成功"
    });
  }
  showDeleteDialog.value = false;
  filterMachines();
}

function closeDialog() {
  showAddDialog.value = false;
  editingMachine.value = null;
  machineForm.name = "";
  machineForm.description = "";
  machineForm.xmlFileName = "";
}

onMounted(() => {
  loadMachines();
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}

.row-spacing {
  margin-top: 5px;
  margin-bottom: 10px;
}
</style>
