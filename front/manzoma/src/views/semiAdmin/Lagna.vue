div
<template>
  <div class="dashboard-container">
    <div class="header">
      <h1>اللجان</h1>

      <button class="btn btn-primary" @click="openModal('add')">
        <i class="fas fa-plus"></i> لجنه جديد
      </button>
    </div>

    <LagnaTableContainer
      :filtered-lagnas="filteredLagnas"
      @edit-lagna="(lagna) => openModal('edit', lagna)"
      @delete-lagna="deleteLagna"
    />

    <LagnaModal
      :is-modal-open="isModalOpen"
      :is-edit-mode="isEditMode"
      :current-lagna="currentLagna"
      :is-delete-confirm-open="isDeleteConfirmOpen"
      :lagna-to-delete-name="lagnaToDeleteName"
      @update:current-lagna="(val) => (currentLagna = val)"
      @close="isModalOpen = false"
      @save="saveLagna"
      @confirm-delete="confirmDelete"
      @cancel-delete="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
// import LagnaTable from '@/components/mainAdmin/LagnaTable2.vue'
import LagnaModal from '@/components/mainAdmin/lagna/LagnaModal.vue'
import LagnaTableContainer from '@/components/mainAdmin/lagna/LagnaTableContainer.vue'

const lagnas = ref([
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
let currentLagna = ref({ id: null, name: '', email: '', phone: '', status: 'نشط' })

const isDeleteConfirmOpen = ref(false)
const lagnaToDeleteId = ref(null)
const lagnaToDeleteName = ref('')

const filteredLagnas = computed(() => {
  const s = searchText.value.toLowerCase()
  if (!s) return lagnas.value

  return lagnas.value.filter(
    (u) =>
      u.name.toLowerCase().includes(s) || u.email.toLowerCase().includes(s) || u.phone.includes(s),
  )
})

function openModal(mode, lagna = null) {
  isEditMode.value = mode === 'edit'

  currentLagna.value = isEditMode.value
    ? { ...lagna }
    : { id: null, name: '', email: '', phone: '', status: 'نشط' }

  isModalOpen.value = true
}

function saveLagna() {
  if (isEditMode.value) {
    const idx = lagnas.value.findIndex((u) => u.id === currentLagna.value.id)
    lagnas.value[idx] = { ...currentLagna.value }
  } else {
    lagnas.value.push({ ...currentLagna.value, id: nextId.value++ })
  }
  isModalOpen.value = false
}

function deleteLagna(id) {
  const u = lagnas.value.find((u) => u.id === id)
  lagnaToDeleteId.value = id
  lagnaToDeleteName.value = u.name
  isDeleteConfirmOpen.value = true
}

function confirmDelete() {
  lagnas.value = lagnas.value.filter((u) => u.id !== lagnaToDeleteId.value)
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
