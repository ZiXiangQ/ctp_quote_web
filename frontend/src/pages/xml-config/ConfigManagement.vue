<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="q-ma-none">
          配置管理 - {{ machine?.name }}
        </h4>
        <p class="text-grey-6 q-ma-none">
          管理机器配置版本和参数
        </p>
      </div>
      <div class="col-auto">
        <q-btn color="secondary" icon="upload" label="导入XML" class="q-mr-sm" @click="showImportDialog = true" />
        <q-btn color="primary" icon="download" label="导出XML" @click="exportConfig" />
      </div>
    </div>

    <!-- 版本选择 -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row items-center">
          <div class="col">
            <q-select v-model="selectedVersion" :options="versionOptions" label="选择配置版本" outlined
              @update:model-value="loadVersionConfig" />
          </div>
          <div class="col-auto q-ml-md">
            <q-btn color="positive" icon="add" label="新建版本" class="q-mr-sm" @click="showVersionDialog = true" />
            <q-btn v-if="selectedVersion" color="primary" icon="check" label="激活版本" class="q-mr-sm"
              @click="activateVersion" />
            <q-btn v-if="selectedVersion" color="negative" icon="delete" label="删除版本" @click="deleteVersion" />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- 配置类型列表 -->
    <q-card>
      <q-list>
        <q-item v-ripple clickable @click="editCoreConfig">
          <q-item-section avatar>
            <q-icon name="settings" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>核心配置</q-item-label>
            <q-item-label caption>
              文件路径、系统参数等基础配置
            </q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-badge :color="coreConfigStatus.color" :label="coreConfigStatus.label" />
          </q-item-section>
        </q-item>

        <q-separator />

        <q-item v-ripple clickable @click="editRiskConfig">
          <q-item-section avatar>
            <q-icon name="security" color="warning" />
          </q-item-section>
          <q-item-section>
            <q-item-label>默认风险配置</q-item-label>
            <q-item-label caption>
              价格限制、数量限制、持仓限制等风险参数
            </q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-badge :color="riskConfigStatus.color" :label="riskConfigStatus.label" />
          </q-item-section>
        </q-item>

        <q-separator />



        <q-separator />

        <q-item v-ripple clickable @click="editInstrumentConfigs">
          <q-item-section avatar>
            <q-icon name="list_alt" color="secondary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>合约配置</q-item-label>
            <q-item-label caption>
              特定合约的风险控制配置
            </q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-badge :color="instrumentConfigStatus.color" :label="instrumentConfigStatus.label" />
          </q-item-section>
        </q-item>
      </q-list>
    </q-card>

    <!-- 新建版本对话框 -->
    <q-dialog v-model="showVersionDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">
            新建配置版本
          </div>
        </q-card-section>

        <q-card-section>
          <q-form class="q-gutter-md" @submit="createVersion">
            <q-input v-model="versionForm.version_name" label="版本名称" :rules="[val => !!val || '请输入版本名称']" outlined />
            <q-input v-model="versionForm.version_number" label="版本号" :rules="[val => !!val || '请输入版本号']" outlined />
            <q-input v-model="versionForm.description" label="描述" type="textarea" outlined />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" @click="showVersionDialog = false" />
          <q-btn color="primary" label="创建" @click="createVersion" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- 导入XML对话框 -->
    <q-dialog v-model="showImportDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">
            导入XML配置
          </div>
        </q-card-section>

        <q-card-section>
          <q-file v-model="importFile" label="选择XML文件" accept=".xml" outlined @update:model-value="handleFileSelect" />
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
import { api } from "@/services/api";
import { useQuasar } from "quasar";
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

interface Machine {
  id: number
  name: string
  description: string
  status: string
}

interface ConfigVersion {
  id: number
  version_name: string
  version_number: string
  description: string
  is_active: boolean
  created_at: string
}

const route = useRoute();
const router = useRouter();
const $q = useQuasar();

const machine = ref<Machine | null>(null);
const versions = ref<ConfigVersion[]>([]);
const selectedVersion = ref<ConfigVersion | null>(null);
const showVersionDialog = ref(false);
const showImportDialog = ref(false);
const importFile = ref<File | null>(null);
const importing = ref(false);

const versionForm = reactive({
  version_name: "",
  version_number: "",
  description: ""
});

const versionOptions = computed(() =>
  versions.value.map(v => ({
    label: `${v.version_name} (${v.version_number})`,
    value: v
  }))
);

const coreConfigStatus = computed(() => {
  // 这里应该根据实际配置状态返回
  return { color: "positive", label: "已配置" };
});

const riskConfigStatus = computed(() => {
  return { color: "positive", label: "已配置" };
});

const userConfigStatus = computed(() => {
  return { color: "warning", label: "未配置" };
});

const instrumentConfigStatus = computed(() => {
  return { color: "positive", label: "已配置" };
});

async function loadMachine() {
  const machineId = route.params.id;
  try {
    const response = await api.get(`/v1/machines/${machineId}`);
    machine.value = response.data.data;
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "加载机器信息失败"
    });
  }
}

async function loadVersions() {
  const machineId = route.params.id;
  try {
    const response = await api.get(`/v1/machines/${machineId}/versions`);
    versions.value = response.data.data || [];

    // 默认选择激活的版本
    const activeVersion = versions.value.find(v => v.is_active);
    if (activeVersion) {
      selectedVersion.value = activeVersion;
    }
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "加载版本列表失败"
    });
  }
}

function loadVersionConfig() {
  if (selectedVersion.value) {
    // 加载选中版本的配置
    console.log("Loading config for version:", selectedVersion.value.id);
  }
}

async function createVersion() {
  const machineId = route.params.id;
  try {
    await api.post(`/v1/machines/${machineId}/versions`, versionForm);
    $q.notify({
      type: "positive",
      message: "版本创建成功"
    });
    showVersionDialog.value = false;
    versionForm.version_name = "";
    versionForm.version_number = "";
    versionForm.description = "";
    loadVersions();
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "版本创建失败"
    });
  }
}

async function activateVersion() {
  if (!selectedVersion.value) return;

  const machineId = route.params.id;
  try {
    await api.put(`/v1/machines/${machineId}/versions/${selectedVersion.value.id}/activate`);
    $q.notify({
      type: "positive",
      message: "版本激活成功"
    });
    loadVersions();
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "版本激活失败"
    });
  }
}

async function deleteVersion() {
  if (!selectedVersion.value) return;

  $q.dialog({
    title: "确认删除",
    message: `确定要删除版本 "${selectedVersion.value.version_name}" 吗？`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    const machineId = route.params.id;
    try {
      await api.delete(`/v1/machines/${machineId}/versions/${selectedVersion.value!.id}`);
      $q.notify({
        type: "positive",
        message: "版本删除成功"
      });
      loadVersions();
    } catch (error) {
      $q.notify({
        type: "negative",
        message: "版本删除失败"
      });
    }
  });
}

function handleFileSelect(file: File) {
  importFile.value = file;
}

async function importXML() {
  if (!importFile.value) return;

  const machineId = route.params.id;
  const formData = new FormData();
  formData.append("file", importFile.value);

  try {
    importing.value = true;
    await api.post(`/v1/machines/${machineId}/import`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });
    $q.notify({
      type: "positive",
      message: "XML导入成功"
    });
    showImportDialog.value = false;
    importFile.value = null;
    loadVersions();
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "XML导入失败"
    });
  } finally {
    importing.value = false;
  }
}

async function exportConfig() {
  const machineId = route.params.id;
  try {
    const response = await api.get(`/v1/machines/${machineId}/export`, {
      responseType: "blob"
    });

    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `riskManager_${machine.value?.name || "config"}.xml`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

    $q.notify({
      type: "positive",
      message: "XML导出成功"
    });
  } catch (error) {
    $q.notify({
      type: "negative",
      message: "XML导出失败"
    });
  }
}

function editCoreConfig() {
  if (!selectedVersion.value) {
    $q.notify({
      type: "warning",
      message: "请先选择配置版本"
    });
    return;
  }
  router.push(`/machines/${route.params.id}/config/core/${selectedVersion.value.id}`);
}

function editRiskConfig() {
  if (!selectedVersion.value) {
    $q.notify({
      type: "warning",
      message: "请先选择配置版本"
    });
    return;
  }
  router.push(`/machines/${route.params.id}/config/risk/${selectedVersion.value.id}`);
}



function editInstrumentConfigs() {
  if (!selectedVersion.value) {
    $q.notify({
      type: "warning",
      message: "请先选择配置版本"
    });
    return;
  }
  router.push(`/machines/${route.params.id}/config/instruments/${selectedVersion.value.id}`);
}

onMounted(() => {
  loadMachine();
  loadVersions();
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}

.q-item {
  border-radius: 8px;
  margin: 4px 0;
}

.q-item:hover {
  background-color: var(--q-primary-light);
}
</style>
