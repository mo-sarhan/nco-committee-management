<template>
  <div class="afrperson-container">
    <!-- <pageNavigation /> -->

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
      :showReasonPopup="activePopup === 'reason'"
      @close="closePopup"
      :tableData="personCommit.reasons_info"
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
      :tableData="person?.travel"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
    />
    <!-- :tableData="person.travel?.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))" -->
    <VotingDataPopup
      v-if="activePopup === 'voting'"
      @close="closePopup"
      :votes="votes"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      :votingInfo="personCommit.votes_info_test"
    />
    <StartVotingPopup
      v-if="activePopup === 'start_voting'"
      @close="closePopup"
      :votes="votes"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      @addVote="(voting) => addNewMemberVote(voting)"
    />
    <finalDecition
      v-if="activePopup === 'setFinalDecision'"
      @close="closePopup"
      :votes="votes"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
      @changeVote="(voting) => addNewMemberVote(voting)"
    />
    <ImageUploadPanel
      v-if="activePopup === 'photo'"
      @close="closePopup"
      :photos="filteredPhotos"
      :allowUploadImage="false"
      :mil_sir="id"
    />
    <SecPerson
      v-if="activePopup === 'sec_situation'"
      :showPopup="activePopup === 'sec_situation'"
      @close="closePopup"
      :tableData="person.security"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
    />
    <reportPopub
      v-if="appearReport"
      :tableFields="ReportTableFields"
      :mainLagnaName="ReportMainLagnaName"
      :lagnaNameType="ReportLagnaNameType"
      :stikyHeader="true"
      @close="closeReportPopup"
    />
    <DescitionNotesPopup
      v-if="activePopup === 'desitin_notes'"
      :showPopup="activePopup === 'desitin_notes'"
      @close="closePopup"
      :desc="decision"
      :userNamePer="person.person_name"
      :degree="person.degree_name"
    />

    <InspireWorkReport
      v-if="isInspireWorkReportOpen"
      @close="isInspireWorkReportOpen = false"
      :person_id="currentPerson.comm_data?.person_id"
      :person="person"
    />

    <inspireWorkShow
      v-if="activePopup === 'inspire_work'"
      :degree="person.degree_name"
      :userNamePer="person.person_name"
      :showReasonPopup="activePopup === 'inspire_work'"
      @close="closePopup"
      :tableData="person.psycholgical_report"
    />

    <!-- <Acceptpop
      :userNamePer="persona?.person_name"
      :degree="person?.degree_name"
      :showReasonPopup="true"
      @close="closePopup"
      :tableData="
        person.vote_1.sort((a, b) => {
          a.priority_number > b.priority_number
        })
      "
      :tableDataٍSec="
        person.vote_2.sort((a, b) => {
          a.priority_number > b.priority_number
        })
      "
    /> -->

    <!-- <OpinionManager
      :personName="person.person_name"
      :personDegree="person.degree_name"
      :showPersonPopup="true"
      @close="closePopup"
      :mil="person.mil_ser"
      ref="pop"
    /> -->
    <!-- v-if="this.member == 'رئيس هيئة التنظيم والإدارة للقوات المسلحة'" -->
    <!-- <poea
      :showPopup="true"
      @close="closePopup"
      :tableData="personData.peo_reason"
      :userNamePer="personData.person_name"
      :unit_name="personData.unit_name"
      :degree="personData.degree_name"
    /> -->

    <div id="capture-area">
      <div class="wating-window nouser" v-if="!currentPerson.comm_data?.person_id">
        <div class="wating-logo">
          <img src="/src/assets/Images/شعار الهيئه.png" alt="Logo" />
        </div>
        <h1>هيئة التنظيم والإدارة ق.م</h1>
      </div>
      <!--  start user data  -->
      <div class="users" v-else>
        <!-- ================= DATA ================= -->
        <div class="subHeader">
          <div class="hayaLogo">
            <img src="@/assets/Images/logo.png" alt="logo" width="50px" />
            <h1>هيئة التنظيم والإدارة ق.م</h1>
          </div>
          <div class="lagnaName">
            <p>{{ personCommit.root_committe_name }}</p>
          </div>
        </div>
        <div class="mainUserData">
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
                :withoutGrid="true"
              />
            </div>
            <!-- :section-expand="spliter.punnDataSpliter" -->
            <div class="section-slot" :style="{ order: sectionOrder('punishment') }">
              <section-block
                title="العقوبات"
                :fields="punishmentFields"
                v-if="load && isSectionVisible('punishment')"
                :page-key="PAGE_KEY"
                section-key="punishment"
                @section-open="spliter.punnDataSpliter = !spliter.punnDataSpliter"
                :withoutGrid="true"
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
                >
                  <!-- جهاز العمل النفسى sits next to the unpaid leave card -->
                  <template v-slot:additionFields>
                    <div
                      v-if="person.psycholgical_report.length > 0"
                      style="display: flex; align-items: center; justify-content: center"
                    >
                      <button class="btn btn-primary" @click="openPopup('inspire_work')">
                        جهاز العمل النفسى
                      </button>
                    </div>
                  </template>
                </section-block>
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
                :withoutGrid="true"
              />
            </div>

            <!-- سبب العرض - only for لجان عدم الصلاحية -->
            <div
              class="section-slot"
              :style="{ order: sectionOrder('presenting_reason') }"
              v-if="isUnfitnessCommitte"
            >
              <section-block
                title="سبب العرض"
                :fields="presentingReasonFields"
                v-if="load && isSectionVisible('presenting_reason')"
                :page-key="PAGE_KEY"
                section-key="presenting_reason"
                :section-expand="spliter.presentingReasonSpliter"
                @section-open="spliter.presentingReasonSpliter = !spliter.presentingReasonSpliter"
                :withoutGrid="true"
              />
            </div>

            <!-- :section-expand="spliter.reasonDataSpliter" -->
            <div class="section-slot" :style="{ order: sectionOrder('reasons') }">
              <section-block
                :title="reasonsTitle"
                :fields="reasonsFields"
                v-if="load && isSectionVisible('reasons')"
                :page-key="PAGE_KEY"
                section-key="reasons"
                @section-open="spliter.reasonDataSpliter = !spliter.reasonDataSpliter"
              />
            </div>

            <!-- :section-expand="spliter.famillyDataSpliter" -->
            <div class="section-slot" :style="{ order: sectionOrder('family') }">
              <section-block
                title="البيانات الإجتماعية"
                :fields="familyFields"
                v-if="load && isSectionVisible('family')"
                :page-key="PAGE_KEY"
                section-key="family"
                @section-open="spliter.famillyDataSpliter = !spliter.famillyDataSpliter"
                :withoutGrid="true"
              />
            </div>
            <!-- :section-expand="spliter.priviousDecisionsDataSpliter" -->

            <!--               v-if="personCommit?.snap_info?.opinions.length > 0" -->
            <div class="section-slot" :style="{ order: sectionOrder('lagna_decisions') }">
            <section-block
              title="الآراء"
              :fields="lagnaDecisionFields"
              v-if="isSectionVisible('lagna_decisions')"
              :page-key="PAGE_KEY"
              section-key="lagna_decisions"
              @section-open="
                spliter.priviousDecisionsDataSpliter = !spliter.priviousDecisionsDataSpliter
              "
              :withoutGrid="true"
            >
              <template v-slot:additionFields>
                <!-- <fieldShow
                  fieldShowLabel="رأى رئيس هيئة التنظيم و الادارة"
                  :fieldShowLabelStyle="{
                    background: '#6d6d6d',
                    color: 'white',
                    minWidth: 'max-content',
                  }"
                  :fieldShowDataStyle="{
                    background: 'white',
                    // color: 'white',
                  }"
                  :actionFlag="true"
                >
                  <template v-slot:actionData>
                    <select
                      v-model="selectedFinalDecision"
                      class="final-select"
                      @change="saveFinalDecision($event.target.value)"
                    >
                      <option disabled value="">-- اختر الرأى --</option>

                      <option
                        v-for="vote in personsStore.votesTypes"
                        :key="vote?.opinion_code"
                        :value="vote?.opinion_code"
                      >
                        {{ vote.opinion_name }}
                      </option>
                    </select>
                  </template>
                </fieldShow> -->
                <fieldShow
                  :fieldShowLabel="
                    'قرار ' +
                    (personCommit.comm_header?.profile?.job
                      ? personCommit.comm_header?.profile?.job
                      : 'لم يتم وضع رئيس اللجنة')
                  "
                  :fieldShowStyle="{
                    width: 'fit-content',
                  }"
                  :fieldShowLabelStyle="{
                    background: '#0a820f',
                    color: 'white',
                    width: 'max-content',
                    padding: '10px 12px',
                  }"
                  :fieldShowDataStyle="{
                    background: 'white',
                    borderRadius: '10px',
                    width: '0%',
                    // color: 'white',
                  }"
                  :actionFlag="true"
                  @click="open_final_decision ? openPopup('setFinalDecision') : () => {}"
                >
                  <template v-slot:actionData>
                    <div class="final-select">
                      <span style="width: 200px" :class="voteClass(finalDecision?.opinion_code)">
                        {{ finalDecision?.opinion_name ? finalDecision?.opinion_name : ' ' }}
                      </span>
                    </div>

                    <!-- <select
                      :disabled="authStore.user.info.username !== 'manager'"
                      v-model="selectedFinalDecision"
                      class="final-select"
                      @change="saveFinalDecision($event.target.value)"
                    >
                      <option value="0">بدون</option>

                      <option
                        v-for="vote in personsStore.votesTypes"
                        :key="vote?.opinion_code"
                        :value="vote?.opinion_code"
                      >
                        {{ vote.opinion_name }}
                      </option>
                    </select> -->
                  </template>
                </fieldShow>
                <!-- <div v-if="spliter.finalDecisionSpliter" class="final-decision-box">
                  <div class="final-select-wrapper">
                    <div>
                      <label class="final-label"> اختيار القرار النهائي </label>
                    </div>

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
              </template>
            </section-block>
            </div>

            <div class="Lagna-oreder-container">
              <p class="Lagna-oreder">
                {{ convertToArabicNumbers(personCommit?.committe_order) }} /
                {{ convertToArabicNumbers(personCommit?.comm_total) }}
              </p>
            </div>

            <!-- ================= FINAL DECISION VOTING ================= -->
            <!-- <SecSpliter
              splitTitle="التصويت والقرار النهائي"
              @expand="spliter.finalDecisionSpliter = !spliter.finalDecisionSpliter"
            /> -->
          </div>

          <div class="counters">
            <!-- avatar / image -->
            <div class="image-item" @click="openPopup('photo')">
              <img
                v-if="mainPhoto"
                :src="mainPhoto"
                crossorigin="anonymous"
                class="preview"
                alt="user image"
              />

              <div v-else class="avatar-placeholder">
                <span>{{ avatarLetter }}</span>
              </div>
            </div>

            <!-- commititColors[personLagnaData?.committe_type.type_id]
                  ? commititColors[personLagnaData?.committe_type.type_id]['style']
                  :  -->
            <div class="rejection_data" style>
              <div class="traq" v-if="personCommit?.committe_type.type_id" style="color: #b7281e">
                <p>{{ personCommit?.committe_type.type_name }}</p>
              </div>
            </div>

            <div class="votes-box" v-if="votes?.length > 0">
              <div
                v-for="(vote, index) in votes"
                :key="index"
                class="vote-item"
                @mouseenter="activeTooltip = index"
                @mouseleave="activeTooltip = null"
              >
                <!-- اسم التصويت -->
                <div class="vote-header">
                  <p class="vote-name">{{ vote.vote_name }}</p>
                  <p class="vote-percent">{{ vote.percent }}%</p>
                </div>

                <!-- Progress Bar -->
                <div class="vote-bar-wrapper">
                  <div
                    class="vote-bar"
                    :class="getVoteClass(vote.vote_name)"
                    :style="{ width: vote.percent + '%' }"
                  ></div>
                </div>

                <!-- العدد -->
                <div class="vote-footer">
                  <p class="vote-number" @click.stop="toggleTooltip(index)">
                    {{ vote.vote_count }} صوت
                  </p>
                </div>

                <!-- Tooltip -->
                <transition name="fade">
                  <div v-if="activeTooltip === index" class="tooltip-box">
                    <div class="tooltip-title">المصوتين</div>

                    <div v-for="(voter, i) in vote.voters" :key="i" class="tooltip-item">
                      {{ voter.rank }} / {{ voter.full_name }}
                    </div>
                  </div>
                </transition>
              </div>
            </div>

            <button
              v-if="votes?.length > 0 && 2 < 1"
              class="show-votes-btn"
              @click="openPopup('voting')"
            >
              عرض نتيجة التصويت
            </button>

            <!-- <button v-if="true" class="show-votes-btn" @click="openVotingPopup = !openVotingPopup">
              بداء التصويت
            </button> -->

            <!-- popup -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useLagnaStore } from '@/stores/lagna'
import { usePersonsStore } from '@/stores/persons'
import { convertToArabicNumbers, getWsUrl } from '@/utils/glopal'
import {
  useUiSettingsPage,
  PRESENTING_PAGE_KEY,
  PRESENTING_SPLITTERS,
} from '@/composables/useUiSettingsPage'
import html2canvas from 'html2canvas'
// import { jsPDF } from "jspdf"

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
import OpinionsSection from '@/components/mainAdmin/AfrPersons/profile/OpinionsSection.vue'
import Courses from '@/components/global/popup/courses.vue'
import InspireWorkReport from '../../mainAdmin/lagna/inspireWorkReport.vue'
import Poea from '@/components/global/popup/Poea.vue'
import Acceptpop from '@/components/global/popup/acceptpop.vue'
import VotingDataPopup from '@/components/global/popup/votingDataPopup.vue'
import StartVotingPopup from '@/components/global/popup/StartVotingPopup.vue'
import finalDecition from '@/components/global/popup/finalDecition.vue'
import SecPerson from '@/components/global/popup/sec-person.vue'
import DescitionNotesPopup from '@/components/global/popup/descitionNotesPopup.vue'
import ReasonsPopup from '@/components/global/popup/reasonsPopup.vue'
import inspireWorkShow from '@/components/global/popup/inspireWorkShow.vue'
import reportPopub from '@/components/global/popup/reportPopub.vue'
import fieldShow from '@/components/mainAdmin/AfrPersons/profile/fieldShow.vue'
import SecSpliter from '../../../components/mainAdmin/AfrPersons/profile/secSpliter.vue'
import { useAuthStore } from '@/stores/authStore.js'

const route = useRoute()
const lagnaStore = useLagnaStore()
const personsStore = usePersonsStore()
const authStore = useAuthStore()
console.log('route.params', route.params)
const committe_code = Number(route.params.committe_code)
const spacific_id = Number(route.params.spacific_id)
const activePopup = ref(null)
const open_final_decision = ref(false)
const selectedFinalDecision = ref('')
const finalDecision = ref({})
const mainPhoto = computed(() => {
  const p = photos.value.find((p) => p.photo_type_code === 1)
  return p ? getWsUrl(p.photo_path) : null
})

/* ================= STATE ================= */
const openVotingPopup = ref(false)
const appearReport = ref(false)
const isWatingToDownload = ref(false)
const ReportMainLagnaName = ref('')
const ReportLagnaNameType = ref('')
const isInspireWorkReportOpen = ref(false)
const currentPerson = ref({})
const lagnaArmyReport = ref({})
const person = ref({})
const personCommit = ref({})
const punishments = ref([])
const votes = ref([])
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
const decision = ref({})

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
  priviousDecisionsDataSpliter: true,
  finalDecisionSpliter: true,
  travelDataSpliter: true,
  reasonDataSpliter: true,
  presentingReasonSpliter: true,
})

/* ================= UI SETTINGS ================= */
// this screen has its own layout, separate from the profile screens
const PAGE_KEY = PRESENTING_PAGE_KEY
const { sectionOrder, isSectionVisible, loadUiSettings } = useUiSettingsPage(
  PRESENTING_PAGE_KEY,
  PRESENTING_SPLITTERS,
)

const popups = reactive({
  isVisiable: false,
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
let showVotesPopup = ref(false)

// const votes = ref([
//   {
//     vote_name: 'عدم استمرار',
//     vote_count: 3,
//     voters: [
//       { rank: 'اللواء', name: 'محمد صبحى' },
//       { rank: 'اللواء', name: 'محمد صبحى' },
//       { rank: 'اللواء', name: 'محمد صبحى' },
//     ],
//   },
//   {
//     vote_name: 'استمرار',
//     vote_count: 3,
//     voters: [
//       { rank: 'اللواء', name: 'محمد صبحى' },
//       { rank: 'اللواء', name: 'محمد صبحى' },
//       { rank: 'اللواء', name: 'محمد صبحى' },
//     ],
//   },
// ])

const activeTooltip = ref(null)

// const totalVotes = () => votes.value.reduce((sum, v) => sum + v.vote_count, 0)

// const getPercentage = (count) => {
//   const total = totalVotes()
//   return total ? Math.round((count / total) * 100) : 0
// }

const getVoteClass = (name) => {
  if (!name) return 'accepted'
  // if (name.includes('استمرار')) return 'accepted'
  // if (name.includes('عدم')) return 'rejected'
  return 'accepted'
}

const toggleTooltip = (index) => {
  activeTooltip.value = activeTooltip.value === index ? null : index
}

const handleClickOutside = () => {
  activeTooltip.value = null
}

function addNewInspireWorkReport() {
  isInspireWorkReportOpen.value = true
}
// ----------------- methods ------------------
const avatarLetter = computed(() =>
  person.value.person_name ? person.value.person_name.charAt(0) : '؟',
)

const fullAddress = computed(() => {
  return `${person.value.person_adress || '---'} - ${person.value.markaz_name || '--'} - ${person.value.mohafza_name || '--'}`
})
const unitPeriodService = computed(() => {
  return `${person.value.unit_interval_m == 0 && person.value.unit_interval_y == 0 ? `${toAr(person.value.unit_interval_d)} يوم` : ''} ${person.value.unit_interval_m == 0 ? '' : ` ${toAr(`${person.value.unit_interval_m || '---'}`)} شهر `} ${person.value.unit_interval_y == 0 ? '' : ` ${person.value.unit_interval_y == 0 ? '' : '/'}`} ${person.value.unit_interval_y == 0 ? '' : `${toAr(`${person.value.unit_interval_y || '---'} سنه`)}`}`
})

const numYearsOfServices = computed(() => {
  return `${person.value.tot_ser_m == 0 ? '' : ` ${toAr(`${person.value.tot_ser_m || '---'}`)} شهر `} ${person.value.tot_ser_y == 0 ? '' : ` ${person.value.tot_ser_m == 0 ? '' : '/'}  `} ${person.value.tot_ser_y == 0 ? '' : `${toAr(`${person.value.tot_ser_y || '---'} سنه`)}`}`
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

const filteredPhotos = computed(() => {
  console.log('photos.value', photos.value)
  return photos.value
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

// عدم الصلاحية is committee type 1; only then is سبب العرض shown
const UNFITNESS_COMMITTE_TYPE = 1
const isUnfitnessCommitte = computed(
  () => Number(personCommit.value?.committe_type?.type_id) === UNFITNESS_COMMITTE_TYPE,
)

const presentingReasonFields = computed(() => [
  {
    key: 'presenting_reason',
    label: 'سبب العرض',
    value: personCommit.value?.snap_info?.add_reason || 'لايكن',
    fieldShowDataStyle: {
      whiteSpace: 'pre-wrap',
      textAlign: 'start',
    },
  },
])

// لجان عدم الصلاحية show سبب العرض separately, so this block becomes the
// opinions summary there; every other committee keeps calling it الاسباب
const reasonsTitle = computed(() => (isUnfitnessCommitte.value ? 'ملخص الاراء' : 'الاسباب'))

const reasonsFields = computed(() => [
  {
    key: 'reasons_summary',
    label: reasonsTitle.value,
    // value: personsStore.reasons[personsStore.reasons?.length - 1]?.descrption,
    value:
      personCommit.value.reasons_info.length > 0
        ? personCommit.value.reasons_info.at(-1)?.descrption
        : 'لايكن',
    click: () => openPopup('reason'),
    danger: true,
    fieldShowDataStyle: {
      maxWidth: personCommit.value.reasons_info.length == 0 ? '400px' : '',
    },
  },
])

const filteredRelations = computed(() => person.value.family_info[relationLabel.value] || [])

const sortedConsistencies = computed(() =>
  [...(person.value.consistancies || [])].sort(
    (a, b) => new Date(b.check_date) - new Date(a.check_date),
  ),
)

function toAr(number, numKey = 'notFound') {
  if (number === null || number === undefined) return '---'
  return convertToArabicNumbers(number)
}

const votesOptions = computed(() => {
  let options = []
  personsStore.votesTypes.forEach((e) => {
    options.push({
      label: e.opinion_name,
      value: e.opinion_code,
    })
  })
  return options
})
const commititColors = computed(() => {
  return {
    1: { style: 'color:#b7281e' },
    2: { style: 'color:#b7281e' },
    3: { style: 'color:#b7281e' },
    4: { style: 'color:#b7281e' },
    5: { style: 'color:#b7281e' },
  }
})
/* ================= FIELD CONFIGS ================= */
// const basicFields = computed(() => [
//   { label: 'الرقم العسكري', value: toAr(person.value.mil_no, 'mil_no') },
//   { label: 'الدرجة', value: person.value.degree_name },
//   { label: 'الاسم', value: person.value.person_name },
//   { label: 'السلاح', value: person.value.army_name },
//   { label: 'تبعية الوحدة', value: person.value.prnt_army_name },
//   { label: 'الفئة', value: person.value.fea_name },
//   { label: 'الوظيفة', value: person.value.army_job_name },
//   { label: 'تاريخ التطوع', value: toAr(person.value.come_in_date) },
//   { label: 'تاريخ صرف الراتب العالي', value: toAr(`${person.value.rateb_date}`) },
//   {
//     label: 'عدد سنوات الخدمة',
//     value: numYearsOfServices.value,
//     fieldShowLabelStyle: {
//       background: '#ffc107',
//     },
//   },
//   {
//     label: 'تاريخ الترقية الحالية',
//     value: toAr(person.value.curr_degree_date, 'curr_degree_date'),
//     click: () => openPopup('history'),
//   },
//   {
//     label: 'تاريخ الترقي المنتــظر',
//     value: toAr(`${person.value.upgrade_date || '---'}`),
//     fieldShowStyle: {
//       backgroundColor:
//         new Date(person.value.upgrade_date).getTime() < new Date().getTime()
//           ? 'rgba(163 226 255 )'
//           : 'white',
//     },
//   },
//   {
//     label: 'الوحدة',
//     value: person.value.unit_name,
//     click: () => openPopup('units'),
//   },
//   { label: 'تاريــخ الضم علي الوحدة', value: toAr(person.value.to_unit_date) },

//   { label: 'مدة الخدمة بالوحدة', value: unitPeriodService.value },
//   { label: 'تاريــخ الميــلاد', value: toAr(`${person.value.birth_date}`) || '---' },
//   { label: 'العنوان المدني', value: fullAddress.value },
//   {
//     label: 'متوسط تقرير الكفاءة لاخر ثلاث سنوات',
//     value:
//       person.value?.effecincy_avg?.length > 0 ? person.value?.effecincy_avg[0]?.grade : 'لا يوجد',
//     click: () => openPopup('eff'),
//     fieldShowLabelStyle: {
//       fontSize: '13px',
//       background: '#faa23c',
//       cursor: 'pointer',
//     },
//   },
//   {
//     label: 'التاهيل',
//     // value: person.value.education[person.value.education?.length - 1]?.dawra_name,
//     // value: person.value.education[0]?.dawra_name,

//     value: person.value.education.length > 0 ? 'مؤهل' : 'غير مؤهل',
//     click: () => openPopup('education'),
//   },
//   {
//     label: 'الموقف الامنــي',
//     value: person.value?.security.length > 0 ? 'يـوجــد' : 'لا يـوجــد',
//     click: () => openPopup('sec_situation'),
//     fieldShowLabelStyle: {
//       background: '#d63024',
//       color: 'white',
//     },
//   },

//   { label: 'السن', value: toAr(`${person.value.tot_years}`) || '---' },
//   { label: 'الطول', value: toAr(`${person.value.length || '---'}`) || '---' },
//   { label: 'الوزن', value: toAr(`${person.value.weight || '---'}`) || '---' },
//   {
//     label: 'فرق الوزن',
//     value: Number(person.value.over_weight)
//       ? toAr(Number(person.value.over_weight)) + ' كجم  '
//       : 'لايكن',
//   },

//   {
//     label: 'التناسق',
//     value:
//       (person.value.consis_name ? person.value.consis_name : 'لايكن') +
//       ' (طبقا لمعدل الكتلة الجسمانية) ',
//     fieldShowLabelStyle: {
//       background: person.value.consis != 0 ? '#0a820f' : '#d63024',
//       color: person.value.consis != 0 ? 'white' : 'white',
//     },
//   },
// ])

const basicFields = computed(() => [
  {
    key: 'mil_no',
    label: 'الرقم العسكري',
    value: toAr(person.value.mil_no, 'mil_no'),
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'come_in_date',
    label: 'تاريخ التطوع',
    value: toAr(person.value.come_in_date),
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'curr_degree_date',
    label: 'تاريخ الترقية الحالية',
    value: toAr(person.value.curr_degree_date, 'curr_degree_date'),
    click: () => openPopup('history'),
    fieldShowLabelStyle: {
      minWidth: '160px',
      background: '#faa23c',
    },
  },
  {
    key: 'birth_date',
    label: 'تاريــخ الميــلاد',
    value: toAr(`${person.value.birth_date}`) || '---',
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'length',
    label: 'الطول',
    value: toAr(`${person.value.length || '---'}`) || '---',
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },

  {
    key: 'degree_name',
    label: 'الدرجة',
    value: person.value.degree_name,
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'rateb_date',
    label: 'تاريخ صرف الراتب العالي',
    value: toAr(`${person.value.rateb_date}`),
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'upgrade_date',
    label: 'تاريخ الترقي المنتــظر',
    value: toAr(`${person.value.upgrade_date || '---'}`),
    fieldShowStyle: {
      backgroundColor:
        new Date(person.value.upgrade_date).getTime() < new Date().getTime()
          ? 'rgba(163 226 255 )'
          : 'white',
    },
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'age',
    label: 'السن',
    value: toAr(`${person.value.tot_years}`) || '---',
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'weight',
    label: 'الوزن',
    value: toAr(`${person.value.weight || '---'}`) || '---',
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },

  {
    key: 'person_name',
    label: 'الاسم',
    value: person.value.person_name,
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'service_years',
    label: 'عدد سنوات الخدمة',
    value: numYearsOfServices.value,
    fieldShowLabelStyle: {
      background: 'rgb(217 217 217)',
      minWidth: '160px',
      // border: '1px solid green',

      border: ' 5px solid green',
    },
  },
  {
    key: 'education',
    label: 'التاهيل',
    // value: person.value.education[person.value.education?.length - 1]?.dawra_name,
    // value: person.value.education[0]?.dawra_name,

    value: person.value.education.length > 0 ? 'مؤهل' : 'غير مؤهل',
    click: () => openPopup('education'),
    fieldShowLabelStyle: {
      minWidth: '160px',
      background: '#faa23c',
    },
  },
  { key: 'address', label: 'العنوان المدني', value: fullAddress.value },
  {
    key: 'over_weight',
    label: 'فرق الوزن',
    value: Number(person.value.over_weight)
      ? toAr(Number(person.value.over_weight)) + ' كجم  '
      : 'لايكن',
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },

  {
    key: 'unit_name',
    label: 'الوحدة',
    value: person.value.unit_name,
    click: () => openPopup('units'),
    fieldShowLabelStyle: {
      minWidth: '160px',
      background: '#faa23c',
    },
  },
  {
    key: 'unit_prnt_name',
    label: 'تبعية الوحدة',
    value: person.value.prnt_army_name,
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'to_unit_date',
    label: 'تاريــخ الضم علي الوحدة',
    value: toAr(person.value.to_unit_date),
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'army_name',
    label: 'السلاح',
    value: person.value.army_name,
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },

  {
    key: 'consistency',
    label: 'التناسق',
    value:
      (person.value.consis_name ? person.value.consis_name : 'لايكن') +
      ' (طبقا لمعدل الكتلة الجسمانية) ',
    fieldShowLabelStyle: {
      // background: person.value.consis != 0 ? '#0a820f' : '#d63024',
      border: person.value.consis != 0 ? '5px solid #0a820f' : '5px solid #d63024',
      color: person.value.consis != 0 ? 'black' : 'black',
      minWidth: '160px',
    },
  },

  {
    key: 'army_job_name',
    label: 'الوظيفة',
    value: person.value.army_job_name,
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'fea_name',
    label: 'الفئة',
    value: person.value.fea_name,
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'unit_period_service',
    label: 'مدة الخدمة بالوحدة',
    value: unitPeriodService.value,
    fieldShowLabelStyle: {
      minWidth: '160px',
    },
  },
  {
    key: 'security_status',
    label: 'الموقف الامنــي',
    value: person.value?.security.length > 0 ? 'يـوجــد' : 'لا يـوجــد',
    click: () => openPopup('sec_situation'),
    fieldShowLabelStyle: {
      background: '#d63024',
      color: 'white',
      minWidth: '160px',
    },
  },
  {
    key: 'effecincy_avg',
    label: 'متوسط تقرير الكفاءة لاخر ثلاث سنوات',
    value:
      person.value?.effecincy_avg?.length > 0 ? person.value?.effecincy_avg[0]?.grade : 'لا يوجد',
    click: () => openPopup('eff'),
    fieldShowLabelStyle: {
      fontSize: '13px',
      background: '#faa23c',
      cursor: 'pointer',
      minWidth: '160px',
    },
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
    label: 'المحكمة',
    value: sta.value.court != 0 ? toAr(`${sta.value.court}`) : 'لايكن',
    click: () => openCourt(3),
  },
  {
    // v-if="sta.value.other > 0 && punshiments.length > 0"
    key: 'punishment_civil_court',
    label: 'المحكمة المدنية',
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
      // minWidth: '660px',
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
            `${person.value.travel[0].start_date != null ? person.value.travel[0].start_date : 'لايكن'}`,
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
            `${person.value.travel[0].end_date != null ? person.value.travel[0].end_date : 'لايكن'}`,
            'medicalFields',
          )
        : 'لايكن',
    click: () => openPopup('travel'),
    danger: true,
  },
])

const familyFields = computed(() => [
  {
    key: 'marital_state',
    label: 'الحالة الاجتماعية',
    value: person.value.marital_state_name
      ? person.value.family_statistic[0].curr_marrige > 1
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
    // label: 'وظيفة الوالد',
    key: 'father_job',
    label: 'مؤهل/وظيفة الوالد',
    click: () => openRelation([3], 'father'),
    value:
      person.value.family_statistic.length > 0
        ? person.value.family_statistic[0]?.father_job
        : 'لايكن',
  },
  {
    // label: 'وظيفة الوالده',
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

const lagnaDecisionFields = computed(() => {
  return personCommit?.value?.snap_info?.opinions.map((dec) => ({
    label: dec.opinion_type_data?.opinion_name,
    value: dec.opinion_data?.opinion_name ? dec?.opinion_data?.opinion_name : ' ',
    // fieldShowDataStyle: {
    //   backgroundColor: decisionColor(op.opinion_code),
    //   fontWeight: '600',
    // },
    click: () => openDesitinNotes(dec),
  }))
})

function decisionColor(code) {
  switch (code) {
    case 1:
      return 'rgba(111, 255, 166, 0.5)' // قبول
    case 2:
      return 'rgba(255, 111, 111, 0.5)' // رفض
    default:
      return 'rgba(200,200,200,0.4)'
  }
}

const ReportTableFields = computed((row) => {
  return {
    tabs: [
      {
        key: 'by_person_army',
        label: 'السلاح',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_army_name',
            value: (row, index, isTotal) => (isTotal ? '' : row.person_army_name),
            key1: 'person_army_name',
            label: 'السلاح',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'by_person_prnt_army',
        label: 'التبعية',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_prnt_army_name',
            value: (row) => row.person_prnt_army_name,
            key1: 'person_prnt_army_name',
            label: 'التبعية',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'by_prnt_a_army',
        label: 'السلاح / التبعية',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 3 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_army_name',
            value: (row) => row.person_army_name,
            key1: 'person_army_name',
            label: 'السلاح',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'person_prnt_army_name',
            value: (row) => row.person_prnt_army_name,
            key1: 'person_prnt_army_name',
            label: 'التبعية',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',
            // RowsMerge: 2,
            ColsMerge: 2,

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'by_serv_army',
        label: 'الخدمة',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 2 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_serv_name',
            value: (row) => row.person_serv_name,
            key1: 'person_serv_name',
            label: 'الخدمة',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
      {
        key: 'all',
        label: 'السلاح / التبعية / الخدمة',
        data: 'army_report',
        columns: [
          {
            key: 'index',
            label: 'م',
            // hRowspan: 3,
            colColspan: (row, index, isTotal) => (isTotal ? 4 : 1),
            value: (row, index, isTotal) => (isTotal ? row.person_army_name : index + 1),
          },
          {
            key: 'person_army_name',
            value: (row) => row.person_army_name,
            key1: 'person_army_name',
            label: 'السلاح',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'person_prnt_army_name',
            value: (row) => row.person_prnt_army_name,
            key1: 'person_prnt_army_name',
            label: 'التبعية',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'person_serv_name',
            value: (row) => row.person_serv_name,
            key1: 'person_serv_name',
            label: 'الخدمة',
            hide: (row, index, isTotal) => isTotal,
            rowClickable: true,
          },
          {
            key: 'st_10',
            value: (row) => row.st_10,
            label: 'تسجيل',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_20',
            value: (row) => row.st_20,
            label: 'مراجعة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_30',
            value: (row) => row.st_30,
            label: 'تصديق دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_40',
            value: (row) => row.st_40,
            label: 'منتظر إنعقاد اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_50',
            value: (row) => row.st_50,
            label: 'حضور اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_60',
            value: (row) => row.st_60,
            label: 'عدم الحضور',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_70',
            value: (row) => row.st_70,
            label: 'مثول امام اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'st_99',
            value: (row) => row.st_99,
            label: 'لم يصدق على دخول اللجنة',

            rowClickable: true,
            copyable: true,
          },
          {
            key: 'total',
            value: (row) => row.total,
            label: 'الإجمالي',

            rowClickable: true,
            copyable: true,
          },
        ],
      },
    ],
    reportData: null,
  }
})

async function appearLagnaReport() {
  console.log('valuepppppppppp', currentPerson.value.comm_report)
  ReportMainLagnaName.value = currentPerson.value.comm_report.root_committe_name
  ReportLagnaNameType.value = currentPerson.value.comm_report.committe_type.type_name
  // let reportData = await store.fetchCommittReports(row.committe_code, row.lagna_type_id)
  ReportTableFields.value.reportData = currentPerson.value.comm_report.army_report
  appearReport.value = true
  console.log(
    'agnaArmyReport.value.lagna_report[0].army_report =======>',
    currentPerson.value.comm_report.army_report,
  )
}
function closeReportPopup() {
  appearReport.value = false
}
async function saveFinalDecision(final_decision) {
  console.log('final_decision', final_decision)
  try {
    await personsStore.setFinalDecision(
      personCommit.value.comms_codes.committe_code,
      personCommit.value.comms_codes.committe_type,
      personCommit.value.person_id,
      {
        vote: final_decision,
      },
    )

    // await personsStore.addSpecificsPersonOpinions(
    //   personCommit.value.comms_codes.committe_code,
    //   personCommit.value.comms_codes.committe_type,
    //   personCommit.value.person_id,
    //   {
    //     opinion_code: final_decision,
    //     opinion_type: 7,
    //   },
    // )

    await personsStore.fetchPersonOpinions(
      personCommit.value.comms_codes.committe_code,
      personCommit.value.comms_codes.committe_type,
      personCommit.value.person_id,
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

async function addNewMemberVote(final_decision) {
  console.log('final_decision', final_decision)
  try {
    await personsStore.setFinalDecision(
      personCommit.value.comms_codes.committe_code,
      personCommit.value.comms_codes.committe_type,
      personCommit.value.person_id,
      {
        vote: final_decision,
      },
    )

    // await personsStore.addSpecificsPersonOpinions(
    //   personCommit.value.comms_codes.committe_code,
    //   personCommit.value.comms_codes.committe_type,
    //   personCommit.value.person_id,
    //   {
    //     opinion_code: final_decision,
    //     opinion_type: 7,
    //   },
    // )

    // await personsStore.fetchPersonOpinions(
    //   personCommit.value.comms_codes.committe_code,
    //   personCommit.value.comms_codes.committe_type,
    //   personCommit.value.person_id,
    // )

    swal({
      title: 'تم الحفظ',
      text: 'تم حفظ التصويت بنجاح',
      icon: 'success',
      timer: 1200,
      button: false,
    })

    closePopup()
  } catch (error) {
    console.log(error)
    swal({
      title: 'خطأ',
      text: error.response.data.details,
      icon: 'error',
    })
  }
}
/* ================= ACTIONS ================= */
function openPopup(name) {
  console.log('person.value', person.value)
  if (currentPerson.value.length == 0) return
  activePopup.value = name
}
function closePopup() {
  activePopup.value = null
}
function openCourt(type) {
  if (currentPerson.value.length == 0) return
  courtType.value = type
  openPopup('court')
}
function openRelation(types, label) {
  if (currentPerson.value.length == 0) return
  relationTypes.value = types
  relationLabel.value = label
  openPopup('relation')
}
function openDesitinNotes(desc) {
  if (currentPerson.value.length == 0) return
  decision.value = desc
  openPopup('desitin_notes')
}
function voteClass(code) {
  if (code === 1 || code === 4) return 'accepted'
  if (code === 2 || code === 3) return 'rejected'
  return 'pending'
}
onMounted(() => {
  loadUiSettings(spliter)
  document.addEventListener('click', handleClickOutside)
  console.log('authStore', authStore.user.info.username)

  lagnaStore.connectLagnaPersonShowSocket(committe_code, async (data) => {
    console.log('data.event==========>', data.event)
    switch (data.event) {
      case 'show_person':
        console.log('--------------- show_person ---------------')
        console.log(' show_person', data)
        // currentPerson.value = data
        currentPerson.value['main_data'] = data.main_data
        currentPerson.value['comm_data'] = data.comm_data
        personsStore.fetchLagnaOpinionTypes(currentPerson.value.comm_data?.person_id)
        break
      case 'vote':
        currentPerson.value['comm_data'] = data.comm_data
        personsStore.fetchLagnaOpinionTypes(currentPerson.value.comm_data?.person_id)
        break
      case 'settings':
        console.log('data.settings.open_final_decision', data.settings.open_final_decision)
        open_final_decision.value = data.settings.open_final_decision
        personsStore.fetchLagnaOpinionTypes(currentPerson.value.comm_data?.person_id)
        break
      case 'comm_report':
        currentPerson.value['comm_report'] = data.data
        console.log('data.data', data.data)
        await appearLagnaReport()
        // personsStore.fetchLagnaOpinionTypes(currentPerson.value.comm_data?.person_id)
        break
      case 'pong':
        break
      case 'relation':
        if (!currentPerson.value) return
        openRelation()
        break
      case 'punish':
        openCourt(0)
        break
      case 'punish1':
        openCourt(1)
        break
      case 'punish2':
        openCourt(2)
        break
      case 'punish3':
        openCourt(3)
        break
      case 'punish4':
        openCourt(4)
        break
      case 'relation1,15':
        openRelation([1, 15], 'current_marrige')
        break
      case 'relation2,7':
        openRelation([2, 7], 'children')
        break
      case 'relation2':
        openRelation([2], 'sons')
        break
      case 'relation7':
        openRelation([7], 'doughter')
        break
      case 'shhh':
        openRelation([5, 6], 'bro_sis')
        break
      case 'shhh2':
        openRelation([11, 9, 10, 8], 'relatives')
        break
      case 'prev_marrige':
        openRelation([11, 9, 10, 8], 'prev_marrige')
        break
      case 'refresh':
        document.location.reload()

        break

      case 'takeScreen':
        currentPerson.value['main_data'] = data.main_data
        currentPerson.value['comm_data'] = data.comm_data
        personsStore.fetchLagnaOpinionTypes(currentPerson.value.comm_data?.person_id)
        downloadCurrProfileScreen()
        break
      // case 'inspire_work':
      //   addNewInspireWorkReport()
      //   break
      case 'end':
        closePopup()
        break
      case 'close':
        console.log('--------------- close ---------------')
        // person.value = []
        currentPerson.value = []
        closePopup()
        break
      default:
        console.log('data.event', data.event)
        openPopup(data.event)
    }
  })
})

async function downloadCurrProfileScreen() {
  if (!currentPerson.value?.comm_data?.person_id) {
    console.warn('data is still loading, cannot capture screen yet.')
    isWatingToDownload.value = true
    return
  }
  await executeCapture()
}
async function executeCapture() {
  const element = document.getElementById('capture-area')
  if (!element) return

  const personImage = element.getElementsByTagName('img')
  const imagePromises = Array.from(personImage).map((img) => {
    if (img.complete) return Promise.resolve()
    return new Promise((resolve) => {
      img.onload = resolve
      img.onerror = resolve
    })
  })
  await Promise.all(imagePromises)

  const canvas = await html2canvas(element, {
    useCORS: true,
    allowTaint: false,
    scale: 2,
    onclone: (cloneDocument) => {
      const clonedElement = cloneDocument.getElementById('capture-area')
      if (clonedElement) {
        // clonedElement.style.width = '1123px'
        // clonedElement.style.height = '794px'
        clonedElement.style.background = '#eafaff'
        clonedElement.style.fontWeight = '800'
        // clonedElement.style.fontSize = '25px'
        // clonedElement.style.paddingLeft = '5px'
        // clonedElement.style.paddingRight = '5px'
        clonedElement.style.paddingTop = '40px'
        clonedElement.style.paddingBottom = '1px'
        clonedElement.style.boxSizing = 'border-box'

        clonedElement.style.overflow = 'hidden'
        // clonedElement.style.display = 'flex'
        // clonedElement.style.flexDirection = 'column'
        // clonedElement.style.justifyContent = 'space-between'

        clonedElement.style.printColorAdjust = 'exact'
        clonedElement.style.webkitPrintColorAdjust = 'exact'

        // const logoFields = clonedElement.querySelectorByClassName('.hayaLogo')
        // if (logoFields.length === 0) {
        // }
        // logoFields.style.setProperty('display', 'flex', 'important')
        // logoFields.style.visibility = 'visible'
        // logoFields.style.opacity = '1'

        // const screenShotOnlyFields = cloneDocument.querySelectorAll('.hayaLogo')
        // screenShotOnlyFields.forEach((field) => {
        //   field.style.display = 'flex'
        // })

        const allParagraphs = clonedElement.querySelectorAll('p')
        allParagraphs.forEach((p) => {
          // p.style.width = '100%'
          p.style.textAlign = 'center'
          p.style.justifyContent = 'center'
          p.style.fontSize = '16px'
          p.style.fontWeight = '800'
          p.style.display = 'flex'
        })
      }
    },
  })

  // const canvas = await html2canvas(element)
  const image = canvas.toDataURL('image/jpeg', 1.0)

  const link = document.createElement('a')
  link.href = image
  link.download = `${person.value.mil_no}.jpg`
  link.click()
}

onBeforeUnmount(() => {
  lagnaStore.disconnectLagnaPersonShowSocket()
  document.removeEventListener('click', handleClickOutside)
})

watch(
  () => currentPerson.value,
  async (newVal) => {
    console.log('newVal', newVal)
    if (!newVal?.main_data) return
    if (!newVal?.comm_data) return

    if (newVal && isWatingToDownload.value) {
      isWatingToDownload.value = false

      await nextTick()

      await executeCapture()
    }

    load.value = false
    console.log('newVal============>', newVal['comm_data'])
    person.value = newVal?.main_data
    personCommit.value = newVal?.comm_data
    selectedFinalDecision.value = personCommit.value.final_decision?.opinion_code
    lagnaArmyReport.value = newVal?.comm_report
    console.log('lagnaArmyReport', lagnaArmyReport.value)
    votes.value = newVal?.comm_data?.votes_info_test?.votes
    finalDecision.value = newVal.comm_data?.final_decision
    photos.value = newVal?.main_data?.photos || []
    punishments.value = newVal.main_data?.person_punishment || []
    sta.value = person.value?.punishment_statistics?.[0] || {}
    punshiments.value = person.value?.person_punishment || []

    punishLength.value = sta.value?.tot_pa || 0
    punishcourtLength.value = sta.value?.court || 0
    punishStayLength.value = sta.value?.stay || 0
    punishNotStayLength.value = sta.value?.not_stay || 0

    jobunits.value = [...(person.value?.units || [])]
    jobsUnitsLength.value = person.value?.units?.length || 0

    console.log('personCommit.value', personCommit.value)
    load.value = true
  },
  { immediate: true, deep: true },
)
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

.mainUserData {
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
  background: #d8e8f3;
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

.wating-window {
  background: linear-gradient(135deg, #ffffff, #fc9732);
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  color: #fff;
  /* width: 100vw !important; */
  /* z-index: 1000 !important; */
}

.wating-logo {
  text-align: center;
  animation: linear 2s ease-in-out;
}

.wating-logo img {
  width: 400px;
  height: auto;
  animation: rotateYAnim 4s infinite ease-out;
  transition: transform 0.3s ease-in-out;
  /* box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 255, 255, 0.4); */
  border-radius: 20px;
  /* border-radius: 50%; */
}

.wating-window h1 {
  font-size: 3rem;
  margin: 100px 0 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
  font-weight: bold;
  color: black;
}

.final-decision-box {
  /* margin-top: 20px; */
  padding: 9px 10px;
  padding-bottom: 20px;
  border-radius: 10px;
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
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  direction: ltr;
  text-align: center;
  background-color: #ffffff;
  border: 1px solid #ffffff;
  border-radius: 4px;
  padding: 10px 15px;
  font-family: inherit;
  color: #333;
  background-repeat: no-repeat;
  background-position: left 12px center;
  background-size: 14px;
  min-width: 220px;
  transition: 0.2s ease;
  width: -webkit-fill-available;
  border: 0;
}

.final-select:focus {
  border-color: #4c6ef5;
  outline: none;
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
.save-final-btn {
  padding: 8px 16px;
}

.votes-box {
  width: 100%;
  margin-top: 15px;
}

.vote-item {
  position: relative;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 12px;
  margin-bottom: 10px;
  transition: 0.3s;
}

.vote-item:hover {
  transform: translateY(-2px);
}

/* header */
.vote-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.vote-name {
  font-weight: bold;
}

.vote-percent {
  font-size: 13px;
  color: #666;
}
.subHeader {
}

.subHeader .hayaLogo {
  /* display: none; */
  display: flex;
  align-items: center;
  justify-content: center;
}
.subHeader .hayaLogo h1 {
  font-size: 20px;
  color: #e3d400;
}
.lagnaName {
  display: flex;
  align-items: center;
  justify-content: center;
}
.lagnaName p {
  padding: 10px 20px;
  background: #faa23c;
  color: #000000;
  font-weight: 600;
  border-radius: 10px;
}
/* progress */
.vote-bar-wrapper {
  height: 10px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.vote-bar {
  height: 100%;
  transition: width 0.4s ease;
}
.show-votes-btn {
  background: #e67700;
  padding: 10px 20px;
  color: white;
  font-weight: 800;
  border-radius: 10px;
}

/* ألوان */
.vote-bar.accepted {
  background: #2b8a3e;
}

.vote-bar.rejected {
  background: #c92a2a;
}

.vote-bar.pending {
  background: #e67700;
}

/* footer */
.vote-footer {
  margin-top: 6px;
  text-align: right;
}

.vote-number {
  font-weight: bold;
  cursor: pointer;
  color: #4c6ef5;
}

/* tooltip */
.tooltip-box {
  position: absolute;
  left: 106%;
  top: 10%;
  background: #fff;
  border-radius: 12px;
  padding: 10px;
  min-width: 200px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

.tooltip-title {
  font-weight: bold;
  margin-bottom: 6px;
}

.tooltip-item {
  font-size: 13px;
  padding: 4px 0;
  border-bottom: 1px solid #eee;
}

.tooltip-item:last-child {
  border-bottom: none;
}

/* animation */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease;
}

.btn {
  width: fit-content;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(-5px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

.Lagna-oreder-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.Lagna-oreder {
  font-size: large;
  font-weight: bold;
  margin-top: 35px;
  background: white;
  width: fit-content;
  text-align: center;
  padding: 12px 10px;
  border-radius: 14px;
  height: fit-content;
  margin: 14px 0px;
}
@media (max-width: 992px) {
  .mainUserData {
    flex-direction: column;
  }

  .counters {
    width: 100%;
    max-width: 100%;
  }
}
@keyframes rotateYAnim {
  0% {
    transform: rotateY(0deg);
  }

  50% {
    transform: rotateY(90deg);
  }

  100% {
    transform: rotateY(0deg);
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
@media print {
  .subHeader .hayaLogo {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
