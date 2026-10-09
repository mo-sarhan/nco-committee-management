<template>
  <div class="afrperson-container">
    <pageNavigation />

    <div class="header-box">
      <GlopalSearch
        :fields="afrpersonSearch"
        v-model="filters"
        :exportBtns="exportBtns"
        @search="store.setFilters"
        @export="doExport"
        @search-change="glopalStore.fetchArmys"
      />
    </div>

    <div class="white-box">
      <BaseTable
        :rows="store.persons"
        :columns="columns"
        :sortBy="store.filters.sortBy"
        :sortDir="store.filters.sortDir"
        @sort="store.setSort"
        @rowClick="goToProfile"
      >
        <template #actions="{ row }">
          <div class="action-btns">
            <button class="action-btn upload" @click="goToProfile('upload', row)">
              رفع صور <i class="fa-solid fa-upload"></i>
            </button>

            <button class="action-btn cardShow" @click="goToProfile('show', row)">
              عرض الكارت <i class="fa-solid fa-eye"></i>
            </button>
          </div>
        </template>
      </BaseTable>

      <TablePagination
        :page="store.pagination.page"
        :pageSize="store.pagination.pageSize"
        :totalPages="totalPages"
        :showRowSize="showRowSize"
        :rowSize="rowSize"
        @update:page="store.setPage"
        @update:pageSize="store.setPageSize"
      />
    </div>

    <!-- <BackToTop/> -->

    <AfrPersonModal
      :open="isModalOpen"
      :isEdit="isEditMode"
      :modelValue="selectedPerson"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import * as XLSX from 'xlsx'
import ExcelJS from 'exceljs'
import { saveAs } from 'file-saver'
import html2canvas from 'html2canvas'
// import { jsPDF } from "jspdf"
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { loadArabicFont } from '@/utils/arabicFont'

import { ref, computed, onMounted } from 'vue'
import { usePersonsStore } from '@/stores/persons'
import { useRouter } from 'vue-router'

import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import AfrPersonModal from '@/components/mainAdmin/AfrPersons/AfrPersonModal.vue'
import pageNavigation from '@/components/global/pageNavigation.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import BackToTop from '@/components/global/BackToTop.vue'
import { useGlopalStore } from '@/stores/glopal'

const glopalStore = useGlopalStore()
const store = usePersonsStore()
const router = useRouter()

const filters = computed({
  get: () => store.filters,
  set: (val) => store.setFilters(val),
})

const isModalOpen = ref(false)
const isEditMode = ref(false)
const selectedPerson = ref(null)

const totalPages = computed(() => Math.ceil(store.pagination.total / store.pagination.pageSize))
const showRowSize = computed(() =>
  Math.ceil(
    store.pagination.page * store.pagination.pageSize > store.pagination.total
      ? store.pagination.total
      : store.pagination.page * store.pagination.pageSize,
  ),
)
const rowSize = computed(() => Math.ceil(store.pagination.total))
const afrpersonSearch = computed(() => [
  { key: 'mil_no', label: 'الرقم العسكري', placeholder: 'الرقم العسكري' },
  { key: 'person_name', label: 'الاسم', placeholder: 'الاسم' },
  { key: 'unit_name', label: 'الوحدة', placeholder: 'الوحدة' },
  {
    key: 'army_code',
    label: 'السلاح',
    type: 'completeText',
    placeholder: 'اختر السلاح',
    arrayFilter: glopalStore.allArmyNames,
    optionLabel: 'army_name',
    optionValue: 'army_code',
    allOptionLabel: 'كل الاسلحة',
  },
  {
    key: 'prnt_army_code',
    label: 'التبعية',
    type: 'completeText',
    placeholder: 'اختر السلاح',
    arrayFilter: glopalStore.allArmyNames,
    optionLabel: 'army_name',
    optionValue: 'army_code',
    allOptionLabel: 'كل التبعية',
  },
  {
    key: 'person_sex_code',
    label: 'النوع',
    type: 'select',
    placeholder: 'اختر النوع',
    options: [
      { sex_name: 'ذكر', sex_code: 1 },
      { sex_name: 'انثى', sex_code: 2 },
    ],
    opLabelName: 'sex_name',
    opLabelValue: 'sex_code',
    allOptionLabel: 'كل الانواع',
  },
])

const columns = computed(() => [
  {
    key: 'mil_no',
    value: (row) => row.mil_no,
    label: 'الرقم العسكري',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'degree_name',
    value: (row) => row.degree_name,
    label: 'الدرجة',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'person_name',
    value: (row) => row.person_name,
    label: 'الاسم',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'unit_name',
    value: (row) => row.unit_name,
    label: 'الوحدة',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'army_name',
    value: (row) => row.army_name,
    label: 'السلاح',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'prnt_army_code',
    value: (row) => row.prnt_army_name,
    label: 'التبعية',
    sortable: true,
    rowClickable: true,
  },
])

const exportBtns = computed(() => [
  {
    label: 'Excel',
    type: 'excel',
    icon: 'fa-regular fa-file-excel',
    color: 'rgb(108, 218, 108)',
  },
  {
    label: 'pdf',
    type: 'pdf',
    icon: 'fa-regular fa-file-pdf',
    color: 'rgb(108, 218, 108)',
  },
])

function doExport(type) {
  if (type === 'excel') {
    exportExcelStyled()
  }

  if (type === 'pdf') {
    exportPDF()
  }
}

async function exportExcelStyled() {
  const workbook = new ExcelJS.Workbook()
  const worksheet = workbook.addWorksheet('تقرير الراتب العالي')

  // ================= HEADER TITLE =================
  worksheet.mergeCells('A1:E1')
  const titleCell = worksheet.getCell('A1')
  titleCell.value = 'تقرير بيانات الراتب العالي'
  titleCell.font = { size: 16, bold: true }
  titleCell.alignment = { horizontal: 'center' }

  // ================= DATE =================
  worksheet.mergeCells('A2:E2')
  worksheet.getCell('A2').value = `تاريخ التقرير: ${new Date().toLocaleDateString()}`

  // ================= ADD LOGO =================
  const logo = await fetch('/logo.png') // put logo inside public folder
  const logoBuffer = await logo.arrayBuffer()

  const imageId = workbook.addImage({
    buffer: logoBuffer,
    extension: 'png',
  })

  worksheet.addImage(imageId, {
    tl: { col: 4, row: 0 },
    ext: { width: 120, height: 60 },
  })

  // ================= TABLE HEADERS =================
  const headerRow = worksheet.addRow(columns.value.map((c) => c.label))

  headerRow.eachCell((cell) => {
    cell.font = { bold: true }
    cell.alignment = { horizontal: 'center' }
    cell.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'DDDDDD' },
    }
    cell.border = {
      top: { style: 'thin' },
      left: { style: 'thin' },
      bottom: { style: 'thin' },
      right: { style: 'thin' },
    }
  })

  // ================= DATA =================
  store.persons.forEach((row) => {
    const rowData = columns.value.map((col) =>
      typeof col.value === 'function' ? col.value(row) : row[col.key],
    )
    worksheet.addRow(rowData)
  })

  // Auto width
  worksheet.columns.forEach((column) => {
    column.width = 20
  })

  // ================= DOWNLOAD =================
  const buffer = await workbook.xlsx.writeBuffer()
  saveAs(new Blob([buffer]), 'afr_persons_report.xlsx')
}

function exportPDF() {
  const doc = new jsPDF({
    orientation: 'landscape',
  })

  loadArabicFont(doc)
  // Title
  doc.setFontSize(16)
  doc.text('تقرير بيانات الراتب العالي', 140, 15, { align: 'center' })

  // Date
  doc.setFontSize(10)
  doc.text(`تاريخ التقرير: ${new Date().toLocaleDateString()}`, 14, 25)

  // Prepare data
  const tableColumn = columns.value.map((c) => c.label)

  const tableRows = store.persons.map((row) =>
    columns.value.map((col) => (typeof col.value === 'function' ? col.value(row) : row[col.key])),
  )

  autoTable(doc, {
    head: [tableColumn],
    body: tableRows,
    startY: 30,
    styles: {
      fontSize: 8,
      halign: 'center',
    },
    headStyles: {
      fillColor: [41, 128, 185],
    },
  })

  doc.save('afr_persons_report.pdf')
}
onMounted(() => {
  if (!store.persons.length) {
    store.fetchPersons()
  }
  glopalStore.fetchArmys()
})

function openEdit(person) {
  selectedPerson.value = { ...person }
  isEditMode.value = true
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  selectedPerson.value = null
}

// Navigate to profile page
function goToProfile(page, person) {
  console.log(page, person)
  if (page == 'upload') {
    router.push({
      name: 'profileImageUpload',
      params: { id: person.mil_ser, person_name: person.person_name },
    })
  } else if (page == 'show') {
    router.push({
      name: 'AfrPersonProfile',
      params: { id: person.mil_ser, person_name: person.person_name },
    })
  }
}
</script>

<style scoped>
.white-box {
  width: 100%;
  max-width: 100%;
  margin: auto;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.action-btns {
  display: flex;
  gap: 5px;
  justify-content: flex-end;
}
.action-btn {
  cursor: pointer;
  color: white;
  font-size: 16px;
  padding: 10px 20px;
  border-radius: 10px;
  height: fit-content;
  width: max-content;
}
.action-btn.upload p,
.action-btn.cardShow p {
  display: flex;
  margin: 0;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.action-btn.upload {
  background: var(--primary-color);
}
.action-btn.upload:hover {
  background: var(--hover-primary-color);
}
.action-btn.cardShow {
  background: var(--success-color);
}
.action-btn.cardShow:hover {
  background: var(--success-hover-color);
}
</style>
