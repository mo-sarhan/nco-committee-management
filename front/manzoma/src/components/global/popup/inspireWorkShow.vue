<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { convertToArabicNumbers, getWsUrl } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'

/* Props */
const props = defineProps({
  tableData: {
    type: String,
    default: '',
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

const showAttachment = ref(false)
const attachmentUrl = ref(null)
/* Emits */
const emit = defineEmits(['close'])

// function getFileUrl(path) {
//   return getWsUrl(path)
// }
/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number)
}

function closeReasonsPopup() {
  emit('close')
}

function getFileUrl(file) {
  // adjust for your backend path
  const base = import.meta.env.VITE_MEDIA_BASE_URL
  console.log(base)
  return `${base}${file}`
}
function openAttachment(file) {
  attachmentUrl.value = getFileUrl(file)
  showAttachment.value = true
}
function closeAttachment() {
  showAttachment.value = false
  attachmentUrl.value = null
}
onMounted(() => {
  console.log('tableData', props.tableData)
})
</script>

<template>
  <ModalOverlay @close="closeReasonsPopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>
      <!-- Attachment Popup -->
      <div v-if="showAttachment" class="attachment-popup" @click.self="closeAttachment">
        <div class="popup-content">
          <button class="close-btn" @click="closeAttachment">✕</button>
          <img :src="attachmentUrl" alt="attachmentUrl" class="attachment-frame" />
        </div>
      </div>
      <table v-if="tableData.length > 0">
        <thead style="background-color: rgb(180, 180, 180)">
          <tr>
            <th>م</th>
            <th>توصيف الجهاز</th>
            <th>التاريخ</th>
            <th>المرفقات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in tableData" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ row.psych_notes }}</td>
            <td>{{ toAr(`${row.report_date}`) }}</td>
            <td>
              <div v-if="row.psych_attach" class="reason-attachment">
                <span class="text attach" @click="openAttachment(row.psych_attach)">
                  عرض المرفق 📎
                </span>
              </div>
              <div v-else>لايوجد مرفقات</div>
            </td>
          </tr>
        </tbody>
      </table>
      <h1 v-else style="text-align: center">لا يوجد</h1>
      <button @click="closeReasonsPopup()" class="close-btn">رجوع</button>
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

.reason-attachment {
  margin-top: 10px;
}

.reason-attachment a {
  color: #3b5bdb;
  text-decoration: none;
}

/* ATTACHMENT LINK */
.attach {
  color: #2f5bd1;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s;
}

.attach:hover {
  color: #1d3fa3;
  text-decoration: underline;
}

/* ATTACHMENT POPUP */
.attachment-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.popup-content {
  background: #fff;
  width: 85%;
  height: 90%;
  border-radius: 16px;
  position: relative;
  padding: 15px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.25s ease;
  overflow: auto;
}

/* IFRAME */
.attachment-frame {
  /* width: 100%;
  height: 100%; */
  border: none;
  border-radius: 10px;
  margin-top: 25px;
}
</style>
