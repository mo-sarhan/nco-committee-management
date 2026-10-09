<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { convertToArabicNumbers, getWsUrl } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'
import BaseTable from '@/components/global/dataTable/BaseTable.vue'
/* Props */
const props = defineProps({
  tableFields: {
    type: Object,
    default: '',
  },
  mainLagnaName: {
    type: String,
    default: '',
  },
  lagnaNameType: {
    type: String,
    default: '',
  },
  stikyHeader: Boolean,
})
const tableData = ref([])
const activeTab = ref('by_person_army')
/* Emits */
const emit = defineEmits(['close'])

// function getFileUrl(path) {
//   return getWsUrl(path)
// }
/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number)
}

function closeReportPopup() {
  emit('close')
}

function getFileUrl(file) {
  // adjust for your backend path
  const base = import.meta.env.VITE_MEDIA_BASE_URL
  console.log(base)
  return `${base}${file}`
}

onMounted(() => {
  tableData.value = props.tableFields.reportData
  console.log('tableFields', props.tableFields)
  console.log(
    'tableFields.tabs.find((tab) => tab.key === activeTab).columns',
    props.tableFields.tabs.find((tab) => tab.key === activeTab),
  )
  console.log('army_report', tableData.value)
})
</script>

<template>
  <ModalOverlay @close="closeReportPopup()">
    <div class="container">
      <h2>
        <span class="mil-deg"> {{ mainLagnaName }} / </span> {{ lagnaNameType }}
      </h2>
      <div class="lagna-actions" v-if="tableFields.tabs.length">
        <div class="tabs">
          <button
            v-for="t in tableFields.tabs"
            :key="t.key"
            :class="{ active: activeTab === t.key }"
            @click="activeTab = t.key"
          >
            {{ t.label }}
          </button>
        </div>
      </div>
      <!-- <table v-if="tableData">
        <thead style="background-color: rgb(180, 180, 180)">
          <tr>
            <th>م</th>
            <th v-for="heading in tableFields.tabs.find((tab) => tab.key === activeTab).columns">
              {{ heading.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in tableData[activeTab]" :key="index">
            <td>{{ index + 1 }}</td>
            <td
              v-for="heading in tableFields.tabs.find((tab) => tab.key === activeTab).columns"
              :rowspan="heading.RowsMerge"
              :colspan="heading.ColsMerge"
            >
              {{ row[heading.key] }}
            </td>
          </tr>
        </tbody>
      </table> -->
      <div class="white-box white-box-custom">
        <BaseTable
          v-if="tableData"
          :rows="tableData[activeTab]"
          :columns="tableFields.tabs.find((tab) => tab.key === activeTab).columns"
          :totalRows="true"
          :stikyHeader="stikyHeader"
        >
        </BaseTable>
        <h1 v-else style="text-align: center">لا يوجد</h1>
      </div>
      <button @click="closeReportPopup()" class="close-btn">رجوع</button>
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
  width: 100%;
  background-color: #f9f9f9f0;
  max-height: 100%;
  padding: 3px 10px;
  border-radius: 20px;
  margin: 0px 0px;
  height: 100%;
  /* overflow: auto; */
  min-width: 100%;
}
.container h2 {
  text-align: center;
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
.white-box-custom {
  max-height: 600px;
  overflow: scroll;
  padding: 0px;
}
.lagna-actions {
  margin-top: 25px;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  gap: 12px;
  background: #f1f1f1;
  padding: 6px;
  border-radius: 30px;
}

.tabs button {
  padding: 10px 26px;
  border-radius: 25px;
  background: transparent;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s ease;
}

.tabs button:hover {
  background: rgba(0, 0, 0, 0.05);
}

.tabs button.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
}
</style>
