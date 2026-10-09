<script setup>
import { convertToArabicNumbers } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'

/* Props */
const props = defineProps({
  personHistory: {
    type: Array,
    default: () => [],
  },
  personDegree: {
    type: String,
    required: true,
    default: '---',
  },
  personName: {
    type: String,
    required: true,
    default: '---',
  },
})

/* Emits */
const emit = defineEmits(['close'])

/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number)
}

function closeHistoryPopup() {
  emit('close')
}
</script>

<template>
  <ModalOverlay @close="closeHistoryPopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ personDegree }} / </span> {{ personName }}
      </h2>
      <div v-if="personHistory" class="table-container">
        <table>
          <thead>
            <tr>
              <th colspan="4">التجديد</th>
            </tr>
            <tr style="background-color: #80808040">
              <th>م</th>
              <th>التجديد</th>
              <th>تاريخ التجديد</th>
              <th>الملاحظات</th>
            </tr>
            <!-- <th class="head-table">التاريخ</th> -->
          </thead>
          <tbody>
            <tr v-for="(us, index) in personHistory.tagded" :key="us.index">
              <td>{{ toAr(`${index + 1}`) }}</td>
              <td>{{ us.degree_name }}</td>
              <td>{{ toAr(`${us.to_date}`) }}</td>
              <td>
                {{ us.nashra_name }}
                <span v-if="us.refuse_reson_name">--</span>{{ us.refuse_reson_name }}
              </td>
            </tr>
          </tbody>
        </table>
        <table>
          <thead>
            <tr>
              <th colspan="4">الترقي</th>
            </tr>
            <tr style="background-color: #80808040">
              <th>م</th>
              <th>درجة</th>
              <th>تاريخ الترقي</th>
              <th>الملاحظات</th>
            </tr>
          </thead>
          <tbody v-for="(us, index) in personHistory.tarky">
            <tr style="border-bottom: 1px solid">
              <td>{{ toAr(`${index + 1}`) }}</td>
              <td>{{ us.degree_name }}</td>
              <td>{{ toAr(`${us.to_date}`) }}</td>
              <td>
                {{ us.nashra_name }}
                <span v-if="us.refuse_reson_name">--</span>{{ us.refuse_reson_name }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h1 v-else style="text-align: center">لا يوجد بيانات للعرض</h1>
      <button @click="closeHistoryPopup()" class="close-btn">رجوع</button>
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
  max-height: 65vh;
  padding: 25px 50px;
  border-radius: 20px;
  margin: 0 20px;
}
.table-container {
  gap: 16px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100%, 1fr));
  overflow-y: scroll;
  max-height: 46vh;
}
.table-container table {
  width: 100%;
}

.container h2 {
  text-align: center;
}
.table-container::-webkit-scrollbar-thumb {
  width: 10px;
  height: 30px;
  background-color: rgb(19, 14, 14);
}
.table-container::-webkit-scrollbar {
  width: 10px;
  background-color: rgba(139, 138, 138, 0.418);
}
</style>
