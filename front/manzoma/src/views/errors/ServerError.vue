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

<template>
  <BaseError
    code="500"
    title="حدث خطاء"
    buttonText="العودة للرئيسية "
    @onClick="goback"
  />
</template>