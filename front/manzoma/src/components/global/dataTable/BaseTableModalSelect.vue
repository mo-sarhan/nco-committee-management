<template>
  <!-- Add / Edit Modal -->
  <div v-if="open" class="modal-overlay">
    <div class="modal-content">
      <h2>{{ title }}</h2>
      <div class="header-box model-header-box">
        <GlopalSearch
          :fields="tableModelSearch"
          v-model="filters"
          :exportBtns="exportBtns"
          @search="tableSearch"
          @export="doExport"
        />
      </div>

      <div v-for="field in fields" :key="field.name" class="form-group">
        <div class="white-box">
          <BaseTable
            :rows="field.rows"
            :columns="field.columns"
            :selectable="field.selectable"
            :multiSelect="field.multiSelect"
            v-model:selectedRows="modelValue[field.name]"
          >
            <!-- <template #actions="{ row }">
                <div class="action-btns">
            
                  <button @click="$emi('update',row)" class="action-btn edit">
                    تعديل
                    <i class="fa-solid fa-pencil"></i>
                  </button>

                  <button @click="$emi('',row)" class="action-btn delete">
                    حذف 
                    <i class="fa-regular fa-trash-can"></i>
                  </button>
                </div>
              </template> -->
          </BaseTable>

          <TablePagination
            :page="field.pagination.page"
            :pageSize="field.pagination.pageSize"
            :totalPages="field.pagination.totalPages"
            :showRowSize="field.pagination.showRowSize"
            :rowSize="field.pagination.rowSize"
            @update:page="field.pagination.setPage"
            @update:pageSize="field.pagination.setPageSize"
          />
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-primary" type="submit" @click="save">
          {{ submitText }}
        </button>

        <button class="btn cancel-btn" type="button" @click="$emit('close')">إلغاء</button>
      </div>
    </div>
  </div>

  <!-- Delete Confirmation -->
  <div v-if="confirmOpen" class="modal-overlay">
    <div class="modal-content confirm-box">
      <h2>تأكيد الحذف</h2>

      <p>{{ confirmText }}</p>

      <div class="modal-actions">
        <button class="btn btn-danger" @click="$emit('confirmDelete')">حذف</button>
        <button class="btn cancel-btn" @click="$emit('cancelDelete')">إلغاء</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import GlopalSearch from '@/components/fields/glopalSearch.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import TablePagination from '@/components/global/dataTable/TablePagination.vue'
const props = defineProps({
  open: Boolean,
  confirmOpen: Boolean,

  title: String,
  submitText: {
    type: String,
    default: 'حفظ',
  },

  modelValue: {
    type: Object,
    required: true,
  },

  fields: {
    type: Array,
    required: true,
  },

  tableModelSearch: {
    type: Object,
    required: true,
  },
  // filters: {
  //   type: Object,
  //   required: true,
  // },
  exportBtns: {
    type: Array,
    required: false,
  },

  confirmText: {
    type: String,
    default: 'هل أنت متأكد من الحذف؟',
  },
})

const filters = ref({})
const emit = defineEmits([
  'close',
  'save',
  'tableSearch',
  'update:modelValue',
  'confirmDelete',
  'cancelDelete',
])

function save() {
  emit('save', props.modelValue)
}

function tableSearch(filters) {
  console.log('filters.value', filters)
  emit('tableSearch', filters)
}
function doExport(type) {
  // console.log('Export:', type)
}
onMounted(() => {
  // console.log("fields",props.fields)
})
</script>
<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 90%;
  /* max-width: 500px; */
  text-align: right;
  overflow-y: overlay;
  height: 800px;
  border-radius: 20px;
}

.modal-content h2 {
  margin: 0 0 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  color: var(--dark-blue);
}

.form-group {
  margin-bottom: 15px;
}
.model-header-box {
  margin: 0px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

input,
select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  align-items: center;
  justify-content: center;
}

.cancel-btn {
  background: #f1f1f1;
  color: var(--danger-color);
}

.confirm-box {
  max-width: 400px;
}
</style>
