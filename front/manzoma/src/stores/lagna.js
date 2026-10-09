import { defineStore } from 'pinia'
import lagnaService from '@/services/lagnaService'
import { useWebSocketStore } from './useWebSocketStore'
import personsService from '@/services/personsService'

export const useLagnaStore = defineStore('lagnaStore', {
  state: () => ({
    allowedPersons: [],
    lagnas: [],
    specificLagnas: [],

    lagnaMembers: [],
    lagnaPersons: [],
    lagnaType: [],
    lagnaMemberUsersTypes: [],
    lagnaMemberUsers: [],
    // lagnaType: [],
    lagnaCategory: [],

    mainlagnas: [],

    currentLagna: null,
    currentSpecificLagna: null,
    currentPerson: null,

    loading: false,
    error: null,

    filters: {
      committe_name: '',
      // sortBy: 'mil_no',
      // sortDir: 'asc',
    },

    specificFilters: {
      committe_name: '',
      // sortBy: 'mil_no',
      // sortDir: 'asc',
    },

    pagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
    lagnaPersonsPagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
    lagnaMembersPagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
    specificPagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
    allowedPersonsPagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
  }),

  actions: {
    // -------------------------------lagna /committ api,s ------------------------------------------
    async fetchCommittReports(committe_code, lagna_type_id) {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaReport(committe_code, lagna_type_id, {
          // ...this.filters,
          // page: this.pagination.page,
          // page_size: this.pagination.pageSize,
        })

        // this.pagination.total = res.count
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchCommittPhotoReport(committe_code, lagna_type_id) {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaPhotoReport(committe_code, lagna_type_id, {
          // ...this.filters,
          // page: this.pagination.page,
          // page_size: this.pagination.pageSize,
        })

        // this.pagination.total = res.count
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchCommitts() {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnas({
          ...this.filters,
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
        })

        this.lagnas = res.results
        this.pagination.total = res.count
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchMemberCommitts() {
      this.loading = true
      try {
        const res = await lagnaService.fetchMemberLagnas({
          ...this.filters,
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
        })

        this.lagnas = res.results
        this.pagination.total = res.count
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async addNewCommitt(params) {
      this.loading = true
      try {
        const res = await lagnaService.addNewLagna(params)
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async updateCommitt(committe_code, params) {
      this.loading = true
      try {
        const res = await lagnaService.updateLagna(committe_code, params)
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteCommitt(committe_code) {
      this.loading = true
      try {
        const res = await lagnaService.deleteLagna(committe_code)
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async getCommittByCode(committe_code) {
      this.loading = true
      try {
        const res = await lagnaService.getLagnaByid(committe_code)

        this.currentLagna = res
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    // --------------------------- lagna specifics -----------------------
    async fetchCommittSpecifics(committe_code, params) {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaSpecifics(committe_code, {
          ...params,
          ...this.filters,
          page: this.specificPagination.page,
          page_size: this.specificPagination.pageSize,
        })

        this.specificLagnas = res.results
        this.specificPagination.total = res.count
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchOneCommittSpecific(committe_code, spacific_id) {
      this.loading = true
      try {
        const res = await lagnaService.fetchOneLagnaSpecific(committe_code, spacific_id)

        this.currentSpecificLagna = res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async addNewCommittSpecifics(committe_code, params) {
      this.loading = true
      try {
        const res = await lagnaService.addNewLagnaSpecifics(committe_code, params)

        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async updateCommittSpecifics(committe_code, spacific_id, params) {
      this.loading = true
      try {
        const res = await lagnaService.updateLagnaSpecifics(committe_code, spacific_id, params)

        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteCommittSpecifics(committe_code, spacific_id, params) {
      this.loading = true
      try {
        const res = await lagnaService.deleteLagnaSpecifics(committe_code, spacific_id, params)

        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    //  -------------------------- lagna specific Members ----------------------------------
    async fetchSpecificCommittMembers(committe_code, spacific_id, params) {
      this.loading = true
      try {
        const res = await lagnaService.fetchSpecificLagnaMembers(committe_code, spacific_id, {
          ...params,
          ...this.filters,
          page: this.lagnaMembersPagination.page,
          page_size: this.lagnaMembersPagination.pageSize,
        })

        console.log('results--------------------', res.results)
        this.lagnaMembers = res.results
        this.lagnaMembersPagination.total = res.count
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async addNewSpecificCommittMember(committe_code, spacific_id, params) {
      this.loading = true
      try {
        const res = await lagnaService.addNewSpecificLagnaMember(committe_code, spacific_id, params)

        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteSpecificCommittMember(committe_code, spacific_id, member_id) {
      this.loading = true
      try {
        const res = await lagnaService.deleteSpecificLagnaMember(
          committe_code,
          spacific_id,
          member_id,
        )

        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchAllowedSpecificCommittPersons(params) {
      this.loading = true
      try {
        const res = await lagnaService.getAlowedLagnaSpecificPerson({
          ...params,
          ...this.filters,
          page: this.allowedPersonsPagination.page,
          page_size: this.allowedPersonsPagination.pageSize,
        })

        console.log('results--------------------', res.results)
        this.allowedPersons = res.results
        this.allowedPersonsPagination.total = res.count
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    //  -------------------------- lagna specific persons ----------------------------------
    async fetchOneSpecificCommittPerson(committe_code, spacific_id, person_id, params = {}) {
      this.loading = true
      try {
        const res = await lagnaService.fetchOneLagnaSpecificsPerson(
          committe_code,
          spacific_id,
          person_id,
          {
            ...params,
            ...this.filters,
            page: this.lagnaPersonsPagination.page,
            page_size: this.lagnaPersonsPagination.pageSize,
          },
        )

        console.log('res0', res)
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchSpecificCommittPersons(committe_code, spacific_id, params = {}) {
      this.loading = true
      try {
        const res = await lagnaService.fetchSpecificLagnaPersons(committe_code, spacific_id, {
          ...params,
          ...this.filters,
          page: this.lagnaPersonsPagination.page,
          page_size: this.lagnaPersonsPagination.pageSize,
        })

        this.lagnaPersons = res.results
        this.lagnaPersonsPagination.total = res.count
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteSpecificCommittPersons(committe_code, spacific_id, person_id) {
      this.loading = true
      try {
        const res = await lagnaService.deleteLagnaSpecificsPersons(
          committe_code,
          spacific_id,
          person_id,
        )
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async addNewSpecificCommittPerson(committe_code, spacific_id, params) {
      this.loading = true
      try {
        const res = await lagnaService.addNewSpecificLagnaPerson(committe_code, spacific_id, params)

        return res
      } catch (error) {
        console.log('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', error)
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    // -------------------------------lagna category & types api,s ------------------------------------------
    async fetchcommittCategory() {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaCategory()

        this.lagnaCategory = res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchcommittTypes() {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaType()

        this.lagnaType = res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchMainCommitts() {
      this.loading = true
      try {
        const res = await lagnaService.fetchMainLagnas()

        this.mainlagnas = res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchCommittMembersUsers() {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaMembersUsers()
        this.lagnaMemberUsers = res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchCommittMembersTypes() {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaMembersTypes()
        this.lagnaMemberUsersTypes = res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async changeLagnaSpecificsPersonStutus(committe_code, spacific_id, person_id, params) {
      this.loading = true
      try {
        const res = await lagnaService.changeLagnaSpecificsPersonStutus(
          committe_code,
          spacific_id,
          person_id,
          params,
        )
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchLagnaSpecificsPersonShow(committe_code, spacific_id, person_id, params) {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaSpecificsPersonShow(
          committe_code,
          spacific_id,
          person_id,
          params,
        )
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchLagnaSpecificsPersonPopupShow(committe_code, specific_code, params) {
      this.loading = true
      try {
        const res = await lagnaService.fetchLagnaSpecificsPersonPopupShow(
          committe_code,
          specific_code,
          params,
        )
        return res
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },

    connectLagnaPersonShowSocket(committe_code, onMessage = {}) {
      const wsStore = useWebSocketStore()
      const PersonShowSocket = wsStore.connect(
        'PersonShow',
        '/lagna/',
        {
          autoReconnect: true,
          heartbeatInterval: 8000,
        },
        { lagna: committe_code },
      )

      PersonShowSocket.socket.value.onmessage = (event) => {
        const data = JSON.parse(event.data)

        // console.log("data ============>",event)
        if (onMessage) {
          onMessage(data)
        }

        // Ignore ping/pong
        if (data.type === 'pong') return

        this.isLoading = false
      }
    },
    disconnectLagnaPersonShowSocket() {
      useWebSocketStore().disconnect('PersonShow')
    },

    // // -------------------------------lagna members api,s ------------------------------------------
    // async addNewCommittMember(committe_code,params) {
    //   this.loading = true
    //   try {
    //     const res = await lagnaService.addNewLagnaMember(committe_code,params)
    //     return res;
    //   } catch (error) {
    //     this.error = error
    //     throw error
    //   } finally {
    //     this.loading = false
    //   }
    // },
    // async updateCommittMember(committe_code,params ) {
    //   this.loading = true
    //   try {
    //     const res = await lagnaService.updateLagnaMember(committe_code,params )
    //     return res;
    //   } catch (error) {
    //     this.error = error
    //     throw error
    //   } finally {
    //     this.loading = false
    //   }
    // },
    // async deleteCommittMember(committe_code,params) {
    //   this.loading = true
    //   try {
    //     const res = await lagnaService.deleteLagnaMember(committe_code,params )
    //     return res;
    //   } catch (error) {

    //     this.error = error
    //     throw error
    //   } finally {
    //     this.loading = false
    //   }
    // },

    // // -------------------------------lagna persons api,s ------------------------------------------

    // async fetchPersons() {
    //   this.loading = true
    //   try {
    //     const res = await personsService.fetchPersons({
    //       ...this.filters,
    //       page: this.pagination.page,
    //       page_size: this.pagination.pageSize,
    //     })

    //     this.persons = res.results
    //     this.pagination.total = res.count
    //   } catch (error) {
    //     this.error = error
    //   } finally {
    //     this.loading = false
    //   }
    // },

    // async fetchCommittPersons() {
    //   this.loading = true
    //   try {
    //     const res = await lagnaService.fetchLagnaPersons({
    //       ...this.filters,
    //       page: this.pagination.page,
    //       page_size: this.pagination.pageSize,
    //     })
    //     console.log("fetchCommittPersons",res.results)
    //     console.log("this.persons",this.persons)

    //     if (!res.results?.length || !this.persons?.length) {
    //       return []
    //     }

    //     const lagnaMilSet = new Set(
    //       res.results.map(p => p.mil_ser)
    //     )

    //     this.lagnaPersons =  this.persons.filter(person =>
    //       lagnaMilSet.has(person.mil_ser)
    //     )
    //     // this.lagnaPersons = res.results
    //     this.pagination.total = res.count
    //   } catch (error) {
    //     this.error = error
    //   } finally {
    //     this.loading = false
    //   }
    // },
    // async addNewCommittPerson(params) {
    //   this.loading = true
    //   try {
    //     const res = await lagnaService.addNewLagnaPerson(params)
    //     console.log("res========================>",res)
    //     return res;
    //   } catch (error) {
    //     console.log("======================>",error)
    //     this.error = error
    //     throw error
    //   } finally {
    //     this.loading = false
    //   }
    // },
    // async updateCommittPerson(committe_code,params ) {
    //   this.loading = true
    //   try {
    //     const res = await lagnaService.updateLagnaPerson(committe_code,params )
    //     console.log("res========================>",res)
    //     return res;
    //   } catch (error) {
    //     console.log("======================>",error)
    //     this.error = error
    //     throw error
    //   } finally {
    //     this.loading = false
    //   }
    // },
    // async deleteCommittPerson(committe_code,params) {
    //   this.loading = true
    //   try {
    //     const res = await lagnaService.deleteLagnaPerson(committe_code,params )
    //     console.log("res========================>",res)
    //     return res;
    //   } catch (error) {
    //     console.log("======================>",error)
    //     this.error = error
    //     throw error
    //   } finally {
    //     this.loading = false
    //   }
    // },

    // --------------------------------------- fixed ----------------------------------------
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1
      this.fetchCommitts()
    },
    setLagnaPersonsFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.lagnaPersonsPagination.page = 1
      this.fetchSpecificCommittPersons(
        this.currentSpecificLagna?.committe_code,
        this.currentSpecificLagna?.lagna_type_id,
        filters,
      )
    },
    setAllowedPersonsFilters(filters, params) {
      this.filters = { ...this.filters, ...filters }
      this.allowedPersonsPagination.page = 1
      this.fetchAllowedSpecificCommittPersons(params)
    },

    setPage(page) {
      this.pagination.page = page
      this.fetchCommitts()
    },

    setAllowedPersonsPaginationPage(page, params) {
      this.allowedPersonsPagination.page = page
      this.fetchAllowedSpecificCommittPersons(params)
    },

    setAllowedPersonsPaginationPageSize(size, params) {
      console.log(size, params)
      this.allowedPersonsPagination.pageSize = size
      this.allowedPersonsPagination.page = 1
      this.fetchAllowedSpecificCommittPersons(params)
    },
    setPageSize(size) {
      this.pagination.pageSize = size
      this.pagination.page = 1
      this.fetchCommitts()
    },

    setSort(column) {
      if (this.filters.sortBy === column) {
        this.filters.sortDir = this.filters.sortDir === 'asc' ? 'desc' : 'asc'
      } else {
        this.filters.sortBy = column
        this.filters.sortDir = 'asc'
      }
      this.fetchCommitts()
    },

    setSpecificSort(column) {
      if (this.specificFilters.sortBy === column) {
        this.specificFilters.sortDir = this.specificFilters.sortDir === 'asc' ? 'desc' : 'asc'
      } else {
        this.specificFilters.sortBy = column
        this.specificFilters.sortDir = 'asc'
      }
      this.fetchCommittSpecifics(this.currentLagna?.committe_code, this.specificFilters)
    },

    clearCurrent() {
      this.currentPerson = null
    },
  },
})
