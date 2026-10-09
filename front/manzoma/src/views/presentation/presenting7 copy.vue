<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { convertToArabicNumbers } from '@/utils/glopal'
import { useAuthStore } from '@/stores/authStore'
const authStore = useAuthStore()
// Components
import pastUnits from '@/components/global/popup/past-units.vue'
import secPerson from '@/components/global/popup/sec-person.vue'
import travelPopup from '@/components/global/popup/travelPopup.vue'
import courtPopup from '@/components/global/popup/courtPopup.vue'
import CourtPopup from '@/components/global/popup/courtPopup.vue'
import MedicalPopup from '@/components/global/popup/medicalPopup.vue'
import HistoryPopup from '@/components/global/popup/historyPopup.vue'
import PersonPhotoCo from '@/components/global/popup/PersonPhoto.vue'
import RelationPopup from '@/components/global/popup/relationPopup.vue'
import ConsistancyPopup from '@/components/global/popup/consistancyPopup.vue'
import reportVue from '@/components/global/popup/report.vue'
import TraqPopup from '@/components/global/popup/TraqPopup.vue'
import UpdatePopup from '@/components/global/popup/UpdatePopup.vue'
import courses from '@/components/global/popup/courses.vue'
import eff_report from '@/components/global/popup/eff_report.vue'
import reasonsPopup from '@/components/global/popup/reasonsPopup.vue'
import acceptpop from '@/components/global/popup/acceptpop.vue'
import Acceptpop from '@/components/global/popup/acceptpop.vue'
import Poea from '@/components/global/popup/Poea.vue'
import OutmemberReport from '@/components/global/popup/OutmemberReport.vue'
import OpinionManager from '@/components/global/popup/opinionManager.vue'

let milSer = ref('');
let unit = ref('');
let data = ref([]);
let index = ref(0);
let data2 = ref([]);
let jobunits = ref([]);
let usersTable = ref([]);
let filteredUsersTable = ref([]);
let unit_Selection = ref('');
let pern_Selection = ref('');
let lagnaType = ref('all');
let LagnaDay = ref('all');
let primData = ref(true);
let reson = ref(true);
let poea = ref(false);
let isSecVisiable = ref(false);
let count = ref(0);
let reportData = ref({});
let opManager = ref(false);
let reasons = ref('');
let court1 = ref('');
let cortType = ref('');
let preOpinin = ref(null);
let memberForDay = ref(null);
let lastOpinin = ref(null);
let isVisiable = ref(false);
let travelIsVisiable = ref(false);
let courtIsVisiable = ref(false);
let reportIsVisiable = ref(false);
let MedicalIsVisiable = ref(false);
let RelationIsVisiable = ref(false);
let ConsistancyIsVisiable = ref(false);
let HistoryIsVisiable = ref(false);
let TraqIsVisiable = ref(false);
let UpdateIsVisiable = ref(false);
let PersonPhoto = ref(false);
let suggest_unit = ref('');
let lagna = ref([]);
let opinion_member = ref(false);
let vote_member = ref(false);
let personData = ref([]);
let punshiments = ref([]);
let punishLength = ref(0);
let jobsUnitsLength = ref(0);
let punishStayLength = ref(0);
let punishNotStayLength = ref(0);
let jobsunits = ref([]);
let travel = ref([]);
let travelLength = ref(0);
let punishCortLength  = ref(0);
let member_op = ref('');
let member_decision = ref('');
let reasonLength = ref(0);
let vote_0 = ref([]);
let vote_1 = ref([]);
let vote_2 = ref([]);
let habs = ref('');
let sta = ref({});
let hagz = ref('');
let OutReport = ref(false);
let unitPersonsPhoto = ref([]);
let court = ref('');
let disable = ref(false);
let smallPhoto = ref('');
let largePhoto = ref('');
let familyPhoto = ref('');
let current_vote = ref(null);
let muscle_weiht = ref(null);
let medical = ref([]);
let TraqPopupVisible = ref(false);
let UpdatePopupVisible = ref(false);
let rejections_traq = ref([]);
let rejections_update = ref([]);
let attened = ref(false);
let attendDay = ref('');
let checkLagna = ref('1');
let alert = ref(false);
let coursesPopupVisible = ref(false);
let Eff_reportPopupVisible = ref(false);
let reasonsPopupVisible = ref(false);
let AcceptPopupVisible = ref(false);
let RejectPopupVisible = ref(false);
let allMemberInthislagna = ref(localStorage.getItem('allMemberInthislagna'));
let unitPersonsData = ref([]);
let filterUnitPersonsData = ref([]);
let consis = ref('');
let effLength = ref(null);
let opSelection = ref('');
let pernName = ref([]);

const memberType = ref(authStore.user?.member_type || false);
const member = ref(authStore.user?.member_name || '');
const out_user = ref(authStore.user?.out_user || null);
const outMember = ref(authStore.user?.army_code || '');
const user_id = ref(authStore.user?.user_id || false);
const unitName = ref(authStore.user?.unit_name || '');
const show = ref(authStore.user?.show || false);
const vote_type = ref(authStore.user?.vote_type || 3);
const member_job = ref(authStore.user?.member_job || '');
const days = ref(authStore.user?.days || {});
const attendance_number = ref(authStore.user?.attendance_number || 0);
const attended_number = ref(authStore.user?.attended_number || 0);

const user = reactive([])

onMounted(() => {
  console.log('Show flag from store:', show.value)

  console.log(!out_user.value && !show.value)
  if (!out_user.value && !show.value) {
    useSocket()
  } else if (!show.value) {
    UnitsName()
  } else {
    showPerson()
  }

  if (user_id.value == 100) {
    fetchUserDataId()
  }
})
   

function handleDecisionChange() {
  // Same logic as your radio button click
  if (member_decision.value == 1) {
    decision_handel(1)
  } else if (member_decision.value == 2) {
    decision_handel(2)
  } else if (member_decision.value == 0) {
    decision_handel(0) // assuming 4 = postpone/ارجاء
  } else if (member_decision.value == 4) {
    decision_handel(4)
  }
}

function checkConsis() {
  console.log('start')
  if (prsonData.value?.length - 100 >= personData.value?.weight) {
    consis.value = 'لائق'
  } else {
    if (25 >= Number(personData.value?.tot_years) >= 20) {
      ;(25 * (personData.value?.length / 100) * personData.value?.length) / 100 >
      personData.value?.weight
        ? (consis.value = 'لائق')
        : (consis.value = 'غير لائق')
    } else if (30 >= Number(personData.value?.tot_years) >= 26) {
      ;(25.5 * (personData.value?.length / 100) * personData.value?.length) / 100 >
      personData.value?.weight
        ? (consis.value = 'لائق')
        : (consis.value = 'غير لائق')
    } else if (35 >= Number(personData.value.tot_years) >= 31) {
      ;(26.5 * (personData.value.length / 100) * personData.value.length) / 100 >
      personData.value?.weight
        ? (consis.value = 'لائق')
        : (consis.value = 'غير لائق')
    } else if (40 >= Number(personData.value.tot_years) >= 36) {
      ;(27.5 * (personData.value.length / 100) * personData.value.length) / 100 >
      personData.value?.weight
        ? (consis.value = 'لائق')
        : (consis.value = 'غير لائق')
    } else if (50 >= Number(personData.value.tot_years) >= 41) {
      ;(28 * (personData.value.length / 100) * personData.value.length) / 100 >
      personData.value?.weight
        ? (consis.value = 'لائق')
        : (consis.value = 'غير لائق')
    } else if (Number(personData.value.tot_years) > 50) {
      ;(29 * (personData.value.length / 100) * personData.value.length) / 100 >
      personData.value?.weight
        ? (consis.value = 'لائق')
        : (consis.value = 'غير لائق')
    }
  }
  console.log(consis.value)
}

async function showPerson() {
  try {
    const res = await axios.get(`/person/${66701220080}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })
    personData.value = res.data
    sta.value = { ...personData.value.committee_punishment_jobs_sta[0] }
    console.log(sta)
    const h = personData.value.votes?.filter(
      (u) =>
        u.user_data.degree === localStorage.getItem('rank') &&
        u.user_data.member === localStorage.getItem('member_name'),
    )[0]
    current_vote.value = h?.vote_type

    punshiments.value = personData.value.committee_punishment_jobs
   
    punishLength.value = personData.value.committee_punishment_jobs_sta[0]?.total || 'لا يكن'

    punishCortLength.value = personData.value.committee_punishment_jobs_sta[0]?.cort || 'لا يكن'
    punishStayLength.value = personData.value.committee_punishment_jobs_sta[0]?.stay || 'لا يكن'

    punishNotStayLength.value =
      personData.value.committee_punishment_jobs_sta[0]?.not_stay || 'لا يكن'
    jobunits.value = [...(personData.value.committee_jobs || [])]
    jobsUnitsLength.value = personData.value.committee_jobs?.length
    travel.value = [...(personData.value.committee_travel_jobs || [])]
    travelLength.value = personData.value.committee_travel_jobs?.length
    reasonLength.value = personData.value.reasons?.length
    smallPhoto.value = `http://afrad.oma.mil:8080/${personData.value.small_photo}`
    largePhoto.value = `http://afrad.oma.mil:8080/${personData.value.large_photo}`
    familyPhoto.value = `http://afrad.oma.mil:8080/${personData.value.family_photo}`
    member_decision.value = personData.value.final_decision

    effLength.value = personData.value?.efficiency_report.length
    console.log(personData.value?.efficiency_report[Number(effLength)]?.grade_name)
    rejections_traq.value = personData.value?.rejections?.filter((e) => e.sp == 1)
    rejections_update.value = personData.value?.rejections?.filter((e) => e.sp == 2)
    console.log('By index.value', res)
  } catch {
    ;(Error) => console.log(Error)
  }
}

function toAr(number) {
  return convertToArabicNumbers(number)
}

async function UnitsName() {
  let res = await axios.get('/units/', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
  unit.value = res.data
  pernName.value = res.data
}

async function downloadPDF() {
  const element = document.getElementById('capture-area')
  const canvas = await html2canvas(element, {
    scale: 2,
  })
  const imgData = canvas.toDataURL('image/png')

  const { jsPDF } = window.jspdf
  const pdf = new jsPDF({
    orientation: 'l',
    unit: 'mm',
    format: 'a4',
  })

  const imgProps = pdf.getImageProperties(imgData)
  const pdfWidth = pdf.internal.pageSize.getWidth()
  const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width

  pdf.addImage(imgData, 'PNG', 0, 15, pdfWidth, pdfHeight + 45)
  pdf.save(`${personData.value.mil_no}`)
}

async function downloadImage() {
  const element = document.getElementById('capture-area')
  const canvas = await html2canvas(element)
  const image = canvas.toDataURL('image/png')

  const link = document.createElement('a')
  link.href = image
  link.download = `${personData.value.mil_no}`
  link.click()
}

async function fetchDataForOutUser() {
  try {
    const res = await axios.get(
      `/persons/filter/?mil_ser=${milSer.value}&unit_code=${unit_Selection.value}&checklagna=${checkLagna.value}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      },
    )
    data.value = res.data
    console.log(data.value)
    if (data.value.length > 0) {
      const res2 = await axios.get(`/person/${data.value[0].mil_ser}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      data2.value = res2.data
      console.log('hello ', data2.value)
      console.log('hello2 ', data2.value?.mil_ser)
      if (data2.value?.mil_ser) {
        setData(data2.value)
        index.value = 0
      } else {
        personData.value = {}
      }
    }
    // personData.value = data.value[0];
    // console.log(personData.value);
    // console.log(data.value[0]);
  } catch (e) {
    console.log('check error', e)
  }
}

// test changes
async function fetchDataForOutUserByindex(i) {
  try {
    const res = await axios.get(
      `/persons/filter/?mil_ser=${milSer.value}&unit_code=${unit_Selection.value}&checklagna=${checkLagna.value}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      },
    )
    data.value = res.data
    console.log('index.value num', i)
    console.log('By index.value', data.value)
    if (data.value.length > 0) {
      const res2 = await axios.get(`/person/${data.value[i].mil_ser}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      data2.value = res2.data
      console.log('hello ', data2.value)
      console.log('hello2 ', data2.value?.mil_ser)
      if (data2.value?.mil_ser) {
        setData(data2.value)
        index.value = i
        console.log('new', index.value)
      } else {
        personData.value = {}
      }
    }
    // personData.value = data.value[0];
    // console.log(personData.value);
    // console.log(data.value[0]);
  } catch (e) {
    console.log('check error', e)
  }
}

function setData(data) {
  personData.value = { ...data }
  effLength.value = personData.value?.efficiency_report.length
  console.log('000000 ', personData.value?.efficiency_report)

  checkConsis()
  attendDay.value = personData.value.day?.id || ''
  console.log(personData.value.votes)
  sta.value = { ...personData.value.committee_punishment_jobs_sta[0] }
  console.log(sta.value)
  const h = personData.value.votes?.filter(
    (u) =>
      u.user_data.degree === localStorage.getItem('rank') &&
      u.user_data.member === localStorage.getItem('member_name'),
  )[0]
  current_vote.value = h?.vote_type

  punshiments.value = personData.value.committee_punishment_jobs

  punishLength.value = personData.value.committee_punishment_jobs_sta[0]?.total || 'لا يكن'

  punishCortLength.value = personData.value.committee_punishment_jobs_sta[0]?.cort || 'لا يكن'
  punishStayLength.value = personData.value.committee_punishment_jobs_sta[0]?.stay || 'لا يكن'

  punishNotStayLength.value =
    personData.value.committee_punishment_jobs_sta[0]?.not_stay || 'لا يكن'
  jobunits.value  = [...(personData.value.committee_jobs || [])]
  jobsUnitsLength.value = personData.value.committee_jobs?.length
  travel.value = [...(personData.value.committee_travel_jobs || [])]
  travelLength.value = personData.value.committee_travel_jobs?.length
  reasonLength.value = personData.value.reasons?.length
  smallPhoto.value = `http://afrad.oma.mil:8080/${personData.value.small_photo}`
  largePhoto.value = `http://afrad.oma.mil:8080/${personData.value.large_photo}`
  familyPhoto.value = `http://afrad.oma.mil:8080/${personData.value.family_photo}`
  console.log('smal', smallPhoto.value)
  console.log('lg', largePhoto.value)
  console.log('fam', familyPhoto.value)
  member_decision.value = personData.value.final_decision
  rejections_traq.value = personData.value?.rejections?.filter((e) => e.sp == 1)
  rejections_update.value = personData.value?.rejections?.filter((e) => e.sp == 2)
  console.log(largePhoto.value)
  if (vote_type.value == '1') {
    vote_0.value =
      personData.value.votes
        ?.filter((v) => v.vote_type == 0 && v.member_username != 1)
        .map((u) => u.user_data)
        .sort((a, b) => a.priority_number - b.priority_number) || []
    vote_1.value =
      personData.value.votes
        ?.filter((v) => v.vote_type == 1 && v.member_username != 1)
        .map((u) => u.user_data)
        .sort((a, b) => a.priority_number - b.priority_number) || []
    vote_2.value =
      personData.value.votes
        ?.filter((v) => v.vote_type == 2 && v.member_username != 1)
        .map((u) => u.user_data)
        .sort((a, b) => a.priority_number - b.priority_number) || []
  }
  console.log(data)
}
async function gothen() {
  const newArrayData = Array.from(data.value)
  if (index.value < newArrayData.length) {
    ++index.value
  } else {
    index.value = 0
  }

  try {
    // Make the API request
    const res2 = await axios.get(`/person/${newArrayData[index.value].mil_ser}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })

    let data2 = res2.data
    console.log('data from API: ', data2.value)

    if (data2.value?.mil_ser) {
      setData(data2.value)
      // Optionally, decide when to reset `index.value`
      // If you want to reset it after processing one person:
      // index.value = 0;
    } else {
      personData.value = {} // No valid data, clear personData.value
    }
  } catch (e) {
    console.error('Error in fetching data:', e)
  }
}

async function goback() {
  const newArrayData = Array.from(data.value)
  if (index.value > 1) {
    --index.value
  } else {
    index.value = 0
  }

  try {
    // Make the API request
    const res2 = await axios.get(`/person/${newArrayData[index.value].mil_ser}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })

    let data2 = res2.data
    console.log('data from API: ', data2)

    if (data2?.mil_ser) {
      setData(data2)
      // Optionally, decide when to reset `index.value`
      // If you want to reset it after processing one person:
      // index.value = 0;
    } else {
      personData.value = {} // No valid data, clear personData.value
    }
  } catch (e) {
    console.error('Error in fetching data:', e)
  }
}

async function handelChange() {
  let req = await axios.post(
    `/attended/${personData.value?.mil_ser}/`,
    {
      day: attendDay.value,
    },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    },
  )
  attendDay.value = req.data?.day || ''
  if (req.data?.attended_number !== undefined) {
    localStorage.setItem('attendance_number', req.data.attendance_number)
    localStorage.setItem('attended_number', req.data.attended_number)
    attended_number.value = req.data?.attended_number
  }
}

async function fetchUserData() {
  await axios
    .get('persons/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })
    .then((res) => {
      data2.value = [
        ...res.data.filter((t) => t.committe_order != 0),
        ...res.data.filter((t) => t.committe_order == 0),
      ]
      filteredUsersTable.value = usersTable.value
      data.value = usersTable.value
      console.log(usersTable.value)
    })
    .catch((err) => {
      console.log('Error getting data, ', err?.message)
      if (err.status == 401) {
        localStorage.clear()
        $router.push({ name: 'login' })
      }
    })
}

function countMember() {
  if (LagnaDay.value != 'all') {
    memberForDay.value = usersTable.value.filter((e) => e.attended_date == LagnaDay.value)
    console.log(memberForDay.value)
  }
}

function filterUsers() {
  data2.value = usersTable.value.filter((record) => {
    const armyNameFilter = record.army_name == armyName || armyName == 'all'
    // test
    const LagnaDayFilter = record.attended_date == LagnaDay.value || LagnaDay.value == 'all'
    const lagnaTypeFilter = record.type_name == lagnaType.value || lagnaType.value == 'all'

    return armyNameFilter && lagnaTypeFilter && LagnaDayFilter
  })
  console.log('data', data.value)
}

async function fetchDataForOutUserId() {
  try {
    const res = await axios.get(
      `/persons/filter/?mil_ser=${milSer.value}&pern_code=${pern_Selection.value}&unit_code=${unit_Selection.value}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      },
    )
    data = res.data
    console.log(data.value)
    if (data.value.length > 0) {
      const res2 = await axios.get(`/person/${data.value[0].mil_ser}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      data2.value = res2.data
      console.log('hello ', data2.value)
      console.log('hello2 ', data2.value?.mil_ser)
      if (data2.value?.mil_ser) {
        setDataId(data2.value)
        index.value = 0
      } else {
        personData.value = {}
      }
    }
    // personData.value = data.value[0];
    // console.log(personData.value);
    // console.log(data.value[0]);
  } catch (e) {
    console.log('check error', e)
  }
}

async function fetchDataForOutUserByindexId(i) {
  try {
    const res = await axios.get(
      `/persons/filter/?mil_ser=${milSer.value}&unit_code=${unit_Selection.value}&checklagna=${checkLagna}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      },
    )
    data = res.data
    console.log('index.value num', i)
    console.log('By index.value', data.value)
    if (data.value.length > 0) {
      const res2 = await axios.get(`/person/${data.value[i].mil_ser}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      data2.value = res2.data
      console.log('hello ', data2.value)
      console.log('hello2 ', data2.value?.mil_ser)
      if (data2.value?.mil_ser) {
        setDataId(data2.value)
        index.value = i
        console.log('new', index.value)
      } else {
        personData.value = {}
      }
    }
    // personData.value = data.value[0];
    // console.log(personData.value);
    // console.log(data.value[0]);
  } catch (e) {
    console.log('check error', e)
  }
}

function setDataId(data) {
  personData.value = { ...data }
  effLength = personData.value?.efficiency_report.length
  console.log('000000 ', personData.value?.efficiency_report)

  checkConsis()
  attendDay = personData.value.day?.id || ''
  console.log(personData.value.votes)
  sta = { ...personData.value.committee_punishment_jobs_sta[0] }
  console.log(sta)
  const h = personData.value.votes?.filter(
    (u) =>
      u.user_data.degree === localStorage.getItem('rank') &&
      u.user_data.member === localStorage.getItem('member_name'),
  )[0]
  current_vote.value = h?.vote_type

  punshiments.value = personData.value.committee_punishment_jobs

  punishLength.value = personData.value.committee_punishment_jobs_sta[0]?.total || 'لا يكن'

  punishCortLength.value = personData.value.committee_punishment_jobs_sta[0]?.cort || 'لا يكن'
  punishStayLength.value = personData.value.committee_punishment_jobs_sta[0]?.stay || 'لا يكن'

  punishNotStayLength.value =
    personData.value.committee_punishment_jobs_sta[0]?.not_stay || 'لا يكن'
  jobunits.value  = [...(personData.value.committee_jobs || [])]
  jobsUnitsLength.value = personData.value.committee_jobs?.length
  travel.value = [...(personData.value.committee_travel_jobs || [])]
  travelLength.value = personData.value.committee_travel_jobs?.length
  reasonLength.value = personData.value.reasons?.length
  smallPhoto.value= `http://afrad.oma.mil:8080/${personData.value.small_photo}`

  largePhoto.value = `http://afrad.oma.mil:8080/${personData.value.large_photo}`
  familyPhoto.value = `http://afrad.oma.mil:8080/${personData.value.family_photo}`
  member_decision.value = personData.value.final_decision
  rejections_traq.value = personData.value?.rejections?.filter((e) => e.sp == 1)
  rejections_update.value = personData.value?.rejections?.filter((e) => e.sp == 2)
  console.log(largePhoto.value)
  if (vote_type.value == '1') {
    vote_0 =
      personData.value.votes
        ?.filter((v) => v.vote_type == 0 && v.member_username != 1)
        .map((u) => u.user_data)
        .sort((a, b) => a.priority_number - b.priority_number) || []
    vote_1 =
      personData.value.votes
        ?.filter((v) => v.vote_type == 1 && v.member_username != 1)
        .map((u) => u.user_data)
        .sort((a, b) => a.priority_number - b.priority_number) || []
    vote_2 =
      personData.value.votes
        ?.filter((v) => v.vote_type == 2 && v.member_username != 1)
        .map((u) => u.user_data)
        .sort((a, b) => a.priority_number - b.priority_number) || []
  }
  console.log(data)
}

// async function gothen() {
//   const newArrayData = Array.from(data)
//   if (index.value < newArrayData.length) {
//     ++index.value
//   } else {
//     index.value = 0
//   }

//   try {
//     // Make the API request
//     const res2 = await axios.get(`/person/${newArrayData[index.value].mil_ser}/`, {
//       headers: {
//         Authorization: `Bearer ${localStorage.getItem('token')}`,
//       },
//     })

//     let data2 = res2.data
//     console.log('Data from API: ', data2.value)

//     if (data2.value?.mil_ser) {
//       setDataId(data2.value)
//       // Optionally, decide when to reset `index.value`
//       // If you want to reset it after processing one person:
//       // index.value = 0;
//     } else {
//       personData.value = {} // No valid data, clear personData.value
//     }
//   } catch (e) {
//     console.error('Error in fetching data:', e)
//   }
// }

async function gobackId() {
  const newArrayData = Array.from(data.value)
  if (index.value > 1) {
    --index.value
  } else {
    index.value = 0
  }

  try {
    // Make the API request
    const res2 = await axios.get(`/person/${newArrayData[index.value].mil_ser}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })

    let data2 = res2.data
    console.log('data from API: ', data2)

    if (data2?.mil_ser) {
      setDataId(data2)
      // Optionally, decide when to reset `index.value`
      // If you want to reset it after processing one person:
      // index.value = 0;
    } else {
      personData.value = {} // No valid data, clear personData.value
    }
  } catch (e) {
    console.error('Error in fetching data:', e)
  }
}

async function handelChangeId() {
  let req = await axios.post(
    `/attended/${personData.value?.mil_ser}/`,
    {
      day: attendDay,
    },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    },
  )
  attendDay = req.data?.day || ''
  if (req.data?.attended_number !== undefined) {
    localStorage.setItem('attendance_number', req.data.attendance_number)
    localStorage.setItem('attended_number', req.data.attended_number)
    attended_number = req.data?.attended_number
  }
}

async function fetchUserDataId() {
  await axios
    .get('persons/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })
    .then((res) => {
      data2.value = [
        ...res.data.filter((t) => t.committe_order != 0),
        ...res.data.filter((t) => t.committe_order == 0),
      ]
      filteredUsersTable.value = usersTable.value
      data = usersTable.value
      console.log(usersTable.value)
    })
    .catch((err) => {
      console.log('Error getting data, ', err?.message)
      if (err.status == 401) {
        localStorage.clear()
        $router.push({ name: 'login' })
      }
    })
}

function countMemberId() {
  if (LagnaDay.value != 'all') {
    memberForDay = usersTable.value.filter((e) => e.attended_date == LagnaDay.value)
    console.log(memberForDay)
  }
}

function filterUsersId() {
  data2.value = usersTable.value.filter((record) => {
    const armyNameFilter = record.army_name == armyName || armyName == 'all'
    // test
    const LagnaDayFilter =
      (record.attended_date == LagnaDay.value) == '2025-10-05' || LagnaDay.value == '2025-10-09'
    const lagnaTypeFilter = record.type_name == lagnaType.value || lagnaType.value == 'all'

    return armyNameFilter.value.value && lagnaTypeFilter && LagnaDayFilter
  })
  console.log('data', data.value)
}

async function uploadImage() {
  const image1 = document.getElementById('imageInput1')
  const image2 = document.getElementById('imageInput2')
  const image3 = document.getElementById('imageInput3')
  const image4 = document.getElementById('imageInput4')
  const status = document.getElementById('status')
  const formData = new FormData()
  if (
    image1.files.length != 0 &&
    image2.files.length != 0 &&
    image3.files.length != 0 &&
    image4.files.length != 0
  ) {
    formData.append('image1', image1.files[0])
    formData.append('image2', image2.files[0])
    formData.append('image3', image3.files[0])
    formData.append('image4', image3.files[0])
  } else if (image3.files.length != 0) {
    formData.append('image3', image3.files[0])
  } else if (image4.files.length != 0) {
    formData.append('image4', image3.files[0])
  } else if (image1.files.length === 0 && image2.files.length === 0) {
    setTimeout(() => {
      status.textContent = 'يرجى تحميل النصفى و العائلى'
    }, 500)
    return
  }

  if (image1.files.length != 0 && image2.files.length != 0) {
    formData.append('image1', image1.files[0])
    formData.append('image2', image2.files[0])
  }

  if (image4.files.length != 0) {
    formData.append('image4', image4.files[0])
  }

  try {
    const response = await fetch(
      `http://afrad.oma.mil:8080/api/upload_images/${personData.value.mil_ser}/`,
      {
        method: 'POST',
        body: formData,
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      },
    )

    if (response.ok) {
      fetchDataForOutUserByindex(index.value)
      image1 = ''
      image2 = ''
      image3 = ''
      image4 = ''
      setTimeout(() => {
        status.textContent = 'تم تحميل الصور'
        setTimeout(() => {
          status.textContent = ' '
        }, 500)
      }, 1000)

      // setData(data[index.value]);
      // document.location.reload();
    } else {
      status.textContent = 'فشل التحميل'
    }
  } catch (error) {
    console.error('Error uploading image:', error)
    status.textContent = 'خطاء فى التحميل'
  }
}

async function fetchUnitPersonsData() {
  try {
    const res = await axios.get(
      `get_images_report_details/?excel=no&pern_army=${outMember.value}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      },
    )
    unitPersonsData.value = [...res.data]
    filterUnitPersonsData.value = unitPersonsData.value
    console.log('dddddddddddd', res)
  } catch {
    ;(err) => {
      console.log('Error getting data, ', err?.message)
      if (err.status == 401) {
        localStorage.clear()
        $router.push({ name: 'login' })
      }
    }
  }
}


function useSocket() {
  let socket = null
  try {
    socket = new WebSocket(
      `ws://afrad.oma.mil:8080/ws/afr_persons/?token=${localStorage.getItem('token')}`,
    )
  } catch (error) {
    console.log('djfldflsdjflsdjf')
  }

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    console.log(data)
    if (data.message.startsWith('user')) {
      reportData.value = { ...data.data }
      console.log(reportData.value)
      if (reportIsVisiable.value == true) {
        reportIsVisiable.value = false
      } else {
        reportIsVisiable.value = true
      }
    }
    if (data.message.startsWith('person')) {
      personData.value = { ...data.data }
      console.log(personData.value)
      const h = personData.value.votes?.filter(
        (u) =>
          u.user_data.degree === localStorage.getItem('rank') &&
          u.user_data.member === localStorage.getItem('member_name'),
      )[0]

      current_vote.value = h?.vote_type
      // console.log(current_vote.value);
      punshiments.value = personData.value.committee_punishment_jobs
      punishLength.value = personData.value.committee_punishment_jobs_sta[0]?.total
      punishCortLength.value = personData.value.committee_punishment_jobs_sta
      // personData.value.committee_punishment_jobs_sta[0]?.cort;
      effLength.value = personData.value?.efficiency_report.length
      member_decision.value == personData.value.final_decision
      sta.value = { ...personData.value.committee_punishment_jobs_sta[0] }
      console.log(sta.value)
      // \\\\\\\\\\\\\\\\\

      // console.log("0000000000000000000000000",new Date(personData.value.upgrade_date).getTime() )
      // console.log("0000000000000000000000000",new Date().getTime() )
      //   console.log("0000000000000000000000000", )

      // hagz = punshiments.value.filter(
      //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 2
      // )?.length;
      // console.log("hagz1", hagz);
      // hagz2 = punshiments.value.filter(
      //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 1
      // )?.length;
      // console.log("hagz2", hagz2);
      // hagz3 = punshiments.value.filter(
      //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 14
      // )?.length;
      // console.log("hagz3", hagz3);
      // habs = punshiments.value.filter(
      //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 4
      // ).length;

      // court = punshiments.value.filter(
      //   (e) => e.punsh_cort_code == 2
      // ).length;
      court1.value = punshiments.value.filter((e) => e.punsh_cort_code == 3).length
      // habs =
      //   personData.value.committee_punishment_jobs_sta[0]?.not_stay;
      // console.log(
      //   personData.value.committee_punishment_jobs_sta,
      //   "sssssssssssssssjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjss"
      // );
      // hagz = personData.value.committee_punishment_jobs_sta[0]?.stay;
      // court = personData.value.committee_punishment_jobs_sta[0]?.court;

      punishStayLength.value = personData.value.committee_punishment_jobs_sta[0]?.stay
      punishNotStayLength.value = personData.value.committee_punishment_jobs_sta[0]?.not_stay
      jobunits.value  = [...(personData.value.committee_jobs || [])]
      jobsUnitsLength.value = personData.value.committee_jobs?.length
      travel.value = [...(personData.value.committee_travel_jobs || [])]
      travelLength.value = personData.value.committee_travel_jobs?.length
      reasonLength.value = personData.value.reasons?.length
      smallPhoto.value = `http://afrad.oma.mil:8080/${personData.value.small_photo}`
      largePhoto.value = `http://afrad.oma.mil:8080/${personData.value.large_photo}`
      familyPhoto.value = `http://afrad.oma.mil:8080/${personData.value.family_photo}`
      console.log(familyPhoto.value)
      member_decision.value = personData.value.final_decision
      // if (personData.value.tot_years => 20 and personData.value.tot_years < 20){
      // muscle_weiht =
      // }
      member_op.value =
        personData.value.votes?.filter(
          (e) => e.user_data.member == localStorage.getItem('member_name'),
        )[0]?.vote_type || null
      rejections_traq.value = personData.value?.rejections?.filter((e) => e.sp == 1)
      rejections_update.value = personData.value?.rejections?.filter((e) => e.sp == 2)
      // console.log(largePhoto);
      if (vote_type.value == '1') {
        vote_0.value =
          personData.value.votes
            ?.filter((v) => v.vote_type == 0 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
        vote_1.value =
          personData.value.votes
            ?.filter((v) => v.vote_type == 1 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
        vote_2.value =
          personData.value.votes
            ?.filter((v) => v.vote_type == 2 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
      }
      console.log('get there')
      console.log(personData.value)
    } else if (data.message.startsWith('vote')) {
      if (data.data.mil_ser == personData.value.mil_ser) {
        vote_1.value = vote_1.value?.filter((d) => d.member != data.data.member)
        vote_0.value = vote_0.value?.filter((d) => d.member != data.data.member)
        vote_2.value = vote_2.value?.filter((d) => d.member != data.data.member)

        if (data.data.vote_type == 0) {
          vote_0.value.push(data.data)
          vote_0.value.sort((a, b) => a.priority_number - b.priority_number)
        } else if (data.data.vote_type == 1) {
          vote_1.value.push(data.data)
          vote_1.value.sort((a, b) => a.priority_number - b.priority_number)

          console.log(vote_1.value)
        } else if (data.data.vote_type == 2) {
          vote_2.value.push(data.data)
          vote_2.value.sort((a, b) => a.priority_number - b.priority_number)
        }
      }
    } else if (data.message.startsWith('un_vote')) {
      disable.value = true
    } else if (data.message.startsWith('op')) {
      PersonPhoto.value = false
      travelIsVisiable.value = false
      MedicalIsVisiable.value = false
      RelationIsVisiable.value = false
      ConsistancyIsVisiable.value = false
      HistoryIsVisiable.value = false
      courtIsVisiable.value = false
      isVisiable.value = false
      TraqPopupVisible.value = false
      UpdatePopupVisible.value = false
      coursesPopupVisible.value = false
      Eff_reportPopupVisible.value = false
      reasonsPopupVisible.value = false

      // -------------------------------------------------------------------------------------------

      if (data.message.startsWith('use')) {
        console.log('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
      }
      // -------------------------------------------------------------------------------------------

      if (data.data == 'units') {
        if (personData.value.committee_jobs.length > 0) {
          if (isVisiable.value == true) {
            isVisiable.value = false
          } else {
            isVisiable.value = true
          }
        }
      }
      // if (data.data.startsWith("punish")) {
      //   if (personData.value.committee_punishment_jobs.length > 0) {
      //     if (courtIsVisiable == true) {
      //       courtIsVisiable = false;
      //       // courtIsVisiable = false;
      //     } else {
      //       // cortType = data.data.replace("punish", "");
      //       courtIsVisiable = true;
      //     }
      //   }
      // }
      if (data.data == 'medical') {
        if (personData.value.medical_history.length > 0) {
          if (MedicalIsVisiable.value == true) {
            MedicalIsVisiable.value = false
          } else {
            MedicalIsVisiable.value = true
          }
        }
      }
      if (data.data.startsWith('relation')) {
        if (personData.value.relations.length > 0) {
          if (RelationIsVisiable.value == true) {
            RelationIsVisiable.value = false
          } else {
            relationType.value = data.data
              .replace('relation', '')
              .split(',')
              .map((e) => +e)
            console.log(data.data.replace('relation', '').split(','))
            RelationIsVisiable.value = true
          }
        }
      }
      if (data.data.startsWith('consistancy')) {
        if (personData.value.consistancies.length > 0) {
          if (ConsistancyIsVisiable.value == true) {
            ConsistancyIsVisiable.value = false
          } else {
            ConsistancyIsVisiable.value = true
          }
        }
      }
      if (data.data.startsWith('travel')) {
        if (personData.value.committee_travel_jobs.length > 0) {
          if (travelIsVisiable.value == true) {
            travelIsVisiable.value = false
          } else {
            travelIsVisiable.value = true
          }
        }
      }
      if (data.data.startsWith('photo')) {
        if (personData.value.length > 0) {
          if (PersonPhoto.value == true) {
            PersonPhoto.value = false
            // largePhoto = `http://afrad.oma.mil:8080/${personData.value.large_photo}`;
          } else {
            PersonPhoto.value = true
            largePhoto.value = `http://afrad.oma.mil:8080/${personData.value.large_photo}`
          }
        }
      }
      if (data.data.startsWith('family')) {
        if (personData.value.length > 0) {
          if (PersonPhoto.value == true) {
            PersonPhoto.value = false
          } else {
            largePhoto.value = ``
            PersonPhoto.value = true
            familyPhoto.value = `http://afrad.oma.mil:8080/${personData.value.family_photo}`
          }
        }
      }
      if (data.data.startsWith('history')) {
        if (personData.value.history.length > 0) {
          if (HistoryIsVisiable.value == true) {
            HistoryIsVisiable.value = false
          } else {
            HistoryIsVisiable.value = true
          }
        }
      }
      if (data.data.startsWith('rejections_update')) {
        if (personData.value.rejections.filter((e) => e.sp == 2).length > 0) {
          if (UpdatePopupVisible.value == true) {
            UpdatePopupVisible.value = false
          } else {
            UpdatePopupVisible.value = true
          }
        }
      }
      if (data.data.startsWith('rejections_traqi')) {
        if (personData.value.rejections.filter((e) => e.sp == 1).length > 0) {
          if (TraqPopupVisible.value == true) {
            TraqPopupVisible.value = false
          } else {
            TraqPopupVisible.value = true
          }
        }
      }
      if (data.data.startsWith('Courses')) {
        if (personData.value.courses.length > 0) {
          if (coursesPopupVisible.value == true) {
            coursesPopupVisible.value = false
          } else {
            coursesPopupVisible.value = true
          }
        }
      }
      if (data.data.startsWith('Eff_report')) {
        if (personData.value.efficiency_report.length > 0) {
          if (Eff_reportPopupVisible.value == true) {
            Eff_reportPopupVisible.value = false
          } else {
            Eff_reportPopupVisible.value = true
          }
        }
      }
      if (data.data.startsWith('weight')) {
        if (personData.value.consistancies.length > 0) {
          if (ConsistancyIsVisiable.value == true) {
            ConsistancyIsVisiable.value = false
          } else {
            ConsistancyIsVisiable.value = true
          }
        }
      }
      if (data.data.startsWith('opinion')) {
        if (vote_1.value.length > 0 || vote_2.value.length > 0) {
          if (AcceptPopupVisible.value == true) {
            AcceptPopupVisible.value = false
          } else {
            AcceptPopupVisible.value = true
          }
        }
      }
      if (data.data.startsWith('punish')) {
        console.log("i'm here")
        openCourtpopup(0)
      }
      if (data.data.startsWith('punish1')) {
        if (personData.value.committee_punishment_jobs.length > 0) {
          if (courtIsVisiable.value == true) {
            openCourtpopup(1)
          } else {
            closeCourtPopup()
          }
        }
      }
      if (data.data.startsWith('punish2')) {
        if (personData.value.committee_punishment_jobs.length > 0) {
          if (courtIsVisiable.value == true) {
            openCourtpopup(2)
          } else {
            closeCourtPopup()
          }
        }
      }
      if (data.data.startsWith('punish3')) {
        if (personData.value.committee_punishment_jobs.length > 0) {
          if (courtIsVisiable.value == true) {
            openCourtpopup(3)
          } else {
            closeCourtPopup()
          }
        }
      }
      if (data.data.startsWith('punish4')) {
        if (personData.value.committee_punishment_jobs.length > 0) {
          if (courtIsVisiable.value == true) {
            openCourtpopup(4)
          } else {
            closeCourtPopup()
          }
        }
      }
      if (data.data.startsWith('poea')) {
        if (personData.value.sec_req_notes) {
          if (poea.value == false) {
            openPEApopup()
          } else {
            closePoeapopup()
          }
        }
      }
      if (data.data.startsWith('isSecVisiable')) {
        if (personData.value.sec_req_notes) {
          if (isSecVisiable.value == false) {
            openSecpopup()
          } else {
            closeSecpopup()
          }
        }
      }
      if (data.data.startsWith('shhh')) {
        openRelationPopup([5, 6])
      }
      if (data.data.startsWith('shhh2')) {
        openRelationPopup([11, 9, 10, 8])
      }
      if (data.data.startsWith('report')) {
        if (reportIsVisiable.value == true) {
          reportIsVisiable.value = false
        } else {
          reportIsVisiable.value = true
        }
      }
      if (data.data.startsWith('hayaa')) {
        if (opManager.value == true) {
          opManager.value = false
        } else {
          opManager.value = true
        }
      }
      if (data.data.startsWith('save')) {
        $refs.pop.signopinion()
      }
      if (data.data.startsWith('reason')) {
        if (personData.value.reasons.length > 0) {
          if (courtIsVisiable.value == true) {
            reasonsPopupVisible.value = false
          } else {
            reasonsPopupVisible.value = true
          }
        }
      }
      if (data.data.startsWith('takeScreen')) {
        if (localStorage.member_type == 1) {
          downloadImage()
        }
      }
      if (data.data.startsWith('takePdf')) {
        if (localStorage.member_type == 1) {
          downloadPDF()
        }
      }
      if (data.data.startsWith('u_op_reasons')) {
        if (reasonsPopupVisible.value == true) {
          reasonsPopupVisible.value = false
          reasons = ''
        } else {
          reasonsPopupVisible.value = true
          reasons.value = personData.value.opinions.filter(
            (e) => e.sp == 8,
          )[0]?.unit_refuse_reason
        }
      }
      if (data.data.startsWith('a_op_reasons')) {
        if (reasonsPopupVisible.value == true) {
          reasonsPopupVisibl.valuee = false
          reasons.value = ''
        } else {
          reasonsPopupVisible.value = true
          reasons =
            personData.value.opinions.filter((e) => e.sp == 8)[0]?.unt_arm_refuse_reason == ''
              ? personData.value.opinions.filter((e) => e.sp == 8)[0]?.unt_arm_refuse_reason
              : personData.value.opinions.filter((e) => e.sp == 8)[0]?.unit_refuse_reason
        }
      }
      if (data.data.startsWith('takePdf')) {
        if (localStorage.member_type == 1) {
          downloadPDF()
        }
      }
      if (data.data.startsWith('end')) {
        courtIsVisiable.value = false
        poea.value = false
        TraqPopupVisible.value = false
        AcceptPopupVisible.value = false
        ConsistancyIsVisiable.value = false
        coursesPopupVisible.value = false
        UpdatePopupVisible.value = false
        HistoryIsVisiable.value = false
        PersonPhoto.value = false
        travelIsVisiable.value = false
        ConsistancyIsVisiable.value = false
        MedicalIsVisiable.value = false
        RelationIsVisiable.value = false
        courtIsVisiable.value = false
        isVisiable.value = false
        opManager.value = false
      }

      if (data.data.startsWith('close')) {
        personData.value = []
      }
    }
  }
}

function vote_handel(n) {
  axios.get(`vote/${personData.value.mil_ser}/?vote_type=${n}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}

function decision_handel(n) {
  axios
    .get(`vote/${personData.value.mil_ser}/?vote_type=${n}&final_decision=1`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })
    .catch((err) => {
      if (err.status == 401) {
        localStorage.clear()
        $router.push({ name: 'login' })
      }
    })
  console.log(personData.value.mil_ser)
}

function openpopup() {
  isVisiable.value = true
}
function closePopup() {
  isVisiable.value = false
}
function openTravelpopup() {
  travelIsVisiable.value = true
}
function closeTravelPopup() {
  travelIsVisiable.value = false
}
function openCourtpopup(type = 0) {
  cortType.value = type
  courtIsVisiable.value = true
}
function closeCourtPopup() {
  courtIsVisiable.value = false
}
function openMedicalpopup() {
  MedicalIsVisiable.value = true
}
function closeMedicalPopup() {
  MedicalIsVisiable.value = false
}
function openRelationPopup(relationType) {
  relationType.value = relationType
  RelationIsVisiable.value = true
}
function closeRelationPopup() {
  RelationIsVisiable.value = false
}
function openConsistancyPopup() {
  ConsistancyIsVisiable.value = true
}
function closeConsistancyPopup() {
  ConsistancyIsVisiable.value = false
}
function openHistorypopup() {
  console.log('hello')
  HistoryIsVisiable.value = true
}
function closeHistoryPopup() {
  HistoryIsVisiable.value = false
}

function openPhotopopup() {
  PersonPhoto.value = true
}
function closePhotopopup() {
  PersonPhoto.value = false
}
function closeReportPopup() {
  reportIsVisiable.value = false
}

function closeCoursespopup() {
  coursesPopupVisible.value = false
}
function closeEff_reportpopup() {
  Eff_reportPopupVisible.value = false
}
// function closeEff_reportpopup() {
//   Eff_reportPopupVisible = false
// }
function closeReasonsPopup() {
  reasonsPopupVisible.value = false
  reasons.value = ''
}
function openReasonspopup(e) {
  reasons.value = e

  reasonsPopupVisible.value = true
}
function openTraqpopup() {
  TraqPopupVisible.value = true
  console.log('open')
}
function closeTraqpopup() {
  TraqPopupVisible.value = false
}
function openUpdatqpopup() {
  console.log('hello')
  UpdatePopupVisible.value = true
}
function closeUpdatepopup() {
  UpdatePopupVisible.value = false
}

function openAcceptpopup() {
  console.log('hello')
  AcceptPopupVisible.value = true
}
function closeAcceptpopup() {
  AcceptPopupVisible.value = false
}
function openRejectpopup() {
  console.log('hello')
  AcceptPopupVisible.value = true
}
function closeRejectpopup() {
  AcceptPopupVisible.value = false
}
function openPEApopup() {
  console.log('poea')
  poea.value = true
}
function openSecpopup() {
  console.log('isSecVisiable')
  isSecVisiable = true
}
function closePoeapopup() {
  poea.value = false
}
function closeSecpopup() {
  isSecVisiable.value = false
}
function openReportOutMember() {
  console.log('OutReport')
  OutReport = true
  fetchUnitPersonsData()
}
function closeReportOutMember() {
  OutReport.value = false
}
function openOpinionManager() {
  console.log('OutReport')
  opManager.value = true
}
function closeOpinionManager() {
  opManager.value = false
}
</script>
<template>
  <div class="homePage">
    <OpinionManager
      :personName="personData.person_name"
      :personDegree="personData.degree_name"
      :showPersonPopup="opManager"
      @close="closeOpinionManager"
      :mil="personData.mil_ser"
      ref="pop"

    />
    <!-- <OpinionManager
      :personName="personData.person_name"
      :personDegree="personData.degree_name"
      :showPersonPopup="opManager"
      @close="closeOpinionManager"
      :mil="personData.mil_ser"
      ref="pop"
      v-if="member == 'رئيس هيئة التنظيم والإدارة للقوات المسلحة'"
    /> -->

    <!-- popup contents  -->
    <OutmemberReport
      :showCourtPopup="OutReport"
      @close="closeReportOutMember"
      :tableData="unitPersonsData"
      :unit_name="unitName"
      :tablePhoto="unitPersonsPhoto"
    />
    {{ personData.milSer }}
    <pastUnits
      :showPopup="isVisiable"
      @close="closePopup"
      :tableData="jobunits?.sort((a, b) => new Date(a.from_unit_date) - new Date(b.from_unit_date))"
      :userNamePer="personData.person_name"
      :unit_name="personData.unit_name"
      :degree="personData.degree_name"
    />
    <secPerson
      :showPopup="isSecVisiable"
      @close="closeSecpopup"
      :tableData="personData.sec_req_notes"
      :userNamePer="personData.person_name"
      :unit_name="personData.unit_name"
      :degree="personData.degree_name"
    />
    <poea
      :showPopup="poea"
      @close="closePoeapopup"
      :tableData="personData.peo_reason"
      :userNamePer="personData.person_name"
      :unit_name="personData.unit_name"
      :degree="personData.degree_name"
    />
    <travelPopup
      :showTravelPopup="travelIsVisiable"
      @close="closeTravelPopup"
      :tableData="travel?.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))"
      :userNamePer="personData.person_name"
      :degree="personData.degree_name"
    />
    <CourtPopup
      :showCourtPopup="courtIsVisiable"
      @close="closeCourtPopup"
      :tableData="
        punshiments
          ?.sort((a, b) => new Date(b.punish_start_date) - new Date(a.punish_start_date))
          ?.filter((t) => {
            if (!cortType || cortType == 0) {
              return true
            } else if (cortType == 1) {
              return (
                t.punsh_cort_code == 1 &&
                ![4, 17, 18, 19, 26, 29]?.includes(parseInt(t.punishment_code))
              )
            } else if (cortType == 2) {
              return (
                t.punsh_cort_code == 1 &&
                [4, 17, 18, 19, 26, 29]?.includes(parseInt(t.punishment_code))
              )
            } else if (cortType == 3) {
              return t.punsh_cort_code == 2
            } else if (cortType == 4) {
              return t.punsh_cort_code == 3
            } else {
              return false
            }
          })
      "
      :userNamePer="personData.person_name"
      :degree="personData.degree_name"
      :type="cortType"
    />

    <reportVue
      :showCourtPopup="reportIsVisiable"
      @close="closeReportPopup"
      :tableData="reportData"
      :userNamePer="personData.person_name"
      :degree="personData.degree_name"
    />

    <MedicalPopup
      :showmMedicalPopup="MedicalIsVisiable"
      @close="closeMedicalPopup"
      :personName="personData.person_name"
      :personDegree="personData.degree_name"
      :medicalData="personData.medical_history"
    />
    <RelationPopup
      :showRelation="RelationIsVisiable"
      @close="closeRelationPopup"
      :userNamePer="personData.person_name"
      :degree="personData.degree_name"
      :tableData="
        personData.relations
          ?.sort((a, b) => {
            const order = [3, 4, 1, 2, 7, 6, 5]
            return order.indexOf(a.relation_degree_code) - order.indexOf(b.relation_degree_code)
          })
          ?.filter((r) => relationType?.includes(r.relation_degree_code))
      "
    />
    <ConsistancyPopup
      :showConsistancy="ConsistancyIsVisiable"
      @close="closeConsistancyPopup"
      :userNamePer="personData.person_name"
      :degree="personData.degree_name"
      :tableData="
        personData.consistancies?.sort((a, b) => new Date(b.check_date) - new Date(a.check_date))
      "
    />
    <HistoryPopup
      :personName="personData.person_name"
      :personDegree="personData.degree_name"
      :showHistoryPopup="HistoryIsVisiable"
      @close="closeHistoryPopup"
      :personHistory="personData.tagded_history_info"
    />
    <PersonPhotoCo
      :personPhoto="largePhoto"
      :personName="personData.person_name"
      :personDegree="personData.degree_name"
      :showPersonPopup="PersonPhoto"
      :familyPhoto="familyPhoto"
      @close="closePhotopopup"
    />
    <TraqPopup
      :userNamePer="personData?.person_name"
      :degree="personData?.degree_name"
      :showTraqPopup="TraqPopupVisible"
      @close="closeTraqpopup"
      :tableData="rejections_traq"
    />
    <UpdatePopup
      :userNamePer="personData?.person_name"
      :degree="personData?.degree_name"
      :showUpdatePopup="UpdatePopupVisible"
      @close="closeUpdatepopup"
      :tableData="rejections_update"
    />
    <reasonsPopup
      :userNamePer="personData?.person_name"
      :degree="personData?.degree_name"
      :showReasonPopup="reasonsPopupVisible"
      @close="closeReasonsPopup"
      :tableData="reasons"
    />

    <Acceptpop
      :userNamePer="personData?.person_name"
      :degree="personData?.degree_name"
      :showReasonPopup="AcceptPopupVisible"
      @close="closeAcceptpopup"
      :tableData="
        vote_1.sort((a, b) => {
          a.priority_number > b.priority_number
        })
      "
      :tableDataٍSec="
        vote_2.sort((a, b) => {
          a.priority_number > b.priority_number
        })
      "
    />

    <courses
      :userNamePer="personData?.person_name"
      :degree="personData?.degree_name"
      :showCoursesPopup="coursesPopupVisible"
      @close="closeCoursespopup"
      :tableData="
        personData?.courses?.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))
      "
    />
    <eff_report
      :userNamePer="personData?.person_name"
      :degree="personData?.degree_name"
      :showEff_reportPopup="Eff_reportPopupVisible"
      @close="closeEff_reportpopup"
      :tableData="
        personData?.efficiency_report?.sort(
          (a, b) => new Date(b.from_date) > new Date(a.from_date),
        )
      "
    />
    <!-- end popup contents  -->
    <main id="capture-area">
      <div class="homepage nouser" v-if="!personData?.person_name && !out_user && !show">
        <div class="homecontainer">
          <img src="/src/assets/Images/شعار الهيئه.png" alt="Logo" />
        </div>
        <h1>هيئة التنظيم والإدارة ق.م</h1>
      </div>

      <div class="titlePage">
        <!-- <h4
          class="topTitle"
          v-if="personData.type_code != 5 && personData.type_code != 6"
        >
          <span v-if="personData.type_code == 3">
            لجنة ( تجديد/ ترقــي ) </span
          ><span v-if="personData.type_code == 2">
            لجنة ( تجـــديــد ) </span
          ><span v-if="personData.type_code == 1">لجنة ( ترقــي ) </span
          ><span v-if="personData.type_code == 5"
            >إنهاء خدمة ( استقالة )</span
          ><span v-if="personData.type_code == 4">
            إنهاء خدمة ( عدم الرغبة )
          </span>
          <span v-if="personData.type_code == 8">
            إنهاء خدمة ( عدم صلاحية )
          </span>
          <span v-if="personData.type_code == 9">
            إنهاء خدمة ( الرفت الجوازي )
          </span>
          <span v-if="personData.type_code == 10">
            إنهاء خدمة ( تثبيت )
          </span>
          مناظرة لجنة ضباط الصف {{ toAr("2025") }}
        </h4>-->

        <h4 class="topTitle">اللجنة الرئيسية لضباط الصف للقوات المسلحة {{ toAr('2025') }}</h4>
      </div>
      <div class="outUserContainer" v-if="out_user">
        <form @submit.prevent="" class="outUserContainer" v-if="user_id">
          <input
            type="text"
            name
            class="input-field"
            v-model="milSer"
            placeholder="الـبــحـــــث بالـــــــــرقــــــــم الــعـســـــــــكــــري او بالاســـــــــــم"
          />
          <!-- <select name="units" id="units" v-model="unit_Selection" style="padding: 9px;">
            <option value>اخـــتــر الـــوحــــــدة</option>
            <option
              :value="un.unit_code"
              v-for="un in unit"
              :key="index"
            >{{ un.unit_name || "---" }}</option>
          </select>-->
          <!-- <select name="units" id="units" v-model="pern_Selection" style="padding: 9px;" autocomplete>
            <option value>اخـــتــر التبعية</option>
            <option
              :value="un.unit_code"
              v-for="un in pernName"
              :key="index"
            >{{ un.unit_name || "---" }}</option>
          </select>-->
          <input
            type="text"
            class="input-field"
            list="pern_Names"
            id="pern"
            name="pern"
            v-model="unit_Selection"
            placeholder="اختــــــــــــر الوحـــــــــدة"
            style="font-size: 15px"
          />
          <datalist id="pern_Names">
            <option value>اخـــتــر الوحـــــــــدة</option>
            <option :value="un.unit_code" v-for="un in unit" :key="un.unit_code">
              {{ un.unit_name || '---' }}
            </option>
          </datalist>

          <input
            type="text"
            class="input-field"
            list="pern_Names"
            id="pern"
            name="pern"
            v-model="pern_Selection"
            placeholder="اختـــــــــــــــــــــر الـتـبـعـيــــــــــــة"
            style="font-size: 15px"
          />
          <datalist id="pern_Names">
            <option value>اخـــتــر التبعية</option>
            <option :value="un.unit_code" v-for="un in pernName" :key="index">
              {{ un.unit_code || '---' }}
            </option>
          </datalist>
          <input
            type="text"
            class="input-field"
            list="pern_Names"
            id="pern"
            name="pern"
            v-model="army_name"
            placeholder="اختــــــــــــر الســـــــــــــــــلاح"
            style="font-size: 15px"
          />
          <datalist id="pern_Names">
            <option value>الســـــلاح</option>
            <option :value="un.unit_code" v-for="un in unit" :key="index">
              {{ un.unit_name || '---' }}
            </option>
          </datalist>
          <!-- <div class="filter-select-wrapper">
            <span>السلاح</span>
            <select
              name="army-name"
              class="select-input"
              v-model="armyName"
              @change="filterUsers()"
              style="padding: 9px;"
            >
              <option value="all" :value="armyName">جميع الحالات</option>
              <option
                v-for="(us, index) in usersTable
                ?.map((e) => e.army_name)
                .filter((e, i, a) => i === a.indexOf(e))"
                :value="us"
              >{{ us }}</option>
            </select>
          </div>-->
          <button @click="fetchDataForOutUserId()">بحث</button>
        </form>
        <form @submit.prevent="" class="outUserContainer" v-if="!user_id">
          <input
            type="text"
            name
            class="input-field"
            v-model="milSer"
            placeholder="الـبــحـــــث بالـــــــــرقــــــــم الــعـســـــــــكــــري او بالاســـــــــــم"
          />
          <select name="units" id="units" v-model="unit_Selection" style="padding: 9px">
            <option value>اخـــتــر الـــوحــــــدة</option>
            <option :value="un.unit_code" v-for="un in unit" :key="index">
              {{ un.unit_name || '---' }}
            </option>
          </select>
          <select
            name="checklagna"
            id="checkLagna"
            v-model="checkLagna"
            v-if="user_id != 100"
            style="padding: 9px"
          >
            <option value="1">الكل</option>
            <option value="2">المدرج باللجنة</option>
            <option value="3">الغير مدرج باللجنة</option>
          </select>
          <div class="filter-select-wrapper" v-if="user_id == 100">
            <span>اليوم</span>
            <select
              name="army-name"
              class="select-input"
              v-model="LagnaDay"
              @change="(filterUsers(), countMember())"
              style="padding: 9px"
            >
              <option value="all" :value="LagnaDay">جميع الايام</option>
              <option
                v-for="(us, index) in usersTable
                  ?.map((e) => e.attended_date)
                  .filter((e, i, a) => i === a.indexOf(e))"
                :value="us"
              >
                {{ us }}
              </option>
            </select>
          </div>
          <div class="filter-select-wrapper">
            <span>السلاح</span>
            <select
              name="army-name"
              class="select-input"
              v-model="armyName"
              @change="filterUsers()"
              style="padding: 9px"
            >
              <option value="all" :value="armyName">جميع الحالات</option>
              <option
                v-for="(us, index) in usersTable
                  ?.map((e) => e.army_name)
                  .filter((e, i, a) => i === a.indexOf(e))"
                :value="us"
              >
                {{ us }}
              </option>
            </select>
          </div>
          <button
            @click="
              user_id == 100 ? filterUsers() : (fetchDataForOutUser(), fetchUnitPersonsPhoto())
            "
          >
            بحث
          </button>
        </form>
        <button @click="openReportOutMember()" class="btn" v-if="!user_id">
          تقــريـــر الصور
        </button>
      </div>
      <!--  start user data  -->
      <div class="users" v-if="personData?.person_name">
        <div clas class="dataUser">
          <div class="prim-data" @click="primData = !primData">
            <h4>البيانات الأساسية</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>

          <div class="dataForUser" v-if="primData">
            <!-- row one from data  -->
            <div class="test">
              <div class="mil">
                <p class="headUser">الــرقـــم العــسكري</p>
                <p class="otherUnit">{{ toAr(personData.mil_no) || '---' }}</p>
              </div>
              <div class="mil smallMil">
                <p class="headUser">الدرجة</p>
                <p class="otherUnit">{{ personData.degree_name || '---' }}</p>
              </div>
              <div class="mil">
                <p class="headUser">الاسم</p>
                <p class="otherUnit">{{ personData.person_name || '---' }}</p>
              </div>
              <div class="mil">
                <p class="headUser">السلاح</p>
                <p class="otherUnit">{{ personData.army_name || '---' }}</p>
              </div>
              <div class="mil smallMil">
                <p class="headUser">الفئة</p>
                <p class="otherUnit">{{ personData.fea_name || '---' }}</p>
              </div>
              <div class="mil">
                <p class="headUser data-btn" @click="openpopup()">الوحدة</p>
                <p class="otherUnit">{{ toAr(`${personData.unit_name}`) || '---' }}</p>
              </div>
              <div class="mil">
                <p class="headUser">تاريــخ الضم علي الوحدة</p>
                <p class="otherUnit">{{ toAr(`${personData.to_unit_date}`) || '---' }}</p>
              </div>
              <div class="mil">
                <p class="headUser">مدة الخدمة بالوحدة</p>
                <p class="otherUnit">
                  {{ ' ' + ' ' + toAr(`${personData.unit_interval_y || '---'}`) + ' سنه' }}
                  {{ ' / ' }}
                  {{ toAr(`${personData.unit_interval_m || '---'}`) + ' شهر' + ' ' }}
                </p>
              </div>
              <div class="mil">
                <p class="headUser">التبعية</p>
                <p class="otherUnit">{{ personData.pern_army_name || '---' }}</p>
              </div>
              <!-- REPLACE FEA -->
              <div class="mil">
                <p class="headUser">الوظيفة</p>
                <p class="otherUnit">{{ personData.army_job_name || '---' }}</p>
              </div>
              <div class="mil">
                <p class="headUser">تاريخ التطوع</p>
                <p class="otherUnit">{{ toAr(personData.come_in_date) || '---' }}</p>
              </div>
              <div class="mil">
                <p class="headUser">تاريخ صرف الراتب العالي</p>
                <p class="otherUnit">{{ toAr(`${personData.rateb_date}`) || '---' }}</p>
              </div>
              <div class="mil smallMil">
                <p class="headUser smallHndleUser">عدد سنوات الخدمة</p>
                <p class="otherUnit smallOtherUnit">
                  {{ ' ' + ' ' + toAr(`${personData.tot_ser_y || '.'}`) + ' سنه' }}
                  {{ ' / ' }}
                  {{ toAr(`${personData.tot_ser_m || '.'}`) + ' شهر' + ' ' }}
                </p>
              </div>
              <!-- end row two  -->
              <!-- row therr  -->
              <div class="mil smallMil">
                <p @click="openHistorypopup()" class="headUser data-btn">
                  تاريخ الترقي للدرجة الحالية
                </p>
                <p class="otherUnit">{{ toAr(`${personData.curr_degree_date}`) || '---' }}</p>
              </div>
              <div class="mil smallMil">
                <p class="headUser smallHndleUser">تاريخ الترقي المنتــظر</p>
                <p
                  class="otherUnit smallOtherUnit"
                  style="border-radius: 10px !important"
                  :style="{
                    backgroundColor:
                      new Date(personData.upgrade_date).getTime() < new Date().getTime()
                        ? 'rgba(163 226 255 )'
                        : 'white',
                  }"
                >
                  {{ toAr(`${personData.upgrade_date || '---'}`) }}
                </p>
              </div>
              <div class="mil">
                <p class="headUser">العنوان المدني</p>
                <p class="otherUnit">
                  {{ toAr(`${personData.person_adress || '---'}`) || ' ' }} -
                  {{
                    toAr(
                      `${personData.markaz_name == null ? '--' : `${personData.markaz_name}`}`,
                    ) || '---'
                  }}
                  -
                  {{ toAr(`${personData.mohafza_name || '---'}`) || '---' }}
                </p>
              </div>
              <div class="mil smallMil">
                <p class="headUser smallHndleUser">تاريــخ الميــلاد</p>
                <p class="otherUnit smallOtherUnit">
                  {{ toAr(`${personData.birth_date}`) || '---' }}
                </p>
              </div>
              <div class="mil smallMil">
                <p class="headUser smallHndleUser">السن</p>
                <p class="otherUnit smallOtherUnit">
                  {{ toAr(`${personData.tot_years}`) || '---' }}
                </p>
              </div>

              <div class="mil smallMil">
                <p class="headUser">الطول</p>
                <p class="otherUnit">
                  {{ toAr(`${personData.length || '---'}`) || '---' }}
                  سم
                </p>
              </div>
              <div class="mil smallMil">
                <p class="headUser">الوزن</p>
                <p class="otherUnit" style="font-weight: 600">
                  {{ toAr(`${personData.weight || '---'}`) || '---' }}
                  كجم
                </p>
              </div>
              <!-- ظظظظظظظظظظظظظظظظظظ -->

              <div class="mil smallMil">
                <p class="headUser data-btn bunish-btn" @click="openSecpopup()">الموقف الامنــي</p>
                <p class="otherUnit">
                  <span v-if="personData.sec_req_flag" style="color: black">يـوجــد</span>
                  <span v-if="!personData.sec_req_flag" style="color: black">لا يـوجــد</span>
                </p>
              </div>
              <div class="mil">
                <p
                  class="headUser data-btn"
                  @click="Eff_reportPopupVisible = true"
                  style="cursor: pointer; width: 250px"
                >
                  متوسط تقرير الكفاءة لاخر ثلاث سنوات
                </p>
                <p class="otherUnit" v-if="personData?.efficiency_report.length > 0">
                  {{
                    Math.round(
                      (Number(personData?.efficiency_report[0]?.grade_name_1) +
                        Number(personData?.efficiency_report[1]?.grade_name_1) +
                        Number(personData?.efficiency_report[2]?.grade_name_1)) /
                        3,
                    ) < 50
                      ? 'ضعيف'
                      : Math.round(
                            (Number(personData?.efficiency_report[0]?.grade_name_1) +
                              Number(personData?.efficiency_report[1]?.grade_name_1) +
                              Number(personData?.efficiency_report[2]?.grade_name_1)) /
                              3,
                          ) >= 50 &&
                          Math.round(
                            (Number(personData?.efficiency_report[0]?.grade_name_1) +
                              Number(personData?.efficiency_report[1]?.grade_name_1) +
                              Number(personData?.efficiency_report[2]?.grade_name_1)) /
                              3,
                          ) <= 60
                        ? 'مقبول'
                        : Math.round(
                              (Number(personData?.efficiency_report[0]?.grade_name_1) +
                                Number(personData?.efficiency_report[1]?.grade_name_1) +
                                Number(personData?.efficiency_report[2]?.grade_name_1)) /
                                3,
                            ) > 60 &&
                            Math.round(
                              (Number(personData?.efficiency_report[0]?.grade_name_1) +
                                Number(personData?.efficiency_report[1]?.grade_name_1) +
                                Number(personData?.efficiency_report[2]?.grade_name_1)) /
                                3,
                            ) <= 75
                          ? 'جيد'
                          : Math.round(
                                (Number(personData?.efficiency_report[0]?.grade_name_1) +
                                  Number(personData?.efficiency_report[1]?.grade_name_1) +
                                  Number(personData?.efficiency_report[2]?.grade_name_1)) /
                                  3,
                              ) > 75 &&
                              Math.round(
                                (Number(personData?.efficiency_report[0]?.grade_name_1) +
                                  Number(personData?.efficiency_report[1]?.grade_name_1) +
                                  Number(personData?.efficiency_report[2]?.grade_name_1)) /
                                  3,
                              ) <= 90
                            ? 'جيد جدا'
                            : Math.round(
                                  (Number(personData?.efficiency_report[0]?.grade_name_1) +
                                    Number(personData?.efficiency_report[1]?.grade_name_1) +
                                    Number(personData?.efficiency_report[2]?.grade_name_1)) /
                                    3,
                                ) > 90 &&
                                Math.round(
                                  (Number(personData?.efficiency_report[0]?.grade_name_1) +
                                    Number(personData?.efficiency_report[1]?.grade_name_1) +
                                    Number(personData?.efficiency_report[2]?.grade_name_1)) /
                                    3,
                                ) <= 100
                              ? 'ممتاز'
                              : personData?.efficiency_report[0]?.grade_name
                  }}
                </p>
                <p class="otherUnit" v-else>لا يوجد</p>
              </div>
              <div class="mil" style="visibility: hidden">
                <p
                  class="headUser data-btn"
                  @click="Eff_reportPopupVisible = true"
                  style="cursor: pointer"
                >
                  تقرير الكفاءة
                </p>
                <p class="otherUnit" v-if="personData?.efficiency_report.length > 0">
                  {{ personData?.efficiency_report[effLength - 1]?.grade_name }}
                </p>
                <p class="otherUnit" v-else>لا يوجد</p>
              </div>
              <div class="mil smallMil">
                <p class="headUser">فرق الوزن</p>
                <p class="otherUnit">
                  {{
                    Number(personData.length) > 0 && Number(personData.weight) > 0
                      ? toAr(
                          `${
                            (Number(personData.weight) + 100 - Number(personData.length)) * -1 > 0
                              ? (Number(personData.weight) + 100 - Number(personData.length)) * -1 +
                                '-'
                              : Number(personData.weight) + 100 - Number(personData.length)
                          }`,
                        )
                      : '---'
                  }}
                  كجم
                </p>
              </div>

              <div class="mil smallMil" style="overflow: hidden">
                <p class="headUser">التناسق</p>
                <p
                  class="otherUnit"
                  style="height: 100%; transform: translateY(2px); padding: 10px; color: white"
                  :style="{
                    background: personData.consis_name == 'لائق' ? '#0a820f' : '#d63024',
                    color: personData.consis_name == 'لائق' ? '' : 'white',
                  }"
                >
                  {{ personData.consis_name || '--' }}
                  <span style="font-size: 12px">(طبقا لمعدل الكتلة الجسمانية)</span>
                </p>
              </div>
              <!-- <div class="reports"> -->
              <!-- <button></button> -->
              <!-- <button
                  @click="openSecpopup()"
                  class="sec-req"
                  style="font-size: 18px; font-weight: 600;"
                >
                  امنى
              </button>-->
              <!-- </div> -->
              <div class="mil smallMil" v-if="out_user && !user_id">
                <p
                  class="headUser"
                  :style="{
                    background: attendDay != '' ? 'green' : '#d63024 ',
                    color: 'white',
                  }"
                >
                  مدرج باللجنة ({{ attended_number || '---' }} /
                  {{ attendance_number || '---' }})
                </p>
                <select
                  class="otherUnit"
                  style="margin-inline: 10px; border: none; font-size: 19px"
                  v-model="attendDay"
                  @change="handelChange()"
                >
                  <option value>اخـــتــر الــيــوم</option>
                  <option :value="d.id" v-for="d in days" :key="d.id">
                    {{ d.attended_date || '---' }} -
                    {{ d.attended_day || '---' }}
                  </option>
                </select>
              </div>
              <!-- <div class="mil smallMil">
                <p class="headUser">النوع</p>
                <p class="otherUnit">
                  {{ personData.type_name || "ترقي / تجديد" }}
                </p>
              </div>-->
            </div>
          </div>

          <!-- end rows ? -->
          <div
            class="travelSolution"
            style="display: flex; align-items: center; height: 22px"
            v-if="personData.type_code == 7"
          >
            <h4>الالتماس</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <!-- row travel solutions  -->
          <div
            class="test1 otherWidth-travel"
            style="display: flex; justify-content: space-between; margin: 10px 0"
            v-if="personData.type_code == 7"
          >
            <div class="mil" style="min-height: 49px !important">
              <p
                style="background-color: #f98d11d1 !important; color: rgb(0, 0, 0); height: 100%"
                class="headUser data-btn"
                @click="openPEApopup()"
              >
                ملخص الالتماس
              </p>

              <p class="otherUnit">{{ personData.peo_reason || '---' }}</p>
            </div>
            <!-- <div class="mil" style="width: 50%">
              <p class="headUser">الوحدة المقترحة</p>
              <p class="otherUnit">{{ personData.sugg_unit_name }}</p>
            </div>-->
          </div>

          <!-- موقف السفر -->
          <div class="travelSolution" style="display: flex; align-items: center; height: 22px">
            <h4>موقف السفر</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <!-- row travel solutions  -->
          <div class="test otherWidth-travel">
            <div
              class="mil"
              style="max-width: 400px !important"
              :style="{
                maxWidth: travelLength == 0 ? '400px' : '',
              }"
            >
              <p class="headUser data-btn" @click="openTravelpopup()">عدد السفريات</p>

              <p class="otherUnit" v-if="travelLength > 0">{{ toAr(`${travelLength}`) }}</p>
              <p v-else style="text-align: center; width: 100%">لايكن</p>
            </div>
            <div class="mil" v-if="travelLength > 0" style="visibility: hidden">
              <p class="headUser">من</p>
              <p class="otherUnit">
                {{ toAr(`${travel[travelLength - 1]?.start_date}`) || 'لا يكن' }}
              </p>
            </div>
            <div class="mil" v-if="travelLength > 0" style="visibility: hidden">
              <p class="headUser">الي</p>
              <p class="otherUnit">
                {{ toAr(`${travel[travelLength - 1]?.end_date}`) || 'لا يكن' }}
              </p>
            </div>
          </div>
          <!-- end row travel solutions  -->
          <!-- عقوبات   -->
          <div
            class="travelSolution"
            style="display: flex; align-items: center; height: 22px; cursor: pointer"
          >
            <h4 style="margin-left: 10px">العقـــوبات</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>

          <div class="test otherWidth-pun">
            <div
              class="mil"
              style="max-width: 400px !important"
              :style="{
                maxWidth: punshiments.length == 0 ? '400px' : '',
              }"
            >
              <p class="headUser data-btn" @click="openCourtpopup(0)">
                <!-- style="background-color: #b7281e; color: white" -->
                العقوبات
              </p>
              <p class="otherUnit">
                <span v-if="punshiments.length > 0">{{ toAr(`${punishLength}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>
            <div class="mil" v-if="sta.not_stay != 0 && punshiments.length > 0">
              <p class="headUser data-btn" @click="openCourtpopup(1)">الحجز</p>
              <p class="otherUnit">
                <SPAN v-if="sta.not_stay != 0">
                  {{ toAr(`${sta.not_stay}`) }}
                </SPAN>
                <span v-else>لايكن</span>
              </p>
            </div>
            <div class="mil" v-if="punishStayLength != 0 && punshiments.length > 0">
              <p class="headUser data-btn" @click="openCourtpopup(2)">الحبس</p>
              <p class="otherUnit">
                <span v-if="sta.stay != 0">{{ toAr(`${sta.stay}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>

            <div class="mil" v-if="sta.cort != 0 && punshiments.length > 0">
              <p class="headUser data-btn bunish-btn" @click="openCourtpopup(3)">المحكمة</p>
              <p class="otherUnit">
                <span v-if="sta.cort != 0">{{ toAr(`${sta.cort}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>

            <div class="mil" v-if="sta.other > 0 && punshiments.length > 0">
              <p class="headUser data-btn bunish-btn" @click="openCourtpopup(4)">المحكمة المدنية</p>
              <p class="otherUnit">
                <span v-if="sta.other != 0">{{ toAr(`${sta.other}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>
          </div>
          <!-- نهاية العقوبات  -->
          <div
            class="travelSolution"
            style="display: flex; align-items: center; height: 22px"
            v-if="personData.reasons.length > 0"
          >
            <h4 style="margin-left: 10px">الأسـبــاب</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <div class="mil" v-if="personData.reasons.length > 0">
            <p
              class="headUser test"
              style="background-color: #d63024 !important; color: white !important"
            >
              الأسـبــاب
            </p>
            <p class="otherUnit">{{ personData.reasons[0].reason_description }}</p>
          </div>
          <!-- start medical -->

          <div class="travelSolution" style="display: flex; align-items: center; height: 22px">
            <h4 style="margin-left: 10px">الموقف الطبي</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <div class="test otherWidth-med">
            <div
              class="mil"
              :style="{
                maxWidth: personData.medical_history.length == 0 ? '400px' : '',
              }"
            >
              <p
                class="headUser data-btn"
                @click="openMedicalpopup()"
                style="background-color: #d63024"
              >
                اللجان الطبية
              </p>

              <p class="otherUnit">
                <span v-if="personData.medical_history.length > 0">
                  {{ toAr(`${personData.medical_history.length}`) }}
                </span>
                <span v-else>لايكن</span>
              </p>
            </div>

            <div class="mil" v-if="personData.medical_history.length != 0">
              <p class="headUser">التشخيص</p>
              <p class="otherUnit">{{ personData.medical_history[0]?.tashkhes }}</p>
            </div>
          </div>
          <!-- end medical  -->

          <!-- start reson  -->
          <div
            class="travelSolution"
            style="
              display: flex;
              align-items: center;
              height: 22px;
              cursor: pointer;
              margin-bottom: 0;
            "
            @click="reson = !reson"
          >
            <h4 style="margin-left: 10px">البيانات الإجتماعية</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <div class="reson" v-if="reson">
            <div class="test" style="margin-bottom: 0px">
              <div class="mil">
                <p class="headUser data-btn" @click="openRelationPopup([1, 15])">
                  الحالة الاجتماعية
                </p>
                <p class="otherUnit">
                  {{
                    personData.marital_state_code == 1
                      ? 'متزوج ويعول'
                      : personData.marital_state_code == 4
                        ? 'مطلق'
                        : personData.marital_state_code == 2
                          ? 'متزوج'
                          : personData.marital_state_code == 0
                            ? 'اعزب'
                            : personData.marital_state_code == 42
                              ? 'مطلق / متزوج'
                              : '----'
                  }}
                </p>
              </div>
              <div class="mil">
                <p class="headUser">وظيفة الزوجة</p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter(
                      (d) => d.relation_degree_code == 1 || d.relation_degree_code == 1,
                    ).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter((d) => d.relation_degree_code == 1)[0]
                          ?.notes || '--'
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>
              <div class="mil">
                <p class="headUser data-btn" @click="openRelationPopup([2, 7])">عدد الابناء</p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter(
                      (d) => d.relation_degree_code == 2 || d.relation_degree_code == 7,
                    ).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter(
                          (d) => d.relation_degree_code == 2 || d.relation_degree_code == 7,
                        ).length
                      }`,
                    )
                  }}
                </p>

                <p class="otherUnit" v-else>لايكن</p>
              </div>
              <div class="mil">
                <p
                  class="headUser data-btn"
                  @click="openRelationPopup([2])"
                  style="background-color: rgba(111, 210, 255, 64%) !important"
                >
                  الذكور
                </p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter((d) => d.relation_degree_code == 2).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter((d) => d.relation_degree_code == 2).length
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>
              <div class="mil">
                <p
                  class="headUser data-btn"
                  @click="openRelationPopup([7])"
                  style="background-color: rgba(255 207 245) !important"
                >
                  الاناث
                </p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter((d) => d.relation_degree_code == 7).length !==
                    0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter((d) => d.relation_degree_code == 7).length
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>

              <div
                class="mil"
                v-if="
                  personData.relations?.filter((d) => d.relation_degree_code == 3).length > 0
                "
              >
                <p class="headUser">وظيفة الوالد</p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter((d) => d.relation_degree_code == 3).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter((d) => d.relation_degree_code == 3)[0]
                          ?.notes
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>
              <div
                class="mil"
                v-if="
                  personData.relations?.filter((d) => d.relation_degree_code == 4).length > 0
                "
              >
                <p class="headUser">وظيفة الوالده</p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter((d) => d.relation_degree_code == 4).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter((d) => d.relation_degree_code == 4)[0]
                          ?.notes
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>
              <div class="mil">
                <p class="headUser data-btn" @click="openRelationPopup([5, 6])">عدد الاشقاء</p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter(
                      (d) => d.relation_degree_code == 5 || d.relation_degree_code == 6,
                    ).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter(
                          (d) => d.relation_degree_code == 5 || d.relation_degree_code == 6,
                        ).length
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>
              <div class="mil">
                <!-- v-if="
                  personData.relations?.filter(
                    (d) =>
                      (d) =>
                        d.relation_degree_code == 11 ||
                        d.relation_degree_code == 9 ||
                        d.relation_degree_code == 10 ||
                        d.relation_degree_code == 8
                    ).length > 0
                "-->
                <p class="headUser data-btn" @click="openRelationPopup([11, 9, 10, 8])">
                  عدد الاقارب
                </p>
                <p
                  class="otherUnit"
                  v-if="
                    personData.relations?.filter(
                      (d) =>
                        d.relation_degree_code == 11 ||
                        d.relation_degree_code == 9 ||
                        d.relation_degree_code == 10 ||
                        d.relation_degree_code == 8,
                    ).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        personData.relations?.filter(
                          (d) =>
                            d.relation_degree_code == 11 ||
                            d.relation_degree_code == 9 ||
                            d.relation_degree_code == 10 ||
                            d.relation_degree_code == 8,
                        ).length
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>
            </div>
          </div>

          <!-- ================================ Reson -->
          <div
            v-if="
              // personData.type_code == 5 ||
              // personData.type_code == 6 ||
              // personData.type_code == 7 ||
              // personData.type_code == 8 ||
              // personData.type_code == 9
              false
            "
            calss="resonhead"
          >
            <span
              class="resonHead"
              style="color: #b7281e; font-size: 18px; font-weight: 600; margin: none"
              >الاسباب</span
            >
            <h5 v-if="reasonLength == 0">لا يـوجــد اسـبـاب</h5>
            <div class="reasonContainer">
              <!-- v-if="reasonLength !== 0" -->
              <p class="resonText" v-for="re in personData.reasons" :key="index">
                <span
                  v-if="
                    re.reason_relation === '1' ||
                    re.reason_relation === '2' ||
                    re.reason_relation === '3' ||
                    re.reason_relation === '4'
                  "
                  >* {{ re.relation_degree_name }} :</span
                >
                <span v-if="re.reason_relation === '0'">* هــو:</span>
                <span style="margin: 0 5px">
                  {{ re.reason_description + '--' }}
                </span>
              </p>
            </div>
          </div>

          <!-- end reson -->
          <hr v-if="vote_type == '3' || vote_type == '0'" />
          <div class="travelSolution" style="display: flex; align-items: center; height: 22px">
            <!-- @click="opinin = !opinin" -->
            <h4 style="margin-left: 10px">الآراء</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>

          <div class="row">
            <!-- && opinin -->
            <div class="mil" style="width: 15%">
              <p
                class="headUser"
                @click="
                  openReasonspopup(
                    personData.opinions.filter((e) => e.sp == 8)[0]?.unit_refuse_reason,
                  )
                "
              >
                رأي الســـلاح
              </p>
              <p
                class="otherUnit"
                v-if="personData.opinions.filter((e) => e.sp == 8)[0]?.a_op_code == 1"
                style="min-width: 37%"
              >
                <span v-if="personData?.type_code == 8">عدم استمرار</span>
                <span v-else-if="personData.type_code == 10">عدم تثبيت</span>
                <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                  >موافقة</span
                >
                <span v-else-if="personData.type_code == 9">رفت</span>
                <span v-else>اوفق</span>
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 8 && e.a_op_code == 0)"
                class="otherUnit"
                style="min-width: 37%"
              >
                <span v-if="personData.type_code == 8">استمرار</span>
                <span v-else-if="personData.type_code == 10">التثبيت</span>
                <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                  >عدم الموافقة</span
                >
                <span v-else-if="personData.type_code == 9">استمرار</span>
                <span v-else>لا اوافق</span>
              </p>
              <p v-else class="otherUnit">بدون تسجيل</p>
            </div>
            <!-- ======================================= -->
            <!-- v-if="personData.pern_army != personData.army_code && personData.opinions?.filter(
                (e) => e.sp == 8 && (e.ua_op_code == 1 || e.ua_op_code == 0)
            ).length > 0"-->
            <div
              class="mil"
              style="width: 15%"
              v-if="
                personData.pern_army != personData.army_code &&
                personData.opinions?.filter(
                  (e) => e.sp == 8 && (e.ua_op_code == 1 || e.ua_op_code == 0),
                ).length > 0
              "
            >
              <p class="headUser" style="cursor: pointer">رأي التشكيل</p>
              <p
                class="otherUnit"
                v-if="personData.opinions.filter((e) => e.sp == 8)[0]?.ua_op_code == 1"
                style="min-width: 37%"
              >
                <span v-if="personData?.type_code == 8">عدم استمرار</span>
                <span v-else-if="personData.type_code == 10">عدم تثبيت</span>
                <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                  >موافقة</span
                >
                <span v-else-if="personData.type_code == 9">رفت</span>
                <span v-else>اوفق</span>
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 8)[0]?.ua_op_code == 0"
                class="otherUnit"
                style="min-width: 37%"
              >
                <span v-if="personData.type_code == 8">استمرار</span>
                <span v-else-if="personData.type_code == 10">التثبيت</span>
                <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                  >عدم الموافقة</span
                >
                <span v-else-if="personData.type_code == 9">استمرار</span>
                <span v-else>لا اوافق</span>
              </p>
              <p v-else class="otherUnit">بدون تسجيل</p>
            </div>
            <!-- ///////////////////////// -->

            <!-- <button
              class="oma"
              style="
                background: #7d7d7d;
                border-radius: 10px;
                color: white;
                font-size: 18px;
                border: none;
                padding: 8px 15px;
                min-width: 150px;
                width: 200px;
              "
              @click="openOpinionManager()"
            >رأي هيئـــة التنظيـــم والادارة</button>-->

            <div class="mil" style="width: 30%">
              <p
                class="headUser"
                @click="openOpinionManager()"
                style="cursor: pointer; width: 250px"
              >
                رأي رئيس هيئـــة التنظيـــم والادارة ق.م
              </p>
              <p class="otherUnit" style="min-width: 300px !important">
                {{ personData.haya_head_opinion }}
              </p>
            </div>
            <div class="mil" v-if="memberType" style="width: 40%">
              <p
                class="headUser"
                style="
                  min-width: 186px !important;
                  background-color: rgb(21, 142, 33) !important;
                  color: white;
                  font-size: 16px;
                  flex: 1;
                "
              >
                قـــرار السيــــد رئــيس اركــان حـــرب القوات المسلــحــة
              </p>
              <select
                class="otherUnit"
                style="
                  width: 100%;
                  outline: none;
                  border: none;
                  font-size: 16px;
                  font-weight: 600;
                  font-family: cairo;
                "
                v-model="member_decision"
                @change="handleDecisionChange"
                :disabled="member != 'رئيس اركان حرب القوات المسلحة'"
              >
                <option value="4"></option>
                <option value="1" style="font-size: 14px; font-family: 'cairo'; font-weight: 600">
                  <span v-if="personData.type_code == 8">انهاء الخدمة لعدم الصلاحية</span>
                  <span v-else-if="personData.type_code == 10">عدم تثبيت</span>
                  <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                    >موافقة</span
                  >
                  <span v-else-if="personData.type_code == 9">رفت</span>
                  <span v-else>اوفق</span>
                </option>
                <option value="2" style="font-size: 14px; font-family: 'cairo'; font-weight: 600">
                  <span v-if="personData.type_code == 8">استمرار</span>
                  <span v-else-if="personData.type_code == 10">التثبيت</span>
                  <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="personData.type_code == 9">استمرار</span>
                  <span v-else>لا اوافق</span>
                </option>
                <option value="0" style="font-size: 14px; font-family: 'cairo'; font-weight: 600">
                  ارجاء
                </option>
              </select>
            </div>
          </div>
          <!-- ------------------------------------------------------------------------ -->
          <!-- ------------------------------------------------------------------------ -->
          <div
            class="travelSolution"
            style="display: flex; align-items: center; height: 22px"
            v-if="false"
          >
            <!-- @click="opinin = !opinin" -->
            <h4 style="margin-left: 10px">الآراءد</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <div class="opininRes" v-if="false">
            <!-- && opinin -->
            <div class="res-screen">
              <p class="leader">القائد المباشر</p>
              <p
                v-if="personData.opinions.filter((e) => e.sp == 4)[0]?.u_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي.
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 4)[0]?.u_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 4)[0]?.u_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
            <!-- <div class="res-screen">
              <p class="leader">القائد المباشر</p>
              <p class="resLeader" style="background-color: #158e21">موافق</p>
            </div>-->
            <div class="res-screen">
              <p class="leader">قائد المستوى الأعلى</p>
              <p
                v-if="personData.opinions.filter((e) => e.sp == 4)[0]?.ua_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 4)[0]?.ua_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 4)[0]?.ua_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
            <div class="res-screen">
              <p class="leader">رأي السلاح</p>
              <p
                v-if="personData.opinions.filter((e) => e.sp == 4)[0]?.a_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 4)[0]?.a_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 4)[0]?.a_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
          </div>
          <!-- ------------------------------------------------------------------------ -->
          <!-- ------------------------------------------------------------------------ -->

          <div
            class="travelSolution"
            style="display: flex; align-items: center; height: 22px"
            v-if="false"
          >
            <!-- @click="opinin = !opinin" -->
            <h4 style="margin-left: 10px">الآراء في الاستقالة</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <div class="opininRes" v-if="false">
            <!-- && opinin -->
            <div class="res-screen">
              <p class="leader">القائد المباشر</p>
              <p
                v-if="personData.opinions.filter((e) => e.sp == 5)[0]?.u_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي.
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 5)[0]?.u_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 5)[0]?.u_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
            <!-- <div class="res-screen">
              <p class="leader">القائد المباشر</p>
              <p class="resLeader" style="background-color: #158e21">موافق</p>
            </div>-->
            <div class="res-screen">
              <p class="leader">قائد المستوى الأعلى</p>
              <p
                v-if="personData.opinions.filter((e) => e.sp == 5)[0]?.ua_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 5)[0]?.ua_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 5)[0]?.ua_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
            <div class="res-screen">
              <p class="leader">رأي السلاح</p>
              <p
                v-if="personData.opinions.filter((e) => e.sp == 5)[0]?.a_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 5)[0]?.a_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="personData.opinions.filter((e) => e.sp == 5)[0]?.a_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
          </div>

          <!-- ------------------------------------------------------------------------ -->
          <!-- ------------------------------------------------------------------------ -->

          <!-- start opinin -->
          <div class="op">
            <div
              class="travelSolution"
              style="display: flex; align-items: center; height: 22px"
              v-if="personData.type_code == 2 || personData.type_code == 3"
            >
              <!-- @click="opinin = !opinin" -->
              <h4 style="margin-left: 10px">الآراء في التجديد</h4>
              <hr style="background-color: black; font-weight: bolder" />
            </div>
            <div
              class="opininRes"
              v-if="personData.type_code == 2 || personData.type_code == 3"
            >
              <!-- && opinin -->
              <div class="res-screen">
                <p class="leader">القائد المباشر</p>
                <p
                  v-if="personData.opinions.filter((e) => e.sp == 2)[0]?.u_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي.
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 2)[0]?.u_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 2)[0]?.u_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>
              <!-- <div class="res-screen">
              <p class="leader">القائد المباشر</p>
              <p class="resLeader" style="background-color: #158e21">موافق</p>
              </div>-->
              <div class="res-screen">
                <p class="leader">قائد المستوى الأعلى</p>
                <p
                  v-if="personData.opinions.filter((e) => e.sp == 2)[0]?.ua_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 2)[0]?.ua_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 2)[0]?.ua_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>
              <div class="res-screen">
                <p class="leader">رأي السلاح</p>
                <p
                  v-if="personData.opinions.filter((e) => e.sp == 2)[0]?.a_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 2)[0]?.a_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 2)[0]?.a_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>
            </div>
            <div
              class="travelSolution"
              style="display: flex; align-items: center; height: 22px"
              v-if="personData.type_code == 1 || personData.type_code == 3"
            >
              <!-- @click="opinin = !opinin" -->
              <h4 style="margin-left: 10px">الآراء في الترقي</h4>
              <hr style="background-color: black; font-weight: bolder" />
            </div>
            <div
              class="opininRes"
              v-if="personData.type_code == 1 || personData.type_code == 3"
            >
              <!-- && opinin -->
              <div class="res-screen">
                <p class="leader">القائد المباشر</p>
                <p
                  v-if="personData.opinions.filter((e) => e.sp == 1)[0]?.u_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 1)[0]?.u_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 1)[0]?.u_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>

              <div class="res-screen">
                <p class="leader">قائد المستوى الأعلى</p>
                <p
                  v-if="personData.opinions.filter((e) => e.sp == 1)[0]?.ua_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 1)[0]?.ua_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 1)[0]?.ua_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>
              <div class="res-screen">
                <p class="leader">رأي السلاح</p>
                <p
                  v-if="personData.opinions.filter((e) => e.sp == 1)[0]?.a_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 1)[0]?.a_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="personData.opinions.filter((e) => e.sp == 1)[0]?.a_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>
            </div>
          </div>
          <div
            class="member_opinion"
            v-if="personData?.mil_ser && !out_user && !show"
            style="display: none"
          >
            <div class="master-opinin" v-if="vote_type != 1">
              <p class="master-opinin-name">{{ member_job }}</p>
              <form>
                <label style="color: #158e21" class="accept">
                  <input
                    type="radio"
                    value="1"
                    :checked="current_vote == 1"
                    name="opinin-pre"
                    v-model="member_op"
                    @click="member_op == 1 ? vote_handel(4)((member_op = '')) : vote_handel(1)"
                    :disabled="disable"
                  />
                  <span
                    class="customChecked"
                    v-if="member_op == 1"
                    style="background-color: #158e21 !important"
                  ></span>

                  <span v-if="personData.type_code == 8">عدم استمرار</span>
                  <span v-else-if="personData.type_code == 10">عدم تثبيت</span>
                  <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                    >موافقة</span
                  >
                  <span v-else-if="personData.type_code == 9">رفت</span>
                  <span v-else>اوفق</span>
                </label>
                <label style="color: #b7281e" class="rej">
                  <input
                    type="radio"
                    value="2"
                    name="opinin-pre"
                    :checked="current_vote == 2"
                    v-model="member_op"
                    @click="member_op == 2 ? vote_handel(4)((member_op = '')) : vote_handel(2)"
                    :disabled="disable"
                  />
                  <span
                    class="customChecked"
                    v-if="member_op == 2"
                    style="background-color: #b7281e !important"
                  ></span>
                  <span v-if="personData.type_code == 8">استمرار</span>
                  <span v-else-if="personData.type_code == 10">التثبيت</span>
                  <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="personData.type_code == 9">استمرار</span>
                  <span v-else>لا اوافق</span>
                </label>
                <!-- <label style="color: goldenrod" class="notAcceptAndNotrej">
                  <input
                    type="radio"
                    :checked="current_vote == 0"
                    name="opinin-pre"
                    v-model="member_op"
                    @click="vote_handel(0)"
                    :disabled="disable"
                  />
                  <span class="customChecked"></span>

                  ارجاء
                </label>-->
              </form>
            </div>

            <div class="master-opinin" v-if="!out_user && vote_type == 1 && !show">
              <p class="master-opinin-name">قرار اللجنة</p>
              <form>
                <label style="color: #158e21" class="accept">
                  <input
                    type="radio"
                    value="1"
                    name="decision-pre"
                    id="accept-pr"
                    v-model="member_decision"
                    @click="
                      member_decision == 1
                        ? decision_handel(4)((member_decision = ''))
                        : decision_handel(1)
                    "
                    :disabled="disable"
                    :checked="member_decision == 1"
                  />
                  <span
                    class="customChecked"
                    v-if="member_decision == '1'"
                    style="background-color: #158e21 !important"
                  ></span>

                  <span v-if="personData.type_code == 8">عدم استمرار</span>
                  <span v-else-if="personData.type_code == 10">عدم تثبيت</span>
                  <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                    >موافقة</span
                  >
                  <span v-else-if="personData.type_code == 9">رفت</span>
                  <span v-else>اوفق</span>
                </label>
                <label style="color: #b7281e !important; margin: 5px 0" class="rej">
                  <input
                    type="radio"
                    value="2"
                    name="decision-pre"
                    v-model="member_decision"
                    @click="
                      member_decision == 2
                        ? decision_handel(4)((member_decision = ''))
                        : decision_handel(2)
                    "
                    :disabled="disable"
                    :checked="member_decision == 2"
                  />
                  <span
                    class="customChecked"
                    v-if="member_decision == '2'"
                    style="background-color: #b7281e"
                  ></span>

                  <span v-if="personData.type_code == 8">استمرار</span>
                  <span v-else-if="personData.type_code == 10">التثبيت</span>
                  <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="personData.type_code == 9">استمرار</span>
                  <span v-else>لا اوافق</span>
                </label>

                <label style="color: goldenrod; display: none" class="notAcceptAndNotrej">
                  <input
                    type="radio"
                    value="notAndNot"
                    name="decision-pre"
                    v-model="member_decision"
                    @click="
                      member_decision == 2
                        ? decision_handel(4)((member_decision = ''))
                        : decision_handel(2)
                    "
                    :disabled="disable"
                    :checked="personData.final_decision == 0"
                  />
                  <span class="customChecked"></span>
                  ارجاء
                </label>
              </form>
            </div>
          </div>
          <p
            style="
              text-align: center;
              margin: auto;
              font-size: 18px;
              font-weight: 600;
              padding-top: 20px;
            "
            v-if="personData.date_serial"
          >
            {{ toAr(`${personData.date_serial} `) }}/
            {{ toAr(`${personData.afr_persons_len} `) }}
          </p>
          <div class="control" v-if="out_user">
            <div
              class="control-btn"
              style="
                display: flex;
                justify-content: center;
                gap: 50px;
                align-items: center;
                width: 60%;
              "
            >
              <button @click="gothen(data)" v-if="index < data.length">
                الـتـالـي
              </button>
              سجل {{ index + 1 }} من {{ data.length }}
              <button @click="goback(data)">السابق</button>
            </div>
          </div>
        </div>
        <!-- Image and Counters Section -->
        <div class="counters">
          <img
            id="personImage"
            :src="smallPhoto"
            alt="user image"
            crossorigin="anonymous"
            @click="openPhotopopup()"
          />
          <div class="rejection_data" style>
            <div
              class="traq"
              :style="{
                color:
                  personData.rejections?.filter((e) => e.sp == 2).length > 0 ? '#b7281e' : 'green',
              }"
              v-if="personData.type_code == 3 || personData.type_code == 2"
            >
              <p>تجــــديـد</p>
            </div>
            <button
              v-if="personData.rejections?.filter((e) => e.sp == 2).length > 0"
              @click="openUpdatqpopup()"
            >
              موانع التجــديد
            </button>
            <div
              class="traq"
              :style="{
                color:
                  personData.rejections?.filter((e) => e.sp == 1).length > 0 ? '#b7281e' : 'green',
              }"
              v-if="personData.type_code == 3 || personData.type_code == 1"
            >
              <p>تـــرقــــي</p>
            </div>
            <button
              v-if="personData.rejections?.filter((e) => e.sp == 1).length > 0"
              style
              @click="openTraqpopup()"
            >
              موانع التـــرقــــي
            </button>

            <div class="traq" v-if="personData.type_code == 5">
              <p style="border-color: #b7281e !important; color: #b7281e !important">استقالة</p>
            </div>
            <div class="traq" v-if="personData.type_code == 6">
              <p style="border-color: #f98d11d1 !important; color: #f98d11d1 !important">
                تــرشـيــح
              </p>
            </div>
            <div class="traq" v-if="personData.type_code == 8">
              <p style="border-color: #b7281e !important; color: #b7281e !important">عدم صلاحية</p>
            </div>
            <div class="traq" v-if="personData.type_code == 9">
              <p style="border-color: #b7281e !important; color: #b7281e !important">
                الرفت الجوازي
              </p>
            </div>
            <div class="traq" v-if="personData.type_code == 10">
              <p style="border-color: #b7281e !important; color: #b7281e !important">عدم التثبيت</p>
            </div>

            <div class="traq" v-if="personData.type_code == 4">
              <p style="border-color: #b7281e; color: #b7281e">عدم الرغبة</p>
            </div>
            <div class="traq" v-if="personData.type_code == 15">
              <p style="border-color: #b7281e; color: #b7281e">الإستبقاء</p>
            </div>
          </div>

          <div class="traq" v-if="personData.type_code == 7">
            <p style="border-color: #158e21 !important; color: #158e21 !important">التماس</p>
          </div>
          <div class="traq" v-if="personData.type_code == 6">
            <p
              style="
                border-color: #158e21 !important;
                color: #158e21 !important;
                font-size: 14px !important;
              "
            >
              ترشيح منشأت تعليمية
            </p>
          </div>

          <div
            class="counter-container accept-counter"
            v-if="vote_type == '1' && !out_user && !show"
            v-show="vote_1.length > 0"
          >
            <div
              class="counter-circle"
              style="padding: 15px; cursor: pointer"
              @click="openAcceptpopup()"
            >
              <p class="circle-label" style="color: black !important; margin: 0; color: #158e21">
                {{ toAr(`${vote_1.length}`) }}
                <br />

                <span v-if="personData.type_code == 8">عدم استمرار</span>
                <span v-else-if="personData.type_code == 10">عدم تثبيت</span>
                <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                  >موافقة</span
                >
                <span v-else-if="personData.type_code == 9">رفت</span>
                <span v-else>موافق</span>
              </p>
            </div>
            <!-- <div class="counter-names" v-for="us in vote_1" :key="us.id">
              <p>{{ us.degree }} {{ us.member }}</p>
            </div>-->
          </div>
          <div
            class="counter-container reject-counter"
            v-if="vote_type == '1'"
            v-show="vote_2.length > 0"
            style="margin-top: 10px; cursor: pointer"
          >
            <div class="counter-circle" style="padding: 15px" @click="openAcceptpopup()">
              <p
                class="circle-label"
                style="
                  color: black !important;
                  margin: 0;
                  color: #b7281e;
                  display: flex;
                  flex-direction: column;
                "
              >
                <span>{{ toAr(`${vote_2.length}`) }}</span>
                <span style="font-size: 14px; white-space: nowrap">
                  <span v-if="personData.type_code == 8">استمرار</span>
                  <span v-else-if="personData.type_code == 10">التثبيت</span>
                  <span v-else-if="personData.type_code == 5 || personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="personData.type_code == 9">استمرار</span>
                  <span v-else>لا اوافق</span>
                </span>
              </p>
            </div>

            <!-- <div
              class="counter-names"
              v-for="us in vote_2"
              :key="us.id"
              style="w"
            >
              <p>{{ us.degree }} {{ us.member }}</p>
            </div>-->
          </div>
          <div
            class="counter-container suspense-counter"
            v-if="vote_type == '1'"
            v-show="vote_0.length > 0"
            style="display: none"
          >
            <div class="counter-circle" v-if="!out_user && !show">
              <p class="circle-label" style="color: black !important">الارجاء</p>
            </div>
            <div
              class="counter-names"
              v-for="us in vote_0"
              :key="us.id"
              v-if="!out_user && !show"
            >
              <p>{{ us.degree }} / {{ us.member }}</p>
            </div>
          </div>
          <div
            class="suggest_unit"
            style="
              width: 90%;
              min-height: 30px;
              border-radius: 21px;
              border: 7px solid rgb(21, 142, 33);
              margin-top: 5px;
              padding: 5px;
            "
            v-if="personData.type_code == 6"
          >
            <p style="margin: 0; text-align: center">{{ personData.sugg_unit_name }}</p>
          </div>
          <div class="upload-container" v-if="out_user && user_id != 100">
            <div class="image1">
              <label for="imageInput1" id="UploadImg">كارت نصفي</label>
              <input type="file" id="imageInput1" accept="image/*" name="image1" />
            </div>
            <div class="image1">
              <label for="imageInput1" id="UploadImg">كارت طولي</label>
              <input type="file" id="imageInput2" accept="image/*" name="image2" />
            </div>
            <div class="image1">
              <label for="imageInput3" id="UploadImg">كارت عائلى</label>
              <input type="file" id="imageInput3" accept="image/*" name="image3" />
            </div>
            <div class="image1">
              <label for="imageInput4" id="UploadImg">كارت عائلى اضافى</label>
              <input type="file" id="imageInput4" accept="image/*" name="image4" />
            </div>

            <button @click="uploadImage()" style="background: #158e21; margin-top: 20px">
              حفظ
            </button>

            <p id="status"></p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
<style scoped>
.nouser {
  position: absolute;
  top: 50%;
  right: 50%;
  transform: translate(50%, -50%);
}

.users {
  margin: 0 20px;
  display: flex;
  gap: 15px;
}

.dataUser {
  width: 100vw;
  margin-right: 20px;
}

.prim-data {
  display: flex;
  align-items: center;
  cursor: pointer;
  height: 18px !important;
}

.prim-data h4 {
  font-size: 20px;
  padding: 5px;
}

hr {
  flex: 1;
}

.row {
  display: flex;
  justify-content: space-between;
  margin: 13px 0;
  gap: 11px;
}

.data-btn {
  cursor: pointer;
  transition: all 300ms;

  background-color: #f98d11d1 !important;
  color: rgb(5, 1, 1) !important;
  cursor: pointer !important;
}

.bunish-btn {
  background-color: #d63024 !important;
  color: #eee !important;
}

.data-btn:hover {
  transform: scale(1.1);
  /* filter: brightness(0); */
}

/* m#gana*/
.test {
  display: grid;
  flex-wrap: wrap;
  gap: 13px;
  margin: 10px 0;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

@media (max-width: 20px) {
  .test {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}

/*end m#gana*/

.mil {
  background: white;
  border-radius: 13px;
  gap: 13px;
  display: flex;
  align-items: center;
  position: relative;
  font-weight: 700;
  height: 43px;
}

.headUser {
  background-color: #8080804d;
  height: 43px;
  margin: 0;
  position: inherit;
  display: flex;
  align-items: center;
  border-radius: 25px 0px 10px 0px;
  text-align: center;
  place-content: center;
  min-width: 80px;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  padding: 1px 5px;
}

.otherUnit {
  place-content: center;
  text-align: center;
  place-content: center;
  text-align: center;
  width: 100%;
  font-size: 14px;
  padding: 5px 10px;
}

@media (min-width: 1899px) {
  .otherWidth-status {
    width: 80%;
  }

  .otherWidth-med {
    grid-template-columns: 1fr 3fr;
  }
  .otherWidth-travel {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}
@media (min-width: 1899px) {
  .control {
    margin-bottom: 100px;
  }
}

@media (max-width: 1900px) {
  .otherWidth-pun,
  .otherWidth-status,
  .otherWidth-travel,
  .otherWidth-med {
    width: 100% !important;
  }
}

@media (max-width: 1180px) {
  main {
    padding: 0 0 78px 0px;
  }
}

.opininRes {
  display: flex;
  /* justify-content: space-between; */
  font-size: 16px;
  font-weight: 600;
  height: 35px;
  align-items: center;
  gap: 150px;
}

.res-screen {
  justify-content: space-around;
  display: flex;
  gap: 10px;
}

.resLeader {
  padding: 3px;
  min-width: 65px;
  text-align: center;
  border-radius: 6px;
  color: white;
  align-self: center;
  font-size: 14px;
}

.leader {
  font-size: 16px;
}
.sec_req_flag {
  border: 3px solid red;
}

.my-opinin {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.member_opinion {
  display: flex;
  justify-content: center;
  flex-direction: column;
  margin-top: 15px;
}

.master-opinin {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
}

.master-opinin-name {
  font-size: 16px;
  font-weight: 600;
  padding-left: 5px;
  margin: 5px 0;
}
.counters span {
  text-wrap: nowrap;
  margin: -14px;
}

form {
  display: flex;
  justify-content: space-around;
  width: -61%;
  place-items: center;
  font-size: -26px;
  flex: 1;
}

.master-opinin label {
  display: flex;
  font-size: 17px;
  cursor: pointer;
  position: relative;
}

input[type='radio'] {
  display: none;
}

.customChecked {
  position: absolute;
  height: 7px;
  width: 7px;
  right: -18px;
  top: 11px;
  border-radius: 50%;
}

input[type='radio']:checked + span {
  border: 2px solid;
}

/* start past situation section  */
.past-situationsHeader {
  display: flex;
  align-items: center;
  height: 22px;
}

.past-situations {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.past-situations button {
  padding: 8px 12px;
  font-size: 18px;
  font-weight: 600;
  border: 1px solid;
  color: white;
  border-radius: 10px;
  transition: all 250ms;
}

.past-units-btn {
  background-color: gray;
}

.past-units-btn:hover {
  background-color: #929292;
}

.past-travel-btn {
  background-color: #158e21;
}

.past-medical-btn {
  background-color: #dc8a00;
}

.past-travel-btn:hover {
  background-color: #18a726;
}

.past-carts-btn {
  background-color: #b7281e;
}

.past-carts-btn:hover {
  background-color: #d63024;
}

.past-medical-btn:hover {
  background-color: #f3a41b;
}

/* end past situation section  */
/* Start Counter Section */
.counters {
  width: 200px;
  text-align: center;
  margin-bottom: 20px;
}

.counters img {
  width: 185px;
  height: 215px;
}

.counter-container {
  font-size: 15px;
}

.counter-circle {
  width: 60px;
  height: 60px;
  margin: auto;
  border-radius: 50%;
  padding: 10px;
  font-weight: bold;
}

.accept-counter .counter-circle {
  border: 7px solid #158e21;
}

.reports .sec-req {
  background-color: red;
}
.reports .sec-req:hover {
  background-color: red;
}
.accept-counter p {
  color: #158e21;
}

.reject-counter .counter-circle {
  border: 7px solid #b7281e;
}

.reject-counter p {
  color: #b7281e;
}

.suspense-counter .counter-circle {
  border: 7px solid goldenrod;
}

.suspense-counter p {
  color: goldenrod;
}

.counter-names p {
  margin: 9px;
}

.resonHead {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.resonText {
  margin: 0px;
  font-weight: 600;
  font-size: 15px;
  width: 50%;
}

.reasonContainer {
  flex-wrap: wrap;
  display: flex;
}

.homepage {
  background: linear-gradient(135deg, #ffffff, #fc9732);
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  color: #fff;
  width: 100vw !important;
  z-index: 1000 !important;
}

.homecontainer {
  text-align: center;
  animation: linear 2s ease-in-out;
}

.homecontainer img {
  width: 400px;
  height: auto;
  animation: rotateYAnim 4s infinite ease-out;
  transition: transform 0.3s ease-in-out;
  /* box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 255, 255, 0.4); */
  border-radius: 20px;
  /* border-radius: 50%; */
}

.homepage h1 {
  font-size: 3rem;
  margin: 100px 0 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
  font-weight: bold;
  color: black;
}

.outUserContainer {
  justify-content: center;
  display: flex;
  gap: 20px;
  margin-bottom: 10px;
}

.outUserContainer .input-field {
  max-width: 35%;
}

select {
  border: 1px solid rgb(0 0 0 / 23%);
  border-radius: 5px;
  min-width: 70px;
  text-align: center;
  border-radius: 8px;
}

#units:focus {
  border: none;
  box-shadow: 0px 0px 5px var(--secondColor);
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

/* End Counter Section */
.control {
  display: flex;
  justify-content: center;
  width: 92%;
  align-items: center;
  position: absolute;
  margin: 15px 0;
  padding-bottom: 95px;
}

button {
  width: 150px;
  background: var(--secondColor);
  padding: 5px;
  border-radius: 10px;
  color: white;
  font-size: 18px;
  border: none;
}
.reports button {
  width: 150px;
  background: var(--secondColor);
  padding: 15px;
  border-radius: 10px;
  color: white;
  font-size: 18px;
  border: none;
  margin-left: 15px;
}

.control button {
  background: var(--secondColor);
  width: 5rem;
  padding: 5px;
  border-radius: 10px;
  color: white;
  font-size: 18px;
  border: none;
}

button:hover {
  background-color: #d48e19;
}
.oma:hover {
  background-color: #bcbcbc;
  padding: 10px 15px;
  width: 310px;
}

select {
  font-size: 15px;
  text-align: center;
  outline: NONE;
}

option {
  font-size: 15px;
  text-align: start;
  margin: 5px;
  border-bottom: 1px solid black;
}

.traq {
  display: flex;
  justify-content: center;
  height: 108px;
  align-items: center;
}

.traq p {
  padding: 20px;
  border: 7px solid;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  align-items: center;
  display: flex;
  justify-content: center;
  font-weight: bolder;
  font-size: 18px;
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

.upload-container {
  padding: 0px;
}

.upload-container h2 {
  margin: 0;
}

.upload-container input {
  font-size: 13px;
}

#UploadImg {
  font-weight: bold;
  display: block;
  text-align: start;
  padding: 10px 0;
}
#accept-pr {
  position: relative;
}

#accept-pr::after {
  content: '';
  position: fixed;
  height: 50px;
  width: 5px;
  background-color: rgb(21, 142, 33);
  bottom: 10%;
  left: 10%;
  z-index: 10;
}
label::before {
  content: '';
  position: absolute;
  height: 15px;
  width: 15px;
  border: 2px solid;
  right: -22px;
  top: 7px;
  border-radius: 50%;
  box-shadow: 0px 1px 3px 1px;
  display: none;
}
</style>