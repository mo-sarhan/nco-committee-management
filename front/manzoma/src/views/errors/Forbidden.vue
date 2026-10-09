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
    code="401"
    title="ليس لديك صلاحية للوصول لهذه الصفحة"
    buttonText="العودة للرئيسية "
    @onClick="goback"
  />
</template>