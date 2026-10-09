<script setup>
import BaseError from './BaseError.vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const goLogin = () => {
  router.push({
    path: '/login',
    query: { redirect: route.fullPath }
  })
}
</script>

<template>
  <BaseError
    code="401"
    title="يجب تسجيل الدخول"
    buttonText="تسجيل الدخول"
    @onClick="goLogin"
  />
</template>