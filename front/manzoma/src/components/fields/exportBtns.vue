<template>
  <!-- EXPORT -->
  <div class="field">
    <!-- <label class="field-label">تصدير</label> -->

    <div class="dropdown">
      <button class="dropdown-btn">تصدير</button>

      <div class="dropdown-menu">
        <div
          v-for="exportBtn in exportTypesBtns"
          :key="exportBtn.type"
          class="dropdown-item"
          @click="$emit('export', exportBtn.type)"
        >
          {{ exportBtn.label }}
          <i
            :class="exportBtn.icon"
            :style="{ color: exportBtn.color }"
          ></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  exportTypesBtns: {
    type: Array,
    required: true,
  },
})

defineEmits(['export'])
</script>


<style scoped>
.dropdown {
  position: relative;
  display: inline-block;
}
.dropdown-btn {
  padding: 10px 30px;
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
/* Field wrapper */
.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Label */
.field-label {
  font-size: 17px;
  color: #374151;
  font-weight: 600;
  white-space: nowrap;
}
</style>
