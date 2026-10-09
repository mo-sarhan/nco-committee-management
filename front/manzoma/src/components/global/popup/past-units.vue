<script setup>
import { ref, onMounted } from 'vue'
import { convertToArabicNumbers } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'

/* Props */
const props = defineProps({
  tableData: {
    type: Array,
    default: () => [],
  },
  userNamePer: {
    type: String,
    default: '',
  },
  unit_name: {
    type: String,
    default: '',
  },
  degree: {
    type: String,
    default: '',
  },
})

/* Emits */
const emit = defineEmits(['close'])

/* State (data) */
const khaled = ref('hamza')

/* Lifecycle */
onMounted(() => {
  // mounted logic if needed
})

/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number)
}

function closePopup() {
  emit('close')
}
</script>

<template>
  <ModalOverlay @close="closePopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>
      <table>
        <thead style="background-color: rgb(180, 180, 180)">
          <tr>
            <th rowspan="3">م</th>
            <th rowspan="3">الوحدة</th>
            <th colspan="2">مدة الخدمة بالوحــدة</th>
          </tr>
          <tr>
            <th class="head-tabl">مــن</th>
            <th class="head-table" style="border-right: 1px solid">الــي</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(un, index) in tableData"
            :key="index"
            :style="{
              background:
                index == tableData.length - 1 &&
                unit_name == tableData[tableData.length - 1].unit_name
                  ? '#00ff004d'
                  : '',
            }"
          >
            <td>
              {{ toAr(`${index + 1}`) }}
            </td>
            <td>{{ `${un.unit_name || '--'}` }}</td>

            <td>
              {{ toAr(`${un.from_unit_date || '--'}`) || '--' }}
            </td>
            <td v-if="toAr(`${un.to_unit_date}`) != 'null'">
              {{ toAr(`${un.to_unit_date}`) || '--' }}
            </td>
            <td v-else>---</td>
          </tr>
        </tbody>
      </table>
      <button @click="closePopup()" class="close-btn">رجوع</button>
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
