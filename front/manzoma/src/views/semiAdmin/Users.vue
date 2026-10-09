div
<template>
  <div class="dashboard-container">
    <div class="header">
      <h1>المستخدمون</h1>

      <button class="btn btn-primary" @click="openModal('add')">
        <i class="fas fa-plus"></i> مستخدم جديد
      </button>
    </div>

    <UserTableContainer
      :filtered-users="filteredUsers"
      @edit-user="(user) => openModal('edit', user)"
      @delete-user="deleteUser"
    />

    <UserModal
      :is-modal-open="isModalOpen"
      :is-edit-mode="isEditMode"
      :current-user="currentUser"
      :is-delete-confirm-open="isDeleteConfirmOpen"
      :user-to-delete-name="userToDeleteName"
      @update:current-user="(val) => (currentUser = val)"
      @close="isModalOpen = false"
      @save="saveUser"
      @confirm-delete="confirmDelete"
      @cancel-delete="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
// import UserTable from '@/components/mainAdmin/UserTable2.vue'
import UserModal from '@/components/mainAdmin/users/UserModal.vue'
import UserTableContainer from '@/components/mainAdmin/users/UserTableContainer.vue'
import swal from 'sweetalert';

const users = ref([
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  { id: 1, name: 'أحمد سعيد', email: 'ahmad@example.com', phone: '0501234567', status: 'نشط' },
  {
    id: 2,
    name: 'فاطمة محمد',
    email: 'fatima@example.com',
    phone: '0559876543',
    status: 'غير نشط',
  },
])
const nextId = ref(3)

const searchText = ref('')
const isModalOpen = ref(false)
const isEditMode = ref(false)
let currentUser = ref({ id: null, name: '', email: '', phone: '', status: 'نشط' })

const isDeleteConfirmOpen = ref(false)
const userToDeleteId = ref(null)
const userToDeleteName = ref('')

const filteredUsers = computed(() => {
  const s = searchText.value.toLowerCase()
  if (!s) return users.value

  return users.value.filter(
    (u) =>
      u.name.toLowerCase().includes(s) || u.email.toLowerCase().includes(s) || u.phone.includes(s),
  )
})

function openModal(mode, user = null) {
  isEditMode.value = mode === 'edit'

  currentUser.value = isEditMode.value
    ? { ...user }
    : { id: null, name: '', email: '', phone: '', status: 'نشط' }

  isModalOpen.value = true
}

function saveUser() {
  if (isEditMode.value) {
    const idx = users.value.findIndex((u) => u.id === currentUser.value.id)
    users.value[idx] = { ...currentUser.value }
  } else {
    users.value.push({ ...currentUser.value, id: nextId.value++ })
  }
  isModalOpen.value = false
}

function deleteUser(id) {
  const u = users.value.find((u) => u.id === id)
  userToDeleteId.value = id
  userToDeleteName.value = u.name
  isDeleteConfirmOpen.value = true
}

function confirmDelete() {
  users.value = users.value.filter((u) => u.id !== userToDeleteId.value)
  isDeleteConfirmOpen.value = false
}

function cancelDelete() {
  isDeleteConfirmOpen.value = false
}
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  max-width: 1200px;
  margin: auto;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
  border-bottom: 2px solid #eee;
  padding-bottom: 15px;
}

.header h1 {
  margin: 0;
  color: var(--dark-blue);
}

.controls {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.search-input {
  flex-grow: 1;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>
