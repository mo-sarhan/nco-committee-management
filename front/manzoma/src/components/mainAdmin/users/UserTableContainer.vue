<template>
  <div>
    <UserControls
      v-model:search="search"
      v-model:statusFilter="statusFilter"
      v-model:emailFilter="emailFilter"
      v-model:phoneFilter="phoneFilter"
      :uniqueStatus="uniqueStatus"
      :uniqueEmails="uniqueEmails"
      :uniquePhones="uniquePhones"
      @export="handleExport"
    />

    <UserTable
      :users="paginatedUsers"
      :sortBy="sortBy"
      :sortDir="sortDir"
      @sort="sort"
      @icon="icon"
      @editUser="$emit('editUser', $event)"
      @deleteUser="$emit('deleteUser', $event)"
    />

    <TablePagination
      v-if="sortedUsers.length > 0"
      :page="page"
      :pageSize="pageSize"
      :totalPages="totalPages"
      @update:page="page = $event"
      @update:pageSize="pageSize = $event"
    />
  </div>
</template>
<script setup>
import { ref, computed, watch } from 'vue'
import * as XLSX from 'xlsx'
import UserControls from './UserControls.vue'
import UserTable from './UserTable.vue'
import TablePagination from '../../global/dataTable/TablePagination.vue'

// --- Props and Emits ---
const props = defineProps({
  filteredUsers: { type: Array, required: true },
})
defineEmits(['editUser', 'deleteUser'])

// --- Search and Filter State ---
const search = ref('')
const statusFilter = ref('')
const emailFilter = ref('')
const phoneFilter = ref('')

// --- Computed Filter Options ---
const uniqueEmails = computed(() => [...new Set(props.filteredUsers.map((u) => u.email))])
const uniquePhones = computed(() => [...new Set(props.filteredUsers.map((u) => u.phone))])
const uniqueStatus = computed(() => [...new Set(props.filteredUsers.map((u) => u.status))])

// --- Filtered List (based on search/filters) ---
const filteredList = computed(() => {
  return props.filteredUsers.filter((u) => {
    return (
      u.name.toLowerCase().includes(search.value.toLowerCase()) &&
      (statusFilter.value ? u.status === statusFilter.value : true) &&
      (emailFilter.value ? u.email === emailFilter.value : true) &&
      (phoneFilter.value ? u.phone === phoneFilter.value : true)
    )
  })
})

// --- Sorting Logic ---
const sortBy = ref('name')
const sortDir = ref('asc')

function sort(column) {
  if (sortBy.value === column) sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  else {
    sortBy.value = column
    sortDir.value = 'asc'
  }
}

const sortedUsers = computed(() => {
  return [...filteredList.value].sort((a, b) => {
    let A = a[sortBy.value]?.toString().toLowerCase()
    let B = b[sortBy.value]?.toString().toLowerCase()
    if (A < B) return sortDir.value === 'asc' ? -1 : 1
    if (A > B) return sortDir.value === 'asc' ? 1 : -1
    return 0
  })
})

function icon(column) {
  if (sortBy.value !== column) return '↕'
  return sortDir.value === 'asc' ? '↑' : '↓'
}

// --- Pagination Logic ---
const page = ref(1)
const pageSize = ref(5)

const totalPages = computed(() => Math.ceil(sortedUsers.value.length / pageSize.value))

const paginatedUsers = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return sortedUsers.value.slice(start, start + pageSize.value)
})

watch([pageSize, sortedUsers], () => (page.value = 1))

// --- Export Logic ---
const handleExport = (exportChoice) => {
  if (exportChoice === 'excel') exportExcel()
  // Add more export types here if needed (e.g., if (exportChoice === 'csv') exportCSV())
}

const exportExcel = () => {
  const ws = XLSX.utils.json_to_sheet(
    sortedUsers.value.map((u) => ({
      الاسم: u.name,
      'البريد الإلكتروني': u.email,
      الهاتف: u.phone,
      الحالة: u.status,
    })),
  )
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Users')
  XLSX.writeFile(wb, 'users.xlsx')
}
</script>