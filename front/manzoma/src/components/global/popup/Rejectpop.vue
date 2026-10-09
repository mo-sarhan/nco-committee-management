<script setup>
import { convertToArabicNumbers } from "@/utils/glopal";

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

function closeUpdatepopup() {
  emit("close");
}
</script>


<template>
  <ModalOverlay @close="closeUpdatepopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>
      <table>
        <thead caption="gg" style="background-color: rgb(180, 180, 180)">
          <tr>
            <th>م</th>
            <th>المــانـــع</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(tr, index) in tableData" :key="index">
            <td>{{ toAr(`${index + 1}`) }}</td>
            <td>{{ tr.refuse_reson_name }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="closeUpdatepopup()" class="close-btn">رجوع</button>
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
  overflow-y: auto;
}

.container h2 {
  text-align: center;
}
</style>
