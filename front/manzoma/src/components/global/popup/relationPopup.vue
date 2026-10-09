<script setup>
import { convertToArabicNumbers } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'
import { onMounted } from 'vue'

/* Props */
const props = defineProps({
  tableData: {
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
  type: {
    type: String,
    default: '',
  },
  jobFlag: {
    type: Boolean,
    default: false,
  },
  appearYears: {
    type: Boolean,
    default: false,
  },
})

/* Emits */
const emit = defineEmits(['close'])

/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number)
}

function closeRelationPopup() {
  emit('close')
}
onMounted(() => {
  console.log('tableData', props.tableData)
})
</script>

<template>
  <ModalOverlay @close="closeRelationPopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ degree }} / </span>{{ userNamePer }}
      </h2>
      <div v-if="tableData.length > 0" class="tableContaine">
        <table>
          <thead style="background-color: rgb(180, 180, 180)">
            <tr>
              <th rowspan="2">م</th>
              <th rowspan="2">الاسم</th>
              <th>القرابة</th>
              <th v-if="appearYears">السن</th>
              <th>{{ jobFlag ? 'المؤهل/الوظيفة/الحالة الاجتماعية' : 'المؤهل/الوظيفة' }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pun, index) in tableData" :key="index">
              <td>{{ toAr(`${index + 1}`) }}</td>
              <td style="white-space: nowrap">{{ pun.per_name }}</td>
              <td>{{ pun.relation_degree_name }}</td>
              <td style="white-space: nowrap" v-if="appearYears">
                {{
                  `${pun.birth_month == 0 ? '' : ` ${toAr(`${pun.birth_month || '---'}`)} شهر `} ${pun.birth_year == 0 ? '' : ` ${pun.birth_month == 0 ? '' : '/'}  `} ${pun.birth_year == 0 ? '' : `${toAr(`${pun.birth_year || '---'} سنه`)}`}`
                }}
              </td>
              <td>
                {{ pun.notes }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h1 v-else style="text-align: center">لا يوجد</h1>

      <button @click="closeRelationPopup()" class="close-btn">رجوع</button>
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
.tableContaine {
  /* height: 423px; */
  overflow-y: auto;
}
.tableContaine::-webkit-scrollbar-thumb {
  width: 10px;
  height: 30px;
  background-color: rgb(19, 14, 14);
}
.tableContaine::-webkit-scrollbar {
  width: 10px;
  background-color: rgba(139, 138, 138, 0.418);
}
thead {
  background: white;
  position: sticky;
  top: 0px;
}
</style>
