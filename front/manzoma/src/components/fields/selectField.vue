<template>
  <div class="field">
    <label class="field-label">{{ label }}</label>

    <select
      class="filter-select"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="">{{ placeholder }}</option>
      <option
        v-for="opt in options"
        :key="optionsIsList ? opt : opt[opLabelValue]"
        :value="optionsIsList ? opt : opt[opLabelValue]"
      >
        {{ optionsIsList ? opt : opt[opLabelName] }}
      </option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  label: String,
  opLabelName: String,
  opLabelValue: String,
  placeholder: String,
  options: Array,
  optionsIsList: Boolean,
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
.filter-select {
  height: 50px;
  min-width: 220px;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
</style>