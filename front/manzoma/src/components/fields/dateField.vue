<template>
  <div class="field">
    <label class="field-label">{{ label }}</label>
    <input
      type="date"
      class="filter-date"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  label: String,
})

defineEmits(['update:modelValue'])
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
.filter-date {
  height: 50px;
  min-width: 220px;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
</style>