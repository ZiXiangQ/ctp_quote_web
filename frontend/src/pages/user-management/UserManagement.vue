<template>
  <q-page class="q-pa-md">
    <!-- 页面标题 -->
    <div class="row q-mb-md">
      <div class="col-12 flex justify-end">
        <q-btn color="primary" icon="add" label="添加用户" @click="showAddDialog = true" />
      </div>
    </div>



    <!-- 用户列表 -->
    <q-card>
      <q-table :rows="filteredUsers" :columns="columns" row-key="id" :loading="loading" :pagination="pagination"
        binary-state-sort @request="onRequest">
        <template #body-cell-role="props">
          <q-td :props="props">
            <q-badge :color="getRoleColor(props.value)" :label="getRoleLabel(props.value)" />
          </q-td>
        </template>

        <template #body-cell-status="props">
          <q-td :props="props">
            <q-badge :color="getStatusColor(props.value)" :label="getStatusLabel(props.value)" />
          </q-td>
        </template>

        <template #body-cell-last_login="props">
          <q-td :props="props">
            {{ props.value ? formatDateTime(props.value) : '从未登录' }}
          </q-td>
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props">
            <q-btn flat round color="warning" icon="lock" size="sm" @click="resetPassword(props.row)">
              <q-tooltip>重置密码</q-tooltip>
            </q-btn>
            <q-btn flat round color="negative" icon="delete" size="sm" @click="deleteUser(props.row)">
              <q-tooltip>删除</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- 添加用户对话框 -->
    <q-dialog v-model="showAddDialog" persistent>
      <q-card class="add-user-dialog">
        <q-card-section class="dialog-header">
          <div class="row items-center">
            <div class="col">
              <div class="text-h5 text-weight-bold text-primary">
                <q-icon name="person_add" class="q-mr-sm" />
                添加新用户
              </div>
              <div class="text-caption text-grey-6 q-mt-xs">
                创建新的系统用户账户
              </div>
            </div>
            <div class="col-auto">
              <q-btn flat round icon="close" class="close-btn" @click="closeDialog" />
            </div>
          </div>
        </q-card-section>

        <q-separator />

        <q-card-section class="dialog-content">
          <q-form class="q-gutter-lg" @submit="saveUser">
            <!-- 基本信息卡片 -->
            <q-card flat bordered class="form-section">
              <q-card-section class="q-pt-none">
                <div class="row q-col-gutter-md">
                  <div class="col-12 col-md-6">
                    <q-input v-model="userForm.username" label="用户名" :rules="[val => !!val || '必填']"
                      class="custom-input" lazy-rules>
                      <template #prepend>
                        <q-icon name="person" color="primary" />
                      </template>
                    </q-input>
                  </div>
                  <div class="col-12 col-md-6">
                    <q-input v-model="userForm.full_name" label="姓名" class="custom-input" lazy-rules>
                      <template #prepend>
                        <q-icon name="badge" color="primary" />
                      </template>
                    </q-input>
                  </div>
                  <div class="col-12 col-md-6">
                    <q-select v-model="userForm.role" :options="roleOptions" label="用户角色" class="custom-input"
                      emit-value map-options option-value="value" option-label="label">
                      <template #prepend>
                        <q-icon name="admin_panel_settings" color="primary" />
                      </template>
                    </q-select>
                  </div>
                </div>
                <div class="row q-col-gutter-md " style="margin-top: 15px">
                  <div class="col-12 col-md-6">
                    <q-input v-model="userForm.password" label="密码" type="password"
                      :rules="[val => !!val || '必填', val => val.length >= 6 || '至少6位']" class="custom-input"
                      hint="至少6位字符" lazy-rules>
                      <template #prepend>
                        <q-icon name="vpn_key" color="primary" />
                      </template>
                    </q-input>
                  </div>
                  <div class="col-12 col-md-6">
                    <q-input v-model="userForm.confirmPassword" label="确认密码" type="password"
                      :rules="[val => val === userForm.password || '不一致']" class="custom-input" hint="再次输入密码"
                      lazy-rules>
                      <template #prepend>
                        <q-icon name="vpn_key" color="primary" />
                      </template>
                    </q-input>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-form>
        </q-card-section>

        <q-separator />

        <!-- 对话框底部 -->
        <q-card-actions class="dialog-actions">
          <q-space />
          <q-btn flat label="取消" class="cancel-btn" no-caps @click="closeDialog" />
          <q-btn color="primary" label="创建用户" class="save-btn" no-caps icon="add" @click="saveUser" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- 重置密码对话框 -->
    <q-dialog v-model="showResetPasswordDialog" persistent>
      <q-card class="reset-password-dialog">
        <q-card-section>
          <div class="text-h6 text-weight-bold">
            <q-icon name="vpn_key" class="q-mr-sm" />
            重置密码
          </div>
          <div class="text-caption text-grey-6 q-mt-xs">
            为用户 "{{ resetPasswordUser?.username }}" 设置新密码和状态
          </div>
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-form class="q-gutter-md" @submit="confirmResetPassword">
            <!-- 用户状态开关 -->
            <div class="row items-center q-mb-md">
              <div class="col">
                <div class="text-subtitle2 text-weight-medium">
                  <q-icon name="toggle_on" class="q-mr-sm" />
                  用户状态
                </div>
                <div class="text-caption text-grey-6">
                  当前状态：{{ getStatusLabel(resetPasswordUser?.status || 'active') }}
                </div>
              </div>
              <div class="col-auto">
                <q-toggle v-model="newUserStatus" :true-value="'active'" :false-value="'locked'" color="positive"
                  size="lg" />
              </div>
            </div>

            <q-separator class="q-my-md" />

            <!-- 重置密码输入 -->
            <q-input v-model="newPassword" label="新密码" type="password"
              :rules="[val => !!val || '必填', val => val.length >= 6 || '至少6位']" outlined hint="至少6位字符" lazy-rules>
              <template #prepend>
                <q-icon name="lock" color="primary" />
              </template>
            </q-input>
          </q-form>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="取消" @click="closeResetPasswordDialog" />
          <q-btn color="primary" label="重置密码" @click="confirmResetPassword" />
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
          确定要删除用户 "{{ deletingUser?.username }}" 吗？此操作不可撤销。
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
import { useQuasar } from "quasar";
import { onMounted, reactive, ref } from "vue";

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  phone: string;
  role: string;
  status: string;
  department: string;
  description: string;
  last_login: string;
  created_at: string;
  updated_at: string;
}

const $q = useQuasar();

const users = ref<User[]>([]);
const filteredUsers = ref<User[]>([]);
const loading = ref(false);
const showAddDialog = ref(false);
const showDeleteDialog = ref(false);
const showResetPasswordDialog = ref(false);
const deletingUser = ref<User | null>(null);
const resetPasswordUser = ref<User | null>(null);
const newPassword = ref("");
const newUserStatus = ref("active");

const userForm = reactive({
  username: "",
  full_name: "",
  role: "user",
  password: "",
  confirmPassword: ""
});


const roleOptions = [
  { label: "管理员", value: "admin" },
  { label: "普通用户", value: "user" }
];


const columns = [
  {
    name: "username",
    required: true,
    label: "用户名",
    align: "left" as const,
    field: "username",
    sortable: true
  },
  {
    name: "full_name",
    label: "姓名",
    align: "left" as const,
    field: "full_name",
    sortable: true
  },
  {
    name: "role",
    label: "角色",
    align: "center" as const,
    field: "role",
    sortable: true
  },
  {
    name: "status",
    label: "状态",
    align: "center" as const,
    field: "status",
    sortable: true
  },
  {
    name: "last_login",
    label: "最后登录",
    align: "center" as const,
    field: "last_login",
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
  sortBy: "username",
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
});

function getRoleColor(role: string) {
  switch (role) {
    case "admin": return "negative";
    case "user": return "positive";
    default: return "grey";
  }
}

function getRoleLabel(role: string) {
  switch (role) {
    case "admin": return "管理员";
    case "user": return "普通用户";
    default: return "未知";
  }
}

function getStatusColor(status: string) {
  switch (status) {
    case "active": return "positive";
    case "locked": return "warning";
    case "disabled": return "negative";
    default: return "grey";
  }
}

function getStatusLabel(status: string) {
  switch (status) {
    case "active": return "活跃";
    case "locked": return "锁定";
    case "disabled": return "禁用";
    default: return "未知";
  }
}

function formatDateTime(dateTime: string) {
  return new Date(dateTime).toLocaleString();
}

function loadUsers() {
  // 模拟数据
  const mockUsers: User[] = [
    {
      id: 1,
      username: "admin",
      email: "admin@example.com",
      full_name: "系统管理员",
      phone: "13800138000",
      role: "admin",
      status: "active",
      department: "技术部",
      description: "系统管理员账户",
      last_login: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    },
    {
      id: 2,
      username: "operator1",
      email: "operator1@example.com",
      full_name: "操作员1",
      phone: "13800138001",
      role: "operator",
      status: "active",
      department: "交易部",
      description: "交易操作员",
      last_login: new Date(Date.now() - 3600000).toISOString(),
      created_at: new Date(Date.now() - 86400000).toISOString(),
      updated_at: new Date(Date.now() - 86400000).toISOString()
    },
    {
      id: 3,
      username: "user001",
      email: "user001@example.com",
      full_name: "普通用户1",
      phone: "13800138002",
      role: "user",
      status: "active",
      department: "风控部",
      description: "风控专员",
      last_login: new Date(Date.now() - 7200000).toISOString(),
      created_at: new Date(Date.now() - 172800000).toISOString(),
      updated_at: new Date(Date.now() - 172800000).toISOString()
    },
    {
      id: 4,
      username: "readonly001",
      email: "readonly001@example.com",
      full_name: "只读用户1",
      phone: "13800138003",
      role: "readonly",
      status: "locked",
      department: "审计部",
      description: "审计专员",
      last_login: new Date(Date.now() - 86400000).toISOString(),
      created_at: new Date(Date.now() - 259200000).toISOString(),
      updated_at: new Date(Date.now() - 259200000).toISOString()
    }
  ];

  users.value = mockUsers;
  filteredUsers.value = mockUsers;
  pagination.value.rowsNumber = mockUsers.length;
}


function onRequest(props: any) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;
  pagination.value.page = page;
  pagination.value.rowsPerPage = rowsPerPage;
  pagination.value.sortBy = sortBy;
  pagination.value.descending = descending;
  loadUsers();
}


function resetPassword(user: User) {
  resetPasswordUser.value = user;
  newPassword.value = "";
  newUserStatus.value = user.status;
  showResetPasswordDialog.value = true;
}

function confirmResetPassword() {
  if (!newPassword.value || newPassword.value.length < 6) {
    $q.notify({
      type: "negative",
      message: "请输入至少6位的新密码"
    });
    return;
  }

  if (!resetPasswordUser.value) return;

  // 更新用户状态
  resetPasswordUser.value.status = newUserStatus.value;

  // 这里可以调用API重置密码和更新状态
  $q.notify({
    type: "positive",
    message: `用户 ${resetPasswordUser.value.username} 的密码已重置，状态已更新为${getStatusLabel(newUserStatus.value)}`
  });

  closeResetPasswordDialog();
}

function closeResetPasswordDialog() {
  showResetPasswordDialog.value = false;
  resetPasswordUser.value = null;
  newPassword.value = "";
  newUserStatus.value = "active";
}

function unlockUser(user: User) {
  user.status = "active";
  $q.notify({
    type: "positive",
    message: `用户 ${user.username} 已解锁`
  });
}

function deleteUser(user: User) {
  deletingUser.value = user;
  showDeleteDialog.value = true;
}

function saveUser() {
  // 创建用户
  const newUser: User = {
    id: Date.now(),
    username: userForm.username,
    email: "",
    full_name: userForm.full_name,
    phone: "",
    role: userForm.role,
    status: "active",
    department: "",
    description: "",
    last_login: "",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  users.value.push(newUser);
  $q.notify({
    type: "positive",
    message: "用户创建成功"
  });
  closeDialog();
}


function confirmDelete() {
  if (!deletingUser.value) return;

  const index = users.value.findIndex(u => u.id === deletingUser.value!.id);
  if (index > -1) {
    users.value.splice(index, 1);
    $q.notify({
      type: "positive",
      message: "用户删除成功"
    });
  }
  showDeleteDialog.value = false;
}

function closeDialog() {
  showAddDialog.value = false;
  userForm.username = "";
  userForm.full_name = "";
  userForm.role = "user";
  userForm.password = "";
  userForm.confirmPassword = "";
}

onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.q-card {
  border-radius: 8px;
}

/* 添加用户对话框样式 */
.add-user-dialog {
  width: 600px;
  max-width: 90vw;
  border-radius: 8px;
  overflow: hidden;
}

/* 重置密码对话框样式 */
.reset-password-dialog {
  width: 300px;
  max-width: 90vw;
  border-radius: 8px;
  overflow: hidden;
}

/* 确保密码输入框的锁图标不可点击 */
.reset-password-dialog .q-field__prepend .q-icon {
  pointer-events: none;
  cursor: default;
}

/* 确保表单内容不会撑开对话框 */
.add-user-dialog .q-card-section {
  overflow: hidden;
}

/* 限制错误提示文本长度 */
.add-user-dialog .q-field__messages {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .add-user-dialog {
    min-width: 90vw;
    max-width: 95vw;
    margin: 16px;
  }

  .reset-password-dialog {
    min-width: 90vw;
    max-width: 95vw;
    margin: 16px;
  }
}
</style>
