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
});

/* Emits */
const emit = defineEmits(["close"]);

/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number);
}

function closeTravelPopup() {
  emit("close");
}
</script>


<template>
  <ModalOverlay @close="closeTravelPopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>
      <table v-if="tableData.length > 0">
        <thead style="background-color: rgb(180, 180, 180)">
          <tr>
            <th rowspan="2">م</th>
            <th rowspan="2">نـــوع السفـــر</th>
            <th rowspan="2">الـجـهـة</th>
            <!-- <th colspan="4" style="border-bottom: 1px solid">
              مـــدة السفـــر
            </th> -->
          </tr>
          <tr style="border-bottom: 1px solid">
            <th
              class="head-table"
              style="border-left: 1px solid black !important"
            >
              مــن
            </th>
            <th
              class="head-table"
              style="border-left: 1px solid black !important"
            >
              الــي
            </th>
            <!-- <th class="head-table">المدة</th> -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="(tr, index) in tableData" :key="index">
            <td>{{ toAr(`${index + 1}`) }}</td>
            <td>{{ tr.safar_eara_reason_name }}</td>
            <td>{{ tr.country_name || "--" }}</td>
            <td>
              {{ toAr(`${tr.start_date !=null ? tr.start_date :"---"}`) }}
            </td>
            <td style="border-left: 1px solid black !important">
              {{ toAr(`${tr.end_date !=null ? tr.end_date :"---"}`) || "--" }}
            </td>
            <!-- <td>
              <span
                v-if="
                  tr.period.days != 0 ||
                  tr.period.months != 0 ||
                  tr.period.years != 0
                "
              >
                <span v-if="tr.period.days > 0">{{
                  toAr(`${tr.period.days}`) + "  يوم "
                }}</span>
                <span v-if="tr.period.months > 0">{{
                  toAr(`${tr.period.months}`) + "  شهر "
                }}</span>
                <span v-if="tr.period.years > 0">{{
                  toAr(`${tr.period.years}`) + "  سنه "
                }}</span></span
              >
              <span v-else>--</span>
            </td> -->
          </tr>
        </tbody>
      </table>
      <h1 v-else style="text-align: center">لا يكن</h1>
      <button @click="closeTravelPopup()" class="close-btn">رجوع</button>
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
