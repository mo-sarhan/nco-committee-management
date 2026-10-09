<script setup>
import { convertToArabicNumbers } from '@/utils/glopal'
import { computed } from 'vue'
import ModalOverlay from '../ModalOverlay.vue'

/* Props */
const props = defineProps({
  tableData: {
    type: Array,
    default: () => [],
  },
  userNamePer: String,
  degree: String,
})

/* Emits */
const emit = defineEmits(['close'])

function closeCourtPopup() {
  emit('close')
}

function toAr(val) {
  if (val === null || val === undefined) return '---'
  return convertToArabicNumbers(val)
}

/* ===== تقسيم العقوبات ===== */

const habsCodes = [4, 17, 18, 19, 26, 29]

const groupedPunishments = computed(() => {
  const groups = {
    habs: [],
    hagz: [],
    military: [],
    civil: [],
  }

  props.tableData.forEach((p) => {
    const code = parseInt(p.punishment_code)

    if (p.punsh_cort_code == 1) {
      if (habsCodes.includes(code)) {
        groups.habs.forEach((p) => {
          p['appear_period'] = true
        })
        groups.habs.push(p)
        console.log('groups.habs', groups.habs)
      } else {
        groups.hagz.push(p)
      }
    } else if (p.punsh_cort_code == 2) {
      groups.military.push(p)
    } else if (p.punsh_cort_code == 3) {
      groups.civil.push(p)
    }
  })

  return groups
})

/* ===== ترتيب العقوبات ===== */

function sortPunishments(arr) {
  return [...arr].sort((a, b) => new Date(b.punish_start_date) - new Date(a.punish_start_date))
}

/* ===== جدول الأنواع ===== */

const tables = computed(() => [
  { title: 'حجز', appear_period: false, rows: sortPunishments(groupedPunishments.value.hagz) },
  { title: 'حبس', appear_period: true, rows: sortPunishments(groupedPunishments.value.habs) },
  {
    title: 'محاكم عسكرية',
    appear_period: true,
    rows: sortPunishments(groupedPunishments.value.military),
  },
  {
    title: 'محاكم مدنية',
    appear_period: true,
    rows: sortPunishments(groupedPunishments.value.civil),
  },
])
</script>

<template>
  <ModalOverlay @close="closeCourtPopup">
    <div class="container">
      <h2>
        <span class="mil-deg">{{ degree }} / </span>
        {{ userNamePer }}
      </h2>

      <div v-if="tableData.length" class="tableContainer">
        <div v-for="table in tables" :key="table.title" class="court-section">
          <h3 v-if="table.rows.length">{{ table.title }}</h3>
          <table v-if="table.rows.length">
            <thead>
              <tr>
                <th>م</th>
                <!-- <th>المادة</th> -->
                <th style="width: 250px">نص الماده</th>
                <th>النــوع</th>
                <th v-if="table.appear_period">مدة الغياب</th>
                <th>العقوبة</th>
                <th>مدة العقوبة</th>
                <th>من</th>
                <th>الي</th>
                <th>الجريمة</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(pun, index) in table.rows" :key="index">
                <td>{{ toAr(index + 1) }}</td>

                <!-- <td>{{ pun.low_part_no || "---" }}</td> -->
                <td>
                  <span style="color: #d40000">{{ pun.low_part_no }}</span
                  >{{ ' / ' + pun.crime_name }}
                </td>

                <td>{{ pun.punsh_cort || '---' }}</td>

                <td v-if="table.appear_period">
                  {{ toAr(pun.crime_period) }}
                  <span v-if="pun.crime_period"> يوم </span>
                </td>

                <td class="nowrap">
                  {{ pun.punishment_name || '---' }}
                </td>

                <td>
                  {{ toAr(pun.punish_period) }} {{ toAr(pun.punish_period_type) }}
                  <!-- <span v-if="pun.period_year">
                      {{ toAr(pun.period_year) }} سنة
                    </span>
  
                    <span v-if="pun.period_month">
                      {{ toAr(pun.period_month) }} شهر
                    </span>
  
                    <span v-if="pun.period_day">
                      {{ toAr(pun.period_day) }} يوم
                    </span> -->

                  <span v-if="!pun.period_year && !pun.period_month && !pun.period_day"> --- </span>
                </td>
                <td class="nowrap">
                  {{ toAr(pun.punish_start_date) }}
                </td>

                <td class="nowrap">
                  {{ toAr(pun.punish_end_date) }}
                </td>

                <td>{{ pun.notes || '---' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <h1 v-else class="empty">لا يكن</h1>

      <button @click="closeCourtPopup" class="close-btn">رجوع</button>
    </div>
  </ModalOverlay>
</template>

<style scoped>
/* .container{
  width:110vh;
  background:#f9f9f9f0;
  max-height:90vh;
  padding:25px 50px;
  border-radius:20px;
  margin:0 20px;
} */

.container h2 {
  text-align: center;
  margin-bottom: 20px;
}

.tableContainer {
  max-height: 65vh;
  overflow: auto;
}

.court-section {
  margin-bottom: 30px;
}

.court-section h3 {
  margin: 10px 0;
  background: #e5e5e5;
  padding: 8px;
  border-radius: 8px;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  position: sticky;
  top: 0;
  background: #b4b4b4;
}

th,
td {
  padding: 6px 8px;
  border: 1px solid #ccc;
  text-align: center;
}

.nowrap {
  white-space: nowrap;
}

.empty {
  text-align: center;
}

.tableContainer::-webkit-scrollbar {
  width: 10px;
}

.tableContainer::-webkit-scrollbar-thumb {
  background: #333;
}
</style>
