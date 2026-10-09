<template>
  <div class="afrperson-container">
    <pageNavigation />

    <transition name="expand">
      <div class="white-box info-box" v-if="store.currentLagna">
        <div class="box-title-toggle-expand">
          <h2>{{ store.currentLagna.committe_name }}</h2>
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
            <span class="value">{{ store.currentLagna.committe_number }}</span>
          </div>

          <div class="info-item">
            <span class="label">التصنيف</span>
            <span class="value">{{ store.currentLagna.category?.category_name }}</span>
          </div>

          <div class="info-item">
            <span class="label">الحالة</span>
            <span
              class="status-badge"
              :class="store.currentLagna.committe_is_done ? 'done' : 'active'"
            >
              {{ store.currentLagna.committe_is_done ? 'تم الانتهاء' : 'جارى' }}
            </span>
          </div>

          <div class="info-item">
            <span class="label">تاريخ البدء</span>
            <span class="value">{{ store.currentLagna.committe_start_date }}</span>
          </div>

          <div class="info-item">
            <span class="label">تاريخ الانتهاء</span>
            <span class="value">{{ store.currentLagna.committe_end_date }}</span>
          </div>
        </div>
        <div class="lagna-actions">
          <div class="tabs">
            <button
              v-for="t in tabs"
              :key="t.key"
              :class="{ active: activeTab === t.key }"
              @click="changeLagnaPersonsType(t.key)"
            >
              {{ t.label }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- ===== Professional Action Panel ===== -->
    <div class="action-panel">
      <div class="panel-header" @click="panelOpen = !panelOpen">
        <h3>لوحة إجراءات اللجنة</h3>
        <i class="fa-solid fa-chevron-down" :class="{ rotate: panelOpen }"></i>
      </div>

      <transition name="expand">
        <div v-show="panelOpen" class="panel-body">
          <!-- Personal Data -->
          <div class="panel-section">
            <h4>البيانات الشخصية</h4>
            <div class="buttons-grid">
              <button @click="handleMessagePopup('photo')">الصور الشخصية</button>
              <button @click="handleMessagePopup('photo')">الصورة العائلية</button>
              <button @click="handleMessagePopup('units')">الوحدات</button>
              <button @click="handleMessagePopup('history')">تاريخ الترقي</button>
              <button @click="handleMessagePopup('education')">التأهيل</button>
              <button @click="handleMessagePopup('eff')">تقرير الكفاءة</button>
              <button @click="handleMessagePopup('sec_situation')">الموقف الامنى</button>
              <!-- <button @click="handleMessagePopup('travel')">السفر</button> -->
            </div>
          </div>

          <!-- Punishments -->
          <div class="panel-section">
            <h4>الجزاءات</h4>
            <div class="buttons-grid">
              <button @click="handleMessagePopup('punish')">مجمع</button>
              <button @click="handleMessagePopup('punish1')">حجز</button>
              <button @click="handleMessagePopup('punish2')">حبس</button>
              <button @click="handleMessagePopup('punish3')">محكمة</button>
              <button @click="handleMessagePopup('punish4')">محكمة مدنية</button>
            </div>
          </div>

          <!-- Relations -->
          <div class="panel-section">
            <h4>العلاقات</h4>
            <div class="buttons-grid">
              <button @click="handleMessagePopup('relation1,15')">الزوجة</button>
              <button @click="handleMessagePopup('relation2,7')">الأبناء</button>
              <button @click="handleMessagePopup('relation2')">ذكور</button>
              <button @click="handleMessagePopup('relation7')">إناث</button>
              <button @click="handleMessagePopup('shhh')">الأشقاء</button>
              <button @click="handleMessagePopup('shhh2')">الأقارب</button>
              <button @click="handleMessagePopup('prev_marrige')">الزيجات السابقة</button>
            </div>
          </div>

          <!-- Decisions -->
          <div class="panel-section">
            <h4>القرارات والتصويت</h4>
            <div class="buttons-grid">
              <button @click="handleMessagePopup('opinion')">الآراء</button>
              <button @click="handleMessagePopup('start_voting')">فتح التصويت</button>
              <button @click="handleMessagePopup('reset')">إعادة التصويت</button>
              <button @click="handleMessagePopup('poea')">الالتماس</button>
              <button @click="handleMessagePopup('reason')">أسباب</button>
              <button @click="handleMessagePopup('a_op_reasons')">أسباب السلاح</button>
              <button @click="handleMessagePopup('u_op_reasons')">أسباب التشكيل</button>
              <button @click="handleMessagePopup('hayaa')">رأي هيئة التنظيم</button>
              <button @click="handleMessagePopup('end')">رجوع الجميع</button>
              <button @click="handleMessagePopup('close')">شاشة الانتظار</button>
              <button @click="handleMessagePopup('refresh')">تحديث الصفحات</button>
              <button @click="handleMessagePopup('clear_cache')">مسح الكاش</button>
            </div>
          </div>

          <!-- Reports -->
          <div class="panel-section">
            <h4>التقارير</h4>
            <div class="buttons-grid">
              <button @click="openreport()">حضور اللجنة</button>
              <button @click="handleMessagePopup('inspire_work')">تقرير العمل النفسى</button>
              <button @click="handleMessagePopup('voting')">تقرير نتيجة التصويت</button>
              <button @click="handleMessagePopup('comm_report')">تقرير</button>
              <button @click="openreportImagePopup()">صور الأفراد</button>
            </div>
          </div>
        </div>
      </transition>
    </div>
    <!-- ===== Persons / Judgments ===== -->
    <LagnaPersons
      v-if="activeTab"
      :committeCode="committe_code"
      :spacificId="activeTab"
      :addAction="false"
      :rowClick="true"
      :deleteAction="false"
      :updateAction="false"
      :actionsColumn="false"
      :tableColumns="columns"
      @handleRowClick="handleRowClick"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useLagnaStore } from '@/stores/lagna'
import { useRouter, useRoute } from 'vue-router'
import LagnaPersons from '@/components/mainAdmin/lagna/LagnaPersons.vue'
import pageNavigation from '@/components/global/pageNavigation.vue'
import swal from 'sweetalert'
import { h } from 'vue'

const store = useLagnaStore()
const router = useRouter()
const route = useRoute()

const committe_code = computed(() => Number(route.query.committe_code))
console.log('llllllllllllllllllllllllllllllllllllllllllllllllll', route.query.committe_code)
console.log('lllllllllllllllllllll00000000000lll', committe_code.value)

const tabs = computed(() =>
  store.currentLagna?.lagna_types.map((item) => ({
    key: item.lagna_type_id,
    label: item.lagna_type_name,
  })),
)

/* ================= STATE ================= */
const currentPersonId = ref()
console.log('store.currentLagna', store.currentLagna)
const activeTab = ref(null)
console.log('activeTabactiveTabactiveTabactiveTab', activeTab.value)
const infoExpanded = ref(true)

const columns = computed(() => [
  {
    key: 'mil_no',
    value: (row) => row.person.mil_no,
    label: 'الرقم العسكري',
    sortable: true,
    rowClickable: true,
    mark: (row, index, isTotal) => row.person_id == currentPersonId.value,
  },
  {
    key: 'degree_name',
    value: (row) => row.person.degree_name,
    label: 'الدرجة',
    sortable: true,
    rowClickable: true,
    mark: (row, index, isTotal) => row.person_id == currentPersonId.value,
  },
  {
    key: 'person_name',
    value: (row) => row.person.person_name,
    label: 'الاسم',
    sortable: true,
    rowClickable: true,
    mark: (row, index, isTotal) => row.person_id == currentPersonId.value,
  },
  {
    key: 'unit_name',
    value: (row) => row.person.unit_name,
    label: 'الوحدة',
    sortable: true,
    rowClickable: true,
    mark: (row, index, isTotal) => row.person_id == currentPersonId.value,
  },
  {
    key: 'army_name',
    value: (row) => row.person.army_name,
    label: 'السلاح',
    sortable: true,
    rowClickable: true,
    mark: (row, index, isTotal) => row.person_id == currentPersonId.value,
  },
  {
    key: 'prnt_army_name',
    value: (row) => row.person.prnt_army_name,
    label: 'التبعية',
    sortable: true,
    rowClickable: true,
    mark: (row, index, isTotal) => row.person_id == currentPersonId.value,
  },
  {
    key: 'attendance',
    onClick: (row) => updateStatus(row, 50),
    render: (row) =>
      h(
        'input',
        {
          // class: row.mil_ser.photos.length > 0 ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark',
          style: {
            background: '#e7c80a',
            fontSize: '19px',
            cursor: 'pointer',
            padding: '5px 15px',
            color: 'white',
            borderRadius: '15px',
          },
          type: 'checkbox',
        },
        'حضور',
      ),
    notRowClick: true,
    // value : row => row.committe_status_code,
    label: 'حضور',
  },
  {
    key: 'getLagna',
    onClick: (row) => updateStatus(row, 70),
    render: (row) =>
      h(
        'input',
        {
          // class: row.mil_ser.photos.length > 0 ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark',
          style: {
            background: '#e7c80a',
            fontSize: '19px',
            cursor: 'pointer',
            padding: '5px 15px',
            color: 'white',
            borderRadius: '15px',
          },
          type: 'checkbox',
        },
        'مثول امام اللجنة',
      ),
    notRowClick: true,
    // value : row => row.committe_status_code,
    label: 'مثول امام اللجنة',
  },
  {
    key: 'takeScreen',
    onClick: (row) => handleMessagePopup('takeScreen'),
    render: (row) =>
      h(
        'button',
        {
          // class: row.mil_ser.photos.length > 0 ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark',
          style: {
            background: '#e7c80a',
            fontSize: '19px',
            cursor: 'pointer',
            padding: '5px 15px',
            color: 'white',
            borderRadius: '15px',
          },
        },
        'طباعة',
      ),
    // value : row => row.committe_status_code,
    label: 'طباعة صورة',
  },
])
/* ================= ACTIONS ================= */
async function changeLagnaPersonsType(lagnaType) {
  activeTab.value = lagnaType
  await store.fetchSpecificCommittPersons(committe_code.value, activeTab.value)
}

const panelOpen = ref(true)

function openreport() {
  console.log('Open attendance report')
}

function openreportImagePopup() {
  console.log('Open images report')
}

async function updateStatus(row, new_status) {
  console.log('add new review person', row)
  try {
    let res = await store.changeLagnaSpecificsPersonStutus(
      committe_code.value,
      activeTab.value,
      row.person_id,
      { new_status: new_status },
    )
  } catch (error) {
    console.log('errrrrr', error.status)
  }
}

async function handleRowClick(row) {
  try {
    console.log('persos================>', row)
    currentPersonId.value = row.person_id
    const res = await store.fetchLagnaSpecificsPersonShow(
      committe_code.value,
      activeTab.value,
      row.person_id,
    )

    if (res) {
      swal({
        title: 'تم تحميل بيانات الفرد بنجاح',
        text: `تم عرض - ${row.person.person_name}`,
        icon: 'success',
        button: false,
        timer: 1000,
      })
    } else {
      swal({
        title: 'لا توجد بيانات متاحة',
        text: ` برجاء مراجعة - ${row.person.person_name}`,
        icon: 'warning',
        button: false,
        timer: 1000,
      })
    }
  } catch (error) {
    console.error(error)
    swal({
      title: 'حدث خطأ أثناء تحميل البيانات',
      // text: ` برجاء مراجعة - ${row.person_name}`,
      icon: 'error',
      button: false,
      timer: 1500,
    })
  }
}

async function handleMessagePopup(event) {
  try {
    console.log('operation', event)
    const res = await store.fetchLagnaSpecificsPersonPopupShow(
      committe_code.value,
      activeTab.value,
      {
        operation: event,
        spacific_code: activeTab.value,
      },
    )

    if (res) {
      swal({
        title: 'تم تحميل بيانات الفرد بنجاح',
        text: `تم العرض `,
        icon: 'success',
        button: false,
        timer: 1000,
      })
    } else {
      swal({
        title: 'لا توجد بيانات متاحة',
        text: `برجاء مراجعة `,
        icon: 'warning',
        button: false,
        timer: 1000,
      })
    }
  } catch (error) {
    console.error(error)
    swal({
      title: 'حدث خطأ أثناء تحميل البيانات',
      // text: ` برجاء مراجعة - ${row.person_name}`,
      icon: 'error',
      button: false,
      timer: 1500,
    })
  }
}
onMounted(async () => {
  await store.fetchCommittSpecifics(committe_code.value)
  await store.getCommittByCode(committe_code.value)
  await store.fetchcommittCategory()
  await store.fetchcommittTypes()
  console.log('lagnaCategory', store.specificLagnas)
})

watch(
  () => store.currentLagna,
  (lagna) => {
    if (!lagna || !lagna.lagna_types?.length) return

    activeTab.value = lagna.lagna_types[0].lagna_type_id
    console.log('activeTab.value', activeTab.value)
  },
  { immediate: true },
)

watch(
  () => route.query.committe_code,
  async (code) => {
    if (!code) return

    await store.getCommittByCode(Number(code))
  },
  { immediate: true },
)
</script>

<style scoped>
.white-box {
  width: 100%;
  max-width: 100%;
  margin: auto;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}
.table-actions {
  padding-bottom: 30px;
  display: flex;
  align-items: end;
  justify-content: end;
}
.action-btns {
  display: flex;
  gap: 5px;
  justify-content: flex-end;
}
.action-btn {
  cursor: pointer;
  color: white;
  font-size: 16px;
  padding: 10px 20px;
  border-radius: 10px;
  height: fit-content;
  width: max-content;
}
.action-btn.upload p,
.action-btn.cardShow p {
  display: flex;
  margin: 0;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.action-btn.upload {
  background: var(--primary-color);
}
.action-btn.upload:hover {
  background: var(--hover-primary-color);
}
.action-btn.cardShow {
  background: var(--success-color);
}
.action-btn.cardShow:hover {
  background: var(--success-hover-color);
}
.action-btn.edit {
  background: var(--success-color);
}
.action-btn.delete {
  background: var(--danger-color);
}

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

/* ===== Action Panel ===== */
.action-panel {
  margin: 20px 0;
  background: white;
  border-radius: 16px;
  padding: 18px 22px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;

  position: sticky;
  top: 92px;
  z-index: 55;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  color: var(--primary-color);
  font-weight: 600;
}

.panel-header i {
  transition: 0.3s ease;
}

.panel-header i.rotate {
  transform: rotate(180deg);
}

.panel-body {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}
.panel-section {
  margin-top: 25px;
}

.panel-section h4 {
  margin-bottom: 12px;
  font-size: 15px;
  color: #444;
  border-bottom: 1px solid #eee;
  padding-bottom: 6px;
}

.buttons-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.buttons-grid button {
  padding: 7px 14px;
  border-radius: 18px;
  border: none;
  font-size: 13px;
  cursor: pointer;
  background: #f1f3f5;
  color: #333;
  transition: 0.2s ease;
}

.buttons-grid button:hover {
  background: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}
</style>
