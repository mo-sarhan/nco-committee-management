<script setup>
import { computed } from 'vue'

// import { Pie } from 'vue-chartjs'
// import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

import { convertToArabicNumbers } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'

/* Props */
const props = defineProps({
  votes: {
    type: Array,
    default: () => [],
  },
  votingInfo: {
    type: Object,
    default: () => {},
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

/* Emits */
const emit = defineEmits(['close'])

/* total */
const totalVotes = computed(() => props.votes.reduce((sum, v) => sum + v.vote_count, 0))

/* percentage */
const votesStats = computed(() =>
  props.votes.map((v) => ({
    ...v,
    percentage: totalVotes.value ? ((v.vote_count / totalVotes.value) * 100).toFixed(1) : 0,
  })),
)

function toAr(val) {
  return convertToArabicNumbers(val)
}

function closePopup() {
  emit('close')
}

// ChartJS.register(Title, Tooltip, Legend, ArcElement)

// /* chart data */
// const chartData = computed(() => ({
//   labels: props.votes.map((v) => v.vote_name),
//   datasets: [
//     {
//       data: props.votes.map((v) => v.vote_count),
//       backgroundColor: ['#4caf50', '#f44336', '#2196f3', '#ff9800', '#9c27b0'],
//       borderWidth: 1,
//     },
//   ],
// }))

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartData = computed(() => ({
  labels: props.votes.map((v) => v.vote_name),
  datasets: [
    {
      label: 'عدد الأصوات',
      data: props.votes.map((v) => v.vote_count),
      backgroundColor: ['#f44336', '#2196f3', '#ff9800', '#227750'],
      borderRadius: 8,
      barThickness: 40,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  // plugins: {
  //   legend: {
  //     display: false,
  //   },
  // },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: function (context) {
          const vote = votesStats.value[context.dataIndex]
          return `${vote.vote_count} صوت (${vote.percentage}%)`
        },
      },
    },
  },
  indexAxis: 'x',
  scales: {
    x: {
      // beginAtZero: true,
      // ticks: {
      //   callback: function (value) {
      //     console.log('value==================>', value)
      //     return value + ' صوت'
      //   },
      // },
    },
  },
}
</script>

<template>
  <ModalOverlay @close="closePopup()">
    <div class="container">
      <!-- Header -->
      <h2 style="color: red">نتائج التصويت</h2>
      <h2>
        <span class="mil-deg"> {{ degree }} / {{ userNamePer }}</span>
      </h2>

      <!-- <div class="chart-container">
        <Pie :data="chartData" />
      </div> -->
      <div class="voting-end" v-if="votingInfo.members_count == votingInfo.total_votes">
        <p>تم انتهاء التصويت</p>
      </div>
      <div class="chart-container">
        <Bar :data="chartData" :options="chartOptions" />
      </div>

      <!-- ===================== -->
      <!-- 🔥 STATISTICS -->
      <!-- ===================== -->
      <!-- <div class="stats">
        <div v-for="(vote, index) in votesStats" :key="index" class="stat-box">
          <div class="stat-title">{{ vote.vote_name }}</div>

          <div class="stat-numbers">{{ toAr(vote.vote_count) }} صوت</div>

          <div class="stat-percent">{{ toAr(vote.percentage) }}%</div>

          <div class="progress">
            <div class="progress-bar" :style="{ width: vote.percentage + '%' }"></div>
          </div>
        </div>
      </div> -->

      <!-- ===================== -->
      <!-- 👥 VOTERS -->
      <!-- ===================== -->
      <div class="votes-list">
        <div v-for="(vote, index) in votesStats" :key="index" class="vote-section">
          <h3>
            {{ vote.vote_name }} <span>({{ toAr(vote.vote_count) }})</span>
          </h3>

          <div class="voters">
            <div v-for="(voter, i) in vote.voters" :key="i" class="voter">
              {{ voter.rank }} / {{ voter.full_name }}
            </div>
          </div>
        </div>
      </div>

      <button @click="closePopup()" class="close-btn">رجوع</button>
    </div>
  </ModalOverlay>
</template>

<style scoped>
.container {
  background: #ffffff;
  padding: 25px;
  border-radius: 16px;
  width: 95%;
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
.voting-end {
  display: flex;
  align-items: center;
  justify-content: center;
}
.voting-end p {
  background: linear-gradient(135deg, #e63946, #d90429);
  color: #ffffff;
  font-family:
    'segoe UI',
    system-ui sans-serif;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 18px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(230, 57, 70, 0.4);
  border: 1px solid rgba(255, 255, 255, 0, 15);
  animation: alert-pulse-5c499b26 1s infinite ease-in-out;
  transform-origin: center;
  width: fit-content;
  text-align: center;
  margin: 30px 0;

  font-size: 25px;
}
/* .voting-end p {
} */
@keyframes alert-pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 4px 12p rgba(230, 57, 70, 0.4);
  }
  50% {
    transform: scale(1.04);
    box-shadow: 0 4px 20px rgba(230, 57, 70, 0.7);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 4px 12p rgba(230, 57, 70, 0.4);
  }
}
</style>
