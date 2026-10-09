<script>
import axios, { Axios } from 'axios'
import AdminAlertPopup from '@/components/global/popup/adminAlertPopup.vue'
import imagesReport from '@/components/global/popup/imagesReport.vue'
import ImagesReport from '../components/global/popup/imagesReport.vue'
export default {
  data() {
    return {
      searchInput: '',
      afrOpinion: 'all',
      armyName: 'all',
      groupName: 'all',
      dis_name: 'all',
      personStatus: 'all',
      lagnaType: 'all',
      LagnaDay: 'all',
      usersTable: [],
      filteredUsersTable: [],
      userData: {},
      milNumOfFinalDecision: '',
      isPopupVisible: false,
      modalMessage: 'hello',
      popupTimeout: null,
      printImage: false,
      printPdf: null,
      mil_ser: '',
      endData: {},
      attended: this.userData?.attended,
      memberForDay: {},
      doneFlag: this.userData?.done_flag,
      reportImages: false,
      reportData: {},
    }
  },
  components: [imagesReport, AdminAlertPopup],
  mounted() {
    this.fetchUserData()
    this.getreportImages()
    this.useSocket()
  },
  // watch:{
  //   if (this.usersTable.status == 401) {
  //     localStorage.clear();
  //     this.$router.push({ name: "login" });
  //   }
  // },
  methods: {
    async getreportImages() {
      let res = await axios.get('get_images_report/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      console.log('rrrrrrrrrrrrr', res.data)
      this.reportData = { ...res.data }
      // console.log(this.reportData);
    },

    openreportImagePopup() {
      this.reportImages = true
    },
    closereportImagePopup() {
      this.reportImages = false
    },

    // ==============================================================
    useSocket() {
      console.log('socket')
      let socket = null
      try {
        socket = new WebSocket(
          `ws://afrad.oma.mil:8080/ws/afr_persons/?token=${localStorage.getItem('token')}`,
        )
      } catch (error) {
        console.log('error❌', error)
      }
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        this.mil_ser = localStorage.getItem('peopleShow')
        if (data.message.startsWith('final_decision')) {
          this.usersTable = this.usersTable.map((n) => {
            if (data.data.mil_ser == n.mil_ser) {
              return {
                ...n,
                final_decision: data.data.vote_type,
                // printImage: this.printImage,
                // printPdf: this.printPdf,
              }
            } else {
              return n
            }
          })
        }
        // this.filteredUsersTable = this.usersTable;
        this.filterUsers()
        this.countMember()
      }
    },
    countMember() {
      if (this.LagnaDay != 'all') {
        this.memberForDay = this.usersTable.filter((e) => e.attended_date == this.LagnaDay)
        console.log(this.memberForDay)
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
    resetForm() {
      this.searchInput = ''
      this.afrOpinion = 'all'
      this.armyName = 'all'
      this.groupName = 'all'
      this.dis_name = 'all'
      ;((this.dis_name = 'all'),
        (this.personStatus = 'all'),
        (this.lagnaType = 'all'),
        (this.LagnaDay = 'all'),
        this.filterUsers())
    },

    filterUsers() {
      this.filteredUsersTable = this.usersTable.filter((record) => {
        const searchInputFilter =
          record.person_name?.includes(this.searchInput) ||
          record.army_name?.includes(this.searchInput) ||
          record.unit_name?.includes(this.searchInput) ||
          record.committe_order == this.searchInput ||
          String(record.mil_no)?.includes(this.searchInput) ||
          this.searchInput == ''
        const afrOpinionFilter = record.afr_opinion == this.afrOpinion || this.afrOpinion == 'all'
        const armyNameFilter = record.army_name == this.armyName || this.armyName == 'all'
        const groupNameFilter = record.group_no == this.groupName || this.groupName == 'all'
        // test
        const LagnaDayFilter = record.attended_date == this.LagnaDay || this.LagnaDay == 'all'
        const lagnaTypeFilter = record.type_code == this.lagnaType || this.lagnaType == 'all'
        // end test
        const desNameFilter =
          record.final_decision == (this.dis_name == 'اوافق' ? 1 : 2) || this.dis_name == 'all'
        // const personStatusFilter =
        //   this.personStatus == record.personStatus ||
        //   this.personStatus == "all";
        return (
          searchInputFilter &&
          afrOpinionFilter &&
          armyNameFilter &&
          groupNameFilter &&
          desNameFilter &&
          lagnaTypeFilter &&
          LagnaDayFilter
        )
      })
    },

    // test For search user
    // async searchForUser() {
    //   await axios
    //     .get(`persons/?person_name=${this.searchInput}`, {
    //       headers: {
    //         Authorization: `Bearer ${localStorage.getItem("token")}`,
    //       },
    //     })
    //     .then((re) => console.log(re.data));
    // },
    openPopup(pop) {
      console.log(pop)
      axios
        .get(`person/${this.userData.mil_ser}/?op=${pop}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then((re) => {
          if (re.status == 200) {
            this.isPopupVisible = true
            clearTimeout(this.popupTimeout)
            if (pop == 'units') {
              this.modalMessage = `تم عرض وحدات المستخدم`
            } else if (pop == 'punish') {
              this.modalMessage = `تم عرض محاكم المستخدم`
            } else if (pop == 'medical') {
              this.modalMessage = `تم عرض اللجان الطبية المستخدم`
            } else if (pop == 'travel') {
              this.modalMessage = `تم عرض السفر السابق المستخدم`
            } else if (pop == 'photo') {
              this.modalMessage = `تم عرض  الصور الشخصية المستخدم`
            } else if (pop == 'history') {
              this.modalMessage = `تم عرض تاريخ ترقي المستخدم`
            } else if (pop == 'end') {
              this.modalMessage = `تم رجوع  جميع ال popup  المستخدم`
              this.mil_ser = ''
            } else if (pop == 'relation') {
              this.modalMessage = `تم عرض تاريخ البيانات الاجتماعية للمستخدم`
            } else if (pop == 'Courses') {
              this.modalMessage = `تم عرض التأهيل للمستخدم`
            } else if (pop == 'Eff_report') {
              this.modalMessage = `تم عرض تقرير الكفائة للمستخدم`
            } else if (pop == 'close') {
              this.modalMessage = `تم عرض الشاشة الرئيسية`
            } else if (pop == 'opinion') {
              this.modalMessage = `تم عرض الاراء`
            } else if (pop == 'poea') {
              this.modalMessage = `تم عرض الالتماس`
            } else if (pop == 'takeScreen') {
              this.modalMessage = `تم التقاط صورة`
            } else if (pop == 'takePdf') {
              this.modalMessage = `تم تحميل pdf`
            } else if (pop == 'report') {
              this.modalMessage = `تم فتح تقرير الحضور`
            }
            this.popupTimeout = setTimeout(() => {
              this.isPopupVisible = false
            }, 3000)
          }
        })
    },
    openreport() {
      axios.get(`get_lagna_statistics/?lagna_date=${this.LagnaDay}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
    },
    selected(userData) {
      this.userData = userData
      axios
        .get(`person/${userData.mil_ser}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then((res) => {
          if (res.status == 200) {
            clearTimeout(this.popupTimeout)
            this.isPopupVisible = true
            localStorage.setItem('peopleShow', res.data.mil_ser)
     
            this.endData = res.data
            this.modalMessage = ` تم عرض بيانات ${userData.person_name}`
            this.popupTimeout = setTimeout(() => {
              this.isPopupVisible = false
            }, 3000)
            // if (this.memberForDay.length > 0) {
            //   this.$router.push({
            //     name: "home",
            //     query: { count: this.this.memberForDay?.length },
            //   });
            // }
          }
        })
    },
    async decision_handel() {
      await axios.get(`vote/${localStorage.getItem('peopleShow')}/?vote_type=4`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
    },
    async attendedAction(us) {
      try {
        const res = await axios.post(
          `attend_person/${us.mil_ser}/`,
          {
            attended: us.attended,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )
        console.log('Attended updated:', res.data)
      } catch (error) {
        console.error('Error updating attended:', error)
      }
    },
    async doneAction(us) {
      try {
        const res = await axios.post(
          `attend_person/${us.mil_ser}/`,
          {
            done_flag: us.done_flag,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          },
        )
        console.log('DoneFlag updated:', res.data)
      } catch (error) {
        console.error('Error updating done_flag:', error)
      }
    },
  },
  components: { ImagesReport },
}
</script>

<template>
  <div class="adminPage" @click="isPopupVisible = false">
    <AdminAlertPopup
      :showPopup="isPopupVisible"
      @close="isPopupVisible = false"
      :modalMessage="modalMessage"
    />

    <div class="titlePage">
      <h4 class="topTitle">
        مناظرة لجنة الراتب العالي
        <!-- لجنة ( ترقي / تجديد ) راتب عالي نشرة يوليو 


        2025-->
      </h4>
    </div>
    <!-- scearch form  -->
    <form action @submit.prevent>
      <div class="filter-select-wrapper">
        <span>السلاح</span>
        <select name="army-name" class="select-input" v-model="armyName" @change="filterUsers()">
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
      <div class="filter-select-wrapper">
        <span>المجموعه</span>
        <select name="army-name" class="select-input" v-model="groupName" @change="filterUsers()">
          <option value="all" :value="groupName">جميع الحالات</option>
          <option
            v-for="(us, index) in this.usersTable
              ?.map((e) => e.group_no)
              .filter((e, i, a) => i === a.indexOf(e))"
            :value="us"
          >
            {{ us }}
          </option>
        </select>
      </div>
      <!-- test test test test test test test test test test test test test  -->
      <div class="filter-select-wrapper">
        <span>اليوم</span>
        <select
          name="army-name"
          class="select-input"
          v-model="LagnaDay"
          @change="(filterUsers(), countMember())"
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
        <span>نوع اللجنة</span>
        <select name="army-name" class="select-input" v-model="lagnaType" @change="filterUsers()">
          <option value="all" :value="lagnaType">جميع اللجان</option>
          <option
            v-for="(us, index) in this.usersTable
              ?.map((e) => e.type_code)
              .filter((e, i, a) => i === a.indexOf(e))"
            :value="us"
          >
            {{
              us == 1
                ? 'ترقــي'
                : us == 2
                  ? 'تجـــديــد'
                  : us == 3
                    ? 'تجديد/ ترقــي'
                    : us == 4
                      ? 'عدم الرغبة'
                      : us == 5
                        ? 'استقالة'
                        : us == 6
                          ? 'ترشيح'
                          : us == 7
                            ? 'التماس'
                            : us == 8
                              ? ' عدم صلاحية'
                              : us == 9
                                ? 'الرفت الجوازي'
                                : 'التثبيت'
            }}
          </option>
        </select>
        <!-- 
        v-for="(us, index) in this.usersTable
            ?.map((e) => e.type_name)
            .filter((e, i, a) => i === a.indexOf(e))"
            :value="us" -->
      </div>
      <!-- end test end  test end test end test end test test test test test test test test test  -->

      <div class="filter-select-wrapper">
        <span>القرار</span>
        <select name="army-name" class="select-input" v-model="dis_name" @change="filterUsers()">
          <option value="all" :value="dis_name">جميع الحالات</option>
          <option
            v-for="(us, index) in this.usersTable
              ?.map((e) => (e.final_decision == 1 ? 'اوافق' : 'لا اوافق'))
              .filter((e, i, a) => i === a.indexOf(e))"
            :value="us"
          >
            {{ us }}
          </option>
        </select>
      </div>

      <input
        type="text"
        name="search"
        id="search"
        class="search-input"
        placeholder="ادخل محور التصفبة"
        v-model="searchInput"
        @keyup="filterUsers()"
      />
      <button @click="resetForm()" class="btn">Reset</button>
    </form>
    <div class="popupUsers">
      <button @click="openPopup('photo')">الصور الشخصيه</button>
      <button @click="openPopup('family')">الصورة العائلية</button>

      <button @click="openPopup('units')">وحدات</button>
      <button @click="openPopup('history')">تاريخ الترقي</button>
      <button @click="openPopup('Courses')">التأهيل</button>
      <button @click="openPopup('Eff_report')">تقرير الكفائة</button>
      <button @click="openPopup('travel')">السفر</button>
      <!-- <button @click="openPopup('reason')">الاسباب</button> -->

      <button @click="openPopup('punish')">العقوبات - مجمع</button>
      <button @click="openPopup('punish1')">العقوبات (حجز)</button>
      <button @click="openPopup('punish2')">العقوبات (حبس)</button>
      <button @click="openPopup('punish3')">العقوبات (محكمة)</button>
      <button @click="openPopup('punish4')">العقــــوبــــــات (محكمة مدنية)</button>
      <button @click="openPopup('medical')">اللجان الطبية</button>
      <button @click="openPopup('relation1,15')">الزوجة</button>
      <button @click="openPopup('relation2,7')">ابناء</button>
      <button @click="openPopup('relation2')">(ابناء - ذكور)</button>
      <button @click="openPopup('relation7')">(ابناء - اناث)</button>
      <button @click="openPopup('shhh')">الاشقاء</button>
      <button @click="openPopup('shhh2')">الاقارب</button>
      <button @click="openPopup('opinion')">الآراء</button>
      <button @click="openPopup('reset')">إعادة التصويت</button>
      <button @click="openPopup('poea')">الالتماس</button>
      <button @click="openPopup('a_op_reasons')">اسباب السلاح</button>
      <button @click="openPopup('u_op_reasons')">اسـبـاب التشكيل</button>
      <button @click="openPopup('hayaa')">تسجيل رأي هيئة التنظيم والادارة</button>
      <button @click="openPopup('save')">حفظ الرأي</button>

      <button @click="openPopup('end')">رجوع الجميع</button>
      <button @click="openPopup('close')">شاشة الانتظار</button>
      <!-- <button @click="openPopup('weight')">الوزن</button> -->
      <!-- <button @click="openPopup('rejections_update')">موانع التجديد</button>
      <button @click="openPopup('rejections_traqi')">موانع الترقي</button>-->

      <button @click="openreport()">تقرير حضور اللجنة</button>
      <button @click="openreportImagePopup()">تقريرصور الافراد</button>
    </div>
    <div class="table-search">
      <table>
        <thead style="position: sticky !important; top: 0 !important; background: white !important">
          <tr>
            <th>م</th>
            <th>الــرقـــم العــسكري</th>
            <th>الدرجة</th>
            <th>الاســــم</th>
            <th>الســـلاح</th>
            <th>الوحـــدة</th>
            <th>الحالة</th>
            <th>حضور</th>
            <th>تم مناظرته</th>
            <th>صوره</th>
            <th>PDF</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(us, index) in filteredUsersTable"
            :class="
              'UserTableData ' +
              (us.final_decision == 1
                ? 'accepted'
                : us.final_decision == 2
                  ? 'rejected'
                  : us.final_decision == 0
                    ? 'delegated'
                    : '')
            "
            :style="{
              background:
                us.attended == true && us.done_flag == 0
                  ? 'orange'
                  : us.attended == true && us.done_flag == 1
                    ? '#97ff97'
                    : '',
            }"
            :key="us.mil_ser"
          >
            <td>{{ index + 1 }}</td>
            <td @click="selected(us)">{{ us.mil_no }}</td>
            <td @click="selected(us)">{{ us.degree_name }}</td>
            <td @click="selected(us)">{{ us.person_name }}</td>
            <td @click="selected(us)">{{ us.army_name }}</td>
            <td @click="selected(us)">{{ us.unit_name }}</td>
            <td style="white-space: nowrap">{{ us.type_name }}</td>
            <td>
              <input
                type="checkbox"
                v-model="us.attended"
                :true-value="true"
                :false-value="false"
                @change="attendedAction(us)"
                style="height: 35px; width: 35px"
              />
            </td>
            <td>
              <input
                type="checkbox"
                v-model="us.done_flag"
                :true-value="1"
                :false-value="0"
                @change="doneAction(us)"
                style="height: 35px; width: 35px"
              />
            </td>
            <td>
              <button
                class="data-btn"
                v-if="this.endData.mil_ser == us.mil_ser"
                @click="openPopup('takeScreen')"
              >
                طباعة صورة
              </button>
            </td>
            <td>
              <button
                class="data-btn"
                v-if="this.endData.mil_ser == us.mil_ser"
                @click="openPopup('takePdf')"
              >
                طباعة PDF
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p
      style="text-align: end; margin: auto; font-size: 18px; font-weight: 600"
      v-if="this.LagnaDay != 'all'"
    >
      {{ this.userData.date_serial }}/ {{ this.filteredUsersTable.length }}
    </p>
    <ImagesReport
      :showCourtPopup="this.reportImages"
      @close="this.closereportImagePopup"
      :tableData="reportData"
    />
  </div>
</template>

<style scoped>
.data-btn {
  padding: 7px, 4px;
  min-width: 100px;
  height: 34px;
  font-size: 18px;
}
.adminPage {
  display: flex;
  flex-direction: column;
  margin: 1rem 0 2rem;
  gap: 30px;
}

form {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 2rem 20px;
  background-color: #eeeeee;
  box-shadow:
    inset -15px 0 0 #deb209,
    inset 15px 0 0 #deb209,
    0 0 0 1px #deb209;
}

.filter-select-wrapper {
  display: flex;
  gap: 1rem;
}
.filter-select-wrapper span {
  white-space: nowrap;
}
@media (max-width: 1000px) {
  .filter-select-wrapper {
    flex-direction: column;
    align-items: center;
    gap: 1px;
  }
}
.popupUsers {
  display: flex;
  justify-content: center;
  gap: 22px;
  margin: 0 10px;
  flex-wrap: wrap;
}
.popupUsers button {
  width: 140px;
  font-size: 19px;
  border-radius: 10px;
  padding: 5px 0;
  transition: all 250ms;
}
.popupUsers button:hover {
  background-color: #ffffff;
}
.search-input {
  border: 1px solid #c0c0c0;
  border-radius: 10px;
  cursor: pointer;
  font-size: 17px;
  padding: 7px 14px;
  align-self: stretch;
  width: 100%;
  max-width: 450px;
}

.select-input {
  padding: 4px;
  font-size: 18px;
  border: 1px solid #0000008c;
  border-radius: 10px;
  outline: none;
  cursor: pointer;
}

.btn-search {
  padding: 4px;
  font-size: 18px;
  border: 1px solid #0000008c;
  border-radius: 10px;
  outline: none;
  cursor: pointer;
  width: 104px;
  background-color: #f5c200;
  border: 1px solid #deb209;
}

/* .btn-search:hover {
  background-color: #fcd126;
} */

.table-search {
  display: flex;
  justify-content: center;
  height: 500px;
  overflow: auto;
}
/* .table-search tbody {
} */

table {
  width: 85%;
  margin: auto;
  text-align: center;
  background-color: #ffffff;
  border-radius: 35px;
  border-collapse: collapse;
  box-shadow: 0 0 10px grey;
  /* overflow: hidden; */
}

td,
th {
  padding: 10px;
}

th {
  border-left: 1px solid black;
  border-bottom: 1px solid;
}

th:last-child,
td:last-child {
  border-left: none;
}

td {
  border-left: 1px solid black;
}

tbody tr {
  font-size: 18px;
  cursor: pointer;
  border-bottom: 1px solid black;
}

tbody tr:last-child {
  font-size: 18px;
  cursor: pointer;
  border-bottom: none;
}

tbody tr:hover {
  background-color: #81818157;
}

.UserTableData.accepted {
  background-color: #00ff004d;
}
.UserTableData.rejected {
  background-color: #bd00004d;
}
.UserTableData.delegated {
  background-color: #ffe6004d;
}

td span {
  color: white;
  padding: 5px 15px;
  border-radius: 5px;
  display: flex;
  justify-content: center;
}
</style>
