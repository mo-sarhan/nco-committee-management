<script setup>
import { convertToArabicNumbers } from '@/utils/glopal'
import { onMounted } from 'vue'
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
  degree: {
    type: String,
    default: '',
  },
})

/* Emits */
const emit = defineEmits(['close'])

/* Methods */
function closeTraqpopup() {
  emit('close')
}

function toAr(number) {
  return convertToArabicNumbers(number)
}

onMounted(() => {
  // console.log("tableData",props.tableData)
})
</script>

<template>
  <ModalOverlay @close="closeTraqpopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>
      <table>
        <thead caption="gg">
          <tr>
            <th colspan="7">تقرير الكفاءة</th>
          </tr>
          <tr style="background-color: #80808087">
            <th>م</th>
            <th>التقدير</th>
            <th>الدرجة</th>
            <th>الوحدة</th>
            <th style="width: 150px">من</th>
            <th style="width: 150px">الي</th>
            <th>القائد المباشر</th>
            <th>المصدق</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(tr, index) in tableData" :key="index">
            <td>{{ toAr(`${index + 1}`) }}</td>
            <td>
              <span v-if="tr.grade_name != 'nan'">{{ tr.grade_name }}</span
              ><span v-else></span>
            </td>
            <td>
              <span v-if="tr.direct_per_notes != 'nan'">{{
                toAr(`${tr.direct_per_notes.slice(0, 2)}`) + '%'
              }}</span
              ><span v-else></span>
            </td>
            <td>
              <span v-if="tr.unit_name != 'nan'">{{ toAr(`${tr.unit_name}`) }}</span
              ><span v-else></span>
            </td>
            <td>
              <span v-if="tr.from_date != 'nan'">{{ toAr(`${tr.from_date}`) }}</span
              ><span v-else></span>
            </td>
            <td>
              <span v-if="tr.to != 'nan'">{{ toAr(`${tr.to_date}`) }}</span>
              <span v-else> </span>
            </td>
            <td>
              <span v-if="tr.direct_per_name != 'nan'">{{ tr.direct_per_name }}</span
              ><span v-else></span>
            </td>
            <td>
              <span v-if="tr.sign_per_name != 'nan'">{{ tr.sign_per_name }}</span
              ><span v-else></span>
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="closeTraqpopup()" class="close-btn">رجوع</button>
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
table {
  font-size: 15px;
}
.container h2 {
  text-align: center;
}
</style>
