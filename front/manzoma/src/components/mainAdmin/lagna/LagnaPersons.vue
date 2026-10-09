<template>
  <div class="afrperson-container">
    <!-- <pageNavigation /> -->

    <div class="header-box">
      <GlopalSearch
        :fields="lagnaPersonsSearch"
        v-model="lagnaFilters"
        :exportBtns="exportBtns"
        @search="setLagnaPersonsFilters"
        @export="doExport"
        @search-change="glopalStore.fetchArmys"
      />
    </div>

    <div class="white-box">
      <div class="table-actions" v-if="addAction">
        <button @click="addLagnaPerson" class="action-btn edit">
          اضافة فرد جديد
          <i class="fa-solid fa-plus"></i>
        </button>
      </div>

      <BaseTable
        :rows="lagnaStore.lagnaPersons || []"
        :columns="columns"
        :sortBy="lagnaStore.filters.sortBy"
        :sortDir="lagnaStore.filters.sortDir"
        @sort="lagnaStore.setSort"
        @rowClick="handleRowClick"
      >
        <!-- @rowClick="goToDetails" -->
        <template #actions="{ row }" v-if="actionsColumn">
          <div class="action-btns">
            <!-- <button @click="$emit('editLagna', lagna)" class="action-btn edit">
               فرد
              <i class="fa-solid fa-plus"></i>
            </button>
            <button @click="$emit('editLagna', lagna)" class="action-btn edit">
                عضو
              <i class="fa-solid fa-plus"></i>
            </button> -->
            <!-- <button @click="updateLagnaPerson(row)" class="action-btn edit" v-if="updateAction">
              تعديل
              <i class="fa-solid fa-pencil"></i>
            </button> -->

            <button @click="deleteLagnaPerson(row)" class="action-btn delete" v-if="deleteAction">
              حذف
              <i class="fa-regular fa-trash-can"></i>
            </button>
          </div>
        </template>
      </BaseTable>

      <TablePagination
        :page="lagnaStore.lagnaPersonsPagination.page"
        :pageSize="lagnaStore.lagnaPersonsPagination.pageSize"
        :totalPages="totalPages"
        :showRowSize="showRowSize"
        :rowSize="rowSize"
        @update:page="setLagnaPersonsPage"
        @update:pageSize="setLagnaPersonsPageSize"
      />
    </div>

    <BaseTableModalSelect
      :open="isModalOpen"
      :confirmOpen="isDeleteConfirmOpen"
      :title="isEditMode ? 'تعديل فرد' : 'إضافة فرد'"
      :submitText="isEditMode ? 'حفظ' : 'إضافة'"
      v-model="currentCommittPerson"
      :fields="BaseTableModalFields"
      :tableModelSearch="afrpersonSearch"
      :confirmText="`هل تريد حذف فرد -  ${currentCommittPerson.committe_name} ؟`"
      @save="handlePersonsSelected"
      @tableSearch="handlePersonsSearch"
      @close="closeModal"
      @cancelDelete="isDeleteConfirmOpen = false"
    />

    <!-- MODAL -->
    <BaseModalForm
      :open="isReviewModalOpen"
      :title="isReviewEditMode ? 'تحديث الحالة' : 'تحديث الحالة'"
      :submitText="isReviewEditMode ? 'حفظ' : 'إضافة'"
      v-model="reviewPerson"
      :fields="reviewPersonModalFields"
      @save="handleReviewPerson"
      @close="closeReviewPersonModal"
    />

    <BaseModalForm
      :open="isRowsModalOpen"
      :confirmOpen="isRowsDeleteConfirmOpen"
      :title="isRowsEditMode ? 'تعديل فرد' : 'إضافة فرد'"
      :submitText="isRowsEditMode ? 'حفظ' : 'إضافة'"
      v-model="currentRowsCommittPerson"
      :confirmText="`هل تريد حذف فرد -  ${currentRowsCommittPerson?.person?.person_name} ؟`"
      @save="handleRowsModal"
      @close="closeRowsModal"
      @confirmDelete="deleteSpecificCommittPersons"
      @cancelDelete="isRowsDeleteConfirmOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useLagnaStore } from '@/stores/lagna'
import { useRouter } from 'vue-router'
import { h } from 'vue'

import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import BaseModalForm from '@/components/global/dataTable/BaseModalForm.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import swal from 'sweetalert'
import BaseTableModalSelect from '@/components/global/dataTable/BaseTableModalSelect.vue'
import { useGlopalStore } from '@/stores/glopal'
import lagnaService from '@/services/lagnaService'

const glopalStore = useGlopalStore()
// const store = useLagnaStore()
const router = useRouter()
const lagnaStore = useLagnaStore()
const emit = defineEmits(['handleRowClick', 'takeProfileScreen'])

const props = defineProps({
  committeCode: { type: Number, default: 0 },
  spacificId: { type: Number, default: 0 },
  rowClick: { type: Boolean, default: false },
  addAction: { type: Boolean, default: true },
  deleteAction: { type: Boolean, default: true },
  updateAction: { type: Boolean, default: true },
  actionsColumn: { type: Boolean, default: true },
  tableColumns: { type: Array, default: {} },
})

/* ================= STATE ================= */
const dateAttendanc = ref(null)
const currentPerson = ref(null)

const isRowsModalOpen = ref(false)
const isRowsDeleteConfirmOpen = ref(false)
const isRowsEditMode = ref(false)
const currentRowsCommittPerson = ref(getEmptyCommittPerson())

const isModalOpen = ref(false)
const isDeleteConfirmOpen = ref(false)
const isEditMode = ref(false)
const currentCommittPerson = ref(getEmptyCommittPerson())

const isReviewModalOpen = ref(false)
const isReviewEditMode = ref(false)
const reviewPerson = ref(getReviewPerson())

const filters = ref({})
const lagnaFilters = ref({})

const totalPages = computed(() =>
  Math.ceil(lagnaStore.lagnaPersonsPagination.total / lagnaStore.lagnaPersonsPagination.pageSize),
)

const showRowSize = computed(() =>
  Math.ceil(
    lagnaStore.lagnaPersonsPagination.page * lagnaStore.lagnaPersonsPagination.pageSize >
      lagnaStore.lagnaPersonsPagination.total
      ? lagnaStore.lagnaPersonsPagination.total
      : lagnaStore.lagnaPersonsPagination.page * lagnaStore.lagnaPersonsPagination.pageSize,
  ),
)

const rowSize = computed(() => Math.ceil(lagnaStore.lagnaPersonsPagination.total))

const BaseTableModaltotalPages = computed(() =>
  Math.ceil(
    lagnaStore.allowedPersonsPagination.total / lagnaStore.allowedPersonsPagination.pageSize,
  ),
)

const BaseTableModalshowRowSize = computed(() =>
  Math.ceil(
    lagnaStore.allowedPersonsPagination.page * lagnaStore.allowedPersonsPagination.pageSize >
      lagnaStore.allowedPersonsPagination.total
      ? lagnaStore.allowedPersonsPagination.total
      : lagnaStore.allowedPersonsPagination.page * lagnaStore.allowedPersonsPagination.pageSize,
  ),
)

const BaseTableModalrowSize = computed(() => Math.ceil(lagnaStore.allowedPersonsPagination.total))

const lagnaPersonsSearch = computed(() => [
  { key: 'mil_ser__mil_no', label: 'الرقم العسكري', placeholder: 'الرقم العسكري' },
  { key: 'mil_ser__person_name', label: 'الاسم', placeholder: 'الاسم' },
  { key: 'mil_ser__unit_name', label: 'الوحدة', placeholder: 'الوحدة' },
  {
    key: 'mil_ser__army_code',
    label: 'السلاح',
    type: 'completeText',
    placeholder: 'اختر السلاح',
    arrayFilter: glopalStore.allArmyNames,
    optionLabel: 'army_name',
    optionValue: 'army_code',
    allOptionLabel: 'كل الاسلحة',
  },
  {
    key: 'mil_ser__prnt_army_code',
    label: 'التبعية',
    type: 'completeText',
    placeholder: 'اختر السلاح',
    arrayFilter: glopalStore.allArmyNames,
    optionLabel: 'army_name',
    optionValue: 'army_code',
    allOptionLabel: 'كل التبعية',
  },
  {
    key: 'mil_ser__person_sex_code',
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
  {
    key: 'mil_ser__person_status_code',
    label: 'الحالة',
    type: 'select',
    placeholder: 'اختر الحالة',
    options: glopalStore.lagnaStatus,
    // options: [
    //   { status_name: 'تصديق دخول اللجنة', status_code: 30 },
    //   { status_name: 'تصديق عدم دخول اللجنة', status_code: 99 },
    //   { status_name: 'تسجيل يوم دخول اللجنة', status_code: 40 },
    //   { status_name: 'حضور اللجنة', status_code: 50 },
    //   { status_name: 'عدم حضور اللجنة', status_code: 60 },
    // ],
    opLabelName: 'status_name',
    opLabelValue: 'status_code',
    allOptionLabel: 'كل الحالات',
  },
  {
    key: 'person_committe_date',
    label: 'تاريخ الحضور',
    type: 'select',
    placeholder: 'اختر التاريخ',
    options: lagnaDates.value,
    allOptionLabel: 'كل الايام',
    optionsIsList: true,
  },
])
const lagnaDates = computed(() => {
  return lagnaStore?.currentSpecificLagna?.range_dates || []
})
function setLagnaPersonsFilters(filters) {
  lagnaStore.lagnaPersonsPagination.page = 1
  lagnaFilters.value = filters
  lagnaStore.fetchSpecificCommittPersons(props.committeCode, props.spacificId, filters)
}
function setLagnaPersonsPage(page) {
  console.log('page', page)
  console.log('lagnaFilters', lagnaFilters.value)
  lagnaStore.lagnaPersonsPagination.page = page
  lagnaStore.fetchSpecificCommittPersons(props.committeCode, props.spacificId, lagnaFilters.value)
}
function setLagnaPersonsPageSize(pageSize) {
  console.log('pageSize', pageSize)
  console.log('lagnaFilters', lagnaFilters.value)
  lagnaStore.lagnaPersonsPagination.pageSize = pageSize
  lagnaStore.lagnaPersonsPagination.page = 1
  lagnaStore.fetchSpecificCommittPersons(props.committeCode, props.spacificId, lagnaFilters.value)
}
const defaultColumns = [
  {
    key: 'mil_no',
    value: (row) => row.person.mil_no,
    label: 'الرقم العسكري',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'degree_name',
    value: (row) => row.person.degree_name,
    label: 'الدرجة',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'person_name',
    value: (row) => row.person.person_name,
    label: 'الاسم',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'unit_name',
    value: (row) => row.person.unit_name,
    label: 'الوحدة',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'army_name',
    value: (row) => row.person.army_name,
    label: 'السلاح',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'prnt_army_name',
    value: (row) => row.person.prnt_army_name,
    label: 'التبعية',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'committe_status_code',
    onClick: (row) => addNewReviewPerson(row),
    render: (row) =>
      h(
        'span',
        {
          // class: row.mil_ser.photos.length > 0 ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark',
          style: {
            background:
              row.committe_status_code.afr_comm_status_code === 10 ? '#e7c80a' : '#16a34a',
            fontSize: '19px',
            cursor: 'pointer',
            padding: '5px 15px',
            color: 'white',
            borderRadius: '15px',
          },
        },
        row.committe_status_code.afr_comm_status_name,
      ),
    // value : row => row.committe_status_code,
    label: 'الحالة',
    sortable: true,
    copyable: true,
  },
]

const columns = computed(() => {
  return props.tableColumns && props.tableColumns.length > 0 ? props.tableColumns : defaultColumns
})

// const filters = ref({})
/* ================= FORM SCHEMA ================= */
const afrpersonSearch = computed(() => [
  { key: 'mil_no', label: 'الرقم العسكري', placeholder: 'الرقم العسكري' },
  { key: 'person_name', label: 'الاسم', placeholder: 'الاسم' },
  { key: 'unit_name', label: 'الوحدة', placeholder: 'الوحدة' },
  {
    key: 'mil_ser__army_code',
    label: 'السلاح',
    type: 'completeText',
    placeholder: 'اختر السلاح',
    arrayFilter: glopalStore.allArmyNames,
    optionLabel: 'army_name',
    optionValue: 'army_code',
    allOptionLabel: 'كل الاسلحة',
  },
])

const BaseTableModalFields = computed(() => [
  {
    name: 'members',
    label: 'أعضاء اللجنة',
    type: 'table',

    rows: lagnaStore.allowedPersons,
    columns: [
      {
        key: 'mil_no',
        value: (row) => row.mil_no,
        label: 'الرقم العسكري',
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
        key: 'degree_name',
        value: (row) => row.degree_name,
        label: 'الدرجة',
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
    ],
    pagination: {
      page: lagnaStore.allowedPersonsPagination.page,
      pageSize: lagnaStore.allowedPersonsPagination.pageSize,
      totalPages: BaseTableModaltotalPages.value,
      showRowSize: BaseTableModalshowRowSize.value,
      rowSize: BaseTableModalrowSize.value,
      setPage: (p) =>
        lagnaStore.setAllowedPersonsPaginationPage(p, {
          lagna_specific_id: props.spacificId,
          prnt_army: true,
        }),
      setPageSize: (size) =>
        lagnaStore.setAllowedPersonsPaginationPageSize(size, {
          lagna_specific_id: props.spacificId,
          prnt_army: true,
        }),
    },

    selectable: true,
    multiSelect: true,
  },
])

const reviewPersonModalFields = computed(() => [
  {
    name: 'new_status',
    label: '',
    type: 'radio',
    options: [
      { name: 'تصديق دخول اللجنة', code: 30 },
      { name: 'تصديق عدم دخول اللجنة', code: 99 },
      { name: 'تسجيل يوم دخول اللجنة', code: 40 },
      { name: 'حضور اللجنة', code: 50 },
      { name: 'عدم حضور اللجنة', code: 60 }, // مثول امام اللجنة 70 والعكس بتعها يكون حضور 50
    ],
    opLabelName: 'name',
    opLabelValue: 'code',
  },
  { name: 'waiting_date', type: 'date', label: 'يوم دخول اللجنة' },
])

function getEmptyCommittPerson() {
  return {
    mil_ser: '',
    Person_user: '',
    Person_type: '',
    add_user: '',
  }
}

function getReviewPerson() {
  return {
    new_status: '',
  }
}
function addNewReviewPerson(row) {
  console.log('add new review person', row)
  if (row.committe_status_code.afr_comm_status_code == 10) {
    swal({
      title: 'تحذير',
      text: 'لا يمكن تحديث الحالة فى وضع التسجيل',
      icon: 'warning',

      buttons: {
        cancel: {
          text: 'إغلاق',
          value: null,
          visible: true,
          className: 'btn-cancel',
          closeModal: true,
        },
        confirm: {
          text: 'مراجعة الفرد',
          value: 'review',
          visible: true,
          className: 'btn-confirm',
          closeModal: true,
        },
      },
    }).then((value) => {
      if (value === 'review') {
        router.push({
          name: 'specificLagnaPersonProfile',
          params: { id: row.mil_ser, person_name: row.person.person_name },
          query: {
            committe_code: props.committeCode,
            spacific_id: props.spacificId,
            person_id: row.person_id,
          },
        })
      }
    })

    return
  }
  currentPerson.value = row
  isReviewModalOpen.value = true
}

/* ================= ACTIONS ================= */

// ADD
async function addLagnaPerson(row) {
  // console.log("row =======>",row)
  isEditMode.value = false
  currentCommittPerson.value = getEmptyCommittPerson()
  currentCommittPerson.value.committe_code = lagnaStore.currentLagna.committe_code
  currentCommittPerson.value.create_user = lagnaStore.currentLagna.committe_create_user
  isModalOpen.value = true
  await lagnaStore.fetchAllowedSpecificCommittPersons({
    lagna_specific_id: props.spacificId,
    prnt_army: true,
  })
}
// udate
// function updateLagnaPerson(row) {
//   // console.log("row =======>",row)
//   isEditMode.value = true
//   currentCommittPerson.value = row
//   isModalOpen.value = true
// }

// DELETE FLOW
function deleteLagnaPerson(row) {
  console.log('row', row)
  currentRowsCommittPerson.value = row
  isRowsDeleteConfirmOpen.value = true
}

function closeReviewPersonModal() {
  isReviewModalOpen.value = false
  reviewPerson.value = getReviewPerson()
}
function closeModal() {
  isModalOpen.value = false
  currentCommittPerson.value = getEmptyCommittPerson()
}
function closeRowsModal() {
  isRowsModalOpen.value = false
  currentRowsCommittPerson.value = getEmptyCommittPerson()
}

function handleRowsModal() {
  // if (isRowsEditMode.value) {
  //   deleteSpecificCommittPersons()
  // } else {
  //   deleteSpecificCommittPersons()
  // }
  closeRowsModal()
}

async function handlePersonsSelected(row) {
  try {
    // Wait for all API calls properly
    isModalOpen.value = false
    await Promise.all(
      row.members.map((person) =>
        lagnaStore.addNewSpecificCommittPerson(props.committeCode, props.spacificId, {
          mil_ser: person.mil_ser,
          committe_code: lagnaStore.currentLagna.committe_code,
          create_user: lagnaStore.currentLagna.committe_create_user,
        }),
      ),
    )

    await lagnaStore.fetchSpecificCommittPersons(props.committeCode, props.spacificId)

    swal({
      title: 'تم اضافة الافراد',
      text: 'تم التاكيد على اضافة الافرارد بنجاح',
      icon: 'success',
      button: false,
      timer: 1500,
    })
  } catch (error) {
    console.log('errrrrr', error)

    const status = error?.response?.status
    const message =
      error?.response?.data?.details ||
      error?.response?.data?.message ||
      error.message ||
      'حدث خطأ ما'

    if (status === 400) {
      swal({
        title: 'تحذير',
        text: message,
        icon: 'warning',
        //   buttons: {
        //     cancel: {
        //       text: 'إغلاق',
        //       value: null,
        //       visible: true,
        //       className: 'btn-cancel',
        //       closeModal: true,
        //     },
        //     confirm: {
        //       text: 'اضافة رأى',
        //       value: 'addStatus',
        //       visible: true,
        //       className: 'btn-confirm',
        //       closeModal: true,
        //     },
        //   },
        // }).then((value) => {
        //   if (value === 'addStatus') {
        //     addNewOpinion()
        //   }
      })
    } else {
      swal({
        title: 'حدثت مشكلة',
        text: message,
        icon: 'error',
        button: 'حاول مره اخرى',
      })
    }
  }
}

async function handlePersonsSearch(filters) {
  console.log('filters', filters)

  lagnaStore.fetchAllowedSpecificCommittPersons({
    ...filters,
    lagna_specific_id: props.spacificId,
    prnt_army: true,
  })
}
async function handleReviewPerson() {
  try {
    let res = await lagnaStore.changeLagnaSpecificsPersonStutus(
      props.committeCode,
      props.spacificId,
      currentPerson.value.person_id,
      reviewPerson.value,
    )

    isModalOpen.value = false
    let popupDesc = ''
    if (reviewPerson.value.new_status == 30) {
      popupDesc = 'تصديق دخول اللجنة'
    } else if (reviewPerson.value.new_status == 99) {
      popupDesc = '	لم يصدق على دخول اللجنة'
    } else if (reviewPerson.value.new_status == 40) {
      popupDesc = '	منتظر إنعقاد اللجنة'
    } else if (reviewPerson.value.new_status == 60) {
      popupDesc = 'عدم الحضور'
    } else if (reviewPerson.value.new_status == 50) {
      popupDesc = '	حضور اللجنة'
    }
    swal({
      title: 'تم تحديث الحالة',
      text: popupDesc,
      icon: 'success',
      button: false,
      timer: 1500,
    })
  } catch (error) {
    console.log('errrrrr', error)
    swal({
      title: 'حدثت مشكلة',
      text: error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }

  await lagnaStore.fetchSpecificCommittPersons(props.committeCode, props.spacificId)
}

async function deleteSpecificCommittPersons() {
  try {
    console.log('currentRowsCommittPerson?.person?.person_name', currentRowsCommittPerson.value)
    await lagnaStore.deleteSpecificCommittPersons(
      props.committeCode,
      props.spacificId,
      currentRowsCommittPerson.value.person_id,
    )
    isRowsDeleteConfirmOpen.value = false
    await lagnaStore.fetchSpecificCommittPersons(props.committeCode, props.spacificId)
    swal({
      title: 'تم حذف الفرد بنجاح',
      text: 'تم حذف الفرد بنجاح',
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

function handleRowClick(person) {
  console.log('person', person)
  if (props.rowClick) {
    emit('handleRowClick', person)
  } else {
    router.push({
      name: 'specificLagnaPersonProfile',
      params: { id: person.mil_ser, person_name: person.person.person_name },
      query: {
        committe_code: props.committeCode,
        spacific_id: props.spacificId,
        person_id: person.person_id,
      },
    })
  }
}

onMounted(async () => {
  await lagnaStore.fetchOneCommittSpecific(props.committeCode, props.spacificId)
  await lagnaStore.fetchSpecificCommittPersons(props.committeCode, props.spacificId)
  await lagnaStore.fetchcommittCategory()
  await lagnaStore.fetchcommittTypes()
  await glopalStore.fetchArmys()

  console.log('lagnaStore.lagnaPersons', lagnaStore?.currentSpecificLagna?.range_dates)
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
.action-btn.delete {
  background: var(--danger-color);
}
/* Confirm Button */
.btn-confirm {
  background-color: #d33 !important; /* Red */
  border: none !important;
  color: white !important;
}

/* Cancel Button */
.btn-cancel {
  background-color: #6c757d !important; /* Gray */
  border: none !important;
  color: white !important;
}

/* Optional hover effect */
.btn-confirm:hover {
  background-color: #b52a2a !important;
}

.btn-cancel:hover {
  background-color: #5a6268 !important;
}
</style>
