<script setup>
import { convertToArabicNumbers } from '@/utils/glopal'
import { computed, ref } from 'vue'
import ModalOverlay from '../ModalOverlay.vue'

/* Props */
const props = defineProps({
  desc: {
    type: Array,
    default: () => [],
  },
  userNamePer: String,
  degree: String,
})

/* Emits */
const emit = defineEmits(['close'])

function closedesitionNotesPopup() {
  emit('close')
}

function toAr(val) {
  if (val === null || val === undefined) return '---'
  return convertToArabicNumbers(val)
}
const showAttachment = ref(false)
const attachmentUrl = ref(null)

function openAttachment(file) {
  attachmentUrl.value = getFileUrl(file)
  showAttachment.value = true
}

function closeAttachment() {
  showAttachment.value = false
  attachmentUrl.value = null
}

function getFileUrl(file) {
  // adjust for your backend path
  const base = import.meta.env.VITE_MEDIA_BASE_URL
  console.log(base)
  return `${base}${file}`
}
</script>

<template>
  <ModalOverlay @close="closedesitionNotesPopup">
    <div class="container">
      <h2>
        <span class="mil-deg">{{ degree }} / </span>
        {{ userNamePer }}
      </h2>

      <div class="decisions">
        <div class="decision-row" v-if="desc?.opinion_notes">
          <!-- Notes -->
          <div class="decision-main">
            <span class="label">ملاحظات:</span>
            <span class="text">{{ desc.opinion_notes }}</span>
          </div>
        </div>
        <div class="decision-row" v-if="desc?.opinion_attached">
          <!-- Attachment -->
          <div v-if="desc?.opinion_attached" class="decision-main">
            <span class="label">مرفق:</span>
            <span class="text attach" @click="openAttachment(desc.opinion_attached)">
              عرض المرفق 📎
            </span>
          </div>
        </div>
        <h1 v-else class="empty">لا يوجد ملاحظات او مرفقات</h1>
      </div>

      <!-- Attachment Popup -->
      <div v-if="showAttachment" class="attachment-popup" @click.self="closeAttachment">
        <div class="popup-content">
          <button class="close-btn" @click="closeAttachment">✕</button>
          <img :src="attachmentUrl" alt="attachmentUrl" class="attachment-frame" />
        </div>
      </div>

      <button @click="closedesitionNotesPopup" class="close-btn">رجوع</button>
    </div>
  </ModalOverlay>
</template>

<style scoped>
.container {
  width: 95%;
  max-width: 900px;
  background: #ffffff;
  max-height: 90vh;
  padding: 30px 25px;
  border-radius: 20px;
  margin: 0 auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow-y: auto;
}

/* HEADER */
.container h2 {
  text-align: center;
  margin-bottom: 25px;
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.mil-deg {
  color: #d9363e;
  font-weight: 600;
}

.empty {
  text-align: center;
  font-size: 22px;
  margin: 30px 0;
}

/* DECISION CARD */
.decisions {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.decision-row {
  background: #f9fbff;
  border: 1px solid #eef1f7;
  border-radius: 16px;
  padding: 15px;
  transition: 0.2s ease;
}

.decision-row:hover {
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
}

/* ROW CONTENT */
.decision-main {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

/* LABEL */
.label {
  background: #eef1f7;
  color: #555;
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 25px;
  font-weight: 600;
  white-space: nowrap;
}

/* DECISION BADGE */
.decision {
  background: #e6edff;
  color: #2f5bd1;
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
}

/* TEXT */
.text {
  color: #444;
  font-size: 25px;
  line-height: 1.6;
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

/* ANIMATION */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
