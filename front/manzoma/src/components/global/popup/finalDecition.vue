<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { convertToArabicNumbers } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'
import { usePersonsStore } from '@/stores/persons'

const personsStore = usePersonsStore()
/* Props */
const props = defineProps({
  votes: {
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
})

const selectedFinalDecision = ref('')

/* Emits */
const emit = defineEmits(['close', 'addVote'])

function toAr(val) {
  return convertToArabicNumbers(val)
}

function submit() {
  emit('changeVote', selectedFinalDecision.value)
  closePopup()
}
function closePopup() {
  emit('close')
}
</script>

<template>
  <ModalOverlay @close="closePopup()">
    <div class="container">
      <!-- Header -->
      <h2 style="color: red">القرار النهائى</h2>
      <h2>
        <span class="mil-deg"> {{ degree }} / {{ userNamePer }}</span>
      </h2>

      <div class="final-decision-box">
        <div class="final-select-wrapper">
          <div
            v-for="vote in personsStore.votesTypes"
            :key="vote?.opinion_code"
            style="display: flex; align-items: center; gap: 10px"
          >
            <input
              :id="vote?.opinion_code"
              name="vote_code"
              type="radio"
              :value="vote?.opinion_code"
              v-model="selectedFinalDecision"
              @change="submit"
            />
            <label :for="vote?.opinion_code" class="final-label"> {{ vote.opinion_name }}</label>
          </div>
        </div>
      </div>
    </div>
  </ModalOverlay>
</template>

<style scoped>
.finalDecitionContainer {
  background: #ffffff;
  padding: 25px;
  border-radius: 16px;
  /* width: 95%; */
  max-width: 900px;
  margin: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* Header */
h2 {
  text-align: center;
  margin-bottom: 10px;
}

.mil-deg {
  color: #888;
}

/* chart */
.chart-container {
  max-width: 300px;
  margin: 0 auto 20px;
}

/* ================= */
/* 🔥 STATS */
/* ================= */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.stat-box {
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  padding: 15px;
  border-radius: 14px;
  text-align: center;
  transition: 0.3s;
  border: 1px solid #eee;
}

.stat-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.stat-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-numbers {
  color: #555;
}

.stat-percent {
  font-size: 22px;
  font-weight: bold;
  margin-top: 5px;
}

/* progress */
.progress {
  height: 8px;
  background: #eee;
  border-radius: 10px;
  margin-top: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 10px;
  transition: 0.4s ease;
}

/* dynamic colors */
.stat-box:nth-child(1) .progress-bar {
  background: #4caf50;
}
.stat-box:nth-child(2) .progress-bar {
  background: #f44336;
}
.stat-box:nth-child(3) .progress-bar {
  background: #2196f3;
}
.stat-box:nth-child(4) .progress-bar {
  background: #ff9800;
}

/* ================= */
/* 👥 VOTERS */
/* ================= */
.vote-section {
  margin-top: 20px;
  padding: 12px;
  border-radius: 12px;
  background: #fafafa;
  border: 1px solid #eee;
}

.vote-section h3 {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.vote-section h3 span {
  color: #dc3545;
}

.voters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.voter {
  background: white;
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  transition: 0.2s;
}

.voter:hover {
  background: #4caf50;
  color: white;
  cursor: pointer;
}

/* button */
.close-btn {
  margin-top: 20px;
  width: 100%;
  padding: 10px;
  border: none;
  background: #333;
  color: white;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;
}

.close-btn:hover {
  background: #000;
}
.vote-section {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chart-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto 25px;
  padding: 15px;
  background: #fafafa;
  border-radius: 12px;
  border: 1px solid #eee;
}

.final-decision-box {
  margin-top: 40px;
  margin-bottom: 40px;
  padding: 20px;
  border-radius: 14px;
  background: #ffffff;
  border: 1px solid #e0e4ff;
}

.vote-row {
  display: grid;
  grid-template-columns: 160px 1fr 40px;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.vote-label {
  font-weight: 600;
}

.vote-bar-wrapper {
  height: 12px;
  background: #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.vote-bar {
  height: 100%;
  transition: width 0.3s ease;
}

.vote-bar.accepted {
  background: #2b8a3e;
}

.vote-bar.rejected {
  background: #c92a2a;
}

.vote-bar.pending {
  background: #e67700;
}

.vote-count {
  text-align: center;
  font-weight: bold;
}

.final-result {
  margin-top: 25px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.final-select-wrapper {
  display: flex;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
  justify-content: space-around;
}

.final-label {
  font-weight: 700;
  font-size: 21px;
}

.final-select {
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid #ffffff;
  min-width: 220px;
  transition: 0.2s ease;
}

.final-select:focus {
  border-color: #4c6ef5;
  outline: none;
}

.save-final-btn {
  padding: 8px 16px;
}
</style>
