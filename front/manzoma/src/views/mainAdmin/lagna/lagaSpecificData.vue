<template>
  <div class="afrperson-container">
    <pageNavigation />

    <transition name="expand">
      <div class="white-box info-box" v-if="store.currentLagna">
        <div class="box-title-toggle-expand">
          <h2>{{ store.currentLagna.committe_name }}</h2>
          <div class="info-toggle" @click="infoExpanded = !infoExpanded">
            <span>
              {{ infoExpanded ? 'إخفاء التفاصيل' : 'عرض التفاصيل' }}
            </span>
            <i class="fa-solid fa-chevron-down" :class="{ rotate: infoExpanded }"></i>
          </div>
        </div>

        <div class="info-grid" v-show="infoExpanded">
          <div class="info-item">
            <span class="label">رقم اللجنة</span>
            <span class="value">{{ store.currentLagna.committe_number }}</span>
          </div>

          <div class="info-item">
            <span class="label">التصنيف</span>
            <span class="value">{{ store.currentLagna.category?.category_name }}</span>
          </div>

          <div class="info-item">
            <span class="label">الحالة</span>
            <span
              class="status-badge"
              :class="store.currentLagna.committe_is_done ? 'done' : 'active'"
            >
              {{ store.currentLagna.committe_is_done ? 'تم الانتهاء' : 'جارى' }}
            </span>
          </div>

          <div class="info-item">
            <span class="label">تاريخ البدء</span>
            <span class="value">{{ store.currentLagna.committe_start_date }}</span>
          </div>

          <div class="info-item">
            <span class="label">تاريخ الانتهاء</span>
            <span class="value">{{ store.currentLagna.committe_end_date }}</span>
          </div>
        </div>
      </div>
    </transition>

    <div class="white-box">
      <div class="table-actions">
        <button @click="addSpecificLagna" class="action-btn edit">
          اضافة نوع لجنة جديده
          <i class="fa-solid fa-plus"></i>
        </button>
      </div>
      <BaseTable
        :rows="store.specificLagnas || []"
        :columns="columns"
        :sortBy="store.specificFilters.sortBy"
        :sortDir="store.specificFilters.sortDir"
        @sort="store.setSpecificSort"
        @rowClick="goToSpecificDetails"
      >
        <template #actions="{ row }">
          <div class="action-btns">
            <!-- <button @click="$emit('editLagna', lagna)" class="action-btn edit">
              فرد
              <i class="fa-solid fa-plus"></i>
            </button>
            <button @click="$emit('editLagna', lagna)" class="action-btn edit">
              عضو
              <i class="fa-solid fa-plus"></i>
            </button> -->
            <button @click="appearLagnaReportPhoto(row)" class="action-btn lagnaReport">
              تقرير صور اللجنة
              <i class="fa-solid fa-file"></i>
            </button>
            <button @click="appearLagnaReport(row)" class="action-btn lagnaReport">
              تقرير اللجنة
              <i class="fa-solid fa-file"></i>
            </button>
            <button @click="startPrepareCommitte(row)" class="action-btn prepeare">
              تجهيز اللجنة
              <i class="fa-solid fa-screwdriver-wrench"></i>
            </button>
            <button @click="updateSpecificLagna(row)" class="action-btn edit">
              تعديل
              <i class="fa-solid fa-pencil"></i>
            </button>

            <button @click="deleteLagna(row)" class="action-btn delete">
              حذف
              <i class="fa-regular fa-trash-can"></i>
            </button>
          </div>
        </template>
      </BaseTable>

      <TablePagination
        :page="store.specificPagination.page"
        :pageSize="store.specificPagination.pageSize"
        :totalPages="totalPages"
        :showRowSize="showRowSize"
        :rowSize="rowSize"
        @update:page="store.setPage"
        @update:pageSize="store.setPageSize"
      />
    </div>

    <reportPopub
      v-if="appearReport"
      :tableFields="ReportTableFields"
      :mainLagnaName="ReportMainLagnaName"
      :lagnaNameType="ReportLagnaNameType"
      :stikyHeader="true"
      @close="closeReportPopup"
    />
    <PhotoreportPopub
      v-if="appearPhotoReport"
      :tableFields="PhotoReportTableFields"
      :mainLagnaName="ReportMainLagnaName"
      :lagnaNameType="ReportLagnaNameType"
      :stikyHeader="true"
      @close="closePhotoReportPopup"
    />

    <!-- MODAL -->
    <BaseModalForm
      :open="isModalOpen"
      :confirmOpen="isDeleteConfirmOpen"
      :title="isEditMode ? 'تعديل نوع اللجنة' : 'إضافة نوع اللجنة'"
      :submitText="isEditMode ? 'حفظ' : 'إضافة'"
      v-model="currentSpecificCommitt"
      :fields="fields"
      :confirmText="`هل تريد حذف نوع اللجنة  -  ${currentSpecificCommitt.lagna_type_name} ؟`"
      @save="save"
      @close="closeModal"
      @cancelDelete="isDeleteConfirmOpen = false"
      @confirmDelete="deleteCommitt"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useLagnaStore } from '@/stores/lagna'
import { useRouter, useRoute } from 'vue-router'

import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import pageNavigation from '@/components/global/pageNavigation.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseModalForm from '@/components/global/dataTable/BaseModalForm.vue'
import reportPopub from '@/components/global/popup/reportPopub.vue'
import PhotoreportPopub from '@/components/global/popup/reportPopub.vue'
import swal from 'sweetalert'

const store = useLagnaStore()
const router = useRouter()
const route = useRoute()

const committe_code = route.params.committe_code

/* ================= STATE ================= */
const persons = ref([])

const isModalOpen = ref(false)
const isDeleteConfirmOpen = ref(false)
const isEditMode = ref(false)
const currentSpecificCommitt = ref(getEmptyCommitt())
const selectedCommitId = ref(null)
const appearReport = ref(false)
const appearPhotoReport = ref(false)
const ReportMainLagnaName = ref('')
const ReportLagnaNameType = ref('')
const infoExpanded = ref(true)

const totalPages = computed(() =>
  Math.ceil(store.specificPagination.total / store.specificPagination.pageSize),
)

const showRowSize = computed(() =>
  Math.ceil(
    store.specificPagination.page * store.specificPagination.pageSize >
      store.specificPagination.total
      ? store.specificPagination.total
      : store.specificPagination.page * store.specificPagination.pageSize,
  ),
)

const rowSize = computed(() => Math.ceil(store.specificPagination.total))

const columns = computed(() => [
  {
    key: 'lagna_type_name',
    value: (row) => row.lagna_type_name,
    key1: 'lagna_type_name',
    label: 'نوع اللجنة',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'start_date',
    value: (row) => row.start_date,
    label: 'تاريخ بدء اللجنة',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'end_date',
    value: (row) => row.end_date,
    label: 'تاريخ انتهاء اللجنة',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
])

/* ================= FORM SCHEMA ================= */

const fields = computed(() => [
  {
    name: 'committe_type',
    label: 'نوع اللجنة',
    type: 'select',
    options: store.lagnaType,
    opLabelName: 'type_name',
    opLabelValue: 'type_id',
  },
  //   { name: 'committe_name', label: 'اسم اللجنة', required: true },
  { name: 'start_date', type: 'date', label: 'تاريخ بداء اللجنة', required: true },
  { name: 'end_date', type: 'date', label: 'تاريخ انتهاء اللجنة', required: true },
])
const ReportTableFields = computed((row) => {
  return {
    tabs: [
      {
        key: 'by_person_army',
        label: 'السلاح',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_army_name',
            value: (row, index, isTotal) => (isTotal ? '' : row.person_army_name),
            key1: 'person_army_name',
            label: 'السلاح',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'by_person_prnt_army',
        label: 'التبعية',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_prnt_army_name',
            value: (row) => row.person_prnt_army_name,
            key1: 'person_prnt_army_name',
            label: 'التبعية',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'by_prnt_a_army',
        label: 'السلاح / التبعية',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 3 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_army_name',
            value: (row) => row.person_army_name,
            key1: 'person_army_name',
            label: 'السلاح',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'person_prnt_army_name',
            value: (row) => row.person_prnt_army_name,
            key1: 'person_prnt_army_name',
            label: 'التبعية',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',
            // RowsMerge: 2,
            ColsMerge: 2,

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'by_serv_army',
        label: 'الخدمة',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_serv_name',
            value: (row) => row.person_serv_name,
            key1: 'person_serv_name',
            label: 'الخدمة',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'all',
        label: 'السلاح / التبعية / الخدمة',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 4 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_army_name',
            value: (row) => row.person_army_name,
            key1: 'person_army_name',
            label: 'السلاح',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'person_prnt_army_name',
            value: (row) => row.person_prnt_army_name,
            key1: 'person_prnt_army_name',
            label: 'التبعية',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'person_serv_name',
            value: (row) => row.person_serv_name,
            key1: 'person_serv_name',
            label: 'الخدمة',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
    ],
    reportData: null,
  }
})
const PhotoReportTableFields = computed((row) => {
  return {
    tabs: [
      {
        key: 'by_person_army',
        label: 'السلاح',
        data: 'results',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'mil_no',
            // value: (row, index, isTotal) => (isTotal ? '' : row.person_army_name),
            value: (row) => row.mil_no,
            key1: 'mil_no',
            label: 'رقم عسكري',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'degree_name',
            value: (row) => row.degree_name,
            label: 'درجة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'person_name',
            value: (row) => row.person_name,
            label: 'الاسم',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'army_name',
            value: (row) => row.army_name,
            label: 'السلاح',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'prnt_army_name',
            value: (row) => row.prnt_army_name,
            label: 'التبعية',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
    ],
    reportData: null,
  }
})

function getEmptyCommitt() {
  console.log('store.currentLagna', store.currentLagna)
  return {
    start_date: store.currentLagna?.committe_start_date,
    end_date: store.currentLagna?.committe_end_date,
    committe_type: '',
  }
}

function goToSpecificDetails(row) {
  console.log('sssssssssssssssssssssssssssssssssssssss', row)
  store.fetchOneCommittSpecific(row.committe_code, row.lagna_type_id)
  router.push({
    name: 'lagnaDetails',
    params: {
      committe_code: row.committe_code,
      spacific_id: row.lagna_type_id,
      specific_name: row.lagna_type_name,
      committe_name: row.committe_name,
    },
  })
}

/* ================= ACTIONS ================= */

// ADD
function addSpecificLagna(row) {
  console.log('row =======>', row)
  isEditMode.value = false
  currentSpecificCommitt.value = getEmptyCommitt()
  isModalOpen.value = true
}
// udate
function updateSpecificLagna(row) {
  console.log('row =======>', row)
  isEditMode.value = true
  currentSpecificCommitt.value = row
  isModalOpen.value = true
}

function startPrepareCommitte(row) {
  console.log('row =======>', row)
}
async function appearLagnaReport(row) {
  ReportMainLagnaName.value = store.currentLagna.committe_name
  ReportLagnaNameType.value = row.lagna_type_name
  let reportData = await store.fetchCommittReports(row.committe_code, row.lagna_type_id)
  ReportTableFields.value.reportData = reportData.army_report
  appearReport.value = true
  console.log('row =======>', row)
}

async function appearLagnaReportPhoto(row) {
  ReportMainLagnaName.value = store.currentLagna.committe_name
  ReportLagnaNameType.value = row.lagna_type_name
  let reportData = await store.fetchCommittPhotoReport(row.committe_code, row.lagna_type_id)
  PhotoReportTableFields.value.reportData = reportData
  appearPhotoReport.value = true
  console.log('row =======>', row)
  console.log('reportData =======>', reportData)
  console.log('phot reptot tabasdf =======>', PhotoReportTableFields.value.reportData)
}

// DELETE FLOW
function deleteLagna(row) {
  console.log(row)
  currentSpecificCommitt.value = row
  isDeleteConfirmOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  currentSpecificCommitt.value = getEmptyCommitt()
}
function closeReportPopup() {
  appearReport.value = false
}
function closePhotoReportPopup() {
  appearPhotoReport.value = false
}

// SAVE (ADD or EDIT)
function save() {
  if (isEditMode.value) {
    updateCommitt()
  } else {
    addCommitt()
  }
  closeModal()
}

// ADD LOGIC
async function addCommitt() {
  console.log('currentSpecificCommitt', currentSpecificCommitt.value)
  try {
    await store.addNewCommittSpecifics(committe_code, { ...currentSpecificCommitt.value })
    await store.fetchCommittSpecifics(committe_code)
    swal({
      title: 'تم اضافة اللجنة بنجاح',
      text: 'تم اضافة اللجنة بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء الاضافة' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

// UPDATE LOGIC
async function updateCommitt() {
  try {
    await store.updateCommittSpecifics(committe_code, currentSpecificCommitt.value.lagna_type_id, {
      ...currentSpecificCommitt.value,
    })
    await store.fetchCommittSpecifics(committe_code)
    swal({
      title: 'تم تعديل اللجنة بنجاح',
      text: 'تم تعديل اللجنة بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء التعديل' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

async function deleteCommitt() {
  try {
    await store.deleteCommittSpecifics(committe_code, currentSpecificCommitt.value.lagna_type_id)
    isDeleteConfirmOpen.value = false
    await store.fetchCommittSpecifics(committe_code)
    swal({
      title: 'تم حذف اللجنة بنجاح',
      text: 'تم حذف اللجنة بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء الحذف' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

onMounted(async () => {
  await store.fetchCommittSpecifics(committe_code)
  await store.getCommittByCode(committe_code)
  await store.fetchcommittCategory()
  await store.fetchcommittTypes()
  console.log('lagnaCategory', store.specificLagnas)
  console.log('store.currentLagna', store.currentLagna)
})
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
.table-actions {
  padding-bottom: 30px;
  display: flex;
  align-items: end;
  justify-content: end;
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
.action-btn.edit {
  background: var(--success-color);
}
.action-btn.prepeare {
  background: #ffc107;
}
.action-btn.lagnaReport {
  background: #07c5ff;
}
.action-btn.delete {
  background: var(--danger-color);
}

.info-box {
  margin-bottom: 15px;
  padding: 20px 25px;
  border-radius: 14px;
  background: linear-gradient(180deg, #ffffff, #f9f9f9);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
}

/* ===== Header ===== */
.info-box h2 {
  display: inline-block;
  margin-bottom: 20px;
  padding: 8px 18px;
  font-size: 20px;
  font-weight: bold;
  background: var(--primary-color);
  color: white;
  border-radius: 30px;
}

/* ===== Info Grid ===== */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 15px;
}

/* ===== Info Item ===== */
.info-item {
  background: white;
  padding: 5px 10px;
  border-radius: 12px;
  border: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: 0.2s ease;
}

.info-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.info-item .label {
  font-size: 13px;
  color: #888;
}

.info-item .value {
  font-size: 16px;
  font-weight: 600;
  color: #222;
}

/* ===== Status Badge ===== */
.status-badge {
  width: fit-content;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
}

.status-badge.done {
  background: rgba(40, 167, 69, 0.15);
  color: #28a745;
}

.status-badge.active {
  background: rgba(255, 193, 7, 0.2);
  color: #d39e00;
}

/* ===== Tabs Area ===== */
.lagna-actions {
  margin-top: 25px;
  display: flex;
  justify-content: center;
}

.tabs {
  display: flex;
  gap: 12px;
  background: #f1f1f1;
  padding: 6px;
  border-radius: 30px;
}

.tabs button {
  padding: 10px 26px;
  border-radius: 25px;
  background: transparent;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s ease;
}

.tabs button:hover {
  background: rgba(0, 0, 0, 0.05);
}

.tabs button.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
}

/* ----------------------------------------------------------------------------------------------- */
.lagna-counters {
  display: flex;
  gap: 15px;
  margin: 15px 0 20px;
  flex-wrap: wrap;
}

.counter-card {
  flex: 1;
  min-width: 200px;
  background: white;
  border-radius: 14px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid #eee;
  transition: 0.2s ease;
}

.counter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

/* Icon */
.counter-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.counter-icon.members {
  background: rgba(0, 123, 255, 0.15);
  color: #007bff;
}

.counter-icon.persons {
  background: rgba(40, 167, 69, 0.15);
  color: #28a745;
}

.box-title-toggle-expand {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
/* Text */
.counter-info {
  display: flex;
  flex-direction: column;
}

.counter-value {
  font-size: 22px;
  font-weight: bold;
  color: #222;
}

.counter-label {
  font-size: 13px;
  color: #777;
}

.info-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  color: var(--primary-color);
  font-weight: 500;
  margin-bottom: 10px;
}

.info-toggle i {
  transition: transform 0.3s ease;
}

.info-toggle i.rotate {
  transform: rotate(180deg);
}

/* ===== Expand Animation ===== */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.35s ease;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
