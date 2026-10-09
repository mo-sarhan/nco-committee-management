<template>
  <div class="field">
    <label class="field-label">{{ label }}</label>

    <div class="date-range">
      <input
        type="date"
        class="filter-date"
        :value="model.start"
        @input="update('start', $event.target.value)"
      />

      <span class="separator">—</span>

      <input
        type="date"
        class="filter-date"
        :value="model.end"
        @input="update('end', $event.target.value)"
      />
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  modelValue: Object,
  label: String,
})

const emit = defineEmits(['update:modelValue'])

const model = reactive({
  start: props.modelValue?.start || '',
  end: props.modelValue?.end || '',
})

function update(key, value) {
  model[key] = value
}

watch(model, () => {
  emit('update:modelValue', { ...model })
}, { deep: true })
</script>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.field-label {
  font-size: 17px;
  font-weight: 600;
}
.date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}
.filter-date {
  height: 50px;
  min-width: 140px;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.separator {
  font-weight: bold;
}
</style>