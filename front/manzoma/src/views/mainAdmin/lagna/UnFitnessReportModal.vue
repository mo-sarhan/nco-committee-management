<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <div v-if="loading" class="loading-overlay">جاري التحميل...</div>

      <div class="modal-header">
        <h2>تقرير عرض لجنة (عدم الصلاحية)</h2>
      </div>

      <form @submit.prevent="submitForm">
        <!-- ================= BASIC DATA ================= -->
        <div class="accordion-item">
          <div class="accordion-header" @click="basicOpen = !basicOpen">
            <div>البيانات الأساسية</div>
            <span class="arrow">
              <i v-if="basicOpen" class="fa-solid fa-chevron-up"></i>
              <i v-else class="fa-solid fa-chevron-down"></i>
            </span>
          </div>

          <transition name="fade">
            <div v-show="basicOpen" class="accordion-body">
              <div class="grid-2">
                <div class="field">
                  <label>الرقم العسكري</label>
                  <div class="display-value">{{ form.military_no }}</div>
                </div>
                <div class="field">
                  <label>الدرجة</label>
                  <div class="display-value">{{ form.degree }}</div>
                </div>
                <div class="field">
                  <label>الاسم</label>
                  <div class="display-value">{{ form.name }}</div>
                </div>
                <div class="field">
                  <label>السلاح</label>
                  <div class="display-value">{{ form.weapon }}</div>
                </div>
                <div class="field">
                  <label>الوحدة</label>
                  <div class="display-value">{{ form.unit }}</div>
                </div>
                <div class="field">
                  <label>تاريخ الضم</label>
                  <div class="display-value">{{ form.to_unit_date }}</div>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- ================= RECORDS ================= -->
        <div class="section">
          <div class="action-header">
            <div class="section-title">العروض</div>

            <div v-if="!hasNewRecord" class="action-btn" @click="createNewRecord">
              + إضافة عرض جديد
            </div>
          </div>

          <div v-for="(record, rIndex) in form.records" :key="rIndex" class="accordion-item">
            <!-- Record Header -->
            <div class="accordion-header" @click="toggleRecord(rIndex)">
              <div>
                عرض {{ record.commander_type }}
                <span v-if="record.isOld" class="old-badge"> (عرض سابق) </span>
              </div>

              <span class="arrow">
                <i v-if="record.open" class="fa-solid fa-chevron-up"></i>
                <i v-else class="fa-solid fa-chevron-down"></i>
              </span>
            </div>

            

            <!-- Record Body -->
            <transition name="fade">
              <div v-show="record.open" class="accordion-body">
                <!-- ================= COMMANDER ================= -->
                <div class="accordion-item nested">
                  <div
                    class="accordion-header"
                    @click.stop="record.commanderOpen = !record.commanderOpen"
                  >
                    <div>بيانات قائد الوحدة</div>
                    <span class="arrow">
                      <i v-if="record.commanderOpen" class="fa-solid fa-chevron-up"></i>
                      <i v-else class="fa-solid fa-chevron-down"></i>
                    </span>
                  </div>

                  <transition name="fade">
                    <div v-show="record.commanderOpen" class="accordion-body">
                      <div class="grid-2">
                        <div class="field">
                          <label>الرتبة</label>
                          <select v-if="!record.isOld" v-model="record.commander_rank">
                            <option value="">اختر الرتبة</option>
                            <option
                              v-for="rank in rankOptions"
                              :key="rank.rank_code"
                              :value="rank.rank_code"
                            >
                              {{ rank.rank_name }}
                            </option>
                          </select>
                          <div v-else class="display-value">
                            {{ record.commander_rank }}
                          </div>
                        </div>

                        <div class="field" v-if="!record.isOld">
                          <label>الوظيفة بالجهة</label>
                          <select  v-model="record.commander_type">
                            <option value="">اختر الوظيفة</option>
                            <option
                              v-for="rank in commanderJobs"
                              :key="rank.comm_des_id"
                              :value="rank.comm_des_id"
                            >
                              {{ rank.comm_des }}
                            </option>
                          </select>
                        </div>

                        <div class="field">
                          <label>اسم القائد</label>
                          <input v-if="!record.isOld" v-model="record.commander_name" />
                          <div v-else class="display-value">
                            {{ record.commander_name }}
                          </div>
                        </div>

                        <div class="field">
                          <label>الوظيفة</label>
                          <input v-if="!record.isOld" v-model="record.comm_job" />
                          <div v-else class="display-value">
                            {{ record.comm_job }}
                          </div>
                        </div>

                        <div class="field">
                          <label>تاريخ استلام الوحدة</label>
                          <input v-if="!record.isOld" type="date" v-model="record.comm_unit_date" />
                          <div v-else class="display-value">
                            {{ record.comm_unit_date }}
                          </div>
                        </div>

                        <div class="field">
                          <label>رقم الهاتف</label>
                          <input v-if="!record.isOld" v-model="record.commander_phone" />
                          <div v-else class="display-value">
                            {{ record.telphone_no }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </transition>
                </div>

                <!-- ================= PROS CONS ================= -->
                <div class="accordion-item nested" v-if="record.pros_cons_list.length > 0 && !record.isOld">
                  <div
                    class="accordion-header"
                    @click.stop="record.prosConsOpen = !record.prosConsOpen"
                  >
                    <div>الإيجابيات والسلبيات</div>
                    <span class="arrow">
                      <i v-if="record.prosConsOpen" class="fa-solid fa-chevron-up"></i>
                      <i v-else class="fa-solid fa-chevron-down"></i>
                    </span>
                  </div>

                  <transition name="fade">
                    <div v-show="record.prosConsOpen" class="accordion-body">
                      <div
                        v-for="(item, index) in record.pros_cons_list"
                        :key="index"
                        class="accordion-item nested-2"
                      >
                        <div class="accordion-header" @click.stop="item.open = !item.open">
                          <div>
                            {{ item.type === 1 ? 'إيجابية' : 'سلبية' }}
                          </div>

                          <span class="arrow">
                            <i v-if="item.open" class="fa-solid fa-chevron-up"></i>
                            <i v-else class="fa-solid fa-chevron-down"></i>
                          </span>
                        </div>

                        <transition name="fade">
                          <div v-show="item.open" class="accordion-body">
                            <div class="grid-2">
                              <div class="field" v-if="!record.isOld">
                                <label>النوع</label>
                                <select v-model="item.po_co_types">
                                  <option
                                    v-for="type in prosCons"
                                    :key="type.pons_cons_type_id"
                                    :value="type.pons_cons_type_id"
                                  >
                                    {{ type.pons_cons_name }}
                                  </option>
                                </select>
                              </div>
                  
                              <div class="field full-width">
                                <label>الملاحظات</label>
                                <textarea v-if="!record.isOld" v-model="item.po_co_notes"></textarea>
                                <div v-else class="display-value">
                                  {{ item.po_co_notes }}
                                </div>
                              </div>
                            </div>
                          </div>
                        </transition>
                      </div>

                      <button
                        v-if="!record.isOld"
                        type="button"
                        class="action-btn"
                        @click="addProsCons(rIndex)"
                      >
                        + إضافة ملاحظة
                      </button>
                    </div>
                  </transition>
                </div>

                <!-- ================= OPINIONS ================= -->
                <div class="accordion-item nested" v-if="record.opinions.length > 0 && record.isOld">
                  <div
                    class="accordion-header"
                    @click.stop="record.opinionsOpen = !record.opinionsOpen"
                  >
                    <div>الآراء</div>
                    <span class="arrow">
                      <i v-if="record.opinionsOpen" class="fa-solid fa-chevron-up"></i>
                      <i v-else class="fa-solid fa-chevron-down"></i>
                    </span>
                  </div>

                  <transition name="fade">
                    <div v-show="record.opinionsOpen" class="accordion-body">
                      <div
                        v-for="(opinion, index) in record.opinions"
                        :key="index"
                        class="accordion-item nested-2"
                      >
                        <div class="accordion-header" @click.stop="opinion.open = !opinion.open">
                          <div>رأي رقم {{ index + 1 }}</div>

                          <span class="arrow">
                            <i v-if="opinion.open" class="fa-solid fa-chevron-up"></i>
                            <i v-else class="fa-solid fa-chevron-down"></i>
                          </span>
                        </div>

                        <transition name="fade">
                          <div v-show="opinion.open" class="accordion-body">
                            <div class="field">
                              <label>نوع الرأي</label>
                              <select v-if="!record.isOld" v-model="opinion.opinion_type">
                                <option value="direct_commander">القائد المباشر</option>
                                <option value="formation_commander">قائد التشكيل</option>
                                <option value="admin_manager">مدير الإدارة</option>
                                <option value="other">أخرى</option>
                              </select>
                              <div v-else class="display-value">
                                {{ opinion.opinion_type }}
                              </div>
                            </div>

                            <div class="field">
                              <label>نص الرأي</label>
                              <textarea
                                v-if="!record.isOld"
                                v-model="opinion.opinion_text"
                              ></textarea>
                              <div v-else class="display-value">
                                {{ opinion.opinion_text }}
                              </div>
                            </div>
                          </div>
                        </transition>
                      </div>

                      <button
                        v-if="!record.isOld"
                        type="button"
                        class="action-btn"
                        @click="addOpinion(rIndex)"
                      >
                        + إضافة رأي
                      </button>
                    </div>
                  </transition>
                </div>
              </div>
            </transition>
          </div>
        </div>

        <!-- ACTIONS -->
        <div class="actions">
          <button v-if="hasNewRecord" type="submit" class="btn btn-success">حفظ</button>

          <button type="button" class="btn btn-danger" @click="$emit('close')">إغلاق</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from 'vue'
import lagnaService from '@/services/lagnaService'
import { useGlopalStore } from '@/stores/glopal'
const props = defineProps({
  person: Object,
  pros_cons_Array: Array,
  committe_code: String,
  spacific_id: Number,
  person_id: Number,
})

let glopal = useGlopalStore()
const emit = defineEmits(['close', 'saved'])

const loading = ref(false)

const basicOpen = ref(true)

const rankOptions = glopal.armyRanks
const commanderJobs = glopal.commanderJobs
const prosCons = glopal.ponsCons

console.log('sdssssswsssssssssssssssssssssssssssssssss', prosCons)
const form = reactive({
  military_no: '',
  degree: '',
  name: '',
  weapon: '',
  unit: '',
  to_unit_date: '',
  records: [],
})

const hasNewRecord = computed(() => form.records.some((r) => !r.isOld))

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

    const response = await lagnaService.getLagnaSpecificsPersonSnap(
      props.committe_code,
      props.spacific_id,
      props.person_id,
    )

    console.log("response", response)

    if (!response) return

    form.records = []

    /* ===== CREATE RECORD FOR EACH COMMANDER ===== */

    if (response.commanders?.length) {
      response.commanders.forEach((c, index) => {
        const record = {
          open: index === 0,
          isOld: true,
          prosConsOpen: true,
          commanderOpen: true,
          opinionsOpen: true,

          /* COMMANDER DATA */
          commander_rank: c.commander?.rank_info?.rank_name || '',
          commander_name: c.commander?.comm_name || '',
          comm_job: c.commander?.comm_job || '',
          comm_unit_date: c.commander?.comm_unit_date || '',
          commander_phone: c.commander?.telphone_no || '',
          commander_type: c.commander?.comm_op?.comm_des || '',
          telphone_no: c.commander?.telphone_no || '',

          /* OPINION */
          opinions: c.opinion
            ? [
                {
                  opinion_type: c.commander?.comm_op?.comm_des || '',
                  opinion_text: c.opinion,
                  open: true,
                },
              ]
            : [],

          /* PROS CONS */
          pros_cons_list:
            c.pons_cons?.map((p) => ({
              po_co_types: p.po_co?.pons_cons_name || '',
              category: p.po_co_types,
              po_co_notes: p.po_co_notes,
              open: true,
            })) || [],
        }

        form.records.push(record)
      })
    }

  } finally {
    loading.value = false
  }
}

function createNewRecord() {
  form.records.unshift({
    service_status: '',
    prosConsOpen: true,
    commanderOpen: true,
    opinionsOpen: true,
    pros_cons_list: [{ po_co_types: 'pros', category: '', po_co_notes: '', open: true }],
    opinions: [{ opinion_type: '', opinion_text: '', open: true }],
    commanders: [],
    open: true,
    isOld: false,
  })
  // form.records.push({
  //   service_status: '',
  //   prosConsOpen: true,
  //   commanderOpen: true,
  //   opinionsOpen: true,
  //   pros_cons_list: [{ type: 'pros', category: '', notes: '', open: true }],
  //   opinions: [{ opinion_type: '', opinion_text: '', open: true }],
  //   commanders: [],
  //   open: true,
  //   isOld: false,
  // })
}

function toggleRecord(index) {
  form.records[index].open = !form.records[index].open
}

function addProsCons(recordIndex) {
  form.records[recordIndex].pros_cons_list.push({ // A porblem here need to make sure that type = po_co_types and notes = po_co_notes
    po_co_types: 'pros',
    category: '',
    po_co_notes: '',
  })
}

function removeProsCons(rIndex, index) {
  form.records[rIndex].pros_cons_list.splice(index, 1)
}

function getCategoryName(code) {
  const found = prosCons.find((c) => c.pons_cons_type_id === code)
  return found?.pons_cons_name || ''
}

async function submitForm() {
  try {
    loading.value = true

    const newRecord = form.records.find((r) => !r.isOld)
    if (!newRecord) return

    const payload = {
      "commanders" :[{
          // service_status: newRecord.service_status,
          person_cons_pons: newRecord.pros_cons_list,
          // write_opinion: newRecord.opinions,
          rank_id: newRecord.commander_rank,
          comm_job: newRecord.comm_job,
          comm_op_type: newRecord.commander_type,
          comm_name: newRecord.commander_name,
          telphone_no: newRecord.commander_phone,
          comm_unit_date: newRecord.comm_unit_date,
        }
      ],
    }

    // {
    //     "commanders":[
    //         {
    //             "rank_id":1,
    //             "comm_op_type":4,
    //             "comm_name":"خالد السعيد",
    //             "comm_job":"رئيس اركان",
    //             "comm_unit_date":"2024-1-1",
    //             "write_opinion":{"opinion_type":1,"opinion_code":5},
    //             "person_cons_pons":[
    //                 {
    //                 "po_co_types":1,
    //                 "po_co_notes":"اي بتنجان"
    //                 }
    //             ]
    //         }

    //     ]
    // }
    await lagnaService.addLagnaSpecificsPersonSnap(
      props.committe_code,
      props.spacific_id,
      props.person_id,
      payload,
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
  background: rgba(0, 0, 0, 0.4);
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

input,
textarea,
select {
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

input[type='radio'] {
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

.accordion-item {
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 15px;
  background: #fafafa;
}

.accordion-item.nested {
  margin-top: 15px;
  background: #fff;
}

.accordion-item.nested-2 {
  margin-top: 10px;
  background: #f9f9f9;
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: bold;
  background: #f1f3f6;
  padding: 10px;
  border-radius: 6px;
}

.accordion-body {
  padding: 15px;
  background: white;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
