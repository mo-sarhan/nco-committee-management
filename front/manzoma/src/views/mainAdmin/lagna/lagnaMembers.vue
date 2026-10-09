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

    <AfrPersonModal
      :open="isModalOpen"
      :isEdit="isEditMode"
      :modelValue="selectedPerson"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePersonsStore } from '@/stores/persons'
import { useRouter } from 'vue-router'

import TablePagination from '@/components/global/dataTable/TablePagination.vue'
import AfrPersonModal from '@/components/mainAdmin/AfrPersons/AfrPersonModal.vue'
import pageNavigation from '@/components/global/pageNavigation.vue'
import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'

const store = usePersonsStore()
const router = useRouter()

const filters = ref({})
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
])

const columns = computed(() => [
  { key: 'mil_no', label: 'الرقم العسكري', sortable: true, rowClickable: true, copyable: true },
  { key: 'person_name', label: 'الاسم', sortable: true, rowClickable: true, copyable: true },
  { key: 'degree_name', label: 'الدرجة', sortable: true, rowClickable: true, copyable: true },
  { key: 'unit_name', label: 'الوحدة', sortable: true, rowClickable: true, copyable: true },
  { key: 'army_name', label: 'السلاح', sortable: true, rowClickable: true, copyable: true },
])

const exportBtns = computed(() => [
  {
    label: 'Excel',
    type: 'excel',
    icon: 'fa-regular fa-file-excel',
    color: 'rgb(108, 218, 108)',
  },
])

function doExport(type) {
  console.log('Export:', type)
}

onMounted(() => {
  store.fetchPersons()
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
