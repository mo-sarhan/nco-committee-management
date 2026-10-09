<script>
import axios from "axios";
export default {
  data() {
    return {
      LagnaDay: "all",
      usersTable: [],
      filteredUsersTable: [],
      armyName: "all",
    };
  },
  mounted() {
    this.filterUsers();
    this.countMember();
    this.countMember();

    // countMember() {
    //   if (this.LagnaDay != "all") {
    //     this.memberForDay = this.usersTable.filter(
    //       (e) => e.attended_date == this.LagnaDay
    //     );
    //     console.log(this.memberForDay);
    //   }
    //     }
  },

  methods: {
    countMember() {
      if (this.LagnaDay != "all") {
        this.memberForDay = this.usersTable.filter(
          (e) => e.attended_date == this.LagnaDay
        );
        console.log(this.memberForDay);
      }
    },
    async fetchUserData() {
      await axios
        .get("persons/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((res) => {
          this.usersTable = [
            ...res.data.filter((t) => t.committe_order != 0),
            ...res.data.filter((t) => t.committe_order == 0),
          ];
          this.filteredUsersTable = this.usersTable;
          console.log(this.usersTable);
        })
        .catch((err) => {
          console.log("Error getting data, ", err?.message);
          if (err.status == 401) {
            localStorage.clear();
            this.$router.push({ name: "login" });
          }
        });
    },
    resetForm() {
      this.searchInput = "";
      this.afrOpinion = "all";
      this.armyName = "all";
      this.groupName = "all";
      this.dis_name = "all";
      this.filterUsers();
    },
    filterUsers() {
      this.filteredUsersTable = this.usersTable.filter((record) => {
        const searchInputFilter =
          record.person_name?.includes(this.searchInput) ||
          record.army_name?.includes(this.searchInput) ||
          record.unit_name?.includes(this.searchInput) ||
          record.committe_order == this.searchInput ||
          String(record.mil_no)?.includes(this.searchInput) ||
          this.searchInput == "";
        const afrOpinionFilter =
          record.afr_opinion == this.afrOpinion || this.afrOpinion == "all";
        const armyNameFilter =
          record.army_name == this.armyName || this.armyName == "all";
        const groupNameFilter =
          record.group_no == this.groupName || this.groupName == "all";
        // test
        const LagnaDayFilter =
          record.attended_date == this.LagnaDay || this.LagnaDay == "all";
        const lagnaTypeFilter =
          record.type_name == this.lagnaType || this.lagnaType == "all";
        // end test
        const desNameFilter =
          record.final_decision == (this.dis_name == "اوافق" ? 1 : 2) ||
          this.dis_name == "all";
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
        );
      });
    },
  },
};
</script>
<template>
  <div class="container">
    <form @submit.prevent="">
      <div class="filter">
        <div class="filter-select-wrapper">
          <span>اليوم</span>
          <select
            name="army-name"
            class="select-input"
            v-model="LagnaDay"
            @change="filterUsers(), countMember()"
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
      </div>
      <div class="filter-select-wrapper">
        <span>السلاح</span>
        <select
          name="army-name"
          class="select-input"
          v-model="armyName"
          @change="filterUsers()"
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
    </form>
  </div>
</template>
