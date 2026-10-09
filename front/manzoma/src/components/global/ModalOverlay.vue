<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineEmits(['close'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  background: #fff;
  border-radius: 14px;
  padding: 24px;
  width: fit-content;
  max-width: 95%;
  max-height: 90vh;
  min-width: 55%;
  overflow-y: auto;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}
</style>
