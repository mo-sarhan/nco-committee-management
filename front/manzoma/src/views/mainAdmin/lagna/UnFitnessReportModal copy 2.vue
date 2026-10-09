<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">

      <div v-if="loading" class="loading-overlay">
        جاري التحميل...
      </div>

      <!-- Header -->
      <div class="modal-header">
        <h2>تقرير عرض لجنة (عدم الصلاحية)</h2>
      </div>

      <form @submit.prevent="submitForm">

        <!-- ================= BASIC DATA ================= -->
        <div class="section">
          <div class="section-title">البيانات الأساسية عن ضابط الصف</div>

          <div class="grid-2">
            <div class="field"><label>الرقم العسكري</label><div class="display-value">{{ form.military_no }}</div></div>
            <div class="field"><label>الدرجة</label><div class="display-value">{{ form.degree }}</div></div>
            <div class="field"><label>الاسم</label><div class="display-value">{{ form.name }}</div></div>
            <div class="field"><label>السلاح</label><div class="display-value">{{ form.weapon }}</div></div>
            <div class="field"><label>الوحدة</label><div class="display-value">{{ form.unit }}</div></div>
            <div class="field"><label>تاريخ الضم</label><div class="display-value">{{ form.to_unit_date }}</div></div>
          </div>
        </div>

        <!-- ================= RECORDS ================= -->
        <div class="section">
          <div class="action-header">
            <div class="section-title">العروض</div>

            <div
              v-if="!hasNewRecord"
              class="action-btn"
              @click="createNewRecord"
            >
              + إضافة عرض جديد
            </div>
          </div>

          <div
            v-for="(record, rIndex) in form.records"
            :key="rIndex"
            class="dynamic-box"
          >
            <div class="row-header" @click="toggleRecord(rIndex)">
              <div>
                عرض رقم {{ rIndex + 1 }}
                <span v-if="record.isOld" class="old-badge">(عرض سابق)</span>
              </div>
            </div>

            <transition name="fade">
              <div v-show="record.open" class="row-body">

                <!-- ================= PROS CONS ================= -->
                <div
                  v-for="(item, index) in record.pros_cons_list"
                  :key="index"
                  class="inner-box"
                >
                  <div class="grid-2">

                    <div class="field">
                      <label>النوع</label>

                      <div v-if="record.isOld" class="display-value">
                        {{ item.type === 'pros' ? 'إيجابية' : 'سلبية' }}
                      </div>

                      <select v-else v-model="item.type">
                        <option value="pros">إيجابية</option>
                        <option value="cons">سلبية</option>
                      </select>
                    </div>

                    <div class="field">
                      <label>التصنيف</label>

                      <div v-if="record.isOld" class="display-value">
                        {{ getCategoryName(item.category) }}
                      </div>

                      <select v-else v-model="item.category">
                        <option
                          v-for="type in pros_cons_Array"
                          :key="type.photo_type_code"
                          :value="type.photo_type_code"
                        >
                          {{ type.photo_type_name }}
                        </option>
                      </select>
                    </div>

                    <div class="field full-width">
                      <label>الملاحظات</label>

                      <div v-if="record.isOld" class="display-value">
                        {{ item.notes }}
                      </div>

                      <textarea
                        v-else
                        v-model="item.notes"
                      ></textarea>
                    </div>

                  </div>

                  <button
                    v-if="!record.isOld && record.pros_cons_list.length > 1"
                    type="button"
                    class="remove-btn"
                    @click="removeProsCons(rIndex, index)"
                  >
                    حذف
                  </button>
                </div>

                <button
                  v-if="!record.isOld"
                  type="button"
                  class="btn btn-secondary mt-10"
                  @click="addProsCons(rIndex)"
                >
                  + إضافة ملاحظة
                </button>

                <!-- ================= SERVICE STATUS ================= -->
                <div class="section-title mt-20">مدى جدوى استمراره</div>

                <div v-if="record.isOld" class="display-value">
                  {{ record.service_status === 'useful'
                    ? 'يعود بالنفع'
                    : 'لا يعود بالنفع'
                  }}
                </div>

                <div v-else class="radio-group">
                  <label>
                    <input type="radio" value="useful" v-model="record.service_status"/>
                    يعود بالنفع
                  </label>
                  <label>
                    <input type="radio" value="not_useful" v-model="record.service_status"/>
                    لا يعود بالنفع
                  </label>
                </div>

                <!-- ================= COMMANDER INFO ================= -->
                <div class="section-title mt-20">بيانات قائد الوحدة</div>

                <div class="grid-2">

                  <div class="field">
                    <label>الرتبة</label>

                    <div v-if="record.isOld" class="display-value">
                      {{ record.commander_rank }}
                    </div>

                    <select v-else v-model="record.commander_rank">
                      <option value="">اختر الرتبة</option>
                      <option v-for="rank in rankOptions" :key="rank" :value="rank">
                        {{ rank }}
                      </option>
                    </select>
                  </div>

                  <div class="field">
                    <label>اسم قائد الوحدة</label>

                    <div v-if="record.isOld" class="display-value">
                      {{ record.commander_name }}
                    </div>

                    <input v-else v-model="record.commander_name" />
                  </div>

                  <div class="field">
                    <label>رقم تليفون القائد / CDM</label>

                    <div v-if="record.isOld" class="display-value">
                      {{ record.commander_phone }}
                    </div>

                    <input v-else v-model="record.commander_phone" />
                  </div>

                </div>

                <!-- ================= OPINIONS ================= -->
                <div class="section-title mt-20">الآراء</div>

                <div
                  v-for="(opinion, index) in record.opinions"
                  :key="index"
                  class="inner-box"
                >
                  <div class="field">
                    <label>نوع الرأي</label>

                    <div v-if="record.isOld" class="display-value">
                      {{ opinion.opinion_type }}
                    </div>

                    <select v-else v-model="opinion.opinion_type">
                      <option value="direct_commander">القائد المباشر</option>
                      <option value="formation_commander">قائد التشكيل</option>
                      <option value="admin_manager">مدير الإدارة</option>
                      <option value="other">أخرى</option>
                    </select>
                  </div>

                  <div class="field full-width">
                    <label>نص الرأي</label>

                    <div v-if="record.isOld" class="display-value">
                      {{ opinion.opinion_text }}
                    </div>

                    <textarea
                      v-else
                      v-model="opinion.opinion_text"
                    ></textarea>
                  </div>

                  <button
                    v-if="!record.isOld && record.opinions.length > 1"
                    type="button"
                    class="remove-btn"
                    @click="removeOpinion(rIndex, index)"
                  >
                    حذف
                  </button>
                </div>

                <button
                  v-if="!record.isOld"
                  type="button"
                  class="btn btn-secondary mt-10"
                  @click="addOpinion(rIndex)"
                >
                  + إضافة رأي
                </button>

              </div>
            </transition>
          </div>
        </div>

        <!-- ================= ACTIONS ================= -->
        <div class="actions">
          <button
            v-if="hasNewRecord"
            type="submit"
            class="btn btn-success"
            :disabled="loading"
          >
            حفظ
          </button>

          <button
            type="button"
            class="btn btn-danger"
            @click="$emit('close')"
          >
            إغلاق
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from 'vue'
import lagnaService from '@/services/lagnaService'

const props = defineProps({
  person: Object,
  pros_cons_Array: Array,
  committe_code: String,
  spacific_id: Number,
  person_id: Number
})

const emit = defineEmits(['close', 'saved'])

const loading = ref(false)

const rankOptions = [
  'ملازم',
  'ملازم أول',
  'نقيب',
  'رائد',
  'مقدم',
  'عقيد',
  'عميد',
  'لواء'
]

const form = reactive({
  military_no: '',
  degree: '',
  name: '',
  weapon: '',
  unit: '',
  to_unit_date: '',
  records: []
})

const hasNewRecord = computed(() =>
  form.records.some(r => !r.isOld)
)

onMounted(async () => {
  form.military_no = props.person?.mil_no || ''
  form.degree = props.person?.degree_name || ''
  form.name = props.person?.person_name || ''
  form.weapon = props.person?.army_name || ''
  form.unit = props.person?.unit_name || ''
  form.to_unit_date = props.person?.to_unit_date || ''

  await loadOldData()
})

async function loadOldData() {
  try {
    loading.value = true

    const response =
      await lagnaService.getLagnaSpecificsPersonSnap(
        props.committe_code,
        props.spacific_id,
        props.person_id
      )

    if (response) {
      form.records = [{
        service_status: response.service_status,
        pros_cons_list: response.pros_cons_list || [],
        opinions: response.opinions || [],
        commander_rank: response.commander_rank || '',
        commander_name: response.commander_name || '',
        commander_phone: response.commander_phone || '',
        open: true,
        isOld: true
      }]
    }

  } finally {
    loading.value = false
  }
}

function createNewRecord() {
  form.records.push({
    service_status: '',
    pros_cons_list: [{ type: 'pros', category: '', notes: '' }],
    opinions: [{ opinion_type: '', opinion_text: '' }],
    commander_rank: '',
    commander_name: '',
    commander_phone: '',
    open: true,
    isOld: false
  })
}

function toggleRecord(index) {
  form.records[index].open =
    !form.records[index].open
}

function addProsCons(recordIndex) {
  form.records[recordIndex].pros_cons_list.push({
    type: 'pros',
    category: '',
    notes: ''
  })
}

function removeProsCons(rIndex, index) {
  form.records[rIndex].pros_cons_list.splice(index, 1)
}

function addOpinion(recordIndex) {
  form.records[recordIndex].opinions.push({
    opinion_type: '',
    opinion_text: ''
  })
}

function removeOpinion(rIndex, index) {
  form.records[rIndex].opinions.splice(index, 1)
}

function getCategoryName(code) {
  const found = props.pros_cons_Array.find(
    c => c.photo_type_code === code
  )
  return found?.photo_type_name || ''
}

async function submitForm() {
  try {
    loading.value = true

    const newRecord = form.records.find(r => !r.isOld)
    if (!newRecord) return

    const payload = {
      service_status: newRecord.service_status,
      pros_cons_list: newRecord.pros_cons_list,
      opinions: newRecord.opinions,
      commander_rank: newRecord.commander_rank,
      commander_name: newRecord.commander_name,
      commander_phone: newRecord.commander_phone
    }

    await lagnaService.addLagnaSpecificsPersonSnap(
      props.committe_code,
      props.spacific_id,
      props.person_id,
      payload
    )

    emit('saved')
    emit('close')

  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>




<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-container {
  width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  background: white;
  padding: 25px;
  border-radius: 8px;
  direction: rtl;
  font-family: 'Cairo', sans-serif;
}

.section {
  margin-top: 25px;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 6px;
}

.section-title {
  font-weight: bold;
  margin-bottom: 15px;
  color: #003366;
}

.action-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}


.row-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: bold;
  background: #f1f3f6;
  padding: 10px;
  border-radius: 6px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.field label {
  display: block;
  font-size: 13px;
  margin-bottom: 5px;
}

input, textarea, select {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.radio-group {
  display: flex;
  gap: 40px;
  margin-top: 10px;
}

input[type ='radio']{
  width: auto;
}
.actions {
  margin-top: 30px;
  text-align: center;
  gap: 25px;
}

.dynamic-box {
  border: 1px dashed #ccc;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 6px;
  background: #fafafa;
}

.full-width {
  grid-column: span 2;
}

.remove-btn {
  margin-top: 10px;
  background: red;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.action-btn {
  cursor: pointer;
  background: #1e88e5;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  margin-bottom: 25px;
}

.display-value {
  padding: 8px 10px;
  background-color: #f5f7fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 34px;
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #2c3e50;
}

.row-body {
  margin-top: 15px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.field label {
  display: block;
  font-size: 13px;
  margin-bottom: 5px;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

.display-value {
  padding: 8px 10px;
  background-color: #f5f7fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-weight: 600;
}
</style>