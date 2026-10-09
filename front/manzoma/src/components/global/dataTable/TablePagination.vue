<template>
  <div class="pagination-container">
    <div class="page-size">
      عرض
      <select :value="pageSize" @change="$emit('update:pageSize', Number($event.target.value))">
        <option :value="5">5</option>
        <option :value="10">10</option>
        <option :value="15">15</option>
        <option :value="20">20</option>
        <option :value="30">30</option>
        <option :value="40">40</option>
      </select>
      صف لكل صفحة
    </div>

    <div class="rows-size">عرض {{ showRowSize }} من {{ rowSize }}</div>

    <!-- <div class="pagination-buttons">
      <button :disabled="page === 1" @click="$emit('update:page', page - 1)">السابق</button>

      <span class="page-label"> صفحة {{ page }} من {{ totalPages }} </span>

      <button :disabled="page === totalPages" @click="$emit('update:page', page + 1)">
        التالي
      </button>
    </div> -->
    <div class="pagination-buttons">
      <button :disabled="page === 1" @click="$emit('update:page', page - 1)">السابق</button>

      <!-- First Page -->
      <button v-if="startPage > 1" @click="$emit('update:page', 1)">1</button>

      <span v-if="startPage > 2">...</span>

      <!-- Dynamic Page Numbers -->
      <button
        v-for="p in visiblePages"
        :key="p"
        :class="{ active: p === page }"
        @click="$emit('update:page', p)"
      >
        {{ p }}
      </button>

      <span v-if="endPage < totalPages - 1">...</span>

      <!-- Last Page -->
      <button v-if="endPage < totalPages" @click="$emit('update:page', totalPages)">
        {{ totalPages }}
      </button>

      <button :disabled="page === totalPages" @click="$emit('update:page', page + 1)">
        التالي
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  page: { type: Number, required: true },
  pageSize: { type: Number, required: true },
  rowSize: { type: Number, required: true },
  showRowSize: { type: Number, required: true },
  totalPages: { type: Number, required: true },
})

defineEmits(['update:page', 'update:pageSize'])

const maxVisible = 5

const startPage = computed(() => {
  return Math.max(1, props.page - Math.floor(maxVisible / 2))
})

const endPage = computed(() => {
  return Math.min(props.totalPages, startPage.value + maxVisible - 1)
})

const visiblePages = computed(() => {
  const pages = []
  for (let i = startPage.value; i <= endPage.value; i++) {
    pages.push(i)
  }
  return pages
})
</script>

<style scoped>
/* Only include styles relevant to the pagination */
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-buttons button {
  padding: 7px 15px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
}
.pagination-buttons button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-buttons button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.page-size select {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.page-label {
  margin: 0 10px;
}
</style>
