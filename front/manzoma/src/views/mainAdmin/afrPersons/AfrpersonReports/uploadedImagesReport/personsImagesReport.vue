<template>
  <div class="report-page">
    <pageNavigation />

    <div class="header-box">
      <GlopalSearch
        :fields="unitUploadSearch"
        v-model="filters"
        :exportBtns="exportBtns"
        @search="reportStore.setFilters"
      />
    </div>

    <!-- Table -->
    <div class="white-box">
      <BaseTable
        :rows="reportStore.personsReportData"
        :columns="columns"
        :sortBy="reportStore.filters.sortBy"
        :sortDir="reportStore.filters.sortDir"
        @sort="reportStore.setSort"
      >
      </BaseTable>
      <TablePagination
        :page="reportStore.personsReportPagination.page"
        :pageSize="reportStore.personsReportPagination.pageSize"
        :totalPages="totalPages"
        :showRowSize="showRowSize"
        :rowSize="rowSize"
        @update:page="reportStore.setPersonsPage"
        @update:pageSize="reportStore.setPersonsPageSize"
      />
    </div>

    <ImageUploadPanel
      v-if="popups.showImagePopup"
      @close="closeImageUploadPanel"
      :photos="photos"
      :allowUploadImage="false"
      :mil_sir="id"
      :allowReviewImage="auth.hasRole('rejectors')"
    />
  </div>
</template>
<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { h } from 'vue'

import axios from 'axios'
import { convertToArabicNumbers } from '@/utils/glopal'
import pageNavigation from '@/components/global/pageNavigation.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'

import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import ImageUploadPanel from '@/components/mainAdmin/AfrPersons/ImageUploadPanel.vue'
import { useReportStore } from '@/stores/useReportStore'
import { useLoadingStore } from '@/stores/loadingStore'
import { useAuthStore } from '@/stores/authStore'

const reportStore = useReportStore()
const loadingStore = useLoadingStore()
const auth = useAuthStore()
const router = useRouter()
console.log('auth------------>', auth.hasRole('rejectors'))

const route = useRoute()
const prnt_army_code = route.params.prnt_army_code
const unit_code = route.params.unit_code
const params = route.query

console.log('route.params===============>', route.query)

reportStore.prnt_army_code = prnt_army_code
reportStore.unit_code = unit_code
reportStore.params = params

const popups = reactive({
  showImagePopup: false,
})
const filters = ref({})

const photos = ref([])
const id = ref(null)

const armyName = ref('all')
const totalPages = computed(() =>
  Math.ceil(
    reportStore.personsReportPagination.total / reportStore.personsReportPagination.pageSize,
  ),
)
const showRowSize = computed(() =>
  Math.ceil(
    reportStore.personsReportPagination.page * reportStore.personsReportPagination.pageSize >
      reportStore.personsReportPagination.total
      ? reportStore.personsReportPagination.total
      : reportStore.personsReportPagination.page * reportStore.personsReportPagination.pageSize,
  ),
)
const rowSize = computed(() => Math.ceil(reportStore.personsReportPagination.total))

const unitUploadSearch = computed(() => [
  {
    key: 'prnt_army_name',
    label: 'التبعية',
    placeholder: 'كل التبعية',
    type: 'select',
    options: reportStore.prntArmyName,
    opLabelName: 'prnt_army_name',
    opLabelValue: 'prnt_army_name',
  },
])

const columns = computed(() => [
  {
    key: 'index',
    label: 'م',
    hRowspan: 3,
    colColspan: (row, index, isTotal) => (isTotal ? 3 : 1),
    value: (row, index, isTotal) => (isTotal ? 'الإجمالي' : index + 1),
  },
  {
    key: 'mil_no',
    label: 'الرقم العسكرى',
    hRowspan: 3,
    value: (row) => row.mil_ser.mil_no,
    onClick: (row) => openPhotoTablePopup(row),
  },
  {
    key: 'person_name',
    label: 'الاسم',
    hRowspan: 3,
    value: (row) => row.mil_ser.person_name,
    onClick: (row) => openPhotoTablePopup(row),
  },
  {
    key: 'unit_name',
    label: 'الوحدة',
    hRowspan: 3,
    value: (row) => row.mil_ser.unit_name,
    onClick: (row) => openPhotoTablePopup(row),
  },
  {
    key: 'photos',
    label: 'الصور',
    hRowspan: 3,
    onClick: (row) => openPhotoTablePopup(row),
    render: (row) =>
      h('i', {
        class:
          row.mil_ser.photos.length > 0 ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark',
        style: {
          color: row.mil_ser.photos.length > 0 ? '#16a34a' : '#d41314',
          fontSize: '18px',
          cursor: 'pointer',
        },
      }),
  },

  // {
  //   label: 'صوره',
  //   hColspan: 3,
  //   hRowspan: 1,
  //   children: [
  //     {
  //       key: 'completed',
  //       label: 'نصفى',
  //       // value: row => toAr(row.completed),
  //       render: (row) => ({
  //         template: `
  //           <img
  //             :src="src"
  //             style="width:40px;height:40px;border-radius:6px;cursor:pointer"
  //             @click="open"
  //           />
  //         `,
  //         setup() {
  //           const src = `http://afrad.oma.mil:8080/${row.mil_ser.small_photo}`

  //           function open() {
  //             openphotopup(src)
  //           }

  //           return { src, open }
  //         }
  //       }),
  //       onClick: row =>
  //         reportStore.goToUnitPersonsDetails(row.pern_army, 'small_photo', 7),
  //     },
])

const toAr = (num) => convertToArabicNumbers(num)

async function closeImageUploadPanel() {
  popups.showImagePopup = false
  // await loadPerson()
}

function openPhotoTablePopup(row) {
  popups.showImagePopup = true
  photos.value = row.mil_ser.photos
  id.value = row.mil_ser.mil_ser
  console.log('openPhotoTablePopup', row)
  // await loadPerson()
}

onMounted(async () => {
  console.log('unit_code ============================>', unit_code)
  if (unit_code) {
    await reportStore.getPrntArmyUnitsPersonsReportDetails()
  } else {
    await reportStore.getPrntArmyPersonsReportDetails()
  }
})
watch(
  () => route.query,
  () => {
    reportStore.params = route.query
    reportStore.setPersonsPage(1)
  },
)
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
