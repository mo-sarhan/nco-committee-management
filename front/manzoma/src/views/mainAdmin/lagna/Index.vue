<template>
  <div class="afrperson-container">
    <pageNavigation />

    <div class="header-box">
      <GlopalSearch :fields="lagnaSearch" v-model="filters" @search="store.setFilters" />
    </div>

    <div class="white-box">
      <div class="table-actions">
        <button @click="addLagna" class="action-btn edit">
          اضافة لجنة جديده
          <i class="fa-solid fa-plus"></i>
        </button>
      </div>
      <BaseTable
        :rows="store.lagnas || []"
        :columns="columns"
        :sortBy="store.filters.sortBy"
        :sortDir="store.filters.sortDir"
        @sort="store.setSort"
        @rowClick="goToDetails"
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
            <button @click="updateLagna(row)" class="action-btn edit">
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
        :page="store.pagination.page"
        :pageSize="store.pagination.pageSize"
        :totalPages="totalPages"
        :showRowSize="showRowSize"
        :rowSize="rowSize"
        @update:page="store.setPage"
        @update:pageSize="store.setPageSize"
      />
    </div>

    <!-- MODAL -->
    <BaseModalForm
      :open="isModalOpen"
      :confirmOpen="isDeleteConfirmOpen"
      :title="isEditMode ? 'تعديل لجنة' : 'إضافة لجنة'"
      :submitText="isEditMode ? 'حفظ' : 'إضافة'"
      v-model="currentCommitt"
      :fields="fields"
      :confirmText="`هل تريد حذف لجنة -  ${currentCommitt.committe_name} ؟`"
      @save="save"
      @close="closeModal"
      @confirmDelete="deleteCommitt"
      @cancelDelete="isDeleteConfirmOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useLagnaStore } from '@/stores/lagna'
import { useRouter } from 'vue-router'

import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import pageNavigation from '@/components/global/pageNavigation.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import BaseModalForm from '@/components/global/dataTable/BaseModalForm.vue'
import swal from 'sweetalert'

const store = useLagnaStore()
const router = useRouter()

/* ================= STATE ================= */
const persons = ref([])

const isModalOpen = ref(false)
const isDeleteConfirmOpen = ref(false)
const isEditMode = ref(false)
const currentCommitt = ref(getEmptyCommitt())
const selectedCommitId = ref(null)

const filters = ref({})

const totalPages = computed(() => Math.ceil(store.pagination.total / store.pagination.pageSize))

const showRowSize = computed(() =>
  Math.ceil(
    store.pagination.page * store.pagination.pageSize > store.pagination.total
      ? store.pagination.total
      : store.pagination.page * store.pagination.pageSize,
  ),
)

const rowSize = computed(() => Math.ceil(store.pagination.total))

const lagnaSearch = computed(() => [
  {
    key: 'committe_name',
    type: 'text',
    label: 'اسم اللجنة',
    placeholder: 'بحث اسم اللجنة',
  },
  // {
  //   key: 'type',
  //   type: 'select',
  //   label: 'نوع اللجنة',
  //   placeholder: 'كل اللجان',
  //   options: store.lagnaType,
  //   opLabelName : 'type_name',
  //   opLabelValue : 'type_id',
  // },
  // {
  //   key: 'category',
  //   type: 'select',
  //   label: 'تصنيف اللجنة',
  //   placeholder: 'كل اللجان',
  //   options: store.lagnaCategory,
  //   opLabelName : 'category_name',
  //   opLabelValue : 'category_id',
  // },
  {
    key: 'committe_is_done',
    type: 'select',
    label: 'الحالة',
    placeholder: 'كل الحالات',
    options: [
      { label: 'جارى', value: 'false' },
      { label: 'تم الانتهاء', value: 'true' },
    ],
    opLabelName: 'label',
    opLabelValue: 'value',
  },
  // {
  //   key: 'created_at',
  //   type: 'date',
  //   label: 'تاريخ الإنشاء',
  // },
  // {
  //   key: 'created_between',
  //   type: 'daterange',
  //   label: 'الفترة',
  // },
])

const columns = computed(() => [
  {
    key: 'committe_name',
    value: (row) => row.committe_name,
    label: 'اللجنة',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'prnt_army_code',
    value: (row) => row.army_name,
    label: 'التبعية',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'category',
    value: (row) => row.category?.category_name,
    key1: 'category_name',
    label: 'نوع اللجنة',
    sortable: true,
    rowClickable: true,
  },
  // { key: "type",value : row => row.type?.type_name ,key1 : "type_name", label: 'تصنيف اللجنة', sortable: true,rowClickable:true ,copyable: true},
  {
    key: 'committe_is_done',
    value: (row) => (row.committe_is_done ? 'تم الانتهاء' : 'جارى'),
    label: 'الحالة',
    sortable: true,
    rowClickable: true,
    copyable: true,
    style: {
      background: 'green',
      color: 'white',
      fontSize: 'large',
      textAlign: 'center',
      borderRadius: '10px',
      padding: '5px',
    },
  },
  {
    key: 'committe_start_date',
    value: (row) => row.committe_start_date,
    label: 'تاريخ بدء اللجنة',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'committe_end_date',
    value: (row) => row.committe_end_date,
    label: 'تاريخ انتهاء اللجنة',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
])

const exportBtns = computed(() => [
  {
    label: 'Excel',
    type: 'excel',
    icon: 'fa-regular fa-file-excel',
    color: 'rgb(108, 218, 108)',
  },
])

/* ================= FORM SCHEMA ================= */

const fields = computed(() => [
  { name: 'committe_name', label: 'اسم اللجنة', required: true },
  { name: 'committe_start_date', type: 'date', label: 'تاريخ بداء اللجنة', required: true },
  { name: 'committe_end_date', type: 'date', label: 'تاريخ انتهاء اللجنة', required: true },
  { name: 'committe_number', label: 'رقم اللجنة', required: true },
  // {
  //   name: 'committe_type',
  //   label: 'نوع اللجنة',
  //   type: 'select',
  //   options: store.lagnaType,
  //   opLabelName : 'type_name',
  //   opLabelValue : 'type_id',
  // },
  {
    name: 'main_committe_code',
    label: 'اللجنة الرئيسية',
    type: 'select',
    options: store.mainlagnas,
    opLabelName: 'committe_name',
    opLabelValue: 'committe_code',
  },
  {
    name: 'committe_category',
    label: 'تصنيف اللجنة',
    type: 'select',
    options: store.lagnaCategory,
    opLabelName: 'category_name',
    opLabelValue: 'category_id',
  },
])

function getEmptyCommitt() {
  return {
    committe_name: '',
    committe_start_date: '',
    committe_end_date: '',
    committe_number: '',
    committe_type: '',
    committe_category: '',
  }
}

function goToDetails(row) {
  console.log('sssssssssssssssssssssssssssssssssssssss', row)
  store.currentLagna = row
  console.log('7777777777777', store.currentLagna)
  router.push({
    name: 'lagaSpecificData',
    params: { committe_code: row.committe_code, committe_name: row.committe_name },
  })
}

function handlePersonsSelected({ rows, mode }) {
  rows.forEach((person) => {
    lagnaStore.addNewCommittPerson({
      mil_ser: person.mil_ser,
      committe_code: lagnaStore.currentLagna.committe_code,
      create_user: lagnaStore.currentLagna.committe_create_user,
    })
  })

  lagnaStore.fetchCommittPersons()
  isModalOpen.value = false
}

function addSelectedPersons(persons) {
  persons.forEach((p) => {
    lagnaStore.addNewCommittPerson({
      mil_ser: p.mil_ser,
      committe_code: lagnaStore.currentLagna.committe_code,
    })
  })
}
/* ================= ACTIONS ================= */

// ADD
function addLagna(row) {
  console.log('row =======>', row)
  isEditMode.value = false
  currentCommitt.value = getEmptyCommitt()
  isModalOpen.value = true
}
// udate
function updateLagna(row) {
  console.log('row =======>', row)
  isEditMode.value = true
  currentCommitt.value = row
  isModalOpen.value = true
}

function startPrepareCommitte(row) {
  console.log('row =======>', row)
}

// DELETE FLOW
function deleteLagna(row) {
  currentCommitt.value = row
  isDeleteConfirmOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  currentCommitt.value = getEmptyCommitt()
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
  console.log('currentCommitt', currentCommitt.value)
  try {
    await store.addNewCommitt({ ...currentCommitt.value })
    await store.fetchCommitts()
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
    await store.updateCommitt(currentCommitt.value.committe_code, { ...currentCommitt.value })
    await store.fetchCommitts()
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
    await store.deleteCommitt(currentCommitt.value.committe_code)
    isDeleteConfirmOpen.value = false
    await store.fetchCommitts()
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

function doExport(type) {
  console.log('Export:', type)
}

onMounted(async () => {
  await store.fetchCommitts()
  await store.fetchMainCommitts()
  await store.fetchcommittCategory()
  await store.fetchcommittTypes()
  console.log('lagnaCategory', store.lagnas)
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
</style>
