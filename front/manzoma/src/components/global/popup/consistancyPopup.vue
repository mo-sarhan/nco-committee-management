<script setup>
import { convertToArabicNumbers } from "@/utils/glopal";
import ModalOverlay from "../ModalOverlay.vue";

/* Props */
const props = defineProps({
  tableData: {
    type: Array,
    default: () => [],
  },
  userNamePer: {
    type: String,
    default: "",
  },
  degree: {
    type: String,
    default: "",
  },
  type: {
    type: String,
    default: "",
  },
});

/* Emits */
const emit = defineEmits(["close"]);

/* Methods */
function closeConsistancyPopup() {
  emit("close");
}

function toAr(number) {
  return convertToArabicNumbers(number);
}
</script>


<template>
  <ModalOverlay @close="closeConsistancyPopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span>{{ userNamePer }}
      </h2>
      <div v-if="tableData.length > 0" class="tableContaine">
        <table>
          <thead>
            <tr>
              <th rowspan="2">م</th>
              <th rowspan="2">الطول</th>
              <th>الوزن</th>
              <th>التاريخ</th>
              <th>الوحدة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pun, index) in tableData" :key="index">
              <td>{{ toAr(`${index + 1}`) }}</td>
              <td v-if="pun.length" style="white-space: nowrap">
                {{ toAr(`${pun.length}`) }} سم
              </td>
              <td v-else>لايكن</td>

              <td v-if="pun.weight">{{ toAr(`${pun.weight}`) }} كجم</td>
              <td v-else>لايكن</td>
              <td>
                {{ pun.check_date == "nan" ? "--" : toAr(`${pun.check_date}`) }}
              </td>
              <td style="white-space: nowrap">
                {{ toAr(`${pun.army_name}`) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h1 v-else style="text-align: center">لا يوجد</h1>

      <button @click="closeConsistancyPopup()" class="close-btn">رجوع</button>
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
