<template>
  <div v-if="open" class="modal-overlay">
    <div class="modal-content opinion-popup">

      <h2>إضافة رأي</h2>

      <div class="form-group">
        <label>نوع الرأي</label>
        <select v-model="form.type" class="form-control">
          <option disabled value="">اختر النوع</option>
          <option value="army">رأي السلاح</option>
          <option value="unit">رأي الوحدة</option>
        </select>
      </div>

      <div class="form-group">
        <label>نص الرأي</label>
        <textarea
          v-model="form.text"
          rows="5"
          class="form-control"
          placeholder="اكتب نص الرأي هنا"
        />
      </div>

      <div class="modal-actions">
        <button class="btn btn-primary" @click="submit">
          حفظ
        </button>

        <button class="btn cancel-btn" @click="close">
          إلغاء
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  open: { type: Boolean, required: true }
})

const emit = defineEmits(['close', 'save'])

const form = reactive({
  type: '',
  text: ''
})

watch(() => props.open, (val) => {
  if (!val) reset()
})

function reset() {
  form.type = ''
  form.text = ''
}

function close() {
  emit('close')
}

function submit() {
  if (!form.type || !form.text) {
    alert('برجاء إدخال نوع الرأي ونص الرأي')
    return
  }

  emit('save', {
    type: form.type,
    text: form.text
  })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  width: 500px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 8px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>