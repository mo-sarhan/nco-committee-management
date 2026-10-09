<script setup>
import { useSmartBack } from '@/composables/useSmartBack'

const { goBack } = useSmartBack('/main-admin/afr-persons')
</script>

<template>
  <button @click="goBack" class="goback">
    <span>⬅</span>
    <span>رجوع</span>
  </button>
</template>

<style>

.goback{
    color: var(--mainColor);
    display: flex;
    align-items: center;
}
</style>
