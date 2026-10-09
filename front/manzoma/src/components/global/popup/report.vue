<script setup>
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
  degree: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: '',
  },
})

/* Emits */
const emit = defineEmits(['close'])

/* Methods */
function closeReportPopup() {
  emit('close')
}

function toAr(number) {
  return convertToArabicNumbers(number)
}
</script>

<template>
  <ModalOverlay @close="closeReportPopup()">
    <div class="container" @click.stop>
      <h2>تقــريـــر حضـــــور الـلـجـنــة</h2>
      <div class="tableContaine">
        <table>
          <thead style="background-color: rgb(180, 180, 180)">
            <tr>
              <th rowspan="2">م</th>
              <th rowspan="2">السلاح</th>
              <th>الإجمالي</th>
              <th>موجود</th>
              <th>تخلف</th>
              <th class="">تم مناظرته</th>
              <th class="">لم يتم مناظرته</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pun, index) in tableData" :key="index">
              <td>{{ toAr(`${Number(index) + 1}`) }}</td>
              <td>{{ pun.army_name }}</td>
              <td>{{ toAr(`${pun.total}`) }}</td>
              <td style="white-space: nowrap">
                {{ toAr(`${pun.attended_true}`) }}
              </td>
              <td style="white-space: nowrap">
                {{ toAr(`${pun.attended_false}`) }}
              </td>
              <td style="white-space: nowrap">
                {{ toAr(`${pun.done_flag_true}`) }}
              </td>
              <td style="white-space: nowrap">
                {{ toAr(`${pun.done_flag_false}`) }}
              </td>
            </tr>
            <!-- <tr>
              <td
                colspan="2"
                style="
                  font-size: 18px;
                  font-weight: 600;
                  background: rgb(196, 194, 194);
                "
              >
                الاجمالي
              </td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr> -->
          </tbody>
        </table>
      </div>
      <!-- <h1 v-else style="text-align: center">لا يكن</h1> -->

      <button @click="closeReportPopup()" class="close-btn">رجوع</button>
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
.tableContaine {
  /* height: 423px; */
  overflow-y: auto;
  max-height: 65vh;
  overflow: auto;
}
.tableContaine::-webkit-scrollbar-thumb {
  width: 10px;
  height: 30px;
  background-color: rgb(19, 14, 14);
}
.tableContaine::-webkit-scrollbar {
  width: 10px;
  background-color: rgba(139, 138, 138, 0.418);
}
thead {
  background: white;
  position: sticky;
  top: 0px;
}
</style>
