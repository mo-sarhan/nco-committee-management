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
        :rows="commitiReportData"
        :columns="columns"
        :totalRows="true"
        :sortBy="filters.sortBy"
        :sortDir="filters.sortDir"
        @sort="setSort"
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
import lagnaService from '@/services/lagnaService'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import { useLoadingStore } from '@/stores/loadingStore'
import { useGlopalStore } from '@/stores/glopal'

const glopalStore = useGlopalStore()
const loadingStore = useLoadingStore()
const router = useRouter()
const filters = ref({})
let commitiReportData = ref([])
const armyName = ref('all')

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
    colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
    value: (row, index, isTotal) => (isTotal ? 'الإجمالي' : index + 1),
  },
  {
    key: 'committe_name',
    label: 'اسم اللجنه',
    hRowspan: 3,
    value: (row) => row.committe_name,
  },
  {
    key: 'prnt_army_name',
    label: 'التبعية',
    hRowspan: 3,
    value: (row) => toAr(row.prnt_army_name),
  },
  {
    key: 'type_name',
    label: 'نوع اللجنة',
    hRowspan: 3,
    value: (row) => toAr(row.type_name),
  },
  {
    key: 'person_prnt_army_name',
    label: 'تبعية الافراد',
    hRowspan: 3,
    value: (row) => toAr(row.person_prnt_army_name),
  },
  {
    key: 'army_name',
    label: 'سلاح افراد اللجنة',
    hRowspan: 3,
    value: (row) => toAr(row.army_name),
  },
  {
    key: 'serv_name',
    label: 'سلاح خدمة افراد اللجنة',
    hRowspan: 3,
    value: (row) => toAr(row.serv_name),
  },
  {
    key: 'total',
    label: 'الاجمالى ',
    hRowspan: 3,
    value: (row) => toAr(row.total),
    style: { background: '#ffff72;', fontSize: '17px;' },
  },
  {
    key: 'st_10',
    label: 'مسجل ',
    hRowspan: 3,
    value: (row) => toAr(row.st_10),
  },
  {
    key: 'st_20',
    label: 'مراجعة ',
    hRowspan: 3,
    value: (row) => toAr(row.st_20),
  },
  {
    key: 'st_30',
    label: 'تصديق ',
    hRowspan: 3,
    value: (row) => toAr(row.st_30),
  },
  {
    key: 'st_40',
    label: 'منتظر ',
    hRowspan: 3,
    value: (row) => toAr(row.st_40),
  },
  {
    key: 'st_50',
    label: 'حضور ',
    hRowspan: 3,
    value: (row) => toAr(row.st_50),
  },
  {
    key: 'st_60',
    label: 'عدم حضور ',
    hRowspan: 3,
    value: (row) => toAr(row.st_60),
  },
  {
    key: 'st_70',
    label: 'مثول امام اللجنه',
    hRowspan: 3,
    value: (row) => toAr(row.st_70),
  },
  {
    key: 'st_99',
    label: 'لم يصدق',
    hRowspan: 3,
    value: (row) => toAr(row.st_99),
  },
])

const toAr = (num) => convertToArabicNumbers(num)

function setSort(column) {
  if (filters.sortBy === column) {
    filters.sortDir = filters.sortDir === 'asc' ? 'desc' : 'asc'
  } else {
    filters.sortBy = column
    filters.sortDir = 'asc'
  }
  commitiReportData = lagnaService.fetchCommitiReportData(filters.value)
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

async function getComitiReportData() {
  try {
    const res = await lagnaService.fetchCommitiReportData()
    commitiReportData.value = res.results
  } catch (error) {
    throw error
  }
}

onMounted(() => {
  getComitiReportData()
  console.log('commitiReportData.value', commitiReportData.value)
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
