<template>
  <!-- Add / Edit Modal -->
  <div v-if="open" class="modal-overlay">
    <div class="modal-content">
      <h2>{{ title }}</h2>

      <form @submit.prevent="$emit('save')">
        <div
          v-for="field in fields"
          :key="field.name"
          class="form-group"
        >
          <label>{{ field.label }}</label>

          <!-- INPUT -->
          <input
            v-if="field.type !== 'select' && field.type !== 'select' && field.type !== 'radio' && field.type !== 'file' && field.type !== 'textarea'"
            :type="field.type || 'text'"
            :value="modelValue[field.name]"
            @input="update(field.name, $event.target.value)"
            :required="field.required"
          />

          <!-- SELECT -->
          <select
            v-else-if="field.type === 'select'" 
            :value="modelValue[field.name]"
            @change="update(field.name, $event.target.value)"
          >
            <option
              v-for="opt in field.options"
              :key="opt[field.opLabelValue]"
              :value="opt[field.opLabelValue]"
            >
              {{ opt[field.opLabelName] }}
            </option>
          </select>

          <!-- ================= TEXTAREA ================= -->
          <textarea
            v-else-if="field.type === 'textarea'"
            :rows="field.rows || 4"
            :value="modelValue[field.name]"
            @input="update(field.name, $event.target.value)"
            :required="field.required"
          />

          <!-- ================= RADIO ================= -->
          <div v-else-if="field.type === 'radio'" class="radio-group">
            <label
              v-for="opt in field.options"
              :key="opt[field.opLabelValue]"
              class="radio-item"
            >
              <input
                type="radio"
                :name="field.name"
                :value="opt[field.opLabelValue]"
                :checked="modelValue[field.name] === opt[field.opLabelValue]"
                @change="update(field.name, opt[field.opLabelValue])"
              />
              <p>{{ opt[field.opLabelName] }}</p>
            </label>
          </div>

          <!-- ================= CHECKBOX GROUP ================= -->
          <div v-else-if="field.type === 'checkbox'" class="checkbox-group">
            <label
              v-for="opt in field.options"
              :key="opt[field.opLabelValue]"
              class="checkbox-item"
            >
              <input
                type="checkbox"
                :value="opt[field.opLabelValue]"
                :checked="(modelValue[field.name] || []).includes(opt[field.opLabelValue])"
                @change="toggleCheckbox(field.name, opt[field.opLabelValue])"
              />
              <span>{{ opt[field.opLabelName] }}</span>
            </label>
          </div>

        
          <!-- ================= FILE UPLOAD ================= -->
          <input
            v-else-if="field.type === 'file'"
            type="file"
            :multiple="field.multiple"
            @change="handleFileUpload(field.name, $event)"
          />

          <!-- File Preview Names -->
          <div
            v-if="field.type === 'file' && modelValue[field.name]"
            class="file-preview"
          >
            <div v-if="Array.isArray(modelValue[field.name])">
              <div v-for="(f,i) in modelValue[field.name]" :key="i">
                📎 {{ f.name }}
              </div>
            </div>

            <div v-else>
              📎 {{ modelValue[field.name]?.name }}
            </div>
          </div>

          <BaseTable
          v-if="field.type === 'table'"
          :rows="field.rows"
          :columns="field.columns"
          :selectable="field.selectable"
          :multiSelect="field.multiSelect"
          v-model:selectedRows="modelValue[field.name]"
        />

          
        </div>

        <div class="modal-actions">
          <button class="btn btn-primary" type="submit">
            {{ submitText }}
          </button>

          <button class="btn cancel-btn" type="button" @click="$emit('close')">
            إلغاء
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Delete Confirmation -->
  <div v-if="confirmOpen" class="modal-overlay">
    <div class="modal-content confirm-box">
      <h2>تأكيد الحذف</h2>

      <p>{{ confirmText }}</p>

      <div class="modal-actions">
        <button class="btn btn-danger" @click="$emit('confirmDelete')">
          حذف
        </button>
        <button class="btn cancel-btn" @click="$emit('cancelDelete')">
          إلغاء
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
import { onMounted } from 'vue'
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

  confirmText: {
    type: String,
    default: 'هل أنت متأكد من الحذف؟',
  },
})

const emit = defineEmits([
  'close',
  'save',
  'update:modelValue',
  'confirmDelete',
  'cancelDelete',
])

function update(name, value) {
  emit('update:modelValue', {
    ...props.modelValue,
    [name]: value,
  })
}


function toggleCheckbox(name, value) {
  const current = props.modelValue[name] || []

  let updated
  if (current.includes(value)) {
    updated = current.filter(v => v !== value)
  } else {
    updated = [...current, value]
  }

  emit('update:modelValue', {
    ...props.modelValue,
    [name]: updated,
  })
}

function handleFileUpload(name, event) {
  const files = event.target.files

  emit('update:modelValue', {
    ...props.modelValue,
    [name]: files.length > 1 ? Array.from(files) : files[0],
  })
}
onMounted(()=>{
  // console.log("fields======>",props.fields)
})
</script>
<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
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
    max-width: 500px;
    text-align: right;
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

label {
    font-weight: bold;
    margin-bottom: 5px;
    display: block;
}

input, select {
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


textarea {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  resize: vertical;
}

.radio-group {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 5px;
}

.radio-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  text-wrap: nowrap;
}

.checkbox-group {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 5px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.file-preview {
  margin-top: 8px;
  font-size: 14px;
  color: #555;
}
</style>
