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
    <Courses
      v-if="activePopup === 'education'"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      :showCoursesPopup="activePopup === 'education'"
      @close="closePopup"
      :tableData="person?.education"
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
    <TravelPopup
      v-if="activePopup === 'travel'"
      @close="closePopup"
      :tableData="person.travel?.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
    />

    <div id="capture-area">
      <!--  start user data  -->
      <div class="users">
        <!-- ================= DATA ================= -->
        <div class="dataUser">
          <!-- every block sits in its own slot so the settings screen can
               reorder / hide it without touching this template -->
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
        </div>

        <div class="counters">
          <!-- avatar / image -->
          <div class="image-item" @click="openImagePopup">
            <img v-if="mainPhoto" :src="mainPhoto" class="preview" alt="user image" />

            <div v-else class="avatar-placeholder">
              <span>{{ avatarLetter }}</span>
            </div>
          </div>
          <!-- popup -->
          <ImageUploadPanel
            v-if="popups.showImagePopup"
            @close="closeImageUploadPanel"
            :photos="photos"
            :allowUploadImage="false"
            :mil_sir="id"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePersonsStore } from '@/stores/persons'
import {
  useUiSettingsPage,
  PROFILE_PAGE_KEY,
  PROFILE_SPLITTERS,
} from '@/composables/useUiSettingsPage'
import { convertToArabicNumbers, getWsUrl } from '@/utils/glopal'

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
import TravelPopup from '@/components/global/popup/travelPopup.vue'
import Courses from '../../../components/global/popup/courses.vue'

const activePopup = ref(null)

const mainPhoto = computed(() => {
  const p = photos.value.find((p) => p.photo_type_code === 1)
  return p ? getWsUrl(p.photo_path) : null
})

const route = useRoute()
const id = route.params.id
const personsStore = usePersonsStore()

/* ================= UI SETTINGS ================= */
const PAGE_KEY = PROFILE_PAGE_KEY
const { sectionOrder, isSectionVisible, loadUiSettings } = useUiSettingsPage(
  PROFILE_PAGE_KEY,
  PROFILE_SPLITTERS,
)

/* ================= STATE ================= */
const person = ref({})
const punishments = ref([])
const courtType = ref(0)
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

// --------- punishment ----------
const punshiments = ref([])
let punishLength = ref(0)
let punishStayLength = ref(0)
let punishNotStayLength = ref(0)
let punishcourtLength = ref(0)

// ---------- units ----------
let jobunits = ref([])
let jobsUnitsLength = ref(0)

const spliter = reactive({
  primDataSpliter: true,
  punnDataSpliter: true,
  medicalDataSpliter: true,
  customVacationDataSpliter: true,
  famillyDataSpliter: true,
  travelDataSpliter: true,
})

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
  { key: 'mil_no', label: 'الرقم العسكري', value: toAr(person.value.mil_no, 'mil_no') },
  { key: 'degree_name', label: 'الدرجة', value: person.value.degree_name },
  { key: 'person_name', label: 'الاسم', value: person.value.person_name },
  { key: 'army_name', label: 'السلاح', value: person.value.army_name },
  { key: 'fea_name', label: 'الفئة', value: person.value.fea_name },
  {
    key: 'unit_name',
    label: 'الوحدة',
    value: person.value.unit_name,
    click: () => openPopup('units'),
  },
  { key: 'to_unit_date', label: 'تاريــخ الضم علي الوحدة', value: toAr(person.value.to_unit_date) },
  { key: 'unit_period_service', label: 'مدة الخدمة بالوحدة', value: unitPeriodService.value },
  { key: 'prnt_army_name', label: 'التبعية', value: person.value.prnt_army_name },
  { key: 'army_job_name', label: 'الوظيفة', value: person.value.army_job_name },
  { key: 'come_in_date', label: 'تاريخ التطوع', value: toAr(person.value.come_in_date) },
  {
    key: 'rateb_date',
    label: 'تاريخ صرف الراتب العالي',
    value: toAr(`${person.value.rateb_date}`),
  },
  {
    key: 'service_years',
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
    key: 'curr_degree_date',
    label: 'تاريخ الترقية الحالية',
    value: toAr(person.value.curr_degree_date, 'curr_degree_date'),
    click: () => openPopup('history'),
  },
  {
    key: 'upgrade_date',
    label: 'تاريخ الترقي المنتــظر',
    value: toAr(`${person.value.upgrade_date || '---'}`),
    fieldShowLabelStyle: {
      backgroundColor:
        new Date(person.value.upgrade_date).getTime() < new Date().getTime()
          ? 'rgba(163 226 255 )'
          : '',
    },
  },
  { key: 'address', label: 'العنوان المدني', value: fullAddress.value },
  { key: 'birth_date', label: 'تاريــخ الميــلاد', value: toAr(`${person.value.birth_date}`) || '---' },
  { key: 'age', label: 'السن', value: toAr(`${person.value.tot_years}`) || '---' },
  { key: 'length', label: 'الطول', value: toAr(`${person.value.length || '---'}`) || '---' },
  { key: 'weight', label: 'الوزن', value: toAr(`${person.value.weight || '---'}`) || '---' },
  {
    key: 'effecincy_avg',
    label: 'متوسط تقرير الكفاءة لاخر ثلاث سنوات',
    value:
      person.value?.effecincy_avg?.length > 0
        ? toAr(`${person.value?.effecincy_avg[0]?.grade}`)
        : 'لا يوجد',
    click: () => openPopup('eff'),
  },
  {
    key: 'over_weight',
    label: 'فرق الوزن',
    value: Number(person.value.over_weight)
      ? toAr(Number(person.value.over_weight)).split('-').reverse().join(' - ') + ' كجم '
      : 'لايكن',
  },
  {
    key: 'consistency',
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
    key: 'education',
    label: 'التاهيل',
    //value: person.value.education[person.value.education?.length - 1]?.dawra_name,
    value: person.value.education[0]?.dawra_name,
    click: () => openPopup('education'),
  },
])

const punishmentFields = computed(() => [
  {
    key: 'punishment_total',
    label: 'العقوبات',
    value: sta.value.tot_pa != 0 ? toAr(`${sta.value.tot_pa}`) : 'لايكن',
    click: () => openCourt(0),
  },
  {
    // v-if="sta.value.not_stay != 0 && punshiments.length > 0"
    key: 'punishment_not_stay',
    label: 'الحجز',
    value: sta.value.not_stay != 0 ? toAr(`${sta.value.not_stay}`) : 'لايكن',
    click: () => openCourt(1),
  },
  {
    // v-if="punishStayLength != 0 && punshiments.length > 0"
    key: 'punishment_stay',
    label: 'الحبس',
    value: sta.value.stay != 0 ? toAr(`${sta.value.stay}`) : 'لايكن',
    click: () => openCourt(2),
  },
  {
    // v-if="sta.value.court != 0 && punshiments.length > 0"
    key: 'punishment_military_court',
    label: 'محاكم عسكرية',
    value: sta.value.court != 0 ? toAr(`${sta.value.court}`) : 'لايكن',
    click: () => openCourt(3),
  },
  {
    // v-if="sta.value.other > 0 && punshiments.length > 0"
    key: 'punishment_civil_court',
    label: 'محاكم مدنية',
    value: sta.value.oth != 0 ? toAr(`${sta.value.oth}`) : 'لايكن',
    click: () => openCourt(4),
  },
])

const medicalFields = computed(() => [
  {
    key: 'medical_lagna',
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
    key: 'vacation_without_salary',
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
    key: 'travel_count',
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
    key: 'travel_last_country',
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
    key: 'travel_from',
    label: 'من',
    value:
      person.value.travel.length > 0
        ? toAr(
            `${person.value.travel[person.value.travel.length - 1].start_date != null ? person.value.travel[person.value.travel.length - 1].start_date : '---'}`,
            'medicalFields',
          )
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
  },
  {
    key: 'travel_to',
    label: 'الي',
    value:
      person.value.travel.length > 0
        ? toAr(
            `${person.value.travel[person.value.travel.length - 1].end_date != null ? person.value.travel[person.value.travel.length - 1].end_date : '---'}`,
            'medicalFields',
          )
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
  },
])

// const familyFields = computed(() => [
//   {
//     label: 'الحالة الاجتماعية',
//     value: person.value.marital_state_name
//       ? person.value.family_statistic[0].curr_marrige > 1
//         ? `(  ${toAr(person.value.family_statistic[0].curr_marrige)}  ) - ${person.value.marital_state_name}`
//         : person.value.marital_state_name
//       : 'لايكن',
//     // value: person.value.marital_state_name ? person.value.marital_state_name : 'لايكن',
//     click: () => openRelation([1, 15], 'current_marrige'),
//   },

const familyFields = computed(() => [
  {
    key: 'marital_state',
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
    // label: person.value.person_sex_code == 1 ? 'وظيفة الزوجة' : 'وظيفة الزوج',
    key: 'spouse_job',
    label: person.value.person_sex_code == 1 ? 'مؤهل/وظيفة الزوجة' : 'مؤهل/وظيفة الزوج',
    value:
      person.value.family_statistic.length > 0
        ? person.value.family_statistic[0]?.whife_job
        : 'لايكن',
  },
  {
    key: 'children_count',
    label: 'عدد الابناء',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.son + person.value.family_statistic[0]?.doughter)
        : 'لايكن',
    click: () => openRelation([2, 7], 'children'),
  },
  {
    key: 'sons',
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
    key: 'daughters',
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
    key: 'father_job',
    label: 'مؤهل/وظيفة الوالد',
    click: () => openRelation([3], 'father'),
    value:
      person.value.family_statistic.length > 0
        ? person.value.family_statistic[0]?.father_job
        : 'لايكن',
  },
  {
    key: 'mother_job',
    label: 'مؤهل/وظيفة الوالدة',
    click: () => openRelation([4], 'mother'),
    value:
      person.value.family_statistic.length > 0
        ? person.value.family_statistic[0]?.mother_job
        : 'لايكن',
  },
  {
    key: 'siblings',
    label: 'عدد الاشقاء',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.brother + person.value.family_statistic[0]?.sister)
        : 'لايكن',
    click: () => openRelation([5, 6], 'bro_sis'),
  },
  {
    key: 'relatives',
    label: 'عدد الاقارب',
    value:
      person.value.family_statistic.length > 0
        ? toAr(person.value.family_statistic[0]?.relativ)
        : 'لايكن',
    click: () => openRelation([11, 9, 10, 8], 'relatives'),
  },
  {
    key: 'prev_marriages',
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
  const res = await personsStore.fetchPersonInfo(id)
  person.value = res.data
  photos.value = res.data.photos || []
  punishments.value = res.data.person_punishment || []

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

onMounted(() => {
  // the saved expand state seeds the splitters, the user can still toggle them
  loadUiSettings(spliter)
  loadPerson()
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

/* أي محتوى آخر يظل بعد الأقسام */
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

@media (max-width: 992px) {
  .users {
    flex-direction: column;
  }

  .counters {
    width: 100%;
    max-width: 100%;
  }
}
</style>
