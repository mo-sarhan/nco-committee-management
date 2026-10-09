<template>
  <div class="field">
    <label class="field-label">{{ label }}</label>

    <div class="input-with-icon">
      <input
        type="text"
        class="search-input has-icon"
        :value="modelValue"
        :placeholder="placeholder"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <i v-if="icon" class="fa-solid fa-magnifying-glass search-icon"></i>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  label: String,
  placeholder: String,
  icon: {
    type: Boolean,
    default: true,
  },
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
.search-input {
  height: 50px;
  min-width: 220px;
  padding: 8px 12px 8px 36px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.input-with-icon {
  position: relative;
}
.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}
</style>