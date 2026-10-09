<template>
  <div class="field" ref="wrapper">
    <label v-if="label" class="field-label">{{ label }}</label>

    <div class="input-with-icon">
      <!-- Input -->
      <input
        type="text"
        class="search-input has-icon"
        :placeholder="placeholder"
        v-model="search"
        @focus="open = true"
      />

      <i v-if="icon" class="fa-solid fa-magnifying-glass search-icon"></i>
    </div>

    <!-- Dropdown -->
    <ul v-if="open" class="dropdown">
      <!-- All option -->
      <li v-if="allOptionLabel" @click="clearSelection">
        {{ allOptionLabel }}
      </li>

      <!-- Filtered options -->
      <li v-for="option in filteredOptions" :key="option[optionValue]" @click="selectValue(option)">
        {{ option[optionLabel] }}
      </li>

      <!-- Empty -->
      <li v-if="filteredOptions.length === 0" class="empty">لا توجد نتائج</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: [String, Number],
  label: String,
  placeholder: String,

  /* Array of objects */
  arrayFilter: {
    type: Array,
    default: () => [],
  },

  /* Object display key */
  optionLabel: {
    type: String,
    default: 'label',
  },

  /* Object return key */
  optionValue: {
    type: String,
    default: 'value',
  },

  allOptionLabel: String,

  icon: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue','search-change'])

const search = ref('')
const open = ref(false)
const wrapper = ref(null)

/* Filter options */
const filteredOptions = computed(() => {
  return props.arrayFilter.filter((item) =>
    item?.[props.optionLabel]?.toString().toLowerCase().includes(search.value.toLowerCase()),
  )
})

/* Select option */
function selectValue(option) {
  search.value = option[props.optionLabel]
  emit('update:modelValue', option[props.optionValue])
  open.value = false
}

/* Clear selection */
function clearSelection() {
  search.value = ''
  emit('update:modelValue', '')
  open.value = false
}
watch(search, (val) => {
  emit('search-change', val)
})
/* Sync external value to input */
watch(
  () => props.modelValue,
  (val) => {
    const found = props.arrayFilter.find((item) => item?.[props.optionValue] === val)

    search.value = found ? found[props.optionLabel] : ''
  },
  { immediate: true },
)

/* Close on outside click */
function handleClickOutside(e) {
  if (wrapper.value && !wrapper.value.contains(e.target)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.field {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-label {
  font-size: 17px;
  font-weight: 600;
}

.input-with-icon {
  position: relative;
}

.search-input {
  height: 50px;
  min-width: 220px;
  padding: 8px 12px 8px 36px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

/* Dropdown */
.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  left: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  max-height: 220px;
  overflow-y: auto;
  z-index: 1000;
  margin-top: 4px;
}

.dropdown li {
  padding: 10px 12px;
  cursor: pointer;
}

.dropdown li:hover {
  background: #f3f4f6;
}

.empty {
  text-align: center;
  color: #999;
}
</style>
