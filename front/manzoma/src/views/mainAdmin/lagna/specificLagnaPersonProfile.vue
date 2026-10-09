<template>
  <div class="afrperson-container">
    <pageNavigation />

    <!-- ================= POPUPS ================= -->
    <pastUnits
      v-if="activePopup === 'units'"
      @close="closePopup"
      :tableData="sortedJobunits"
      :userNamePer="person.person_name"
      :unit_name="person.unit_name"
      :degree="person.degree_name"
    />

    <HistoryPopup
      v-if="activePopup === 'history'"
      @close="closePopup"
      :personName="person.person_name"
      :personDegree="person.degree_name"
      :personHistory="person.tagded_history_info"
    />

    <eff_report
      v-if="activePopup === 'eff'"
      @close="closePopup"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      :tableData="sortedEffReports"
    />

    <CourtPopup
      v-if="activePopup === 'court'"
      @close="closePopup"
      :tableData="filteredPunishments"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      :type="courtType"
    />

    <MedicalPopup
      v-if="activePopup === 'medical'"
      @close="closePopup"
      :personName="person.person_name"
      :personDegree="person.degree_name"
      :medicalData="person.medical_history"
    />

    <VacationPopup
      v-if="activePopup === 'vacation'"
      @close="closePopup"
      :personName="person.person_name"
      :personDegree="person.degree_name"
      :vacationData="person.vacation"
    />

    <ReasonsPopup
      v-if="activePopup === 'reason'"
      :degree="person.degree_name"
      :userNamePer="person.person_name"
      @close="closePopup"
      :tableData="reasonsInfo"
    />

    <RelationPopup
      v-if="activePopup === 'relation'"
      @close="closePopup"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      :tableData="filteredRelations"
      :jobFlag="unQualifiedLabels.includes(String(relationLabel))"
      :appearYears="appearYearsLabels.includes(String(relationLabel))"
    />

    <ConsistancyPopup
      v-if="activePopup === 'consistency'"
      @close="closePopup"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      :tableData="sortedConsistencies"
    />

    <Courses
      v-if="activePopup === 'education'"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      :showCoursesPopup="activePopup === 'education'"
      @close="closePopup"
      :tableData="
        //  person?.education?.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))
        person?.education
      "
    />
    <TravelPopup
      v-if="activePopup === 'travel'"
      @close="closePopup"
      :tableData="person.travel?.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
    />

    <UnFitnessReportModal
      v-if="isUnEffReportOpen"
      @close="isUnEffReportOpen = false"
      :committe_code="lagnaPersonParams['committe_code']"
      :spacific_id="lagnaPersonParams['spacific_id']"
      :person_id="lagnaPersonParams['person_id']"
      :person="person"
    />
    <SecPerson
      v-if="activePopup === 'sec_situation'"
      :showPopup="activePopup === 'sec_situation'"
      @close="closePopup"
      :tableData="person.security"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
    />
    <InspireWorkReport
      v-if="isInspireWorkReportOpen"
      @close="isInspireWorkReportOpen = false"
      :person_id="id"
      :person="person"
    />

    <div id="capture-area">
      <!--  start user data  -->
      <div class="users">
        <!-- ================= DATA ================= -->
        <div class="dataUser">
          <div class="section-slot" :style="{ order: sectionOrder('basic') }">
            <section-block
              v-if="load && isSectionVisible('basic')"
              :page-key="PAGE_KEY"
              section-key="basic"
              :section-expand="spliter.primDataSpliter"
              @section-open="spliter.primDataSpliter = !spliter.primDataSpliter"
              title="البيانات الأساسية"
              :fields="basicFields"
            />
          </div>

          <div class="section-slot" :style="{ order: sectionOrder('punishment') }">
            <section-block
              title="العقوبات"
              :fields="punishmentFields"
              v-if="load && isSectionVisible('punishment')"
              :page-key="PAGE_KEY"
              section-key="punishment"
              :section-expand="spliter.punnDataSpliter"
              @section-open="spliter.punnDataSpliter = !spliter.punnDataSpliter"
            />
          </div>
          <!-- <section-block
            title="الموقف الطبي"
            :fields="medicalFields"
            v-if="load && person.person_sex_code == 1"
            :section-expand="spliter.medicalDataSpliter"
            @section-open="spliter.medicalDataSpliter = !spliter.medicalDataSpliter"
          /> -->
          <!-- :section-expand="spliter.medicalDataSpliter" -->
          <div
            class="section-slot"
            style="display: flex; align-items: center; gap: 20px"
            :style="{ order: sectionOrder('medical') }"
          >
            <div style="width: 50%" v-if="isSectionVisible('medical')">
              <section-block
                title="الموقف الطبي"
                :fields="medicalFields"
                v-if="load"
                :page-key="PAGE_KEY"
                section-key="medical"
                :section-expand="spliter.medicalDataSpliter"
                @section-open="spliter.medicalDataSpliter = !spliter.medicalDataSpliter"
              />
            </div>
            <div style="width: 50%" v-if="isSectionVisible('custom_vacation')">
              <section-block
                title="الاجازات الخاصة"
                :fields="customVacationFields"
                v-if="load"
                :page-key="PAGE_KEY"
                section-key="custom_vacation"
                :section-expand="spliter.customVacationDataSpliter"
                @section-open="
                  spliter.customVacationDataSpliter = !spliter.customVacationDataSpliter
                "
              />
            </div>
          </div>

          <div class="section-slot" :style="{ order: sectionOrder('travel') }">
            <section-block
              title="موقف السفر"
              :fields="travelFields"
              v-if="load && isSectionVisible('travel')"
              :page-key="PAGE_KEY"
              section-key="travel"
              :section-expand="spliter.travelDataSpliter"
              @section-open="spliter.travelDataSpliter = !spliter.travelDataSpliter"
            />
          </div>

          <!-- <section-block
            title="الاسباب"
            :fields="reasonsFields"
            v-if="load"
            :section-expand="spliter.reasonDataSpliter"
            @section-open="spliter.reasonDataSpliter = !spliter.reasonDataSpliter"
          /> -->

          <div class="section-slot" :style="{ order: sectionOrder('family') }">
            <section-block
              title="البيانات الإجتماعية"
              :fields="familyFields"
              v-if="load && isSectionVisible('family')"
              :page-key="PAGE_KEY"
              section-key="family"
              :section-expand="spliter.famillyDataSpliter"
              @section-open="spliter.famillyDataSpliter = !spliter.famillyDataSpliter"
            />
          </div>

          <!-- <div class="white-box opinions-section" v-if="personsStore.opinions?.length"> -->

          <!-- <h3 class="section-title">الآراء</h3> -->

          <!-- <section-block
            title="قرارات اللجان"
            :fields="commitiesDecisions"
            v-if="load"
            :section-expand="spliter.commitiesDecisionSpliter"
            @section-open="spliter.commitiesDecisionSpliter = !spliter.commitiesDecisionSpliter"
          /> -->

          <SecSpliter
            splitTitle="الآراء"
            @expand="spliter.opinionDataSpliter = !spliter.opinionDataSpliter"
            v-if="personsStore.opinions?.length"
          />

          <div class="opinions-grid" v-if="spliter.opinionDataSpliter">
            <div
              v-for="op in personsStore.opinions"
              :key="op.opinion_id"
              class="opinion-result-box"
            >
              <!-- HEADER -->
              <div class="opinion-header">
                <span class="opinion-title">
                  {{ op.opinion_type_data?.opinion_name }}
                </span>

                <div class="opinion-actions">
                  <!-- <button class="icon-btn edit" @click="editOpinion(op)">
                    تعديل
                    <i class="fa-solid fa-pencil"></i>
                  </button> -->
                  <button class="icon-btn delete" @click="deleteOpinion(op)">
                    حذف
                    <i class="fa-regular fa-trash-can"></i>
                  </button>
                </div>
              </div>

              <!-- RESULT -->
              <div class="result-row">
                <span class="leader-label">القرار</span>

                <span class="decision-pill" :class="decisionClass(op?.opinion_code)">
                  {{ op.opinion_data?.opinion_name }}
                </span>
              </div>

              <!-- NOTES -->
              <div v-if="op.opinion_notes" class="opinion-notes">
                {{ op.opinion_notes }}
              </div>

              <!-- ATTACHMENT -->
              <div v-if="op.opinion_attached" class="opinion-attachment">
                <span class="text attach" @click="openAttachment(op.opinion_attached)">
                  عرض المرفق 📎
                </span>
              </div>

              <!-- DATE -->
              <div class="opinion-date">
                {{ formatDate(op.create_date) }}
              </div>
            </div>
            <div v-if="showAttachment" class="attachment-popup" @click.self="closeAttachment">
              <div class="popup-content">
                <button class="close-btn" @click="closeAttachment">✕</button>
                <img :src="attachmentUrl" alt="attachmentUrl" class="attachment-frame" />
              </div>
            </div>
          </div>

          <SecSpliter
            splitTitle="الاسباب"
            @expand="spliter.reasonDataSpliter = !spliter.reasonDataSpliter"
            v-if="personsStore.reasons?.length"
          />

          <div class="opinions-grid" v-if="spliter.reasonDataSpliter">
            <div
              v-for="res in personsStore.reasons"
              :key="res.reason_id"
              class="opinion-result-box"
            >
              <!-- HEADER -->
              <div class="opinion-header">
                <span class="opinion-title"> السبب </span>

                <div class="opinion-actions">
                  <!-- <button class="icon-btn edit" @click="editOpinion(op)">
                    تعديل
                    <i class="fa-solid fa-pencil"></i>
                  </button> -->
                  <button class="icon-btn delete" @click="deleteReason(res)">
                    حذف
                    <i class="fa-regular fa-trash-can"></i>
                  </button>
                </div>
              </div>

              <!-- NOTES -->
              <div v-if="res.descrption" class="opinion-notes">
                {{ res.descrption }}
              </div>

              <!-- ATTACHMENT -->
              <div v-if="res.attach" class="opinion-attachment">
                📎
                <a :href="getFileUrl(res.attach)" target="_blank"> عرض المرفق </a>
              </div>

              <!-- DATE -->
              <div class="opinion-date">
                {{ formatDate(res.create_date) }}
              </div>
            </div>
          </div>

          <!-- ================= FINAL DECISION VOTING ================= -->
          <!-- <SecSpliter
            splitTitle="التصويت والقرار النهائي"
            @expand="spliter.finalDecisionSpliter = !spliter.finalDecisionSpliter"
          />

          <div v-if="spliter.finalDecisionSpliter" class="final-decision-box">
            <div class="final-select-wrapper">
              <label class="final-label"> اختيار القرار النهائي </label>

              <select
                v-model="selectedFinalDecision"
                class="final-select"
                @change="saveFinalDecision($event.target.value)"
              >
                <option disabled value="">-- اختر القرار --</option>

                <option
                  v-for="vote in personsStore.votesTypes"
                  :key="vote?.opinion_code"
                  :value="vote?.opinion_code"
                >
                  {{ vote.opinion_name }}
                </option>
              </select>

              <button
                class="btn btn-success save-final-btn"
                :disabled="!selectedFinalDecision"
                @click="saveFinalDecision"
              >
                حفظ القرار
              </button>
            </div>

            <div class="final-result">
              <span>القرار النهائي:</span>
              <span class="decision-pill" :class="voteClass(finalDecision?.opinion_code)">
                {{ finalDecision.opinion_name }}
              </span>
            </div>
          </div> -->

          <!-- </div> -->

          <!-- MODAL -->
          <BaseModalForm
            :open="isModalOpen"
            :confirmOpen="isDeleteConfirmOpen"
            :title="isEditMode ? 'تعديل رائى' : 'إضافة رائى'"
            :submitText="isEditMode ? 'حفظ' : 'إضافة'"
            v-model="currentOpinion"
            :fields="opinionFields"
            :confirmText="`هل تريد حذف رائى -  ${currentOpinion.committe_name} ؟`"
            @save="saveOpinion"
            @close="closeModal"
            @cancelDelete="isDeleteConfirmOpen = false"
          />

          <!-- MODAL -->
          <BaseModalForm
            :open="isReasonModalOpen"
            :confirmOpen="isReasonDeleteConfirmOpen"
            :title="isReasonEditMode ? 'تعديل سبب' : 'إضافة سبب'"
            :submitText="isReasonEditMode ? 'حفظ' : 'إضافة'"
            v-model="currentReason"
            :fields="reasonFields"
            :confirmText="`هل تريد حذف السبب -  ${currentReason.committe_name} ؟`"
            @save="saveReason"
            @close="closeReasonModal"
            @cancelDelete="isReasonDeleteConfirmOpen = false"
          />

          <!-- سبب العرض - one free text kept on the snap itself -->
          <BaseModalForm
            :open="isAddReasonModalOpen"
            title="سبب العرض"
            submitText="حفظ"
            v-model="currentAddReason"
            :fields="addReasonFields"
            @save="saveAddReason"
            @close="closeAddReasonModal"
          />
          <!-- @confirmDelete="deleteOpinion" -->
        </div>

        <div class="counters">
          <!-- avatar / image -->
          <div class="image-item" @click="openImagePopup">
            <img v-if="mainPhoto" :src="mainPhoto" class="preview" alt="user image" />

            <div v-else class="avatar-placeholder">
              <span>{{ avatarLetter }}</span>
            </div>
          </div>

          <!-- commititColors[personLagnaData?.committe_type.type_id]
                  ? commititColors[personLagnaData?.committe_type.type_id]['style']
                  :  -->
          <div class="rejection_data" style>
            <div class="traq" style="color: #b7281e" v-if="personLagnaData?.committe_type?.type_id">
              <p>{{ personLagnaData?.committe_type.type_name }}</p>
            </div>
          </div>
          <div class="profile-actions">
            <button class="btn btn-primary" @click="addNewOpinion()">إضافة رأي</button>
            <button class="btn btn-primary" @click="addNewUnEffReport()">
              إضافة تقرير عدم صلاحية
            </button>
            <button class="btn btn-primary" @click="addNewInspireWorkReport()">
              إضافة تقرير العمل النفسى
            </button>
            <button class="btn btn-primary" @click="addNewReason()">إضافة سبب</button>
            <button class="btn btn-primary" @click="openAddReasonModal()">
              {{ currentAddReason.add_reason ? 'تعديل سبب العرض' : 'إضافة سبب العرض' }}
            </button>
            <button
              class="btn btn-success"
              @click="reviewPersonData(20)"
              v-if="personStatusCode == 10"
            >
              تاكيد المراجعة
            </button>
            <div class="person-status" v-else>تم المراجعة</div>
          </div>
          <!-- popup -->
          <ImageUploadPanel
            v-if="popups.showImagePopup"
            @close="closeImageUploadPanel"
            :photos="photos"
            :allowUploadImage="false"
            :mil_sir="id"
            :allowReviewImage="auth.hasRole('rejectors')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { usePersonsStore } from '@/stores/persons'
import { useLagnaStore } from '@/stores/lagna'
import { convertToArabicNumbers, getWsUrl } from '@/utils/glopal'
import {
  useUiSettingsPage,
  PROFILE_PAGE_KEY,
  PROFILE_SPLITTERS,
} from '@/composables/useUiSettingsPage'
import swal from 'sweetalert'

import pageNavigation from '@/components/global/pageNavigation.vue'
import pastUnits from '@/components/global/popup/past-units.vue'
import HistoryPopup from '@/components/global/popup/historyPopup.vue'
import eff_report from '@/components/global/popup/eff_report.vue'
import ImageUploadPanel from '@/components/mainAdmin/AfrPersons/ImageUploadPanel.vue'
import CourtPopup from '@/components/global/popup/courtPopup.vue'
import MedicalPopup from '@/components/global/popup/medicalPopup.vue'
import VacationPopup from '@/components/global/popup/VacationPopup.vue'
import RelationPopup from '@/components/global/popup/relationPopup.vue'
import ConsistancyPopup from '@/components/global/popup/consistancyPopup.vue'
import sectionBlock from '@/components/mainAdmin/AfrPersons/profile/sectionBlock.vue'
import BaseModalForm from '@/components/global/dataTable/BaseModalForm.vue'
import SecSpliter from '@/components/mainAdmin/AfrPersons/profile/secSpliter.vue'
import ReasonsPopup from '@/components/global/popup/reasonsPopup.vue'
import { reasons } from '@/api/modules/reasons'
import UnFitnessReportModal from './UnFitnessReportModal.vue'
import InspireWorkReport from './inspireWorkReport.vue'
import TravelPopup from '@/components/global/popup/travelPopup.vue'
import Courses from '@/components/global/popup/courses.vue'
import SecPerson from '@/components/global/popup/sec-person.vue'

const activePopup = ref(null)
const auth = useAuthStore()
const mainPhoto = computed(() => {
  const p = photos.value.find((p) => p.photo_type_code === 1)
  return p ? getWsUrl(p.photo_path) : null
})
const router = useRouter()
const route = useRoute()
const id = route.params.id
const lagnaPersonParams = route.query

const personsStore = usePersonsStore()
const lagnaStore = useLagnaStore()
/* ================= STATE ================= */
const person = ref({})
const personLagnaData = ref({})
const reasonsInfo = ref({})
const finalDecision = ref({})
const opinionsInfo = ref({})
const punishments = ref([])
const courtType = ref(0)
const personStatusCode = ref(null)
const isUnEffReportOpen = ref(false)
const isInspireWorkReportOpen = ref(false)
const relationTypes = ref([])
const relationLabel = ref(null)
const unQualifiedLabels = ref(['bro_sis', 'relatives', 'sons', 'doughter', 'children'])
const appearYearsLabels = ref([
  'bro_sis',
  'mother',
  'current_marrige',
  'father',
  'prev_marrige',
  'sons',
  'doughter',
  'children',
])
const photos = ref([])
const selectedFinalDecision = ref('')

const isModalOpen = ref(false)
const isDeleteConfirmOpen = ref(false)
const isEditMode = ref(false)
const currentOpinion = ref(getEmptyOpinion())

const isReasonModalOpen = ref(false)
const isReasonDeleteConfirmOpen = ref(false)
const isReasonEditMode = ref(false)
const currentReason = ref(getEmptyReason())

// سبب العرض
const isAddReasonModalOpen = ref(false)
const currentAddReason = ref({ add_reason: '' })

// --------- punishment ----------
const punshiments = ref([])
let punishLength = ref(0)
let punishStayLength = ref(0)
let punishNotStayLength = ref(0)
let punishcourtLength = ref(0)
const showAttachment = ref(false)
const attachmentUrl = ref(null)
// ---------- units ----------
let jobunits = ref([])
let jobsUnitsLength = ref(0)

const spliter = reactive({
  primDataSpliter: true,
  punnDataSpliter: true,
  medicalDataSpliter: true,
  travelDataSpliter: true,
  customVacationDataSpliter: true,
  commitiesDecisionSpliter: true,
  reasonDataSpliter: true,
  famillyDataSpliter: true,
  opinionDataSpliter: true,
  finalDecisionSpliter: true,
})

/* ================= UI SETTINGS ================= */
// same layout as the standalone profile screen
const PAGE_KEY = PROFILE_PAGE_KEY
const { sectionOrder, isSectionVisible, loadUiSettings } = useUiSettingsPage(
  PROFILE_PAGE_KEY,
  PROFILE_SPLITTERS,
)

const popups = reactive({
  isVisiable: false,
  showImagePopup: false,
  HistoryIsVisiable: false,
  coursesPopupVisible: false,
  Eff_reportPopupVisible: false,
  courtIsVisiable: false,
  MedicalIsVisiable: false,
  RelationIsVisiable: false,
  ConsistancyIsVisiable: false,
})

let sta = ref({})
let load = ref(false)

function getEmptyOpinion() {
  return {
    type: '',
    text: '',
  }
}
function getEmptyReason() {
  return {
    type: '',
    text: '',
  }
}

const commititColors = computed(() => {
  return { style: 'color:#b7281e' }
  // return {
  //   1: { style: 'color:#b7281e' },
  //   2: { style: 'color:#b7281e' },
  //   3: { style: 'color:#b7281e' },
  //   4: { style: 'color:#b7281e' },
  //   5: { style: 'color:#b7281e' },
  // }
})

const opinionFields = computed(() => [
  {
    name: 'opinion_type',
    label: 'نوع الرائى',
    type: 'select',
    options: personsStore.opinionTypes,
    opLabelName: 'opinion_name',
    opLabelValue: 'type_id',
  },
  {
    name: 'opinion_code',
    label: 'الرأي',
    type: 'select',
    options: personsStore.votesTypes,
    opLabelName: 'opinion_name',
    opLabelValue: 'opinion_code',
  },
  {
    name: 'opinion_notes',
    label: 'ملاحظات',
    type: 'textarea',
  },

  {
    name: 'opinion_attached',
    label: 'مرفقات',
    type: 'file',
    multiple: true,
  },
])
const reasonFields = computed(() => [
  {
    name: 'descrption',
    label: 'ملاحظات',
    type: 'textarea',
  },

  {
    name: 'reason_attached',
    label: 'مرفقات',
    type: 'file',
    multiple: true,
  },
])

const addReasonFields = computed(() => [
  {
    name: 'add_reason',
    label: 'سبب العرض',
    type: 'textarea',
  },
])

// SAVE (ADD or EDIT)
function saveOpinion() {
  if (isEditMode.value) {
    addOpinion()
  } else {
    addOpinion()
  }
  closeModal()
}

function saveReason() {
  if (isReasonEditMode.value) {
    addReason()
  } else {
    addReason()
  }
  closeReasonModal()
}

function closeModal() {
  isModalOpen.value = false
  currentOpinion.value = getEmptyOpinion()
}
function closeReasonModal() {
  isReasonModalOpen.value = false
  currentReason.value = getEmptyReason()
}
function addNewUnEffReport() {
  isUnEffReportOpen.value = true
}
function addNewInspireWorkReport() {
  isInspireWorkReportOpen.value = true
}
function addNewOpinion() {
  isModalOpen.value = true
  currentOpinion.value = getEmptyOpinion()
}
function addNewReason() {
  isReasonModalOpen.value = true
  currentReason.value = getEmptyReason()
}

async function saveFinalDecision(final_decision) {
  console.log(final_decision)
  try {
    await personsStore.setFinalDecision(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      {
        vote: final_decision,
      },
    )
    await personsStore.fetchPersonOpinions(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
    )

    swal({
      title: 'تم الحفظ',
      text: 'تم حفظ القرار النهائي بنجاح',
      icon: 'success',
      timer: 1200,
      button: false,
    })
  } catch (error) {
    console.log(error)
    swal({
      title: 'خطأ',
      text: error.response.data.details,
      icon: 'error',
    })
  }
}

function voteClass(code) {
  if (code === 1 || code === 4) return 'accepted'
  if (code === 2 || code === 3) return 'rejected'
  return 'pending'
}

async function reviewPersonData(new_status) {
  console.log('currentCommitt', currentOpinion.value)
  try {
    let res = await lagnaStore.changeLagnaSpecificsPersonStutus(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      { new_status: new_status },
    )
    swal({
      title: 'تم المراجعة',
      text: 'تم التاكيد على المراجعة بنجاح',
      icon: 'success',
      button: false,
      timer: 1500,
    })
    router.back()
  } catch (error) {
    console.log('errrrrr', error.status)

    if (error.status == 400) {
      swal({
        title: 'تحذير',
        text: error.response.data.details,
        icon: 'warning',

        buttons: {
          cancel: {
            text: 'إغلاق',
            value: null,
            visible: true,
            className: 'btn-cancel',
            closeModal: true,
          },
          confirm: {
            text: 'اضافة رائى',
            value: 'addStatus',
            visible: true,
            className: 'btn-confirm',
            closeModal: true,
          },
        },
      }).then((value) => {
        if (value === 'addStatus') {
          addNewOpinion()
        }
      })
    } else {
      swal({
        title: 'حدثت مشكلة',
        text: error.response.data.details,
        icon: 'error',
        confirmButtonText: 'حاول مره اخرى ',
      })
    }
  }
}

async function addOpinion() {
  console.log('currentCommitt', currentOpinion.value)
  try {
    await personsStore.addSpecificsPersonOpinions(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      currentOpinion.value,
    )
    await personsStore.fetchPersonOpinions(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
    )
    swal({
      title: 'تم اضافة الرائى بنجاح',
      text: 'تم اضافة الرائى بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء الاضافة' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

async function deleteOpinion(opinion) {
  console.log('currentCommitt', currentOpinion.value)
  try {
    await personsStore.deleteSpecificsPersonOpinions(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      opinion.opinion_id,
      currentOpinion.value,
    )
    await personsStore.fetchPersonOpinions(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
    )
    swal({
      title: 'تم الحذف ',
      text: 'تم حذف الرائى بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء الاضافة' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

// ------------REASONS --------------------------
async function deleteReason(reason) {
  console.log('currentCommitt', reason)
  try {
    console.log(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      reason.reason_id,
      currentReason.value,
    )
    await personsStore.deleteSpecificsPersonReasons(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      reason.reason_id,
      currentReason.value,
    )
    await personsStore.fetchPersonReasons(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
    )
    swal({
      title: 'تم الحذف ',
      text: 'تم حذف السبب بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء الاضافة' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}
/* ================= سبب العرض ================= */
function openAddReasonModal() {
  isAddReasonModalOpen.value = true
}

function closeAddReasonModal() {
  isAddReasonModalOpen.value = false
  // reload from the snap so a cancelled edit does not stick in the button label
  currentAddReason.value = { add_reason: personLagnaData.value?.snap_info?.add_reason || '' }
}

async function saveAddReason() {
  try {
    const res = await reasons.patchSpecificsPersonAddReason(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      { add_reason: currentAddReason.value.add_reason || null },
    )
    currentAddReason.value = { add_reason: res.data?.add_reason || '' }
    if (personLagnaData.value?.snap_info) {
      personLagnaData.value.snap_info.add_reason = currentAddReason.value.add_reason
    }
    isAddReasonModalOpen.value = false
    swal({
      title: 'تم حفظ سبب العرض',
      text: 'تم حفظ سبب العرض بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء حفظ سبب العرض ' + error,
      icon: 'error',
      button: false,
      timer: 2000,
    })
  }
}

async function addReason() {
  console.log('currentCommitt', currentReason.value)
  try {
    await personsStore.addSpecificsPersonReasons(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
      currentReason.value,
    )
    await personsStore.fetchPersonReasons(
      lagnaPersonParams['committe_code'],
      lagnaPersonParams['spacific_id'],
      lagnaPersonParams['person_id'],
    )
    swal({
      title: 'تم اضافة السبب بنجاح',
      text: 'تم اضافة السبب بنجاح',
      icon: 'success',
      button: false,
      timer: 1000,
    })
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: 'حدثت مشكلة اثناء الاضافة' + error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

function closeAttachment() {
  showAttachment.value = false
  attachmentUrl.value = null
}
function openAttachment(file) {
  attachmentUrl.value = getFileUrl(file)
  showAttachment.value = true
}
// ----------------- methods ------------------
const avatarLetter = computed(() =>
  person.value.person_name ? person.value.person_name.charAt(0) : '؟',
)

const fullAddress = computed(() => {
  return `${person.value.person_adress || '---'} - ${person.value.markaz_name || '--'} - ${person.value.mohafza_name || '--'}`
})
const unitPeriodService = computed(() => {
  return `${toAr(`${person.value.unit_interval_y || '---'}`)}  سنه ${person.value.unit_interval_m == 0 ? '' : `/  ${toAr(`${person.value.unit_interval_m || '---'}`)}  شهر `}`
})

const sortedJobunits = computed(() => {
  return (person.value.units || []).sort(
    (a, b) => new Date(a.from_unit_date) - new Date(b.from_unit_date),
  )
})

const sortedEffReports = computed(() => {
  return (person.value.effecincy_l3y || []).sort(
    (a, b) => new Date(b.from_date) - new Date(a.from_date),
  )
})

const filteredPunishments = computed(() => {
  return punishments.value
    .sort((a, b) => new Date(b.punish_start_date) - new Date(a.punish_start_date))
    .filter((p) => {
      if (!courtType.value || courtType.value == 0) {
        return true
      } else if (courtType.value == 1) {
        return (
          p.punsh_cort_code == 1 && ![4, 17, 18, 19, 26, 29]?.includes(parseInt(p.punishment_code))
        )
      } else if (courtType.value == 2) {
        return (
          p.punsh_cort_code == 1 && [4, 17, 18, 19, 26, 29]?.includes(parseInt(p.punishment_code))
        )
      } else if (courtType.value == 3) {
        return p.punsh_cort_code == 2
      } else if (courtType.value == 4) {
        return p.punsh_cort_code == 3
      } else {
        return false
      }
    })
})

const filteredRelations = computed(() => person.value.family_info[relationLabel.value] || [])

const sortedConsistencies = computed(() =>
  [...(person.value.consistancies || [])].sort(
    (a, b) => new Date(b.check_date) - new Date(a.check_date),
  ),
)

function toAr(number, numKey = 'notFound') {
  return convertToArabicNumbers(number)
}

/* ================= FIELD CONFIGS ================= */
const basicFields = computed(() => [
  { label: 'الرقم العسكري', value: toAr(person.value.mil_no, 'mil_no') },
  { label: 'الدرجة', value: person.value.degree_name },
  { label: 'الاسم', value: person.value.person_name },
  { label: 'السلاح', value: person.value.army_name },
  { label: 'الفئة', value: person.value.fea_name },
  {
    label: 'الوحدة',
    value: person.value.unit_name,
    click: () => openPopup('units'),
  },
  { label: 'تاريــخ الضم علي الوحدة', value: toAr(person.value.to_unit_date) },
  { label: 'مدة الخدمة بالوحدة', value: unitPeriodService.value },
  { label: 'التبعية', value: person.value.prnt_army_name },
  { label: 'الوظيفة', value: person.value.army_job_name },
  { label: 'تاريخ التطوع', value: toAr(person.value.come_in_date) },
  { label: 'تاريخ صرف الراتب العالي', value: toAr(`${person.value.rateb_date}`) },
  {
    label: 'عدد سنوات الخدمة',
    value:
      ' ' +
      ' ' +
      toAr(`${person.value.tot_ser_y || '.'}`) +
      ' سنه' +
      ' / ' +
      toAr(`${person.value.tot_ser_m || '.'}`) +
      ' شهر' +
      ' ',
  },
  {
    label: 'تاريخ الترقية الحالية',
    value: toAr(person.value.curr_degree_date, 'curr_degree_date'),
    click: () => openPopup('history'),
  },
  {
    label: 'تاريخ الترقي المنتــظر',
    value: toAr(`${person.value.upgrade_date || '---'}`),
    fieldShowStyle: {
      backgroundColor:
        new Date(person.value.upgrade_date).getTime() < new Date().getTime()
          ? 'rgba(163 226 255 )'
          : '',
    },
    // fieldShowLabelStyle: {
    //   backgroundColor:'white',
    // },
  },
  { label: 'العنوان المدني', value: fullAddress.value },
  { label: 'تاريــخ الميــلاد', value: toAr(`${person.value.birth_date}`) || '---' },
  { label: 'السن', value: toAr(`${person.value.tot_years}`) || '---' },
  { label: 'الطول', value: toAr(`${person.value.length || '---'}`) || '---' },
  { label: 'الوزن', value: toAr(`${person.value.weight || '---'}`) || '---' },
  {
    label: 'متوسط تقرير الكفاءة لاخر ثلاث سنوات',
    value:
      person.value?.effecincy_avg?.length > 0 ? person.value?.effecincy_avg[0]?.grade : 'لا يوجد',
    click: () => openPopup('eff'),
  },
  {
    label: 'فرق الوزن',
    value: Number(person.value.over_weight)
      ? toAr(Number(person.value.over_weight)).split('-').reverse().join(' - ') + 'كجم '
      : 'لايكن',
  },
  {
    label: 'التناسق',
    value:
      (person.value.consis_name ? person.value.consis_name : '--') +
      ' (طبقا لمعدل الكتلة الجسمانية) ',
    fieldShowLabelStyle: {
      background: person.value.consis != 0 ? '#0a820f' : '#d63024',
      color: person.value.consis != 0 ? 'white' : 'white',
    },
  },
  {
    label: 'التاهيل',
    //value: person.value.education[person.value.education?.length - 1]?.dawra_name,
    value: person.value.education[0]?.dawra_name,
    click: () => openPopup('education'),
  },
  {
    label: 'الموقف الامنــي',
    value: person.value?.security.length > 0 ? 'يـوجــد' : 'لا يـوجــد',
    click: () => openPopup('sec_situation'),
    fieldShowLabelStyle: {
      background: '#d63024',
      color: 'white',
    },
  },
])

const punishmentFields = computed(() => [
  {
    label: 'العقوبات',
    value: sta.value.tot_pa != 0 ? toAr(`${sta.value.tot_pa}`) : 'لايكن',
    click: () => openCourt(0),
  },
  {
    // v-if="sta.value.not_stay != 0 && punshiments.length > 0"
    label: 'الحجز',
    value: sta.value.not_stay != 0 ? toAr(`${sta.value.not_stay}`) : 'لايكن',
    click: () => openCourt(1),
  },
  {
    // v-if="punishStayLength != 0 && punshiments.length > 0"
    label: 'الحبس',
    value: sta.value.stay != 0 ? toAr(`${sta.value.stay}`) : 'لايكن',
    click: () => openCourt(2),
  },
  {
    // v-if="sta.value.court != 0 && punshiments.length > 0"
    label: 'محاكم عسكرية',
    value: sta.value.court != 0 ? toAr(`${sta.value.court}`) : 'لايكن',
    click: () => openCourt(3),
  },
  {
    // v-if="sta.value.other > 0 && punshiments.length > 0"
    label: 'محاكم مدنية',
    value: sta.value.oth != 0 ? toAr(`${sta.value.oth}`) : 'لايكن',
    click: () => openCourt(4),
  },
])

const medicalFields = computed(() => [
  {
    label: 'اللجان الطبية',
    value:
      person.value.medical_history.length > 0
        ? toAr(`${person.value.medical_history.length}`, 'medicalFields')
        : 'لايكن',
    click: () => openPopup('medical'),
    danger: true,
    fieldShowDataStyle: {
      // maxWidth: person.value.medical_history.length == 0 ? '400px' : '',
    },
    fieldShowStyle: {
      // maxWidth: person.value.medical_history.length == 0 ? '400px' : '',
    },
  },
])

const customVacationFields = computed(() => [
  {
    label: 'الاجازات الخاصة ' + ' بدون مرتب ',
    value:
      person.value.vacation.length > 0
        ? toAr(`${person.value.vacation.length}`, 'customVacationFields')
        : 'لايكن',
    click: () => openPopup('vacation'),
    danger: true,
    fieldShowDataStyle: {
      // maxWidth: person.value.vacation.length == 0 ? '600px' : '',
    },
    fieldShowStyle: {
      // maxWidth: person.value.vacation.length == 0 ? '600px' : '',
      // minWidth: '660px',
    },
  },
])

const travelFields = computed(() => [
  {
    label: 'عدد السفريات',
    value:
      person.value.travel.length > 0
        ? toAr(`${person.value.travel.length}`, 'medicalFields')
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
    fieldShowDataStyle: {
      maxWidth: person.value.travel.length == 0 ? '400px' : '',
    },
  },
  {
    label: 'جهة اخر سفرية',
    value:
      person.value.travel.length > 0
        ? toAr(
            `${person.value.travel[0].country_name != null ? person.value.travel[0].country_name : '---'}`,
            'medicalFields',
          )
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
  },
  {
    label: 'من',
    value:
      person.value.travel.length > 0
        ? toAr(
            `${person.value.travel[0].start_date != null ? person.value.travel[0].start_date : '---'}`,
            'medicalFields',
          )
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
  },
  {
    label: 'الي',
    value:
      person.value.travel.length > 0
        ? toAr(
            `${person.value.travel[0].end_date != null ? person.value.travel[0].end_date : '---'}`,
            'medicalFields',
          )
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
  },
])

const commitiesDecisions = computed(() => [
  {
    label: 'عدد السفريات',
    value:
      person.value.travel.length > 0
        ? toAr(`${person.value.travel.length}`, 'medicalFields')
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
    fieldShowDataStyle: {
      maxWidth: person.value.travel.length == 0 ? '400px' : '',
    },
  },
])
// const reasonsFields = computed(() => [
//   {
//     label: 'الاسباب',
//     // value: reasonsInfo.value.at(-1)?.descrption,
//     value: reasonsInfo.value.length > 0 ? toAr(`${reasonsInfo.value.at(-1)?.descrption}`) : 'لايكن',
//     click: () => openPopup('reason'),
//     danger: true,
//   },
// ])

const familyFields = computed(() => [
  {
    label: 'الحالة الاجتماعية',
    value: person.value.marital_state_name
      ? person.value.family_statistic[0].curr_marrige > 0
        ? `(  ${toAr(person.value.family_statistic[0].curr_marrige)}  ) - ${person.value.marital_state_name}`
        : person.value.marital_state_name
      : 'لايكن',
    // value: person.value.marital_state_name ? person.value.marital_state_name : 'لايكن',
    click: () => openRelation([1, 15], 'current_marrige'),
  },
  {
    label: person.value.person_sex_code == 1 ? 'مؤهل/وظيفة الزوجة' : 'مؤهل/وظيفة الزوج',
    value:
      person.value.family_statistic.length > 0
        ? person.value.family_statistic[0]?.whife_job
        : 'لايكن',
  },
  {
    label: 'عدد الابناء',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.son + person.value.family_statistic[0]?.doughter)
        : 'لايكن',
    click: () => openRelation([2, 7], 'children'),
  },
  {
    label: 'الذكور',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.son)
        : 'لايكن',
    click: () => openRelation([2], 'sons'),
    fieldShowLabelStyle: {
      backgroundColor: 'rgba(111, 210, 255, 0.64) !important',
    },
  },
  {
    label: 'الاناث',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.doughter)
        : 'لايكن',
    click: () => openRelation([7], 'doughter'),
    fieldShowLabelStyle: {
      backgroundColor: 'rgba(255 207 245) !important',
    },
  },
  {
    // label: 'وظيفة الوالد',
    label: 'مؤهل/وظيفة الوالد',
    click: () => openRelation([3], 'father'),
    value:
      person.value.family_statistic.length > 0
        ? person.value.family_statistic[0]?.father_job
        : 'لايكن',
  },
  {
    // label: 'وظيفة الوالده',
    label: 'مؤهل/وظيفة الوالدة',
    click: () => openRelation([4], 'mother'),
    value:
      person.value.family_statistic.length > 0
        ? person.value.family_statistic[0]?.mother_job
        : 'لايكن',
  },
  {
    label: 'عدد الاشقاء',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.brother + person.value.family_statistic[0]?.sister)
        : 'لايكن',
    click: () => openRelation([5, 6], 'bro_sis'),
  },
  {
    label: 'عدد الاقارب',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.relativ)
        : 'لايكن',
    click: () => openRelation([11, 9, 10, 8], 'relatives'),
  },
  {
    label: 'الزيجات السابقة',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.prev_marrige)
        : 'لايكن',
    click: () => openRelation([11, 9, 10, 8], 'prev_marrige'),
  },
])

/* ================= ACTIONS ================= */
function openPopup(name) {
  activePopup.value = name
}
function closePopup() {
  activePopup.value = null
}
function openCourt(type) {
  courtType.value = type
  openPopup('court')
}
function openRelation(types, label) {
  relationTypes.value = types
  relationLabel.value = label
  openPopup('relation')
}
async function closeImageUploadPanel() {
  popups.showImagePopup = false
  // await loadPerson()
}

function openImagePopup() {
  popups.showImagePopup = true
}

/* ================= LOAD ================= */
async function loadPerson() {
  load.value = false
  const res = await lagnaStore.fetchOneSpecificCommittPerson(
    lagnaPersonParams['committe_code'],
    lagnaPersonParams['spacific_id'],
    lagnaPersonParams['person_id'],
  )
  personLagnaData.value = res
  person.value = res.person
  currentAddReason.value = { add_reason: res.snap_info?.add_reason || '' }
  console.log('res=============>', res)
  opinionsInfo.value = res.person.opinions
  reasonsInfo.value = res.reasons_info
  finalDecision.value = res.final_decision
  personStatusCode.value = res.committe_status_code.afr_comm_status_code
  photos.value = res.person.photos || []
  punishments.value = res.person.person_punishment || []

  sta.value = person.value.punishment_statistics[0]
  punshiments.value = person.value.person_punishment

  punishLength.value = person.value.punishment_statistics[0]?.tot_pa || 'لا يكن'

  punishcourtLength.value = person.value.punishment_statistics[0]?.court || 'لا يكن'
  punishStayLength.value = person.value.punishment_statistics[0]?.stay || 'لا يكن'

  punishNotStayLength.value = person.value.punishment_statistics[0]?.not_stay || 'لا يكن'
  jobunits.value = [...(person.value.units || [])]
  jobsUnitsLength.value = person.value.units?.length
  load.value = true
}

function decisionClass(code) {
  return {
    accepted: code === 1 || code === 4, // موافق / استمرار
    rejected: code === 2 || code === 3, // لا أوصي / إنهاء
    pending: code === 0,
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('ar-EG')
}

// function getFileUrl(path) {
//   return getWsUrl(path)
// }

function getFileUrl(file) {
  // adjust for your backend path
  const base = import.meta.env.VITE_MEDIA_BASE_URL
  console.log(base)
  return `${base}${file}`
}

/* ACTIONS */
function editOpinion(opinion) {
  // open modal + fill form
  console.log('edit', opinion)
}

onMounted(async () => {
  await loadUiSettings(spliter)
  await loadPerson()
  await personsStore.fetchLagnaOpinionTypes(lagnaPersonParams['person_id'])
  await personsStore.fetchPersonOpinions(
    lagnaPersonParams['committe_code'],
    lagnaPersonParams['spacific_id'],
    lagnaPersonParams['person_id'],
  )
  await personsStore.fetchPersonReasons(
    lagnaPersonParams['committe_code'],
    lagnaPersonParams['spacific_id'],
    lagnaPersonParams['person_id'],
  )
  console.log('personsStore.reasons', personsStore.reasons)
})
</script>

<style scoped>
/* m#gana*/
.sec-data {
  display: grid;
  flex-wrap: wrap;
  gap: 13px;
  margin: 10px 0;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

@media (max-width: 20px) {
  .sec-data {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}

.users {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

/* البيانات الرئيسية */
.dataUser {
  flex: 1; /* تاخد كل المساحة المتبقية */
  min-width: 0; /* مهم عشان ما تكسرش flex */

  /* عمود مرن عشان ترتيب الأقسام يتغير من شاشة الإعدادات */
  display: flex;
  flex-direction: column;
}

.section-slot {
  min-width: 0;
}

/* أي محتوى آخر (الآراء ... إلخ) يظل بعد الأقسام */
.dataUser > *:not(.section-slot) {
  order: 100;
}

.counters {
  flex: 0 0 240px; /* عرض ثابت صغير */
  max-width: 240px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.counters span {
  text-wrap: nowrap;
  margin: -14px;
}
.counters img {
  width: 300px;
  height: 300px;
}

.avatar-placeholder {
  width: 160px;
  height: 200px;
  border-radius: 12px;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: bold;
  color: #555;
}
.profile-actions {
  position: relative;
  top: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 20px;
}
.image-item {
  border: 2px dashed #ccc;
  border-radius: 14px;
  padding: 12px;
  position: relative;
  /* height: 520px; */
  display: flex;
  flex-direction: column;
}

form {
  display: flex;
  justify-content: space-around;
  width: -61%;
  place-items: center;
  font-size: -26px;
  flex: 1;
}
.rejection_data button {
  width: 63%;
  background: #b7281e !important;
  padding: 7px 0;
  font-size: 18px;
  margin-bottom: 10px;
}

.rejection_data button:hover {
  background: #db3327 !important;
}
.traq {
  display: flex;
  justify-content: center;
  height: 135px;
  align-items: center;
}

.traq p {
  padding: 20px;
  border: 7px solid;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  align-items: center;
  display: flex;
  justify-content: center;
  font-weight: bolder;
  font-size: 18px;
  text-align: center;
}
@media (max-width: 992px) {
  .users {
    flex-direction: column;
  }

  .counters {
    width: 100%;
    max-width: 100%;
  }
}

.opinions-section {
  padding: 20px;
}
.Reasons-section {
  padding: 20px;
}

.section-title {
  margin-bottom: 20px;
  color: var(--dark-blue);
}

.Reasons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.opinions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* BOX */
.opinion-result-box {
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 16px;
  background: #fafafa;
  transition: 0.2s;
}

.opinion-result-box:hover {
  background: #f4f6ff;
  border-color: #dbe4ff;
}

/* HEADER */
.opinion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.opinion-title {
  font-weight: bold;
  color: #333;
}

.opinion-actions {
  display: flex;
  gap: 6px;
}

.icon-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
}

.icon-btn.edit {
  color: #1971c2;
}

.icon-btn.delete {
  color: #c92a2a;
}
.icon-btn.edit:hover {
  color: #1669b6;
}

.icon-btn.delete:hover {
  color: #ac2323;
}

.person-status {
  padding: 10px 20px;
  background: #52bf54;
  color: white;
  border-radius: 10px;
}
/* RESULT */
.result-row {
  margin-top: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.attachment-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
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

/* IFRAME */
.attachment-frame {
  /* width: 100%;
  height: 100%; */
  border: none;
  border-radius: 10px;
  margin-top: 25px;
}
سسسسسس .leader-label {
  color: #666;
  font-size: 14px;
}

/* DECISION */
.decision-pill {
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
}

.decision-pill.accepted {
  background: #d3f9d8;
  color: #2b8a3e;
}

.decision-pill.rejected {
  background: #ffe3e3;
  color: #c92a2a;
}

.decision-pill.pending {
  background: #fff3bf;
  color: #e67700;
}

/* NOTES */
.opinion-notes {
  margin-top: 12px;
  color: #444;
  line-height: 1.6;
}

/* ATTACHMENT */
.opinion-attachment {
  margin-top: 10px;
}

.opinion-attachment .text {
  color: #3b5bdb;
  text-decoration: none;
  cursor: pointer;
}

/* DATE */
.opinion-date {
  margin-top: 12px;
  font-size: 13px;
  color: #888;
  text-align: left;
}

/* Confirm Button */
.btn-confirm {
  background-color: #d33 !important; /* Red */
  border: none !important;
  color: white !important;
}

/* Cancel Button */
.btn-cancel {
  background-color: #6c757d !important; /* Gray */
  border: none !important;
  color: white !important;
}

/* Optional hover effect */
.btn-confirm:hover {
  background-color: #b52a2a !important;
}

.btn-cancel:hover {
  background-color: #5a6268 !important;
}

.final-decision-box {
  margin-top: 20px;
  padding: 20px;
  border-radius: 14px;
  background: #f8f9ff;
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
  margin-top: 25px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.final-label {
  font-weight: 600;
}

.final-select {
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid #ccc;
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
