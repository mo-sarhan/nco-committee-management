<template>
  <BaseError
    code="404"
    title="الصفحة غير موجودة"
    buttonText="العودة للرئيسية"
    @onClick="goback"
  />
</template>


<script setup>
import BaseError from './BaseError.vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const goback = () => {
    console.log("ascaasassa")
  router.push({path: '/'})
}
</script>