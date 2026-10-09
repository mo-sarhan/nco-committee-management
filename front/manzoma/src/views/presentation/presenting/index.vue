<template>
  <div class="afrperson-container">
    <pageNavigation />

    <div class="header-box">
      <GlopalSearch :fields="lagnaSearch" v-model="filters" @search="store.setFilters" />
    </div>

    <div class="white-box">
      <BaseTable
        :rows="store.lagnas || []"
        :columns="columns"
        :sortBy="store.filters.sortBy"
        :sortDir="store.filters.sortDir"
        @sort="store.setSort"
        @rowClick="goToDetails"
      >
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
import swal from 'sweetalert'

const store = useLagnaStore()
const router = useRouter()

/* ================= STATE ================= */
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

function goToDetails(row) {
  console.log('sssssssssssssssssssssssssssssssssssssss', row)
  store.currentLagna = row
  console.log('7777777777777', store.currentLagna)
  router.push({
    name: 'presenting',
    params: { committe_code: row.committe_code, committe_name: row.committe_name },
  })
}

onMounted(async () => {
  await store.fetchMemberCommitts()
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
