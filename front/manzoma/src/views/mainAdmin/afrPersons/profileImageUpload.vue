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

    <div id="capture-area">
      <!--  start user data  -->
      <div class="users">
        <div clas class="dataUser">
          <section-block
            v-if="load"
            :section-expand="spliter.primDataSpliter"
            @section-open="spliter.primDataSpliter = !spliter.primDataSpliter"
            title="البيانات الأساسية"
            :fields="basicFields"
          />
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
            :allowUploadImage="true"
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
import { useRoute } from 'vue-router'
import { usePersonsStore } from '@/stores/persons'
import { convertToArabicNumbers, getWsUrl } from '@/utils/glopal'

import pageNavigation from '@/components/global/pageNavigation.vue'
import pastUnits from '@/components/global/popup/past-units.vue'
import HistoryPopup from '@/components/global/popup/historyPopup.vue'
import eff_report from '@/components/global/popup/eff_report.vue'
import ImageUploadPanel from '@/components/mainAdmin/AfrPersons/ImageUploadPanel.vue'
import sectionBlock from '@/components/mainAdmin/AfrPersons/profile/sectionBlock.vue'
import { useAuthStore } from '@/stores/authStore'

const activePopup = ref(null)

const mainPhoto = computed(() => {
  const p = photos.value.find((p) => p.photo_type_code === 1)
  return p ? getWsUrl(p.photo_path) : null
})

const auth = useAuthStore()
const route = useRoute()
const id = route.params.id
const personsStore = usePersonsStore()
/* ================= STATE ================= */
const person = ref({})
const photos = ref([])
let load = ref(false)

// ---------- units ----------
let jobunits = ref([])
let jobsUnitsLength = ref(0)

const spliter = reactive({
  primDataSpliter: true,
  punnDataSpliter: true,
  medicalDataSpliter: true,
  famillyDataSpliter: true,
})

const popups = reactive({
  isVisiable: false,
  showImagePopup: false,
  HistoryIsVisiable: false,
  Eff_reportPopupVisible: false,
})

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
    value: toAr(person.value.unit_name, 'unit_name'),
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
    fieldShowLabelStyle: {
      backgroundColor:
        new Date(person.value.upgrade_date).getTime() < new Date().getTime()
          ? 'rgba(163 226 255 )'
          : '',
    },
  },
  { label: 'العنوان المدني', value: fullAddress.value },
  { label: 'تاريــخ الميــلاد', value: toAr(`${person.value.birth_date}`) || '---' },
  { label: 'السن', value: toAr(`${person.value.tot_years}`) || '---' },
  { label: 'الطول', value: toAr(`${person.value.length || '---'}`) || '---' },
  { label: 'الوزن', value: toAr(`${person.value.weight || '---'}`) || '---' },
  {
    label: 'متوسط تقرير الكفاءة لاخر ثلاث سنوات',
    value:
      person.value?.effecincy_avg?.length > 0
        ? toAr(`${person.value?.effecincy_avg[0]?.grade}`)
        : 'لا يوجد',
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
])

/* ================= ACTIONS ================= */
function openPopup(name) {
  activePopup.value = name
}
function closePopup() {
  activePopup.value = null
}
async function closeImageUploadPanel() {
  popups.showImagePopup = false
  await loadPerson()
}

function openImagePopup() {
  popups.showImagePopup = true
}

/* ================= LOAD ================= */
async function loadPerson() {
  load.value = false
  const res = await personsStore.fetchBasicPersonInfo(id)
  person.value = res.data

  photos.value = res.data.photos || []

  jobunits.value = [...(person.value.units || [])]
  jobsUnitsLength.value = person.value.units?.length
  load.value = true
}

onMounted(() => {
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

.users {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

/* البيانات الرئيسية */
.dataUser {
  flex: 1; /* تاخد كل المساحة المتبقية */
  min-width: 0; /* مهم عشان ما تكسرش flex */
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
  place-items: center;
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
