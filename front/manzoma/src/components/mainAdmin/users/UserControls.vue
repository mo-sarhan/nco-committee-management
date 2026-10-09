<template>
  <div class="controls-container">
    <input
      :value="search"
      @input="$emit('update:search', $event.target.value)"
      type="text"
      class="search-input"
      placeholder="بحث عن مستخدم..."
    />

    <select
      :value="statusFilter"
      @change="$emit('update:statusFilter', $event.target.value)"
      class="filter-select"
    >
      <option value="">كل الحالات</option>
      <option v-for="u in uniqueStatus" :key="u" :value="u">{{ u }}</option>
    </select>

    <select
      :value="emailFilter"
      @change="$emit('update:emailFilter', $event.target.value)"
      class="filter-select"
    >
      <option value="">كل الإيميلات</option>
      <option v-for="u in uniqueEmails" :key="u" :value="u">{{ u }}</option>
    </select>

    <select
      :value="phoneFilter"
      @change="$emit('update:phoneFilter', $event.target.value)"
      class="filter-select"
    >
      <option value="">كل الأرقام</option>
      <option v-for="p in uniquePhones" :key="p" :value="p">{{ p }}</option>
    </select>

    <div class="dropdown">
      <button class="dropdown-btn">تصدير</button>
      <div class="dropdown-menu">
        <div class="dropdown-item" @click="$emit('export', 'excel')">
          Excel <i class="fa-regular fa-file-excel" style="color: rgb(108, 218, 108)"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  // v-model props
  search: String,
  statusFilter: String,
  emailFilter: String,
  phoneFilter: String,
  // filter options
  uniqueStatus: Array,
  uniqueEmails: Array,
  uniquePhones: Array,
})

defineEmits([
  'update:search',
  'update:statusFilter',
  'update:emailFilter',
  'update:phoneFilter',
  'export', // Emit to parent to handle the export
])
</script>

<style scoped>
/* Only include styles relevant to the controls, such as .controls-container, .search-input, .filter-select, and the dropdown styles */
.controls-container {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 15px;
}
.search-input {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  flex: 1;
}
.filter-select {
  padding: 7px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
/* EXPORT DROPDOWN STYLES */
.dropdown {
  position: relative;
  display: inline-block;
}
.dropdown-btn {
  padding: 8px 12px;
  cursor: pointer;
  background-color: var(--success-color);
  color: #fff;
  border-radius: 10px;
  border: none; /* Add border: none; for button */
}
.dropdown-menu {
  display: none;
  position: absolute;
  background: #fff;
  border: 1px solid #ddd;
  min-width: 116px;
  top: 45px;
  right: -15px;
  border-radius: 10px;
  background: #e0ecf5;
  z-index: 10; /* Add z-index to ensure it's on top */
}
.dropdown-menu::before {
  content: '';
  position: absolute;
  top: -8px;
  right: 40px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid #e0ecf5;
  filter: drop-shadow(0px -1px 1px rgba(0, 0, 0, 0.1));
}
.dropdown:hover .dropdown-menu {
  display: block;
}
.dropdown-item {
  display: flex;
  padding: 8px 10px;
  cursor: pointer;
  color: black;
  font-weight: 400;
  align-items: center;
  justify-content: space-evenly;
}
.dropdown-item:hover {
  background: #d1e3f1;
}
</style>