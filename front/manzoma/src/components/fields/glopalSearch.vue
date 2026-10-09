<template>
  <div class="controls-container">
    <div class="controles">
      <div class="search-fields">
        <div class="fields">
          <component
            v-for="field in fields"
            :key="field.key"
            :is="getComponent(field.type)"
            v-model="localFilters[field.key]"
            v-bind="field"
            @keyup.enter="submit"
            @search-change="handleSearchChange(field.key, $event)"
          />
        </div>

        <button class="search-group" @click="submit">
          بحث
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
        </button>
      </div>

      <div class="exports" v-if="exportBtns?.length">
        <ExportBtns :exportTypesBtns="exportBtns" @export="$emit('export', $event)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import SearchField from '@/components/fields/searchField.vue'
import searchableSelectField from '@/components/fields/searchableSelectField.vue'
import SelectField from '@/components/fields/selectField.vue'
import DateField from '@/components/fields/dateField.vue'
import DateRangeField from '@/components/fields/dateRangeField.vue'
import ExportBtns from '@/components/fields/exportBtns.vue'

const props = defineProps({
  fields: Array,
  modelValue: Object,
  exportBtns: Array,
})

const emit = defineEmits(['update:modelValue','search-change', 'search', 'export'])

const localFilters = reactive({ ...props.modelValue })

// watch(localFilters, () => {
//   emit('update:modelValue', { ...localFilters })
// }, { deep: true })
function handleSearchChange(key, value) {
  console.log(key, value)
  emit('search-change', { [key]: value })
}
function submit() {
  emit('search', { ...localFilters })
}

function getComponent(type) {
  return {
    select: SelectField,
    date: DateField,
    daterange: DateRangeField,
    text: SearchField,
    completeText: searchableSelectField,
  }[type || 'text']
}
</script>

<style scoped>
.controls-container {
  margin-bottom: 15px;
}
.controles {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}
.search-fields {
  display: flex;
  gap: 30px;
  align-items: flex-end;
}
.search-group {
  background: var(--mainColor);
  padding: 10px 40px;
  border-radius: 10px;
  color: white;
  font-size: 18px;
  font-weight: 600;
  transition: background 0.2s;
}
.search-group:hover {
  background: var(--secondColor);
  cursor: pointer;
}
.fields {
  display: flex;
  align-items: center;
  gap: 20px;
}
</style>
