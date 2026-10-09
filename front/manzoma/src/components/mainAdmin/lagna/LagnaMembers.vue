<template>
  <div class="afrperson-container">
    <!-- <pageNavigation /> -->

    <!-- <div class="header-box">
      <GlopalSearch :fields="lagnaSearch" v-model="filters" :exportBtns="exportBtns" @search="store.setFilters" @export="doExport"  />
    </div> -->

    <div class="white-box">
      <div class="table-actions">
        <button @click="addLagnaMember" class="action-btn edit">
          اضافة عضو جديده
          <i class="fa-solid fa-plus"></i>
        </button>
      </div>

      <BaseTable
        :rows="store.lagnaMembers || []"
        :columns="columns"
        :sortBy="store.filters.sortBy"
        :sortDir="store.filters.sortDir"
        @sort="store.setSort"
      >
        <!-- @rowClick="goToDetails" -->
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
            <!-- <button @click="updateLagnaMember(row)" class="action-btn edit">
              تعديل
              <i class="fa-solid fa-pencil"></i>
            </button> -->

            <button @click="deleteLagnaMember(row)" class="action-btn delete">
              حذف
              <i class="fa-regular fa-trash-can"></i>
            </button>
          </div>
        </template>
      </BaseTable>

      <TablePagination
        :page="store.lagnaMembersPagination.page"
        :pageSize="store.lagnaMembersPagination.pageSize"
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
      :title="isEditMode ? 'تعديل عضو' : 'إضافة عضو'"
      :submitText="isEditMode ? 'حفظ' : 'إضافة'"
      v-model="currentCommittMember"
      :fields="fields"
      :confirmText="`هل تريد حذف عضو -  ${currentCommittMember?.user_info?.username} ؟`"
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
import { h } from 'vue'

import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import BaseModalForm from '@/components/global/dataTable/BaseModalForm.vue'
import swal from 'sweetalert'

const store = useLagnaStore()
const router = useRouter()

const props = defineProps({
  committeCode: { type: Number, default: 0 },
  spacificId: { type: Number, default: 0 },
})

/* ================= STATE ================= */
const isModalOpen = ref(false)
const isDeleteConfirmOpen = ref(false)
const isEditMode = ref(false)
const currentCommittMember = ref(getEmptyCommittMember())

const filters = ref({})

const totalPages = computed(() =>
  Math.ceil(store.lagnaMembersPagination.total / store.lagnaMembersPagination.pageSize),
)

const showRowSize = computed(() =>
  Math.ceil(
    store.lagnaMembersPagination.page * store.lagnaMembersPagination.pageSize >
      store.lagnaMembersPagination.total
      ? store.lagnaMembersPagination.total
      : store.lagnaMembersPagination.page * store.lagnaMembersPagination.pageSize,
  ),
)

const rowSize = computed(() => Math.ceil(store.lagnaMembersPagination.total))

const columns = computed(() => [
  {
    key: 'member_user',
    value: (row) => row.user_info.username,
    label: 'اسم العضو',
    sortable: true,
    rowClickable: true,
  },
  {
    key: 'member_type',
    value: (row) => row.type_info.member_type_name,
    label: 'نوع العضو',
    sortable: true,
    rowClickable: true,
  },
  //   { key: 'delete_flag',value : row => row.delete_flag, label: '', sortable: true ,rowClickable:true},
  // { key: 'active_flag',
  //   render: (row) =>
  //     h('i', {
  //       class: row.active_flag > true ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark',
  //       style: {
  //         color: row.active_flag > true ? '#16a34a' : '#d41314',
  //         fontSize: '18px',
  //         cursor: 'pointer',
  //       },
  //   }), label: 'الحالة', sortable: true ,rowClickable:true},
  {
    key: 'create_date	',
    value: (row) => row.create_date,
    label: 'تاريخ اضافة العضو',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
  {
    key: 'create_user',
    value: (row) => `انشاء بواسطة ${row.created_user.username}`,
    label: 'المنشاء',
    sortable: true,
    rowClickable: true,
    copyable: true,
  },
])

/* ================= FORM SCHEMA ================= */

const fields = computed(() => [
  {
    name: 'member_user',
    label: 'اسم العضو',
    type: 'select',
    options: store.lagnaMemberUsers,
    opLabelName: 'username',
    opLabelValue: 'id',
  },
  {
    name: 'member_type',
    label: 'نوع العضو',
    type: 'select',
    options: store.lagnaMemberUsersTypes,
    opLabelName: 'member_type_name',
    opLabelValue: 'vote_type',
  },
])

function getEmptyCommittMember() {
  return {
    committe_code: '',
    member_user: '',
    member_type: '',
    create_user: '',
  }
}

/* ================= ACTIONS ================= */

// ADD
function addLagnaMember(row) {
  // console.log("row =======>",row)
  isEditMode.value = false
  currentCommittMember.value = getEmptyCommittMember()
  currentCommittMember.value.committe_code = store.currentLagna.committe_code
  currentCommittMember.value.create_user = store.currentLagna.committe_create_user
  isModalOpen.value = true
}
// udate
// function updateLagnaMember(row) {
//   // console.log("row =======>",row)
//   isEditMode.value = true
//   currentCommittMember.value = row
//   isModalOpen.value = true
// }

// DELETE FLOW
function deleteLagnaMember(row) {
  currentCommittMember.value = row
  console.log('cccccccccccccc', currentCommittMember.value.member_id)
  isDeleteConfirmOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  currentCommittMember.value = getEmptyCommittMember()
}

// SAVE (ADD or EDIT)
function save() {
  if (isEditMode.value) {
    // updateCommittMember()
  } else {
    addNewCommittMember()
  }
  closeModal()
}

// ADD LOGIC
async function addNewCommittMember() {
  // console.log("currentCommittMember",currentCommittMember.value)
  try {
    await store.addNewSpecificCommittMember(props.committeCode, props.spacificId, {
      ...currentCommittMember.value,
    })
    await store.fetchSpecificCommittMembers(props.committeCode, props.spacificId)
    swal({
      title: 'تم اضافة العضو بنجاح',
      text: 'تم اضافة العضو بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء الاضافة - ' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

// UPDATE LOGIC
// async function updateCommittMember() {
//   try {
//     await store.updateSpecificCommittMember(props.committeCode,props.spacificId,{...currentCommittMember.value})
//     await store.fetchSpecificCommittMembers(props.committeCode,props.spacificId);
//       swal({
//         title: 'تم تعديل اللجنة بنجاح',
//         text: 'تم تعديل اللجنة بنجاح',
//         icon: 'success',
//         button: false,
//         timer: 1000,
//       })
//   } catch (error) {
//     swal({
//       title: 'حدثت مشكلة',
//       text: 'حدثت مشكلة اثناء التعديل'+error,
//       icon: 'error',
//       confirmButtonText: 'حاول مره اخرى ',
//     })
//   }
// }

async function deleteCommitt() {
  try {
    console.log(currentCommittMember.value.member_id)
    await store.deleteSpecificCommittMember(
      props.committeCode,
      props.spacificId,
      currentCommittMember.value.member_id,
    )
    isDeleteConfirmOpen.value = false
    await store.fetchSpecificCommittMembers(props.committeCode, props.spacificId)
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
  await store.fetchSpecificCommittMembers(props.committeCode, props.spacificId)
  await store.fetchcommittCategory()
  await store.fetchcommittTypes()
  await store.fetchCommittMembersUsers()
  await store.fetchCommittMembersTypes()
  console.log('lagnaMembers ============//// ', store.lagnaMembers)
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
