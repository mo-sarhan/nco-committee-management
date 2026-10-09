<script>
import pastUnits from '@/components/popup/past-units.vue'
import secPerson from '@/components/popup/sec-person.vue'
import travelPopup from '@/components/popup/travelPopup.vue'
import courtPopup from '@/components/popup/courtPopup.vue'
import CourtPopup from '@/components/popup/courtPopup.vue'
import MedicalPopup from '@/components/popup/medicalPopup.vue'
import HistoryPopup from '@/components/popup/historyPopup.vue'
import PersonPhoto from '@/components/popup/PersonPhoto.vue'
import RelationPopup from '@/components/popup/relationPopup.vue'
import ConsistancyPopup from '@/components/popup/consistancyPopup.vue'
import reportVue from '@/components/popup/report.vue'
import axios from 'axios'
import TraqPopup from '@/components/popup/TraqPopup.vue'
import UpdatePopup from '@/components/popup/UpdatePopup.vue'
import courses from '@/components/popup/courses.vue'
import eff_report from '@/components/popup/eff_report.vue'
import reasonsPopup from '@/components/popup/reasonsPopup.vue'
import acceptpop from '@/components/popup/acceptpop.vue'
import { convertToArabicNumbers } from '@/utils/glopal'
import Acceptpop from '@/components/popup/acceptpop.vue'
import Poea from '@/components/popup/Poea.vue'
import OutmemberReport from '@/components/popup/OutmemberReport.vue'
import OpinionManager from '../components/global/popup/opinionManager.vue'
export default {
  data() {
    return {
      milSer: '',
      unit: '',
      data: [],
      index: 0,
      data2: [],
      rejection_res: [],
      rejection_traq: [],
      rejection_update: [],
      usersTable: [],
      filteredUsersTable: [],
      unit_Selection: '',
      pern_Selection: '',
      lagnaType: 'all',
      LagnaDay: 'all',
      primData: true,
      reson: true,
      poea: false,
      isSecVisiable: false,
      count: 0,
      reportData: {},
      opManager: false,
      reasons: '',
      // opinin: true,
      preOpinin: null,
      memberForDay: null,
      lastOpinin: null,
      isVisiable: false,
      travelIsVisiable: false,
      courtIsVisiable: false,
      reportIsVisiable: false,
      MedicalIsVisiable: false,
      RelationIsVisiable: false,
      ConsistancyIsVisiable: false,
      HistoryIsVisiable: false,
      TraqIsVisiable: false,
      UpdateIsVisiable: false,
      PersonPhoto: false,
      suggest_unit: '',
      user: [],
      lagna: [],
      opinion_member: false,
      vote_member: false,
      personData: [],
      punshiments: [],
      punishLength: 0,
      jobsUnitsLength: 0,
      jobsunits: [],
      travel: [],
      travelLength: 0,
      member_op: '',
      member_decision: '',
      reasonLength: 0,
      member_job: '',
      vote_0: [],
      vote_1: [],
      vote_2: [],
      habs: '',
      sta: {},
      hagz: '',
      OutReport: false,
      unitName: '',
      unitPersonsPhoto: [],
      court: '',
      // sta: this.personData.committee_punishment_jobs_sta,
      disable: false,
      vote_type: 3,
      smallPhoto: '',
      largePhoto: '',
      familyPhoto: '',
      current_vote: null,
      muscle_weiht: null,
      medical: [],
      out_user: null,
      user_id: false,
      TraqPopupVisible: false,
      UpdatePopupVisible: false,
      rejections_traq: [],
      rejections_update: [],
      attened: false,
      days: {},
      attendDay: '',
      attended_number: '',
      attendance_number: '',
      checkLagna: '1',
      alert: false,
      coursesPopupVisible: false,
      Eff_reportPopupVisible: false,
      reasonsPopupVisible: false,
      AcceptPopupVisible: false,
      RejectPopupVisible: false,
      allMemberInthislagna: localStorage.getItem('allMemberInthislagna'),
      unitPersonsData: [],
      filterUnitPersonsData: [],
      show: false,
      outMember: '',
      consis: '',
      memberType: false,
      effLength: null,
      opSelection: '',
      pernName: [],
      member: '',
    }
  },
  components: {
    pastUnits,
    secPerson,
    Poea,
    travelPopup,
    courtPopup,
    CourtPopup,
    MedicalPopup,
    PersonPhoto,
    HistoryPopup,
    RelationPopup,
    ConsistancyPopup,
    TraqPopup,
    UpdatePopup,
    eff_report,
    courses,
    reasonsPopup,
    acceptpop,
    Acceptpop,
    reportVue,
    OutmemberReport,
    // opinion,
    OpinionManager,
  },

  mounted() {
    // check consis

    this.memberType = localStorage.getItem('member_type')

    this.member = localStorage.getItem('member_name')
    // checkout_user
    this.out_user = localStorage.getItem('out_user') == 'true'
    this.outMember = localStorage.getItem('army_code')
    this.user_id = localStorage.getItem('user_id') == 100
    this.unitName = localStorage.getItem('unit_name')
    this.show = localStorage.getItem('show')
    console.log(this.show)
    // vote_type =  =
    // 1 --> can vote and decide
    this.vote_type = localStorage.getItem('vote_type')
    if (!this.out_user && !this.show) {
      this.useSocket()
      // console.log(this.data);
    } else if (!this.show) {
      this.UnitsName()
    } else {
      this.showPerson()
    }

    if (this.user_id == 100) {
      this.fetchUserDataId()
    }

    this.member_job = localStorage.getItem('member_job')
    this.days = JSON.parse(localStorage.getItem('days'))
    this.attendance_number = JSON.parse(localStorage.getItem('attendance_number'))
    this.attended_number = JSON.parse(localStorage.getItem('attended_number'))
  },
  methods: {
    handleDecisionChange() {
      // Same logic as your radio button click
      if (this.member_decision == 1) {
        this.decision_handel(1)
      } else if (this.member_decision == 2) {
        this.decision_handel(2)
      } else if (this.member_decision == 0) {
        this.decision_handel(0) // assuming 4 = postpone/ارجاء
      } else if (this.member_decision == 4) {
        this.decision_handel(4)
      }
    },

    checkConsis() {
      console.log('start')
      if (this.prsonData?.length - 100 >= this.personData?.weight) {
        this.consis = 'لائق'
      } else {
        if (25 >= Number(this.personData?.tot_years) >= 20) {
          ;(25 * (this.personData?.length / 100) * this.personData?.length) / 100 >
          this.personData?.weight
            ? (this.consis = 'لائق')
            : (this.consis = 'غير لائق')
        } else if (30 >= Number(this.personData?.tot_years) >= 26) {
          ;(25.5 * (this.personData?.length / 100) * this.personData?.length) / 100 >
          this.personData?.weight
            ? (this.consis = 'لائق')
            : (this.consis = 'غير لائق')
        } else if (35 >= Number(this.personData.tot_years) >= 31) {
          ;(26.5 * (this.personData.length / 100) * this.personData.length) / 100 >
          this.personData?.weight
            ? (this.consis = 'لائق')
            : (this.consis = 'غير لائق')
        } else if (40 >= Number(this.personData.tot_years) >= 36) {
          ;(27.5 * (this.personData.length / 100) * this.personData.length) / 100 >
          this.personData?.weight
            ? (this.consis = 'لائق')
            : (this.consis = 'غير لائق')
        } else if (50 >= Number(this.personData.tot_years) >= 41) {
          ;(28 * (this.personData.length / 100) * this.personData.length) / 100 >
          this.personData?.weight
            ? (this.consis = 'لائق')
            : (this.consis = 'غير لائق')
        } else if (Number(this.personData.tot_years) > 50) {
          ;(29 * (this.personData.length / 100) * this.personData.length) / 100 >
          this.personData?.weight
            ? (this.consis = 'لائق')
            : (this.consis = 'غير لائق')
        }
      }
      console.log(this.consis)
    },
    // ==========================================================
    async showPerson() {
      try {
        const res = await axios.get(`/person/${66701220080}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        this.personData = res.data
        this.sta = { ...this.personData.committee_punishment_jobs_sta[0] }
        console.log(this.sta)
        const h = this.personData.votes?.filter(
          (u) =>
            u.user_data.degree === localStorage.getItem('rank') &&
            u.user_data.member === localStorage.getItem('member_name'),
        )[0]
        this.current_vote = h?.vote_type

        this.punshiments = this.personData.committee_punishment_jobs

        this.punishLength = this.personData.committee_punishment_jobs_sta[0]?.total || 'لا يكن'

        this.punishCortLength = this.personData.committee_punishment_jobs_sta[0]?.cort || 'لا يكن'
        this.punishStayLength = this.personData.committee_punishment_jobs_sta[0]?.stay || 'لا يكن'

        this.punishNotStayLength =
          this.personData.committee_punishment_jobs_sta[0]?.not_stay || 'لا يكن'
        this.jobunits = [...(this.personData.committee_jobs || [])]
        this.jobsUnitsLength = this.personData.committee_jobs?.length
        this.travel = [...(this.personData.committee_travel_jobs || [])]
        this.travelLength = this.personData.committee_travel_jobs?.length
        this.reasonLength = this.personData.reasons?.length
        this.smallPhoto = `http://afrad.oma.mil:8080/${this.personData.small_photo}`
        this.largePhoto = `http://afrad.oma.mil:8080/${this.personData.large_photo}`
        this.familyPhoto = `http://afrad.oma.mil:8080/${this.personData.family_photo}`
        this.member_decision = this.personData.final_decision

        this.effLength = this.personData?.efficiency_report.length
        console.log(this.personData?.efficiency_report[Number(this.effLength)]?.grade_name)
        this.rejections_traq = this.personData?.rejections?.filter((e) => e.sp == 1)
        this.rejections_update = this.personData?.rejections?.filter((e) => e.sp == 2)
        console.log('By index', res)
      } catch {
        ;(Error) => console.log(Error)
      }
    },

    toAr(number) {
      return convertToArabicNumbers(number)
    },
    async UnitsName() {
      let res = await axios.get('/units/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      this.unit = res.data
      this.pernName = res.data
    },

    async downloadPDF() {
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
      pdf.save(`${this.personData.mil_no}`)
    },

    async downloadImage() {
      const element = document.getElementById('capture-area')
      const canvas = await html2canvas(element)
      const image = canvas.toDataURL('image/png')

      const link = document.createElement('a')
      link.href = image
      link.download = `${this.personData.mil_no}`
      link.click()
    },

    async fetchDataForOutUser() {
      try {
        const res = await axios.get(
          `/persons/filter/?mil_ser=${this.milSer}&unit_code=${this.unit_Selection}&checklagna=${this.checkLagna}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )
        this.data = res.data
        console.log(this.data)
        if (this.data.length > 0) {
          const res2 = await axios.get(`/person/${this.data[0].mil_ser}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          })
          this.data2 = res2.data
          console.log('hello ', this.data2)
          console.log('hello2 ', this.data2?.mil_ser)
          if (this.data2?.mil_ser) {
            this.setData(this.data2)
            this.index = 0
          } else {
            this.personData = {}
          }
        }
        // this.personData = this.data[0];
        // console.log(this.personData);
        // console.log(this.data[0]);
      } catch (e) {
        console.log('check error', e)
      }
    },

    // test changes
    async fetchDataForOutUserByindex(i) {
      try {
        const res = await axios.get(
          `/persons/filter/?mil_ser=${this.milSer}&unit_code=${this.unit_Selection}&checklagna=${this.checkLagna}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )
        this.data = res.data
        console.log('index num', i)
        console.log('By index', this.data)
        if (this.data.length > 0) {
          const res2 = await axios.get(`/person/${this.data[i].mil_ser}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          })
          this.data2 = res2.data
          console.log('hello ', this.data2)
          console.log('hello2 ', this.data2?.mil_ser)
          if (this.data2?.mil_ser) {
            this.setData(this.data2)
            this.index = i
            console.log('new', this.index)
          } else {
            this.personData = {}
          }
        }
        // this.personData = this.data[0];
        // console.log(this.personData);
        // console.log(this.data[0]);
      } catch (e) {
        console.log('check error', e)
      }
    },
    setData(data) {
      this.personData = { ...data }
      this.effLength = this.personData?.efficiency_report.length
      console.log('000000 ', this.personData?.efficiency_report)

      this.checkConsis()
      this.attendDay = this.personData.day?.id || ''
      console.log(this.personData.votes)
      this.sta = { ...this.personData.committee_punishment_jobs_sta[0] }
      console.log(this.sta)
      const h = this.personData.votes?.filter(
        (u) =>
          u.user_data.degree === localStorage.getItem('rank') &&
          u.user_data.member === localStorage.getItem('member_name'),
      )[0]
      this.current_vote = h?.vote_type

      this.punshiments = this.personData.committee_punishment_jobs

      this.punishLength = this.personData.committee_punishment_jobs_sta[0]?.total || 'لا يكن'

      this.punishCortLength = this.personData.committee_punishment_jobs_sta[0]?.cort || 'لا يكن'
      this.punishStayLength = this.personData.committee_punishment_jobs_sta[0]?.stay || 'لا يكن'

      this.punishNotStayLength =
        this.personData.committee_punishment_jobs_sta[0]?.not_stay || 'لا يكن'
      this.jobunits = [...(this.personData.committee_jobs || [])]
      this.jobsUnitsLength = this.personData.committee_jobs?.length
      this.travel = [...(this.personData.committee_travel_jobs || [])]
      this.travelLength = this.personData.committee_travel_jobs?.length
      this.reasonLength = this.personData.reasons?.length
      this.smallPhoto = `http://afrad.oma.mil:8080/${this.personData.small_photo}`
      this.largePhoto = `http://afrad.oma.mil:8080/${this.personData.large_photo}`
      this.familyPhoto = `http://afrad.oma.mil:8080/${this.personData.family_photo}`
      console.log('smal', this.smallPhoto)
      console.log('lg', this.largePhoto)
      console.log('fam', this.familyPhoto)
      this.member_decision = this.personData.final_decision
      this.rejections_traq = this.personData?.rejections?.filter((e) => e.sp == 1)
      this.rejections_update = this.personData?.rejections?.filter((e) => e.sp == 2)
      console.log(this.largePhoto)
      if (this.vote_type == '1') {
        this.vote_0 =
          this.personData.votes
            ?.filter((v) => v.vote_type == 0 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
        this.vote_1 =
          this.personData.votes
            ?.filter((v) => v.vote_type == 1 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
        this.vote_2 =
          this.personData.votes
            ?.filter((v) => v.vote_type == 2 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
      }
      console.log(data)
    },
    async gothen() {
      const newArrayData = Array.from(this.data)
      if (this.index < newArrayData.length) {
        ++this.index
      } else {
        this.index = 0
      }

      try {
        // Make the API request
        const res2 = await axios.get(`/person/${newArrayData[this.index].mil_ser}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })

        let data2 = res2.data
        console.log('Data from API: ', data2)

        if (data2?.mil_ser) {
          this.setData(data2)
          // Optionally, decide when to reset `this.index`
          // If you want to reset it after processing one person:
          // this.index = 0;
        } else {
          this.personData = {} // No valid data, clear personData
        }
      } catch (e) {
        console.error('Error in fetching data:', e)
      }
    },
    async goback() {
      const newArrayData = Array.from(this.data)
      if (this.index > 1) {
        --this.index
      } else {
        this.index = 0
      }

      try {
        // Make the API request
        const res2 = await axios.get(`/person/${newArrayData[this.index].mil_ser}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })

        let data2 = res2.data
        console.log('Data from API: ', data2)

        if (data2?.mil_ser) {
          this.setData(data2)
          // Optionally, decide when to reset `this.index`
          // If you want to reset it after processing one person:
          // this.index = 0;
        } else {
          this.personData = {} // No valid data, clear personData
        }
      } catch (e) {
        console.error('Error in fetching data:', e)
      }
    },
    async handelChange() {
      let req = await axios.post(
        `/attended/${this.personData?.mil_ser}/`,
        {
          day: this.attendDay,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      )
      this.attendDay = req.data?.day || ''
      if (req.data?.attended_number !== undefined) {
        localStorage.setItem('attendance_number', req.data.attendance_number)
        localStorage.setItem('attended_number', req.data.attended_number)
        this.attended_number = req.data?.attended_number
      }
    },

    async fetchUserData() {
      await axios
        .get('persons/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then((res) => {
          this.usersTable = [
            ...res.data.filter((t) => t.committe_order != 0),
            ...res.data.filter((t) => t.committe_order == 0),
          ]
          this.filteredUsersTable = this.usersTable
          this.data = this.usersTable
          console.log(this.usersTable)
        })
        .catch((err) => {
          console.log('Error getting data, ', err?.message)
          if (err.status == 401) {
            localStorage.clear()
            this.$router.push({ name: 'login' })
          }
        })
    },
    countMember() {
      if (this.LagnaDay != 'all') {
        this.memberForDay = this.usersTable.filter((e) => e.attended_date == this.LagnaDay)
        console.log(this.memberForDay)
      }
    },
    filterUsers() {
      this.data2 = this.usersTable.filter((record) => {
        const armyNameFilter = record.army_name == this.armyName || this.armyName == 'all'
        // test
        const LagnaDayFilter = record.attended_date == this.LagnaDay || this.LagnaDay == 'all'
        const lagnaTypeFilter = record.type_name == this.lagnaType || this.lagnaType == 'all'

        return armyNameFilter && lagnaTypeFilter && LagnaDayFilter
      })
      console.log('data', this.data)
    },
    // ======================================================================================
    // strat id report for head
    // ======================================================================================
    async fetchDataForOutUserId() {
      try {
        const res = await axios.get(
          `/persons/filter/?mil_ser=${this.milSer}&pern_code=${this.pern_Selection}&unit_code=${this.unit_Selection}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )
        this.data = res.data
        console.log(this.data)
        if (this.data.length > 0) {
          const res2 = await axios.get(`/person/${this.data[0].mil_ser}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          })
          this.data2 = res2.data
          console.log('hello ', this.data2)
          console.log('hello2 ', this.data2?.mil_ser)
          if (this.data2?.mil_ser) {
            this.setDataId(this.data2)
            this.index = 0
          } else {
            this.personData = {}
          }
        }
        // this.personData = this.data[0];
        // console.log(this.personData);
        // console.log(this.data[0]);
      } catch (e) {
        console.log('check error', e)
      }
    },

    async fetchDataForOutUserByindexId(i) {
      try {
        const res = await axios.get(
          `/persons/filter/?mil_ser=${this.milSer}&unit_code=${this.unit_Selection}&checklagna=${this.checkLagna}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )
        this.data = res.data
        console.log('index num', i)
        console.log('By index', this.data)
        if (this.data.length > 0) {
          const res2 = await axios.get(`/person/${this.data[i].mil_ser}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          })
          this.data2 = res2.data
          console.log('hello ', this.data2)
          console.log('hello2 ', this.data2?.mil_ser)
          if (this.data2?.mil_ser) {
            this.setDataId(this.data2)
            this.index = i
            console.log('new', this.index)
          } else {
            this.personData = {}
          }
        }
        // this.personData = this.data[0];
        // console.log(this.personData);
        // console.log(this.data[0]);
      } catch (e) {
        console.log('check error', e)
      }
    },
    setDataId(data) {
      this.personData = { ...data }
      this.effLength = this.personData?.efficiency_report.length
      console.log('000000 ', this.personData?.efficiency_report)

      this.checkConsis()
      this.attendDay = this.personData.day?.id || ''
      console.log(this.personData.votes)
      this.sta = { ...this.personData.committee_punishment_jobs_sta[0] }
      console.log(this.sta)
      const h = this.personData.votes?.filter(
        (u) =>
          u.user_data.degree === localStorage.getItem('rank') &&
          u.user_data.member === localStorage.getItem('member_name'),
      )[0]
      this.current_vote = h?.vote_type

      this.punshiments = this.personData.committee_punishment_jobs

      this.punishLength = this.personData.committee_punishment_jobs_sta[0]?.total || 'لا يكن'

      this.punishCortLength = this.personData.committee_punishment_jobs_sta[0]?.cort || 'لا يكن'
      this.punishStayLength = this.personData.committee_punishment_jobs_sta[0]?.stay || 'لا يكن'

      this.punishNotStayLength =
        this.personData.committee_punishment_jobs_sta[0]?.not_stay || 'لا يكن'
      this.jobunits = [...(this.personData.committee_jobs || [])]
      this.jobsUnitsLength = this.personData.committee_jobs?.length
      this.travel = [...(this.personData.committee_travel_jobs || [])]
      this.travelLength = this.personData.committee_travel_jobs?.length
      this.reasonLength = this.personData.reasons?.length
      this.smallPhoto = `http://afrad.oma.mil:8080/${this.personData.small_photo}`

      this.largePhoto = `http://afrad.oma.mil:8080/${this.personData.large_photo}`
      this.familyPhoto = `http://afrad.oma.mil:8080/${this.personData.family_photo}`
      this.member_decision = this.personData.final_decision
      this.rejections_traq = this.personData?.rejections?.filter((e) => e.sp == 1)
      this.rejections_update = this.personData?.rejections?.filter((e) => e.sp == 2)
      console.log(this.largePhoto)
      if (this.vote_type == '1') {
        this.vote_0 =
          this.personData.votes
            ?.filter((v) => v.vote_type == 0 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
        this.vote_1 =
          this.personData.votes
            ?.filter((v) => v.vote_type == 1 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
        this.vote_2 =
          this.personData.votes
            ?.filter((v) => v.vote_type == 2 && v.member_username != 1)
            .map((u) => u.user_data)
            .sort((a, b) => a.priority_number - b.priority_number) || []
      }
      console.log(data)
    },
    async gothen() {
      const newArrayData = Array.from(this.data)
      if (this.index < newArrayData.length) {
        ++this.index
      } else {
        this.index = 0
      }

      try {
        // Make the API request
        const res2 = await axios.get(`/person/${newArrayData[this.index].mil_ser}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })

        let data2 = res2.data
        console.log('Data from API: ', data2)

        if (data2?.mil_ser) {
          this.setDataId(data2)
          // Optionally, decide when to reset `this.index`
          // If you want to reset it after processing one person:
          // this.index = 0;
        } else {
          this.personData = {} // No valid data, clear personData
        }
      } catch (e) {
        console.error('Error in fetching data:', e)
      }
    },
    async gobackId() {
      const newArrayData = Array.from(this.data)
      if (this.index > 1) {
        --this.index
      } else {
        this.index = 0
      }

      try {
        // Make the API request
        const res2 = await axios.get(`/person/${newArrayData[this.index].mil_ser}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })

        let data2 = res2.data
        console.log('Data from API: ', data2)

        if (data2?.mil_ser) {
          this.setDataId(data2)
          // Optionally, decide when to reset `this.index`
          // If you want to reset it after processing one person:
          // this.index = 0;
        } else {
          this.personData = {} // No valid data, clear personData
        }
      } catch (e) {
        console.error('Error in fetching data:', e)
      }
    },
    async handelChangeId() {
      let req = await axios.post(
        `/attended/${this.personData?.mil_ser}/`,
        {
          day: this.attendDay,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      )
      this.attendDay = req.data?.day || ''
      if (req.data?.attended_number !== undefined) {
        localStorage.setItem('attendance_number', req.data.attendance_number)
        localStorage.setItem('attended_number', req.data.attended_number)
        this.attended_number = req.data?.attended_number
      }
    },

    async fetchUserDataId() {
      await axios
        .get('persons/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then((res) => {
          this.usersTable = [
            ...res.data.filter((t) => t.committe_order != 0),
            ...res.data.filter((t) => t.committe_order == 0),
          ]
          this.filteredUsersTable = this.usersTable
          this.data = this.usersTable
          console.log(this.usersTable)
        })
        .catch((err) => {
          console.log('Error getting data, ', err?.message)
          if (err.status == 401) {
            localStorage.clear()
            this.$router.push({ name: 'login' })
          }
        })
    },
    countMemberId() {
      if (this.LagnaDay != 'all') {
        this.memberForDay = this.usersTable.filter((e) => e.attended_date == this.LagnaDay)
        console.log(this.memberForDay)
      }
    },
    filterUsersId() {
      this.data2 = this.usersTable.filter((record) => {
        const armyNameFilter = record.army_name == this.armyName || this.armyName == 'all'
        // test
        const LagnaDayFilter =
          (record.attended_date == this.LagnaDay) == '2025-10-05' || this.LagnaDay == '2025-10-09'
        const lagnaTypeFilter = record.type_name == this.lagnaType || this.lagnaType == 'all'

        return armyNameFilter && lagnaTypeFilter && LagnaDayFilter
      })
      console.log('data', this.data)
    },
    // ========================================================================
    // ========================================================================
    // ========================================================================
    // ========================================================================
    async uploadImage() {
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
          `http://afrad.oma.mil:8080/api/upload_images/${this.personData.mil_ser}/`,
          {
            method: 'POST',
            body: formData,
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )

        if (response.ok) {
          this.fetchDataForOutUserByindex(this.index)
          image1.value = ''
          image2.value = ''
          image3.value = ''
          image4.value = ''
          setTimeout(() => {
            status.textContent = 'تم تحميل الصور'
            setTimeout(() => {
              status.textContent = ' '
            }, 500)
          }, 1000)

          // this.setData(data[this.index]);
          // document.location.reload();
        } else {
          status.textContent = 'فشل التحميل'
        }
      } catch (error) {
        console.error('Error uploading image:', error)
        status.textContent = 'خطاء فى التحميل'
      }
    },
    async fetchUnitPersonsData() {
      try {
        const res = await axios.get(
          `get_images_report_details/?excel=no&pern_army=${this.outMember}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )
        this.unitPersonsData = [...res.data]
        this.filterUnitPersonsData = this.unitPersonsData
        console.log('dddddddddddd', res)
      } catch {
        ;(err) => {
          console.log('Error getting data, ', err?.message)
          if (err.status == 401) {
            localStorage.clear()
            this.$router.push({ name: 'login' })
          }
        }
      }
    },
    // async uploadAddImage() {
    //   const addImage = document.getElementById("addImage");
    //   const status = document.getElementById("status");
    //   const formData = new FormData();

    //   if (addImage.files.length != 0) {
    //     formData.append("image", addImage.files[0]);
    //   }

    //   try {
    //     const response = await fetch(
    //       `http://afrad.oma.mil:8080/api/upload_additional_images/${this.personData.mil_ser}/`,
    //       {
    //         method: "POST",
    //         body: formData,
    //         headers: {
    //           Authorization: `Bearer ${localStorage.getItem("token")}`,
    //         },
    //       }
    //     );

    //     if (response.ok) {
    //       this.fetchDataForOutUserByindex(this.index);

    //       setTimeout(() => {
    //         status.textContent = "تم الرفع بنجاح";
    //         setTimeout(() => {
    //           status.textContent = " ";
    //         }, 500);
    //       }, 1000);

    //       // this.setData(data[this.index]);
    //       // document.location.reload();
    //     } else {
    //       status.textContent = "فشل الرفع";
    //     }
    //   } catch (error) {
    //     console.error("Error uploading image:", error);
    //     status.textContent = "خطاء فى رفع الصور";
    //   }
    // },
    useSocket() {
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
          this.reportData = { ...data.data }
          console.log(this.reportData)
          if (this.reportIsVisiable == true) {
            this.reportIsVisiable = false
          } else {
            this.reportIsVisiable = true
          }
        }
        if (data.message.startsWith('person')) {
          this.personData = { ...data.data }
          console.log(this.personData)
          const h = this.personData.votes?.filter(
            (u) =>
              u.user_data.degree === localStorage.getItem('rank') &&
              u.user_data.member === localStorage.getItem('member_name'),
          )[0]

          this.current_vote = h?.vote_type
          // console.log(this.current_vote);
          this.punshiments = this.personData.committee_punishment_jobs
          this.punishLength = this.personData.committee_punishment_jobs_sta[0]?.total
          this.punishCortLength = this.personData.committee_punishment_jobs_sta
          // this.personData.committee_punishment_jobs_sta[0]?.cort;
          this.effLength = this.personData?.efficiency_report.length
          this.member_decision == this.personData.final_decision
          this.sta = { ...this.personData.committee_punishment_jobs_sta[0] }
          console.log(this.sta)
          // \\\\\\\\\\\\\\\\\

          // console.log("0000000000000000000000000",new Date(this.personData.upgrade_date).getTime() )
          // console.log("0000000000000000000000000",new Date().getTime() )
          //   console.log("0000000000000000000000000", )

          // this.hagz = this.punshiments.filter(
          //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 2
          // )?.length;
          // console.log("hagz1", this.hagz);
          // this.hagz2 = this.punshiments.filter(
          //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 1
          // )?.length;
          // console.log("hagz2", this.hagz2);
          // this.hagz3 = this.punshiments.filter(
          //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 14
          // )?.length;
          // console.log("hagz3", this.hagz3);
          // this.habs = this.punshiments.filter(
          //   (e) => e.punsh_cort_code == 1 && e.punishment_code == 4
          // ).length;

          // this.court = this.punshiments.filter(
          //   (e) => e.punsh_cort_code == 2
          // ).length;
          this.court1 = this.punshiments.filter((e) => e.punsh_cort_code == 3).length
          // this.habs =
          //   this.personData.committee_punishment_jobs_sta[0]?.not_stay;
          // console.log(
          //   this.personData.committee_punishment_jobs_sta,
          //   "sssssssssssssssjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjss"
          // );
          // this.hagz = this.personData.committee_punishment_jobs_sta[0]?.stay;
          // this.court = this.personData.committee_punishment_jobs_sta[0]?.court;

          this.punishStayLength = this.personData.committee_punishment_jobs_sta[0]?.stay
          this.punishNotStayLength = this.personData.committee_punishment_jobs_sta[0]?.not_stay
          this.jobunits = [...(this.personData.committee_jobs || [])]
          this.jobsUnitsLength = this.personData.committee_jobs?.length
          this.travel = [...(this.personData.committee_travel_jobs || [])]
          this.travelLength = this.personData.committee_travel_jobs?.length
          this.reasonLength = this.personData.reasons?.length
          this.smallPhoto = `http://afrad.oma.mil:8080/${this.personData.small_photo}`
          this.largePhoto = `http://afrad.oma.mil:8080/${this.personData.large_photo}`
          this.familyPhoto = `http://afrad.oma.mil:8080/${this.personData.family_photo}`
          console.log(this.familyPhoto)
          this.member_decision = this.personData.final_decision
          // if (this.personData.tot_years => 20 and this.personData.tot_years < 20){
          // this.muscle_weiht =
          // }
          this.member_op =
            this.personData.votes?.filter(
              (e) => e.user_data.member == localStorage.getItem('member_name'),
            )[0]?.vote_type || null
          this.rejections_traq = this.personData?.rejections?.filter((e) => e.sp == 1)
          this.rejections_update = this.personData?.rejections?.filter((e) => e.sp == 2)
          // console.log(this.largePhoto);
          if (this.vote_type == '1') {
            this.vote_0 =
              this.personData.votes
                ?.filter((v) => v.vote_type == 0 && v.member_username != 1)
                .map((u) => u.user_data)
                .sort((a, b) => a.priority_number - b.priority_number) || []
            this.vote_1 =
              this.personData.votes
                ?.filter((v) => v.vote_type == 1 && v.member_username != 1)
                .map((u) => u.user_data)
                .sort((a, b) => a.priority_number - b.priority_number) || []
            this.vote_2 =
              this.personData.votes
                ?.filter((v) => v.vote_type == 2 && v.member_username != 1)
                .map((u) => u.user_data)
                .sort((a, b) => a.priority_number - b.priority_number) || []
          }
          console.log('get there')
          console.log(this.personData)
        } else if (data.message.startsWith('vote')) {
          if (data.data.mil_ser == this.personData.mil_ser) {
            this.vote_1 = this.vote_1?.filter((d) => d.member != data.data.member)
            this.vote_0 = this.vote_0?.filter((d) => d.member != data.data.member)
            this.vote_2 = this.vote_2?.filter((d) => d.member != data.data.member)

            if (data.data.vote_type == 0) {
              this.vote_0.push(data.data)
              this.vote_0.sort((a, b) => a.priority_number - b.priority_number)
            } else if (data.data.vote_type == 1) {
              this.vote_1.push(data.data)
              this.vote_1.sort((a, b) => a.priority_number - b.priority_number)

              console.log(this.vote_1)
            } else if (data.data.vote_type == 2) {
              this.vote_2.push(data.data)
              this.vote_2.sort((a, b) => a.priority_number - b.priority_number)
            }
          }
        } else if (data.message.startsWith('un_vote')) {
          this.disable = true
        } else if (data.message.startsWith('op')) {
          this.PersonPhoto = false
          this.travelIsVisiable = false
          this.MedicalIsVisiable = false
          this.RelationIsVisiable = false
          this.ConsistancyIsVisiable = false
          this.HistoryIsVisiable = false
          this.courtIsVisiable = false
          this.isVisiable = false
          this.TraqPopupVisible = false
          this.UpdatePopupVisible = false
          this.coursesPopupVisible = false
          this.Eff_reportPopupVisible = false
          this.reasonsPopupVisible = false

          // -------------------------------------------------------------------------------------------

          if (data.message.startsWith('use')) {
            console.log('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
          }
          // -------------------------------------------------------------------------------------------

          if (data.data == 'units') {
            if (this.personData.committee_jobs.length > 0) {
              if (this.isVisiable == true) {
                this.isVisiable = false
              } else {
                this.isVisiable = true
              }
            }
          }
          // if (data.data.startsWith("punish")) {
          //   if (this.personData.committee_punishment_jobs.length > 0) {
          //     if (this.courtIsVisiable == true) {
          //       this.courtIsVisiable = false;
          //       // this.courtIsVisiable = false;
          //     } else {
          //       // this.cortType = data.data.replace("punish", "");
          //       this.courtIsVisiable = true;
          //     }
          //   }
          // }
          if (data.data == 'medical') {
            if (this.personData.medical_history.length > 0) {
              if (this.MedicalIsVisiable == true) {
                this.MedicalIsVisiable = false
              } else {
                this.MedicalIsVisiable = true
              }
            }
          }
          if (data.data.startsWith('relation')) {
            if (this.personData.relations.length > 0) {
              if (this.RelationIsVisiable == true) {
                this.RelationIsVisiable = false
              } else {
                this.relationType = data.data
                  .replace('relation', '')
                  .split(',')
                  .map((e) => +e)
                console.log(data.data.replace('relation', '').split(','))
                this.RelationIsVisiable = true
              }
            }
          }
          if (data.data.startsWith('consistancy')) {
            if (this.personData.consistancies.length > 0) {
              if (this.ConsistancyIsVisiable == true) {
                this.ConsistancyIsVisiable = false
              } else {
                this.ConsistancyIsVisiable = true
              }
            }
          }
          if (data.data.startsWith('travel')) {
            if (this.personData.committee_travel_jobs.length > 0) {
              if (this.travelIsVisiable == true) {
                this.travelIsVisiable = false
              } else {
                this.travelIsVisiable = true
              }
            }
          }
          if (data.data.startsWith('photo')) {
            if (this.personData.length > 0) {
              if (this.PersonPhoto == true) {
                this.PersonPhoto = false
                // this.largePhoto = `http://afrad.oma.mil:8080/${this.personData.large_photo}`;
              } else {
                this.PersonPhoto = true
                this.largePhoto = `http://afrad.oma.mil:8080/${this.personData.large_photo}`
              }
            }
          }
          if (data.data.startsWith('family')) {
            if (this.personData.length > 0) {
              if (this.PersonPhoto == true) {
                this.PersonPhoto = false
              } else {
                this.largePhoto = ``
                this.PersonPhoto = true
                this.familyPhoto = `http://afrad.oma.mil:8080/${this.personData.family_photo}`
              }
            }
          }
          if (data.data.startsWith('history')) {
            if (this.personData.history.length > 0) {
              if (this.HistoryIsVisiable == true) {
                this.HistoryIsVisiable = false
              } else {
                this.HistoryIsVisiable = true
              }
            }
          }
          if (data.data.startsWith('rejections_update')) {
            if (this.personData.rejections.filter((e) => e.sp == 2).length > 0) {
              if (this.UpdatePopupVisible == true) {
                this.UpdatePopupVisible = false
              } else {
                this.UpdatePopupVisible = true
              }
            }
          }
          if (data.data.startsWith('rejections_traqi')) {
            if (this.personData.rejections.filter((e) => e.sp == 1).length > 0) {
              if (this.TraqPopupVisible == true) {
                this.TraqPopupVisible = false
              } else {
                this.TraqPopupVisible = true
              }
            }
          }
          if (data.data.startsWith('Courses')) {
            if (this.personData.courses.length > 0) {
              if (this.coursesPopupVisible == true) {
                this.coursesPopupVisible = false
              } else {
                this.coursesPopupVisible = true
              }
            }
          }
          if (data.data.startsWith('Eff_report')) {
            if (this.personData.efficiency_report.length > 0) {
              if (this.Eff_reportPopupVisible == true) {
                this.Eff_reportPopupVisible = false
              } else {
                this.Eff_reportPopupVisible = true
              }
            }
          }
          if (data.data.startsWith('weight')) {
            if (this.personData.consistancies.length > 0) {
              if (this.ConsistancyIsVisiable == true) {
                this.ConsistancyIsVisiable = false
              } else {
                this.ConsistancyIsVisiable = true
              }
            }
          }
          if (data.data.startsWith('opinion')) {
            if (this.vote_1.length > 0 || this.vote_2.length > 0) {
              if (this.AcceptPopupVisible == true) {
                this.AcceptPopupVisible = false
              } else {
                this.AcceptPopupVisible = true
              }
            }
          }
          if (data.data.startsWith('punish')) {
            console.log("i'm here")
            this.openCourtpopup(0)
          }
          if (data.data.startsWith('punish1')) {
            if (this.personData.committee_punishment_jobs.length > 0) {
              if (this.courtIsVisiable == true) {
                this.openCourtpopup(1)
              } else {
                this.closeCourtPopup()
              }
            }
          }
          if (data.data.startsWith('punish2')) {
            if (this.personData.committee_punishment_jobs.length > 0) {
              if (this.courtIsVisiable == true) {
                this.openCourtpopup(2)
              } else {
                this.closeCourtPopup()
              }
            }
          }
          if (data.data.startsWith('punish3')) {
            if (this.personData.committee_punishment_jobs.length > 0) {
              if (this.courtIsVisiable == true) {
                this.openCourtpopup(3)
              } else {
                this.closeCourtPopup()
              }
            }
          }
          if (data.data.startsWith('punish4')) {
            if (this.personData.committee_punishment_jobs.length > 0) {
              if (this.courtIsVisiable == true) {
                this.openCourtpopup(4)
              } else {
                this.closeCourtPopup()
              }
            }
          }
          if (data.data.startsWith('poea')) {
            if (this.personData.sec_req_notes) {
              if (this.poea == false) {
                this.openPEApopup()
              } else {
                this.closePoeapopup()
              }
            }
          }
          if (data.data.startsWith('isSecVisiable')) {
            if (this.personData.sec_req_notes) {
              if (this.isSecVisiable == false) {
                this.openSecpopup()
              } else {
                this.closeSecpopup()
              }
            }
          }
          if (data.data.startsWith('shhh')) {
            this.openRelationPopup([5, 6])
          }
          if (data.data.startsWith('shhh2')) {
            this.openRelationPopup([11, 9, 10, 8])
          }
          if (data.data.startsWith('report')) {
            if (this.reportIsVisiable == true) {
              this.reportIsVisiable = false
            } else {
              this.reportIsVisiable = true
            }
          }
          if (data.data.startsWith('hayaa')) {
            if (this.opManager == true) {
              this.opManager = false
            } else {
              this.opManager = true
            }
          }
          if (data.data.startsWith('save')) {
            this.$refs.pop.signopinion()
          }
          if (data.data.startsWith('reason')) {
            if (this.personData.reasons.length > 0) {
              if (this.courtIsVisiable == true) {
                this.reasonsPopupVisible = false
              } else {
                this.reasonsPopupVisible = true
              }
            }
          }
          if (data.data.startsWith('takeScreen')) {
            if (localStorage.member_type == 1) {
              this.downloadImage()
            }
          }
          if (data.data.startsWith('takePdf')) {
            if (localStorage.member_type == 1) {
              this.downloadPDF()
            }
          }
          if (data.data.startsWith('u_op_reasons')) {
            if (this.reasonsPopupVisible == true) {
              this.reasonsPopupVisible = false
              this.reasons = ''
            } else {
              this.reasonsPopupVisible = true
              this.reasons = this.personData.opinions.filter(
                (e) => e.sp == 8,
              )[0]?.unit_refuse_reason
            }
          }
          if (data.data.startsWith('a_op_reasons')) {
            if (this.reasonsPopupVisible == true) {
              this.reasonsPopupVisible = false
              this.reasons = ''
            } else {
              this.reasonsPopupVisible = true
              this.reasons =
                this.personData.opinions.filter((e) => e.sp == 8)[0]?.unt_arm_refuse_reason == ''
                  ? this.personData.opinions.filter((e) => e.sp == 8)[0]?.unt_arm_refuse_reason
                  : this.personData.opinions.filter((e) => e.sp == 8)[0]?.unit_refuse_reason
            }
          }
          if (data.data.startsWith('takePdf')) {
            if (localStorage.member_type == 1) {
              this.downloadPDF()
            }
          }
          if (data.data.startsWith('end')) {
            this.courtIsVisiable = false
            this.poea = false
            this.TraqPopupVisible = false
            this.AcceptPopupVisible = false
            this.ConsistancyIsVisiable = false
            this.coursesPopupVisible = false
            this.UpdatePopupVisible = false
            this.HistoryIsVisiable = false
            this.PersonPhoto = false
            this.travelIsVisiable = false
            this.ConsistancyIsVisiable = false
            this.MedicalIsVisiable = false
            this.RelationIsVisiable = false
            this.courtIsVisiable = false
            this.isVisiable = false
            this.opManager = false
          }

          if (data.data.startsWith('close')) {
            this.personData = []
          }
        }
      }
    },
    vote_handel(n) {
      axios.get(`vote/${this.personData.mil_ser}/?vote_type=${n}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
    },
    decision_handel(n) {
      axios
        .get(`vote/${this.personData.mil_ser}/?vote_type=${n}&final_decision=1`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .catch((err) => {
          if (err.status == 401) {
            localStorage.clear()
            this.$router.push({ name: 'login' })
          }
        })
      console.log(this.personData.mil_ser)
    },
    openpopup() {
      this.isVisiable = true
    },
    closePopup() {
      this.isVisiable = false
    },
    openTravelpopup() {
      this.travelIsVisiable = true
    },
    closeTravelPopup() {
      this.travelIsVisiable = false
    },
    openCourtpopup(type = 0) {
      this.cortType = type
      this.courtIsVisiable = true
    },
    closeCourtPopup() {
      this.courtIsVisiable = false
    },
    openMedicalpopup() {
      this.MedicalIsVisiable = true
    },
    closeMedicalPopup() {
      this.MedicalIsVisiable = false
    },
    openRelationPopup(relationType) {
      this.relationType = relationType
      this.RelationIsVisiable = true
    },
    closeRelationPopup() {
      this.RelationIsVisiable = false
    },
    openConsistancyPopup() {
      this.ConsistancyIsVisiable = true
    },
    closeConsistancyPopup() {
      this.ConsistancyIsVisiable = false
    },
    openHistorypopup() {
      console.log('hello')
      this.HistoryIsVisiable = true
    },
    closeHistoryPopup() {
      this.HistoryIsVisiable = false
    },

    openPhotopopup() {
      this.PersonPhoto = true
    },
    closePhotopopup() {
      this.PersonPhoto = false
    },
    closeReportPopup() {
      this.reportIsVisiable = false
    },

    closeCoursespopup() {
      this.coursesPopupVisible = false
    },
    closeEff_reportpopup() {
      this.Eff_reportPopupVisible = false
    },
    closeEff_reportpopup() {
      this.Eff_reportPopupVisible = false
    },
    closeReasonsPopup() {
      this.reasonsPopupVisible = false
      this.reasons = ''
    },
    openReasonspopup(e) {
      this.reasons = e

      this.reasonsPopupVisible = true
    },
    openTraqpopup() {
      this.TraqPopupVisible = true
      console.log('open')
    },
    closeTraqpopup() {
      this.TraqPopupVisible = false
    },
    openUpdatqpopup() {
      console.log('hello')
      this.UpdatePopupVisible = true
    },
    closeUpdatepopup() {
      this.UpdatePopupVisible = false
    },

    openAcceptpopup() {
      console.log('hello')
      this.AcceptPopupVisible = true
    },
    closeAcceptpopup() {
      this.AcceptPopupVisible = false
    },
    openRejectpopup() {
      console.log('hello')
      this.AcceptPopupVisible = true
    },
    closeRejectpopup() {
      this.AcceptPopupVisible = false
    },
    openPEApopup() {
      console.log('poea')
      this.poea = true
    },
    openSecpopup() {
      console.log('isSecVisiable')
      this.isSecVisiable = true
    },
    closePoeapopup() {
      this.poea = false
    },
    closeSecpopup() {
      this.isSecVisiable = false
    },
    openReportOutMember() {
      console.log('OutReport')
      this.OutReport = true
      this.fetchUnitPersonsData()
    },
    closeReportOutMember() {
      this.OutReport = false
    },
    openOpinionManager() {
      console.log('OutReport')
      this.opManager = true
    },
    closeOpinionManager() {
      this.opManager = false
    },
  },
}
</script>
<template>
  <div class="homePage">
    <OpinionManager
      :personName="this.personData.person_name"
      :personDegree="this.personData.degree_name"
      :showPersonPopup="opManager"
      @close="closeOpinionManager"
      :mil="personData.mil_ser"
      ref="pop"
      v-if="this.member == 'رئيس هيئة التنظيم والإدارة للقوات المسلحة'"
    />

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
      :medicalData="this.personData.medical_history"
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
          ?.filter((r) => this.relationType?.includes(r.relation_degree_code))
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
      :personName="this.personData.person_name"
      :personDegree="this.personData.degree_name"
      :showHistoryPopup="HistoryIsVisiable"
      @close="closeHistoryPopup"
      :personHistory="personData.history"
    />
    <PersonPhoto
      :personPhoto="this.largePhoto"
      :personName="this.personData.person_name"
      :personDegree="this.personData.degree_name"
      :showPersonPopup="PersonPhoto"
      :familyPhoto="this.familyPhoto"
      @close="closePhotopopup"
    />
    <TraqPopup
      :userNamePer="this.personData?.person_name"
      :degree="this.personData?.degree_name"
      :showTraqPopup="this.TraqPopupVisible"
      @close="this.closeTraqpopup"
      :tableData="rejections_traq"
    />
    <UpdatePopup
      :userNamePer="this.personData?.person_name"
      :degree="this.personData?.degree_name"
      :showUpdatePopup="this.UpdatePopupVisible"
      @close="this.closeUpdatepopup"
      :tableData="rejections_update"
    />
    <reasonsPopup
      :userNamePer="this.personData?.person_name"
      :degree="this.personData?.degree_name"
      :showReasonPopup="this.reasonsPopupVisible"
      @close="this.closeReasonsPopup"
      :tableData="this.reasons"
    />

    <Acceptpop
      :userNamePer="this.personData?.person_name"
      :degree="this.personData?.degree_name"
      :showReasonPopup="this.AcceptPopupVisible"
      @close="this.closeAcceptpopup"
      :tableData="
        this.vote_1.sort((a, b) => {
          a.priority_number > b.priority_number
        })
      "
      :tableDataٍSec="
        this.vote_2.sort((a, b) => {
          a.priority_number > b.priority_number
        })
      "
    />

    <courses
      :userNamePer="this.personData?.person_name"
      :degree="this.personData?.degree_name"
      :showCoursesPopup="this.coursesPopupVisible"
      @close="this.closeCoursespopup"
      :tableData="
        this.personData?.courses?.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))
      "
    />
    <eff_report
      :userNamePer="this.personData?.person_name"
      :degree="this.personData?.degree_name"
      :showEff_reportPopup="this.Eff_reportPopupVisible"
      @close="this.closeEff_reportpopup"
      :tableData="
        this.personData?.efficiency_report?.sort(
          (a, b) => new Date(b.from_date) > new Date(a.from_date),
        )
      "
    />
    <!-- end popup contents  -->
    <main id="capture-area">
      <div class="homepage nouser" v-if="!this.personData?.person_name && !out_user && !this.show">
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
          <span v-if="this.personData.type_code == 3">
            لجنة ( تجديد/ ترقــي ) </span
          ><span v-if="this.personData.type_code == 2">
            لجنة ( تجـــديــد ) </span
          ><span v-if="this.personData.type_code == 1">لجنة ( ترقــي ) </span
          ><span v-if="this.personData.type_code == 5"
            >إنهاء خدمة ( استقالة )</span
          ><span v-if="this.personData.type_code == 4">
            إنهاء خدمة ( عدم الرغبة )
          </span>
          <span v-if="this.personData.type_code == 8">
            إنهاء خدمة ( عدم صلاحية )
          </span>
          <span v-if="this.personData.type_code == 9">
            إنهاء خدمة ( الرفت الجوازي )
          </span>
          <span v-if="this.personData.type_code == 10">
            إنهاء خدمة ( تثبيت )
          </span>
          مناظرة لجنة ضباط الصف {{ toAr("2025") }}
        </h4>-->

        <h4 class="topTitle">اللجنة الرئيسية لضباط الصف للقوات المسلحة {{ toAr('2025') }}</h4>
      </div>
      <div class="outUserContainer" v-if="out_user">
        <form @submit.prevent="" class="outUserContainer" v-if="this.user_id">
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
                v-for="(us, index) in this.usersTable
                ?.map((e) => e.army_name)
                .filter((e, i, a) => i === a.indexOf(e))"
                :value="us"
              >{{ us }}</option>
            </select>
          </div>-->
          <button @click="fetchDataForOutUserId()">بحث</button>
        </form>
        <form @submit.prevent="" class="outUserContainer" v-if="!this.user_id">
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
            v-if="this.user_id != 100"
            style="padding: 9px"
          >
            <option value="1">الكل</option>
            <option value="2">المدرج باللجنة</option>
            <option value="3">الغير مدرج باللجنة</option>
          </select>
          <div class="filter-select-wrapper" v-if="this.user_id == 100">
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
                v-for="(us, index) in this.usersTable
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
                v-for="(us, index) in this.usersTable
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
              this.user_id == 100 ? filterUsers() : (fetchDataForOutUser(), fetchUnitPersonsPhoto())
            "
          >
            بحث
          </button>
        </form>
        <button @click="openReportOutMember()" class="btn" v-if="!this.user_id">
          تقــريـــر الصور
        </button>
      </div>
      <!--  start user data  -->
      <div class="users" v-if="this.personData?.person_name">
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
                <p class="otherUnit">{{ `${personData.unit_name}` || '---' }}</p>
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
                  {{ ' ' + ' ' + toAr(`${this.personData.tot_ser_y || '.'}`) + ' سنه' }}
                  {{ ' / ' }}
                  {{ toAr(`${this.personData.tot_ser_m || '.'}`) + ' شهر' + ' ' }}
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
                      new Date(this.personData.upgrade_date).getTime() < new Date().getTime()
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
                  <span v-if="this.personData.sec_req_flag" style="color: black">يـوجــد</span>
                  <span v-if="!this.personData.sec_req_flag" style="color: black">لا يـوجــد</span>
                </p>
              </div>
              <div class="mil">
                <p
                  class="headUser data-btn"
                  @click="this.Eff_reportPopupVisible = true"
                  style="cursor: pointer; width: 250px"
                >
                  متوسط تقرير الكفاءة لاخر ثلاث سنوات
                </p>
                <p class="otherUnit" v-if="this.personData?.efficiency_report.length > 0">
                  {{
                    Math.round(
                      (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                        Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                        Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                        3,
                    ) < 50
                      ? 'ضعيف'
                      : Math.round(
                            (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                              Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                              Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                              3,
                          ) >= 50 &&
                          Math.round(
                            (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                              Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                              Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                              3,
                          ) <= 60
                        ? 'مقبول'
                        : Math.round(
                              (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                                Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                                Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                                3,
                            ) > 60 &&
                            Math.round(
                              (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                                Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                                Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                                3,
                            ) <= 75
                          ? 'جيد'
                          : Math.round(
                                (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                                  Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                                  Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                                  3,
                              ) > 75 &&
                              Math.round(
                                (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                                  Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                                  Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                                  3,
                              ) <= 90
                            ? 'جيد جدا'
                            : Math.round(
                                  (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                                    Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                                    Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                                    3,
                                ) > 90 &&
                                Math.round(
                                  (Number(this.personData?.efficiency_report[0]?.grade_name_1) +
                                    Number(this.personData?.efficiency_report[1]?.grade_name_1) +
                                    Number(this.personData?.efficiency_report[2]?.grade_name_1)) /
                                    3,
                                ) <= 100
                              ? 'ممتاز'
                              : this.personData?.efficiency_report[0]?.grade_name
                  }}
                </p>
                <p class="otherUnit" v-else>لا يوجد</p>
              </div>
              <div class="mil" style="visibility: hidden">
                <p
                  class="headUser data-btn"
                  @click="this.Eff_reportPopupVisible = true"
                  style="cursor: pointer"
                >
                  تقرير الكفاءة
                </p>
                <p class="otherUnit" v-if="this.personData?.efficiency_report.length > 0">
                  {{ this.personData?.efficiency_report[this.effLength - 1]?.grade_name }}
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
                    background: this.personData.consis_name == 'لائق' ? '' : '#d63024',
                    color: this.personData.consis_name == 'لائق' ? '' : 'white',
                  }"
                >
                  {{ this.personData.consis_name || '--' }}
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
              <div class="mil smallMil" v-if="this.out_user && !this.user_id">
                <p
                  class="headUser"
                  :style="{
                    background: this.attendDay != '' ? 'green' : '#d63024 ',
                    color: 'white',
                  }"
                >
                  مدرج باللجنة ({{ this.attended_number || '---' }} /
                  {{ this.attendance_number || '---' }})
                </p>
                <select
                  class="otherUnit"
                  style="margin-inline: 10px; border: none; font-size: 19px"
                  v-model="attendDay"
                  @change="handelChange()"
                >
                  <option value>اخـــتــر الــيــوم</option>
                  <option :value="d.id" v-for="d in this.days" :key="d.id">
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

              <p class="otherUnit">{{ this.personData.peo_reason || '---' }}</p>
            </div>
            <!-- <div class="mil" style="width: 50%">
              <p class="headUser">الوحدة المقترحة</p>
              <p class="otherUnit">{{ this.personData.sugg_unit_name }}</p>
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
                maxWidth: this.travelLength == 0 ? '400px' : '',
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
                maxWidth: this.punshiments.length == 0 ? '400px' : '',
              }"
            >
              <p class="headUser data-btn" @click="openCourtpopup(0)">
                <!-- style="background-color: #b7281e; color: white" -->
                العقوبات
              </p>
              <p class="otherUnit">
                <span v-if="this.punshiments.length > 0">{{ toAr(`${this.punishLength}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>
            <div class="mil" v-if="this.sta.not_stay != 0 && this.punshiments.length > 0">
              <p class="headUser data-btn" @click="openCourtpopup(1)">الحجز</p>
              <p class="otherUnit">
                <SPAN v-if="this.sta.not_stay != 0">
                  {{ toAr(`${this.sta.not_stay}`) }}
                </SPAN>
                <span v-else>لايكن</span>
              </p>
            </div>
            <div class="mil" v-if="this.punishStayLength != 0 && this.punshiments.length > 0">
              <p class="headUser data-btn" @click="openCourtpopup(2)">الحبس</p>
              <p class="otherUnit">
                <span v-if="this.sta.stay != 0">{{ toAr(`${this.sta.stay}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>

            <div class="mil" v-if="this.sta.cort != 0 && this.punshiments.length > 0">
              <p class="headUser data-btn bunish-btn" @click="openCourtpopup(3)">المحكمة</p>
              <p class="otherUnit">
                <span v-if="this.sta.cort != 0">{{ toAr(`${this.sta.cort}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>

            <div class="mil" v-if="this.sta.other > 0 && this.punshiments.length > 0">
              <p class="headUser data-btn bunish-btn" @click="openCourtpopup(4)">المحكمة المدنية</p>
              <p class="otherUnit">
                <span v-if="this.sta.other != 0">{{ toAr(`${this.sta.other}`) }}</span>
                <span v-else>لايكن</span>
              </p>
            </div>
          </div>
          <!-- نهاية العقوبات  -->
          <div
            class="travelSolution"
            style="display: flex; align-items: center; height: 22px"
            v-if="this.personData.reasons.length > 0"
          >
            <h4 style="margin-left: 10px">الأسـبــاب</h4>
            <hr style="background-color: black; font-weight: bolder" />
          </div>
          <div class="mil" v-if="this.personData.reasons.length > 0">
            <p
              class="headUser test"
              style="background-color: #d63024 !important; color: white !important"
            >
              الأسـبــاب
            </p>
            <p class="otherUnit">{{ this.personData.reasons[0].reason_description }}</p>
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
                maxWidth: this.personData.medical_history.length == 0 ? '400px' : '',
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
                <span v-if="this.personData.medical_history.length > 0">
                  {{ toAr(`${this.personData.medical_history.length}`) }}
                </span>
                <span v-else>لايكن</span>
              </p>
            </div>

            <div class="mil" v-if="this.personData.medical_history.length != 0">
              <p class="headUser">التشخيص</p>
              <p class="otherUnit">{{ this.personData.medical_history[0]?.tashkhes }}</p>
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
                    this.personData.marital_state_code == 1
                      ? 'متزوج ويعول'
                      : this.personData.marital_state_code == 4
                        ? 'مطلق'
                        : this.personData.marital_state_code == 2
                          ? 'متزوج'
                          : this.personData.marital_state_code == 0
                            ? 'اعزب'
                            : this.personData.marital_state_code == 42
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
                    this.personData.relations?.filter(
                      (d) => d.relation_degree_code == 1 || d.relation_degree_code == 1,
                    ).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        this.personData.relations?.filter((d) => d.relation_degree_code == 1)[0]
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
                    this.personData.relations?.filter(
                      (d) => d.relation_degree_code == 2 || d.relation_degree_code == 7,
                    ).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        this.personData.relations?.filter(
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
                    this.personData.relations?.filter((d) => d.relation_degree_code == 2).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        this.personData.relations?.filter((d) => d.relation_degree_code == 2).length
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
                    this.personData.relations?.filter((d) => d.relation_degree_code == 7).length !==
                    0
                  "
                >
                  {{
                    toAr(
                      `${
                        this.personData.relations?.filter((d) => d.relation_degree_code == 7).length
                      }`,
                    )
                  }}
                </p>
                <p class="otherUnit" v-else>لايكن</p>
              </div>

              <div
                class="mil"
                v-if="
                  this.personData.relations?.filter((d) => d.relation_degree_code == 3).length > 0
                "
              >
                <p class="headUser">وظيفة الوالد</p>
                <p
                  class="otherUnit"
                  v-if="
                    this.personData.relations?.filter((d) => d.relation_degree_code == 3).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        this.personData.relations?.filter((d) => d.relation_degree_code == 3)[0]
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
                  this.personData.relations?.filter((d) => d.relation_degree_code == 4).length > 0
                "
              >
                <p class="headUser">وظيفة الوالده</p>
                <p
                  class="otherUnit"
                  v-if="
                    this.personData.relations?.filter((d) => d.relation_degree_code == 4).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        this.personData.relations?.filter((d) => d.relation_degree_code == 4)[0]
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
                    this.personData.relations?.filter(
                      (d) => d.relation_degree_code == 5 || d.relation_degree_code == 6,
                    ).length > 0
                  "
                >
                  {{
                    toAr(
                      `${
                        this.personData.relations?.filter(
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
                  this.personData.relations?.filter(
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
                    this.personData.relations?.filter(
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
                        this.personData.relations?.filter(
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
              // this.personData.type_code == 5 ||
              // this.personData.type_code == 6 ||
              // this.personData.type_code == 7 ||
              // this.personData.type_code == 8 ||
              // this.personData.type_code == 9
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
          <hr v-if="this.vote_type == '3' || this.vote_type == '0'" />
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
                    this.personData.opinions.filter((e) => e.sp == 8)[0]?.unit_refuse_reason,
                  )
                "
              >
                رأي الســـلاح
              </p>
              <p
                class="otherUnit"
                v-if="this.personData.opinions.filter((e) => e.sp == 8)[0]?.a_op_code == 1"
                style="min-width: 37%"
              >
                <span v-if="this.personData?.type_code == 8">عدم استمرار</span>
                <span v-else-if="this.personData.type_code == 10">عدم تثبيت</span>
                <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                  >موافقة</span
                >
                <span v-else-if="this.personData.type_code == 9">رفت</span>
                <span v-else>اوفق</span>
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 8 && e.a_op_code == 0)"
                class="otherUnit"
                style="min-width: 37%"
              >
                <span v-if="this.personData.type_code == 8">استمرار</span>
                <span v-else-if="this.personData.type_code == 10">التثبيت</span>
                <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                  >عدم الموافقة</span
                >
                <span v-else-if="this.personData.type_code == 9">استمرار</span>
                <span v-else>لا اوافق</span>
              </p>
              <p v-else class="otherUnit">بدون تسجيل</p>
            </div>
            <!-- ======================================= -->
            <!-- v-if="this.personData.pern_army != this.personData.army_code && this.personData.opinions?.filter(
                (e) => e.sp == 8 && (e.ua_op_code == 1 || e.ua_op_code == 0)
            ).length > 0"-->
            <div
              class="mil"
              style="width: 15%"
              v-if="
                this.personData.pern_army != this.personData.army_code &&
                this.personData.opinions?.filter(
                  (e) => e.sp == 8 && (e.ua_op_code == 1 || e.ua_op_code == 0),
                ).length > 0
              "
            >
              <p class="headUser" style="cursor: pointer">رأي التشكيل</p>
              <p
                class="otherUnit"
                v-if="this.personData.opinions.filter((e) => e.sp == 8)[0]?.ua_op_code == 1"
                style="min-width: 37%"
              >
                <span v-if="this.personData?.type_code == 8">عدم استمرار</span>
                <span v-else-if="this.personData.type_code == 10">عدم تثبيت</span>
                <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                  >موافقة</span
                >
                <span v-else-if="this.personData.type_code == 9">رفت</span>
                <span v-else>اوفق</span>
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 8)[0]?.ua_op_code == 0"
                class="otherUnit"
                style="min-width: 37%"
              >
                <span v-if="this.personData.type_code == 8">استمرار</span>
                <span v-else-if="this.personData.type_code == 10">التثبيت</span>
                <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                  >عدم الموافقة</span
                >
                <span v-else-if="this.personData.type_code == 9">استمرار</span>
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
                {{ this.personData.haya_head_opinion }}
              </p>
            </div>
            <div class="mil" v-if="this.memberType" style="width: 40%">
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
                :disabled="this.member != 'رئيس اركان حرب القوات المسلحة'"
              >
                <option value="4"></option>
                <option value="1" style="font-size: 14px; font-family: 'cairo'; font-weight: 600">
                  <span v-if="this.personData.type_code == 8">انهاء الخدمة لعدم الصلاحية</span>
                  <span v-else-if="this.personData.type_code == 10">عدم تثبيت</span>
                  <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                    >موافقة</span
                  >
                  <span v-else-if="this.personData.type_code == 9">رفت</span>
                  <span v-else>اوفق</span>
                </option>
                <option value="2" style="font-size: 14px; font-family: 'cairo'; font-weight: 600">
                  <span v-if="this.personData.type_code == 8">استمرار</span>
                  <span v-else-if="this.personData.type_code == 10">التثبيت</span>
                  <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="this.personData.type_code == 9">استمرار</span>
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
                v-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.u_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي.
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.u_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.u_op_code == 0"
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
                v-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.ua_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.ua_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.ua_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
            <div class="res-screen">
              <p class="leader">رأي السلاح</p>
              <p
                v-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.a_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.a_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 4)[0]?.a_op_code == 0"
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
                v-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.u_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي.
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.u_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.u_op_code == 0"
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
                v-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.ua_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.ua_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.ua_op_code == 0"
                class="resLeader"
                style="background-color: #b7281e"
              >
                بدون تسجيل
              </p>
            </div>
            <div class="res-screen">
              <p class="leader">رأي السلاح</p>
              <p
                v-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.a_op_code == 1"
                class="resLeader"
                style="background-color: #158e21"
              >
                اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.a_op_code == 2"
                class="resLeader"
                style="background-color: #b7281e"
              >
                لا اوصـــي
              </p>
              <p
                v-else-if="this.personData.opinions.filter((e) => e.sp == 5)[0]?.a_op_code == 0"
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
              v-if="this.personData.type_code == 2 || this.personData.type_code == 3"
            >
              <!-- @click="opinin = !opinin" -->
              <h4 style="margin-left: 10px">الآراء في التجديد</h4>
              <hr style="background-color: black; font-weight: bolder" />
            </div>
            <div
              class="opininRes"
              v-if="this.personData.type_code == 2 || this.personData.type_code == 3"
            >
              <!-- && opinin -->
              <div class="res-screen">
                <p class="leader">القائد المباشر</p>
                <p
                  v-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.u_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي.
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.u_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.u_op_code == 0"
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
                  v-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.ua_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.ua_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.ua_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>
              <div class="res-screen">
                <p class="leader">رأي السلاح</p>
                <p
                  v-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.a_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.a_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 2)[0]?.a_op_code == 0"
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
              v-if="this.personData.type_code == 1 || this.personData.type_code == 3"
            >
              <!-- @click="opinin = !opinin" -->
              <h4 style="margin-left: 10px">الآراء في الترقي</h4>
              <hr style="background-color: black; font-weight: bolder" />
            </div>
            <div
              class="opininRes"
              v-if="this.personData.type_code == 1 || this.personData.type_code == 3"
            >
              <!-- && opinin -->
              <div class="res-screen">
                <p class="leader">القائد المباشر</p>
                <p
                  v-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.u_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.u_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.u_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>

              <div class="res-screen">
                <p class="leader">قائد المستوى الأعلى</p>
                <p
                  v-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.ua_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.ua_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.ua_op_code == 0"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  بدون تسجيل
                </p>
              </div>
              <div class="res-screen">
                <p class="leader">رأي السلاح</p>
                <p
                  v-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.a_op_code == 1"
                  class="resLeader"
                  style="background-color: #158e21"
                >
                  اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.a_op_code == 2"
                  class="resLeader"
                  style="background-color: #b7281e"
                >
                  لا اوصـــي
                </p>
                <p
                  v-else-if="this.personData.opinions.filter((e) => e.sp == 1)[0]?.a_op_code == 0"
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
            v-if="personData?.mil_ser && !this.out_user && !this.show"
            style="display: none"
          >
            <div class="master-opinin" v-if="this.vote_type != 1">
              <p class="master-opinin-name">{{ this.member_job }}</p>
              <form>
                <label style="color: #158e21" class="accept">
                  <input
                    type="radio"
                    value="1"
                    :checked="current_vote == 1"
                    name="opinin-pre"
                    v-model="member_op"
                    @click="member_op == 1 ? vote_handel(4)((member_op = '')) : vote_handel(1)"
                    :disabled="this.disable"
                  />
                  <span
                    class="customChecked"
                    v-if="member_op == 1"
                    style="background-color: #158e21 !important"
                  ></span>

                  <span v-if="this.personData.type_code == 8">عدم استمرار</span>
                  <span v-else-if="this.personData.type_code == 10">عدم تثبيت</span>
                  <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                    >موافقة</span
                  >
                  <span v-else-if="this.personData.type_code == 9">رفت</span>
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
                    :disabled="this.disable"
                  />
                  <span
                    class="customChecked"
                    v-if="member_op == 2"
                    style="background-color: #b7281e !important"
                  ></span>
                  <span v-if="this.personData.type_code == 8">استمرار</span>
                  <span v-else-if="this.personData.type_code == 10">التثبيت</span>
                  <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="this.personData.type_code == 9">استمرار</span>
                  <span v-else>لا اوافق</span>
                </label>
                <!-- <label style="color: goldenrod" class="notAcceptAndNotrej">
                  <input
                    type="radio"
                    :checked="current_vote == 0"
                    name="opinin-pre"
                    v-model="member_op"
                    @click="vote_handel(0)"
                    :disabled="this.disable"
                  />
                  <span class="customChecked"></span>

                  ارجاء
                </label>-->
              </form>
            </div>

            <div class="master-opinin" v-if="!this.out_user && this.vote_type == 1 && !this.show">
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
                    :disabled="this.disable"
                    :checked="this.member_decision == 1"
                  />
                  <span
                    class="customChecked"
                    v-if="member_decision == '1'"
                    style="background-color: #158e21 !important"
                  ></span>

                  <span v-if="this.personData.type_code == 8">عدم استمرار</span>
                  <span v-else-if="this.personData.type_code == 10">عدم تثبيت</span>
                  <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                    >موافقة</span
                  >
                  <span v-else-if="this.personData.type_code == 9">رفت</span>
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
                    :disabled="this.disable"
                    :checked="this.member_decision == 2"
                  />
                  <span
                    class="customChecked"
                    v-if="member_decision == '2'"
                    style="background-color: #b7281e"
                  ></span>

                  <span v-if="this.personData.type_code == 8">استمرار</span>
                  <span v-else-if="this.personData.type_code == 10">التثبيت</span>
                  <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="this.personData.type_code == 9">استمرار</span>
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
                    :disabled="this.disable"
                    :checked="this.personData.final_decision == 0"
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
            v-if="this.personData.date_serial"
          >
            {{ toAr(`${this.personData.date_serial} `) }}/
            {{ toAr(`${this.personData.afr_persons_len} `) }}
          </p>
          <div class="control" v-if="this.out_user">
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
              <button @click="this.gothen(this.data)" v-if="this.index < this.data.length">
                الـتـالـي
              </button>
              سجل {{ this.index + 1 }} من {{ this.data.length }}
              <button @click="this.goback(this.data)">السابق</button>
            </div>
          </div>
        </div>
        <!-- Image and Counters Section -->
        <div class="counters">
          <img
            id="personImage"
            :src="this.smallPhoto"
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
            v-if="this.vote_type == '1' && !out_user && !this.show"
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

                <span v-if="this.personData.type_code == 8">عدم استمرار</span>
                <span v-else-if="this.personData.type_code == 10">عدم تثبيت</span>
                <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                  >موافقة</span
                >
                <span v-else-if="this.personData.type_code == 9">رفت</span>
                <span v-else>موافق</span>
              </p>
            </div>
            <!-- <div class="counter-names" v-for="us in vote_1" :key="us.id">
              <p>{{ us.degree }} {{ us.member }}</p>
            </div>-->
          </div>
          <div
            class="counter-container reject-counter"
            v-if="this.vote_type == '1'"
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
                  <span v-if="this.personData.type_code == 8">استمرار</span>
                  <span v-else-if="this.personData.type_code == 10">التثبيت</span>
                  <span v-else-if="this.personData.type_code == 5 || this.personData.type_code == 4"
                    >عدم الموافقة</span
                  >
                  <span v-else-if="this.personData.type_code == 9">استمرار</span>
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
            v-if="this.vote_type == '1'"
            v-show="vote_0.length > 0"
            style="display: none"
          >
            <div class="counter-circle" v-if="!this.out_user && !this.show">
              <p class="circle-label" style="color: black !important">الارجاء</p>
            </div>
            <div
              class="counter-names"
              v-for="us in vote_0"
              :key="us.id"
              v-if="!this.out_user && !this.show"
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
            v-if="this.personData.type_code == 6"
          >
            <p style="margin: 0; text-align: center">{{ this.personData.sugg_unit_name }}</p>
          </div>
          <div class="upload-container" v-if="out_user && this.user_id != 100">
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
