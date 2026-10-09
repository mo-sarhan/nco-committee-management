<script setup>
import { convertToArabicNumbers } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'

/* Props */
const props = defineProps({
  personDegree: {
    type: String,
    default: '',
    required: true,
  },
  personName: {
    type: String,
    required: true,
    default: '---',
  },
  vacationData: {
    type: Array,
    default: () => [],
  },
})

/* Emits */
const emit = defineEmits(['close'])

/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number)
}

function closeVacationPopup() {
  emit('close')
}
</script>

<template>
  <ModalOverlay @close="closeVacationPopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ personDegree }} / </span> {{ personName }}
      </h2>
      <table v-if="vacationData.length > 0">
        <thead style="background-color: rgb(180, 180, 180)">
          <tr>
            <th>م</th>
            <th>من</th>
            <th>الى</th>
            <th>السبب</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(me, index) in vacationData" :key="index">
            <td>{{ toAr(`${index + 1}`) }}</td>
            <td>{{ toAr(`${me.start_date}`) }}</td>
            <td>{{ toAr(`${me.end_date}`) }}</td>
            <td>{{ me.notes }}</td>
          </tr>
        </tbody>
      </table>
      <h1 style="text-align: center" v-else>لا يكن</h1>
      <button @click="closeVacationPopup()" class="close-btn">رجوع</button>
    </div>
  </ModalOverlay>
</template>
<style scoped>
.app {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100vw;
  height: 100vh;
  z-index: 10000;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
.container {
  width: 109vh;
  background-color: #f9f9f9f0;
  max-height: 90vh;
  padding: 25px 50px;
  border-radius: 20px;
  margin: 0 20px;
}

.container h2 {
  text-align: center;
}
</style>
