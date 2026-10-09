<template>
  <secSpliter :splitTitle="title" @expand="$emit('sectionOpen')" />

  <div v-if="sectionExpand" class="opinions">
    <div v-for="op in opinions" :key="op.opinion_id" class="opinion">
      <!-- Top line: Type + Decision -->
      <div class="opinion-main">
        <span class="label">{{ op.opinion_type_data.opinion_name }}</span>
        <span class="decision">{{ op.opinion_data.opinion_name }}</span>
      </div>

      <!-- Notes -->
      <div v-if="op.opinion_notes" class="opinion-main">
        <span class="label">ملاحظات:</span>
        <span class="text">{{ op.opinion_notes }}</span>
      </div>

      <!-- Attachment -->
      <div v-if="op.opinion_attached" class="opinion-main">
        <span class="label">مرفق:</span>
        <span class="text attach" @click="openAttachment(op.opinion_attached)">
          عرض المرفق 📎
        </span>
      </div>
    </div>
  </div>

  <!-- Attachment Popup -->
  <div v-if="showAttachment" class="attachment-popup">
    <div class="popup-content">
      <button class="close-btn" @click="closeAttachment">✕</button>
      <iframe v-if="attachmentUrl" :src="attachmentUrl" class="attachment-frame"></iframe>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import secSpliter from '@/components/mainAdmin/AfrPersons/profile/secSpliter.vue'

defineProps({
  title: { type: String, default: 'الآراء' },
  opinions: { type: Array, default: () => [] },
  sectionExpand: { type: Boolean, default: true },
})

defineEmits(['sectionOpen'])

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
  return `/media/${file}`
}
</script>

<style scoped>
.opinions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}

.opinion {
  background: #fff;
  border-radius: 10px;
  padding: 8px 12px;
  border: 1px solid #e6e9ef;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.opinion-main {
  display: flex;
  gap: 10px;
  font-size: 13px;
  flex-wrap: wrap;
  align-items: center;
}

.label {
  background-color: #8080804d;
  height: 43px;
  margin: 0;
  position: inherit;
  display: flex;
  align-items: center;
  border-radius: 25px 0px 10px 0px;
  text-align: center;
  place-content: center;
  min-width: 80px;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  padding: 1px 5px;
}

.decision {
  background: #eef3ff;
  color: #2f5bd1;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
}

.notes,
.attachment {
  display: flex;
  gap: 6px;
  font-size: 13px;
  flex-wrap: wrap;
}

.label {
  font-weight: 600;
  color: #666;
}

.text {
  color: #444;
  font-size: 14px;
}

.attach {
  color: #2f5bd1;
  cursor: pointer;
  font-weight: 600;
}

.attach:hover {
  text-decoration: underline;
}

/* POPUP */
.attachment-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.popup-content {
  background: white;
  width: 80%;
  height: 80%;
  border-radius: 10px;
  position: relative;
  padding: 10px;
}

.attachment-frame {
  width: 100%;
  height: 100%;
  border: none;
}

.close-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  border: none;
  background: #ff4d4f;
  color: white;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
}
</style>
