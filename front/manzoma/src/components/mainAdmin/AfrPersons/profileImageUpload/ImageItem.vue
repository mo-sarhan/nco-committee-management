<template>
  <div class="image-item">
    <div class="status-badge" :class="statusClass">
      <span class="dot"></span>
      {{ item.photo_status?.status_name || 'غير محدد' }}
    </div>

    <!-- ===== REJECT REASONS DISPLAY ===== -->
    <div
      v-if="
        (item.photo_status?.status_name?.includes('رفض') ||
          item.photo_status?.status_name?.includes('مرفوض')) &&
        item.reject_reason?.length
      "
      class="reject-reasons-display"
    >
      <div class="reasons-title">أسباب الرفض</div>

      <div class="reasons-list">
        <span v-for="(reason, index) in formattedRejectReasons" :key="index" class="reason-chip">
          ✖ {{ reason }}
        </span>
      </div>
    </div>

    <label class="upload-label">
      كارت {{ item.label }}
      <small v-if="item.familySerial">- زوجة: {{ item.familySerial }}</small>
    </label>

    <div class="drop-zone" @click="$emit('zoom', preview)">
      <img v-if="preview" :src="preview" class="preview cover" />
      <span v-else>لا توجد صورة</span>
    </div>

    <!-- ===== REVIEW ACTIONS ===== -->
    <div v-if="reviewMode" class="review-actions">
      <div class="decision-buttons" v-if="allowReviewImage">
        <button
          :class="['accept-btn', item.decision === 1 && 'active']"
          @click.stop="acceptImage"
        >
          ✔ قبول
        </button>

        <button
          :class="['reject-btn', rejectionallow && 'active']"
          @click.stop="startReject"
        >
          ✖ رفض
        </button>
      </div>

      <!-- Reject Reason -->
      <div v-if="rejectionallow" class="reject-reason">
        <select v-model="item.reject_reason" @change="selectRejectReason">
          <option value="">اختر سبب الرفض</option>
          <option
            v-for="reason in rejectReasons"
            :key="reason.reject_code"
            :value="reason.reject_code"
          >
            {{ reason.reject_name }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  item: Object,
  preview: String,
  reviewMode: Boolean,
  allowReviewImage: Boolean,
  rejectReasons: Array,
})

const emit = defineEmits(['decisionChange', 'zoom'])

const rejectionallow = ref(false)

/* ===== STATUS COLOR ===== */
const statusClass = computed(() => {
  const status = props.item.photo_status?.status_name?.toLowerCase()

  if (!status) return 'status-pending'
  if (status.includes('قبول') || status.includes('مقبول')) return 'status-approved'
  if (status.includes('رفض') || status.includes('مرفوض')) return 'status-rejected'

  return 'status-pending'
})

/* ===== FORMAT REJECT REASONS ===== */
const formattedRejectReasons = computed(() => {
  const rejectList = props.item?.reject_reason
  if (!Array.isArray(rejectList)) return []

  const names = rejectList.flatMap((reject) =>
    Array.isArray(reject.reason) ? reject.reason.map((r) => r.reject_name) : [],
  )

  return [...new Set(names)]
})

/* ===== ACCEPT IMAGE ===== */
function acceptImage() {
  rejectionallow.value = false
  props.item.reject_reason = null
  props.item.decision = 1

  emit('decisionChange', props.item)
}

/* ===== START REJECT ===== */
function startReject() {
  props.item.decision = 0
  rejectionallow.value = true
}

/* ===== SELECT REJECT REASON ===== */
function selectRejectReason() {
  if (!props.item.reject_reason) return

  emit('decisionChange', props.item)
}
</script>

<style scoped>
.image-item {
  border: 2px solid #e0e0e0;
  border-radius: 14px;
  padding: 16px;
  background-color: #fff;
  position: relative;
  /* height: 520px; */
  display: flex;
  flex-direction: column;
  transition:
    transform 0.3s,
    box-shadow 0.3s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 16px; /* Space between items */
}

.image-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.upload-label {
  font-weight: 600;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  display: inline-block;
  margin-bottom: 30px;
  transition: color 0.2s;
  text-align: center;
}

.upload-label:hover {
  color: var(--mainColor);
}

.drop-zone {
  height: 410px;
  width: 100%; /* Take full width of the container */
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  border: 2px dashed #ccc;
  border-radius: 8px;
  transition: background-color 0.3s ease;
  margin-bottom: 12px;
}

.drop-zone:hover {
  background: #f0f0f0;
}

.preview {
  width: 100%;
  height: 100%;
  /* object-fit: cover; */
  border-radius: 8px;
  transition: transform 0.3s ease-in-out;
}

.preview.cover {
  cursor: pointer;
}

.preview.cover:hover {
  transform: scale(1.05);
}

.review-actions {
  margin-top: 12px;
}

.decision-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-bottom: 8px;
}

.accept-btn,
.reject-btn {
  flex: 1;
  padding: 6px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.accept-btn {
  background: #e8f7ec;
  color: #1b7f3c;
}

.reject-btn {
  background: #fdeaea;
  color: #b42318;
}

.accept-btn.active {
  background: #1b7f3c;
  color: white;
}

.reject-btn.active {
  background: #b42318;
  color: white;
}

.reject-reason select {
  width: 100%;
  padding: 6px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
/* ===== STATUS BADGE ===== */

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 12px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
  letter-spacing: 0.3px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(6px);
  transition: all 0.3s ease;
}

/* ================= REJECT REASONS DISPLAY ================= */

.reject-reasons-display {
  margin-top: 10px;
  padding: 10px;
  border-radius: 10px;
  background: linear-gradient(135deg, #fff5f5, #ffe3e3);
  border: 1px solid #f5c2c2;
}

.reasons-title {
  font-size: 12px;
  font-weight: 700;
  color: #b42318;
  margin-bottom: 6px;
  text-align: center;
  letter-spacing: 0.4px;
}

.reasons-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
}

.reason-chip {
  background: white;
  color: #b42318;
  border: 1px solid #f1a1a1;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(180, 35, 24, 0.1);
  transition: all 0.2s ease;
}

.reason-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(180, 35, 24, 0.2);
}

/* small animated dot */
.status-badge .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

/* Approved */
.status-approved {
  background: linear-gradient(135deg, #e6f9f0, #c8f2dd);
  color: #087443;
}

.status-approved .dot {
  background-color: #0bbf6a;
}

/* Rejected */
.status-rejected {
  background: linear-gradient(135deg, #fdecec, #f8d0d0);
  color: #b42318;
}

.status-rejected .dot {
  background-color: #e11d48;
}

/* Pending */
.status-pending {
  background: linear-gradient(135deg, #fff7e6, #ffe5b4);
  color: #a15c00;
}

.status-pending .dot {
  background-color: #f59e0b;
}

/* Animation */
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.3);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.7;
  }
}
</style>
