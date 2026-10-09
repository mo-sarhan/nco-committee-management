<template>
  <div class="report-page">
    <pageNavigation />

    <!-- <div class="header-box">
      <GlopalSearch
        :fields="unitUploadSearch"
        v-model="filters"
        :exportBtns="exportBtns"
        @search="reportStore.setFilters"
        @search-change="glopalStore.fetchArmys"
      />
    </div> -->

    <!-- Table -->
    <div class="white-box">
      <BaseTable
        :rows="filteredReportData"
        :columns="columns"
        :totalRows="true"
        :sortBy="reportStore.filters.sortBy"
        :sortDir="reportStore.filters.sortDir"
        @sort="reportStore.setSort"
      >
      </BaseTable>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { convertToArabicNumbers } from '@/utils/glopal'
import { useReportStore } from '@/stores/useReportStore'
import pageNavigation from '@/components/global/pageNavigation.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import { useLoadingStore } from '@/stores/loadingStore'
import { useGlopalStore } from '@/stores/glopal'

const glopalStore = useGlopalStore()
const reportStore = useReportStore()
const loadingStore = useLoadingStore()
const router = useRouter()
const filters = ref({})
const armyName = ref('all')

// const popupOpen = ref(false)
// const popupRows = ref([])
// const popupColumns = ref([])
// const popupTitle = ref('')

const unitUploadSearch = computed(() => [
  {
    key: 'army_name',
    label: 'التبعية',
    type: 'completeText',
    placeholder: 'اختر التبعية',
    arrayFilter: glopalStore.allArmyNames,
    optionLabel: 'army_name',
    optionValue: 'army_code',
    allOptionLabel: 'كل التبعية',
  },
])

const columns = computed(() => [
  {
    key: 'index',
    label: 'م',
    hRowspan: 3,
    colColspan: (row, index, isTotal) => (isTotal ? 1 : 1),
    value: (row, index, isTotal) => (isTotal ? '' : index + 1),
  },
  {
    key: 'army',
    label: 'التبعية',
    hRowspan: 3,
    value: (row) => row.prnt_army_name,
    hide: (row, index, isTotal) => isTotal,
    onClick: (row) => goToUnitDetails(row.prnt_army_code),
  },
  {
    key: 'total',
    label: 'إجمالي الأفراد',
    hRowspan: 3,
    value: (row) => toAr(row.total),
    onClick: (row) => goToPersonsDetails(row.prnt_army_code),
  },
  {
    label: 'صور',
    hColspan: 2,
    children: [
      {
        key: 'completed',
        label: 'مستكمل',
        value: (row) => toAr(row.completed),
        onClick: (row) => goToPersonsDetails(row.prnt_army_code, { completed_flag: 1 }),
      },
      {
        key: 'un_completed',
        label: 'غير مستكمل',
        value: (row) => toAr(row.un_completed),
        onClick: (row) => goToPersonsDetails(row.prnt_army_code, { completed_flag: 0 }),
      },
    ],
  },
  {
    key: 'un_checked',
    label: 'لم يُراجع',
    hRowspan: 3,
    value: (row) => toAr(row.un_checked),
    onClick: (row) =>
      goToPersonsDetails(row.prnt_army_code, { checked_flag: 0, completed_flag: 1 }),
  },
  {
    key: 'checked',
    label: 'تمت المراجعة',
    hRowspan: 3,
    value: (row) => toAr(row.checked),
    onClick: (row) => goToPersonsDetails(row.prnt_army_code, { checked_flag: 1 }),
  },
  {
    key: 'refused',
    label: 'مرفوض',
    hRowspan: 3,
    value: (row) => toAr(row.not_approved),
    onClick: (row) => goToPersonsDetails(row.prnt_army_code, { approved_flag: 0, checked_flag: 1 }),
  },
  {
    key: 'approved',
    label: 'مقبول',
    hRowspan: 3,
    value: (row) => toAr(row.approved),
    onClick: (row) => goToPersonsDetails(row.prnt_army_code, { approved_flag: 1 }),
  },
  {
    key: 'rest',
    label: 'متبقي',
    hRowspan: 3,
    value: (row) => toAr(row.rest),
  },
])

const filteredReportData = computed(() => {
  if (reportStore.isLoading || !reportStore.reportData.length) return []
  return reportStore.filteredReportData(armyName.value)
})

const armyOptions = computed(() => [...new Set(reportStore.reportData.map((r) => r.pern_name))])

const toAr = (num) => convertToArabicNumbers(num)

const resetForm = () => (armyName.value = 'all')

const exportBtns = computed(() => [
  {
    label: 'Excel',
    type: 'excel',
    icon: 'fa-regular fa-file-excel',
    color: 'rgb(108, 218, 108)',
  },
])

const getreportImagesEXCEL = async () => {
  try {
    const res = await axios.get('get_images_report/?excel=yes', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      responseType: 'blob',
    })

    const blob = new Blob([res.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })

    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'images_report.xlsx'
    link.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    console.error(e)
  }
}

const goToUnitDetails = (prnt_army_code) => {
  router.push({
    name: 'unitsImagesReport',
    params: { prnt_army_code: prnt_army_code },
  })
}

const goToPersonsDetails = (prnt_army_code, params) => {
  router.push({
    name: 'personsImagesReport',
    params: { prnt_army_code: prnt_army_code },
    query: params,
  })
}

onMounted(() => {
  reportStore.connectReportSocket()
  glopalStore.fetchArmys()
})
</script>

<style scoped>
.report-page {
}
.filters {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group select {
  padding: 6px 12px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  border: none;
}

.btn.reset {
  background: #e0e0e0;
}

.btn.excel {
  background: #9c0000;
  color: white;
}

.table-wrapper {
  height: calc(100vh - 260px);
  overflow: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  position: sticky;
  top: 0;
  background: #dedede;
  z-index: 1;
}

th,
td {
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #ccc;
}

tbody tr:hover {
  background: #f1f1f1;
}

tbody tr.total {
  background: #ce9d53;
  font-weight: bold;
}

.clickable {
  cursor: pointer;
  color: #0047ab;
}

.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.spinner {
  width: 70px;
  height: 70px;
  border: 6px solid #ccc;
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
