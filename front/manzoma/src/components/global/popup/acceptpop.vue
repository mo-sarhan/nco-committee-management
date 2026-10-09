<script setup>
import { convertToArabicNumbers } from "@/utils/glopal";
import ModalOverlay from "../ModalOverlay.vue";

/* Props */
const props = defineProps({
  tableData: {
    type: Array,
    default: () => [],
  },
  tableDataٍSec: {
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
});

/* Emits */
const emit = defineEmits(["close"]);

/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number);
}

function closeAcceptpopup() {
  emit("close");
}
</script>


<template>
  <ModalOverlay @close="closeAcceptpopup()">
    <div class="container">
      <h2 style="margin: 0">آراء أعضاء اللجنة</h2>
      <h2 style="margin-top: 0">
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>
      <div class="con" style="display: flex; gap: 50px">
        <table style="height: fit-content">
          <thead
            caption="gg"
            style="background-color: rgb(21, 142, 33); color: white"
          >
            <tr>
              <th v-if="tableData.length > 0">م</th>
              <th>موافق</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="tableData.length == 0" colspan="2">
              <td style="text-align: center">لايكن</td>
            </tr>
            <tr v-for="(tr, index) in tableData" :key="index">
              <td>{{ toAr(`${index + 1}`) }}</td>
              <td>{{ tr.member }}</td>
            </tr>
          </tbody>
        </table>
        <table style="height: fit-content">
          <thead caption="gg" style="background-color: #9c0000; color: white">
            <tr>
              <th v-if="tableDataٍSec.length > 0">م</th>
              <th>غير موافق</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="tableDataٍSec.length == 0" colspan="2">
              <td style="text-align: center">لايكن</td>
            </tr>
            <tr v-for="(tr, index) in tableDataٍSec" :key="index">
              <td>{{ toAr(`${index + 1}`) }}</td>
              <td>{{ tr.member }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="closeAcceptpopup()" class="close-btn">رجوع</button>
    </div>
  </ModalOverlay>
</template>
<style scoped>

</style>
