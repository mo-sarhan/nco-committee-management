<template>
  <div>
    <LagnaControls
      v-model:search="search"
      v-model:statusFilter="statusFilter"
      v-model:emailFilter="emailFilter"
      v-model:phoneFilter="phoneFilter"
      :uniqueStatus="uniqueStatus"
      :uniqueEmails="uniqueEmails"
      :uniquePhones="uniquePhones"
      @export="handleExport"
    />

    <LagnaTable
      :lagnas="paginatedLagnas"
      :sortBy="sortBy"
      :sortDir="sortDir"
      @sort="sort"
      @icon="icon"
      @editLagna="$emit('editLagna', $event)"
      @deleteLagna="$emit('deleteLagna', $event)"
    />

    <TablePagination
      v-if="sortedLagnas.length > 0"
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
import LagnaControls from './LagnaControls.vue'
import LagnaTable from './LagnaTable.vue'
import TablePagination from '../../global/dataTable/TablePagination.vue'

// --- Props and Emits ---
const props = defineProps({
  filteredLagnas: { type: Array, required: true },
})
defineEmits(['editLagna', 'deleteLagna'])

// --- Search and Filter State ---
const search = ref('')
const statusFilter = ref('')
const emailFilter = ref('')
const phoneFilter = ref('')

// --- Computed Filter Options ---
const uniqueEmails = computed(() => [...new Set(props.filteredLagnas.map((u) => u.email))])
const uniquePhones = computed(() => [...new Set(props.filteredLagnas.map((u) => u.phone))])
const uniqueStatus = computed(() => [...new Set(props.filteredLagnas.map((u) => u.status))])

// --- Filtered List (based on search/filters) ---
const filteredList = computed(() => {
  return props.filteredLagnas.filter((u) => {
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

const sortedLagnas = computed(() => {
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

const totalPages = computed(() => Math.ceil(sortedLagnas.value.length / pageSize.value))

const paginatedLagnas = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return sortedLagnas.value.slice(start, start + pageSize.value)
})

watch([pageSize, sortedLagnas], () => (page.value = 1))

// --- Export Logic ---
const handleExport = (exportChoice) => {
  if (exportChoice === 'excel') exportExcel()
  // Add more export types here if needed (e.g., if (exportChoice === 'csv') exportCSV())
}

const exportExcel = () => {
  const ws = XLSX.utils.json_to_sheet(
    sortedLagnas.value.map((u) => ({
      الاسم: u.name,
      'البريد الإلكتروني': u.email,
      الهاتف: u.phone,
      الحالة: u.status,
    })),
  )
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Lagnas')
  XLSX.writeFile(wb, 'lagnas.xlsx')
}
</script>