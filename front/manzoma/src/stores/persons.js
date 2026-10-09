import { defineStore } from 'pinia'
import personsService from '@/services/personsService'

export const usePersonsStore = defineStore('persons', {
  state: () => ({
    persons: [],
    currentPerson: null,

    opinions: [],
    reasons: [],
    opinionTypes: [],
    votesTypes: [],

    loading: false,
    error: null,

    filters: {
      mil_no: '',
      person_name: '',
      unit_name: '',
      sortBy: '',
      sortDir: '',
    },

    pagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
  }),

  actions: {
    async fetchPersons() {
      this.loading = true
      try {
        const res = await personsService.fetchPersons({
          ...this.filters,
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
        })

        this.persons = res.results
        this.pagination.total = res.count
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async fetchPersonInfo(mil_ser) {
      this.loading = true
      this.error = null
      try {
        const data = await personsService.fetchPersonInfo(mil_ser)
        this.cuuDetailePersons = data
        this.loaded = true
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchLaganPersonInfo(mil_ser) {
      this.loading = true
      this.error = null
      try {
        const data = await personsService.fetchLaganPersonInfo(mil_ser)
        this.cuuDetailePersons = data
        this.loaded = true
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchBasicPersonInfo(mil_ser) {
      this.loading = true
      this.error = null
      try {
        const data = await personsService.fetchBasicPersonInfo(mil_ser)
        this.cuuPersons = data
        this.loaded = true
        return data
      } catch (error) {
        this.error = error
        throw error
      } finally {
        this.loading = false
      }
    },
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1
      this.fetchPersons()
    },

    setPage(page) {
      this.pagination.page = page
      this.fetchPersons()
    },

    setPageSize(size) {
      this.pagination.pageSize = size
      this.pagination.page = 1
      this.fetchPersons()
    },

    setSort(column) {
      if (this.filters.sortBy === column) {
        this.filters.sortDir = this.filters.sortDir === 'asc' ? 'desc' : 'asc'
      } else {
        this.filters.sortBy = column
        this.filters.sortDir = 'asc'
      }
      this.fetchPersons()
    },

    async fetchPerson(mil_ser) {
      this.loading = true
      try {
        this.currentPerson = await personsService.fetchPersonInfo(mil_ser)
      } finally {
        this.loading = false
      }
    },

    async fetchLagnaOpinionTypes(person_id) {
      this.loading = true
      try {
        console.log("+++++++++++++++>",person_id)
        const res = await personsService.fetchLagnaOpinionTypes(person_id)
        this.opinionTypes = res.opinions
        this.votesTypes = res.votes
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },

    async fetchPersonOpinions(committe_code, spacific_id, person_id, params) {
      this.loading = true
      try {
        const res = await personsService.fetchSpecificsPersonOpinions(
          committe_code,
          spacific_id,
          person_id,
          params,
        )

        this.opinions = res.results
        // this.pagination.total = res.count
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async addSpecificsPersonOpinions(committe_code, spacific_id, person_id, params) {
      this.loading = true
      try {
        const res = await personsService.addSpecificsPersonOpinions(
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
    async setFinalDecision(committe_code, spacific_id, person_id, params) {
      this.loading = true
      try {
        const res = await personsService.addPersonFinalDecision(
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
    async deleteSpecificsPersonOpinions(committe_code, spacific_id, person_id, opinion_id, params) {
      this.loading = true
      try {
        const res = await personsService.deleteSpecificsPersonOpinions(
          committe_code,
          spacific_id,
          person_id,
          opinion_id,
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
    async fetchPersonReasons(committe_code, spacific_id, person_id, params) {
      this.loading = true
      try {
        const res = await personsService.fetchSpecificsPersonReasons(
          committe_code,
          spacific_id,
          person_id,
          params,
        )

        console.log('reasons', res)
        this.reasons = res
        // this.pagination.total = res.count
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async addSpecificsPersonReasons(committe_code, spacific_id, person_id, params) {
      this.loading = true
      try {
        const res = await personsService.addSpecificsPersonReasons(
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
    async deleteSpecificsPersonReasons(committe_code, spacific_id, person_id, reason_id, params) {
      this.loading = true
      try {
        const res = await personsService.deleteSpecificsPersonReasons(
          committe_code,
          spacific_id,
          person_id,
          reason_id,
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

    clearCurrent() {
      this.currentPerson = null
    },
  },
})
