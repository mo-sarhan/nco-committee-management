<template>
  <div class="afrperson-container">
    <pageNavigation />

    <!-- ===== Lagna Main Info ===== -->

    <transition name="expand">
      <div
        class="white-box info-box"
        v-if="lagnaStore.currentLagna && lagnaStore.currentSpecificLagna"
      >
        <div class="box-title-toggle-expand">
          <h2>{{ lagnaStore.currentLagna.committe_name }}</h2>
          <div class="info-toggle" @click="infoExpanded = !infoExpanded">
            <span>
              {{ infoExpanded ? 'إخفاء التفاصيل' : 'عرض التفاصيل' }}
            </span>
            <i class="fa-solid fa-chevron-down" :class="{ rotate: infoExpanded }"></i>
          </div>
        </div>

        <div class="info-grid" v-show="infoExpanded">
          <div class="info-item">
            <span class="label">رقم اللجنة</span>
            <span class="value">{{ lagnaStore.currentLagna.committe_number }}</span>
          </div>

          <div class="info-item">
            <span class="label">النوع</span>
            <span class="value">{{ lagnaStore.currentSpecificLagna?.lagna_type_name }}</span>
          </div>

          <div class="info-item">
            <span class="label">التصنيف</span>
            <span class="value">{{ lagnaStore.currentLagna.category?.category_name }}</span>
          </div>

          <div class="info-item">
            <span class="label">الحالة</span>
            <span
              class="status-badge"
              :class="lagnaStore.currentLagna.committe_is_done ? 'done' : 'active'"
            >
              {{ lagnaStore.currentLagna.committe_is_done ? 'تم الانتهاء' : 'جارى' }}
            </span>
          </div>

          <div class="info-item">
            <span class="label">تاريخ البدء</span>
            <span class="value">{{ lagnaStore.currentSpecificLagna?.start_date }}</span>
          </div>

          <div class="info-item">
            <span class="label">تاريخ الانتهاء</span>
            <span class="value">{{ lagnaStore.currentSpecificLagna?.end_date }}</span>
          </div>
        </div>
        <div class="lagna-counters">
          <div class="counter-card">
            <div class="counter-icon persons">
              <i class="fa-solid fa-user"></i>
            </div>
            <div class="counter-info">
              <span class="counter-value">{{ lagnaStore.lagnaPersonsPagination.total }}</span>
              <span class="counter-label">عدد الأفراد</span>
            </div>
          </div>

          <div class="counter-card">
            <div class="counter-icon members">
              <i class="fa-solid fa-users"></i>
            </div>
            <div class="counter-info">
              <span class="counter-value">{{ lagnaStore.lagnaMembersPagination.total }}</span>
              <span class="counter-label">عدد الأعضاء</span>
            </div>
          </div>
        </div>
        <div class="lagna-actions">
          <div class="tabs">
            <button
              v-for="t in tabs"
              :key="t.key"
              :class="{ active: activeTab === t.key }"
              @click="activeTab = t.key"
            >
              {{ t.label }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- ===== Tabs ===== -->
    <!-- <div class="white-box"> -->

    <!-- ===== Members ===== -->
    <LagnaMembers
      v-if="activeTab === 'members'"
      :committeCode="committe_code"
      :spacificId="spacific_id"
    />

    <!-- ===== Persons / Judgments ===== -->
    <LagnaPersons
      v-if="activeTab === 'persons'"
      :committeCode="committe_code"
      :spacificId="spacific_id"
    />
    <!-- </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useLagnaStore } from '@/stores/lagna'

import pageNavigation from '@/components/global/pageNavigation.vue'
import LagnaMembers from '@/components/mainAdmin/lagna/LagnaMembers.vue'
import LagnaPersons from '@/components/mainAdmin/lagna/LagnaPersons.vue'

const lagnaStore = useLagnaStore()
const route = useRoute()

const committe_code = Number(route.params.committe_code)
const spacific_id = Number(route.params.spacific_id)

const infoExpanded = ref(true)
const activeTab = ref('persons')

const tabs = [
  { key: 'persons', label: 'أفراد اللجنة' },
  { key: 'members', label: 'أعضاء اللجنة' },
]

onMounted(async () => {
  await lagnaStore.fetchOneCommittSpecific(committe_code, spacific_id)
  await lagnaStore.getCommittByCode(committe_code)
  await lagnaStore.fetchSpecificCommittMembers(committe_code, spacific_id, {})
  await lagnaStore.fetchSpecificCommittPersons(committe_code, spacific_id)
})
</script>

<style scoped>
.info-box {
  margin-bottom: 15px;
  padding: 20px 25px;
  border-radius: 14px;
  background: linear-gradient(180deg, #ffffff, #f9f9f9);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
}

/* ===== Header ===== */
.info-box h2 {
  display: inline-block;
  margin-bottom: 20px;
  padding: 8px 18px;
  font-size: 20px;
  font-weight: bold;
  background: var(--primary-color);
  color: white;
  border-radius: 30px;
}

/* ===== Info Grid ===== */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 15px;
}

/* ===== Info Item ===== */
.info-item {
  background: white;
  padding: 5px 10px;
  border-radius: 12px;
  border: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: 0.2s ease;
}

.info-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.info-item .label {
  font-size: 13px;
  color: #888;
}

.info-item .value {
  font-size: 16px;
  font-weight: 600;
  color: #222;
}

/* ===== Status Badge ===== */
.status-badge {
  width: fit-content;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
}

.status-badge.done {
  background: rgba(40, 167, 69, 0.15);
  color: #28a745;
}

.status-badge.active {
  background: rgba(255, 193, 7, 0.2);
  color: #d39e00;
}

/* ===== Tabs Area ===== */
.lagna-actions {
  margin-top: 25px;
  display: flex;
  justify-content: center;
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

/* ----------------------------------------------------------------------------------------------- */
.lagna-counters {
  display: flex;
  gap: 15px;
  margin: 15px 0 20px;
  flex-wrap: wrap;
}

.counter-card {
  flex: 1;
  min-width: 200px;
  background: white;
  border-radius: 14px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid #eee;
  transition: 0.2s ease;
}

.counter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

/* Icon */
.counter-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.counter-icon.members {
  background: rgba(0, 123, 255, 0.15);
  color: #007bff;
}

.counter-icon.persons {
  background: rgba(40, 167, 69, 0.15);
  color: #28a745;
}

.box-title-toggle-expand {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
/* Text */
.counter-info {
  display: flex;
  flex-direction: column;
}

.counter-value {
  font-size: 22px;
  font-weight: bold;
  color: #222;
}

.counter-label {
  font-size: 13px;
  color: #777;
}

.info-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  color: var(--primary-color);
  font-weight: 500;
  margin-bottom: 10px;
}

.info-toggle i {
  transition: transform 0.3s ease;
}

.info-toggle i.rotate {
  transform: rotate(180deg);
}

/* ===== Expand Animation ===== */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.35s ease;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
