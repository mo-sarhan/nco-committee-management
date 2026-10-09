<template>
  <div class="report-page">
    <pageNavigation />

    <div class="header-box">
      <GlopalSearch
        :fields="unitUploadSearch"
        v-model="filters"
        @search="reportStore.setUnitsFilters"
      />
    </div>

    <!-- Table -->
    <div class="white-box">
      <BaseTable
        :rows="reportStore.unitsReportData"
        :columns="columns"
        :sortBy="reportStore.filters.sortBy"
        :sortDir="reportStore.filters.sortDir"
        @sort="reportStore.setSort"
      >
      </BaseTable>

      <TablePagination
        :page="reportStore.unitsReportPagination.page"
        :pageSize="reportStore.unitsReportPagination.pageSize"
        :totalPages="totalPages"
        :showRowSize="showRowSize"
        :rowSize="rowSize"
        @update:page="reportStore.setUnitsPage"
        @update:pageSize="reportStore.setUnitsPageSize"
      />
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import axios from 'axios'
import { convertToArabicNumbers } from '@/utils/glopal'
import { useReportStore } from '@/stores/useReportStore'
import pageNavigation from '@/components/global/pageNavigation.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'

import { useLoadingStore } from '@/stores/loadingStore'

const reportStore = useReportStore()
const loadingStore = useLoadingStore()
const router = useRouter()

const route = useRoute()
const prnt_army_code = route.params.prnt_army_code
const filters = ref({})
const armyName = ref('all')

const totalPages = computed(() =>
  Math.ceil(reportStore.unitsReportPagination.total / reportStore.unitsReportPagination.pageSize),
)
const showRowSize = computed(() =>
  Math.ceil(
    reportStore.unitsReportPagination.page * reportStore.unitsReportPagination.pageSize >
      reportStore.unitsReportPagination.total
      ? reportStore.unitsReportPagination.total
      : reportStore.unitsReportPagination.page * reportStore.unitsReportPagination.pageSize,
  ),
)
const rowSize = computed(() => Math.ceil(reportStore.unitsReportPagination.total))

const unitUploadSearch = computed(() => [
  // {
  //   key: 'prnt_army_name',
  //   label: 'التبعية',
  //   placeholder: 'كل التبعية',
  //   type: 'select',
  //   options: reportStore.prntArmyName,
  //   opLabelName: 'prnt_army_name',
  //   opLabelValue: 'prnt_army_name',
  // },
  { key: 'unit_name', label: 'الوحدة', placeholder: 'الوحدة' },
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
    key: 'army',
    label: 'التبعية',
    hRowspan: 3,
    value: (row) => row.prnt_army_name,
    hide: (row, index, isTotal) => isTotal,
    // onClick: row => goToUnitDetails(row.prnt_army_code),
  },
  {
    key: 'unit_name',
    label: 'الوحدة',
    hRowspan: 3,
    value: (row) => row.unit_name,
    hide: (row, index, isTotal) => isTotal,
    // onClick: row => openBaseModelTablePopup("units",row.unit_name)
  },
  {
    key: 'total',
    label: 'إجمالي الأفراد',
    hRowspan: 3,
    value: (row) => toAr(row.total),
    onClick: (row) => goToPersonsDetails(row.prnt_army_code, row.unit_code),
  },
  {
    label: 'صور',
    hColspan: 2,
    children: [
      {
        key: 'completed',
        label: 'مستكمل',
        value: (row) => toAr(row.completed),
        onClick: (row) =>
          goToPersonsDetails(row.prnt_army_code, row.unit_code, { completed_flag: 1 }),
      },
      {
        key: 'un_completed',
        label: 'غير مستكمل',
        value: (row) => toAr(row.un_completed),
        onClick: (row) =>
          goToPersonsDetails(row.prnt_army_code, row.unit_code, { completed_flag: 0 }),
      },
    ],
  },
  {
    key: 'un_checked',
    label: 'لم يُراجع',
    hRowspan: 3,
    value: (row) => toAr(row.un_checked),
    onClick: (row) =>
      goToPersonsDetails(row.prnt_army_code, row.unit_code, { checked_flag: 0, completed_flag: 1 }),
  },
  {
    key: 'checked',
    label: 'تمت المراجعة',
    hRowspan: 3,
    value: (row) => toAr(row.checked),
    onClick: (row) => goToPersonsDetails(row.prnt_army_code, row.unit_code, { checked_flag: 1 }),
  },
  {
    key: 'refused',
    label: 'مرفوض',
    hRowspan: 3,
    value: (row) => toAr(row.not_approved),
    onClick: (row) =>
      goToPersonsDetails(row.prnt_army_code, row.unit_code, { approved_flag: 0, checked_flag: 1 }),
  },
  {
    key: 'approved',
    label: 'مقبول',
    hRowspan: 3,
    value: (row) => toAr(row.approved),
    onClick: (row) => goToPersonsDetails(row.prnt_army_code, row.unit_code, { approved_flag: 1 }),
  },
  {
    key: 'rest',
    label: 'متبقي',
    hRowspan: 3,
    value: (row) => toAr(row.rest),
  },
])

const toAr = (num) => convertToArabicNumbers(num)

const goToPersonsDetails = (prnt_army_code, unit_code, params) => {
  reportStore.resetPersonsPagination()
  router.push({
    name: 'personsImagesReport',
    params: { prnt_army_code: prnt_army_code, unit_code: unit_code },
    query: params,
  })
}

onMounted(async () => {
  reportStore.prnt_army_code = prnt_army_code
  await reportStore.getPrntArmyUnitsReportDetails()
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
