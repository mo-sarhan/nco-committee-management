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

function closeCourserepopup() {
  emit("close");
}
</script>


<template>
  <ModalOverlay @close="closeCourserepopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>
      <table>
        <thead caption="gg">
          <tr>
            <th colspan="6">التاهيل</th>
          </tr>
          <tr style="background-color: #80808087">
            <th>م</th>
            <th>اســم الــدورة</th>
            <th>من تاريــخ</th>
            <th>الى تاريــخ</th>
            <th>تقديرالــدورة</th>
            <th>الملاحظات</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(course, index) in tableData" :key="index">
            <td>{{ toAr(`${index + 1}`) }}</td>
            <td>{{ course.dawra_name_detail }}</td>
            <td>{{ course.start_date ? toAr(`${course.start_date}`) : '' }}</td>
            <td>{{ course.end_date ? toAr(`${course.end_date}`) : '' }}</td>
            <td>{{ course.grade_name }}</td>
            <td>{{ toAr(`${course.dawra_name}`) }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="closeCourserepopup()" class="close-btn">رجوع</button>
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
