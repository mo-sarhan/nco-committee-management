<template>
  <footer class="footer" dir="rtl">
    <p>جميع الحقوق محفوظة © {{ currentYear }} - لوحة تحكم المدير</p>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear();
</script>

<style scoped>
.footer {
  background: #f0f0f0;
  text-align: center;
  padding: 15px;
  font-size: 14px;
  color: #666;
  border-top: 1px solid #ddd;
  direction: rtl;
}
</style>
