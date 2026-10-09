<script setup>
import { ref, onMounted } from 'vue'
import { convertToArabicNumbers } from '@/utils/glopal'
import ModalOverlay from '../ModalOverlay.vue'

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
})

/* Emits */
const emit = defineEmits(['close'])

/* State (data) */
const pea = ref('hamza')

/* Lifecycle */
onMounted(() => {
  // Mounted logic if needed
})

/* Methods */
function toAr(number) {
  return convertToArabicNumbers(number)
}

function closePopup() {
  emit('close')
}
</script>
<template>
  <ModalOverlay @close="closePopup()">
    <div class="container">
      <!-- Header -->
      <h2>
        <span class="mil-deg"> {{ degree }} / </span> {{ userNamePer }}
      </h2>

      <!-- Content -->
      <div class="content">
        <!-- Empty -->
        <div v-if="!tableData || tableData.length === 0" class="empty">لا يوجد بيانات</div>

        <!-- Records -->
        <div v-else class="cards">
          <div v-for="(item, index) in tableData" :key="item.secu_id" class="card">
            <!-- Top -->
            <!-- <div class="card-header">
              <span class="index">
                {{ toAr(index + 1) }}
              </span>

              <span class="date">
                {{ toAr(item.create_date) }}
              </span>
            </div> -->

            <!-- Notes -->
            <div class="notes">
              <span v-if="item.notes">
                {{ item.notes }}
              </span>
              <span v-else class="no-notes"> لا يوجد ملاحظات </span>
            </div>

            <!-- Status -->
            <!-- <div class="status">
              <span :class="item.active_flag ? 'active' : 'inactive'">
                {{ item.active_flag ? 'نشط' : 'غير نشط' }}
              </span>
            </div> -->
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="footer">
        <button @click="closePopup()" class="close-btn">رجوع</button>
      </div>
    </div>
  </ModalOverlay>
</template>
<style scoped>
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
/* HEADER */
.header {
  text-align: center;
  margin-bottom: 15px;
}

.divider {
  margin: 0 5px;
  color: #aaa;
}

/* CONTENT */
.content {
  flex: 1;
  overflow-y: auto;
  margin-top: 50px;
}

/* EMPTY */
.empty {
  text-align: center;
  padding: 40px;
  color: #888;
  font-size: 18px;
}

/* CARDS */
.cards {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card {
  background: #f7f9fc;
  border-radius: 12px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  transition: 0.2s;
}

/* .card:hover {
  transform: translateY(-2px);
  background: #eef4ff;
} */

/* HEADER */
.card-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
  margin-bottom: 10px;
}

/* NOTES */
.notes {
  font-size: 14px;
  margin-bottom: 10px;
  line-height: 1.6;
}

.no-notes {
  color: #aaa;
  font-style: italic;
}

/* STATUS */
.status {
  text-align: right;
}

.active {
  color: #2e7d32;
  font-weight: bold;
}

.inactive {
  color: #c62828;
  font-weight: bold;
}

/* FOOTER */
.footer {
  display: flex;
  justify-content: center;
  margin-top: 15px;
}
</style>
