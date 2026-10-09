import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useWebSocketStore } from './useWebSocketStore'
import lagnaService from '@/services/lagnaService'

export const useReportStore = defineStore('report', {
  state: () => ({
    reportData: [],
    personsReportData: [],
    unitsReportData: [],

    prntArmyName: [],
    lastUpdate: null,

    isLoading: true,
    error: null,

    prnt_army_code: null,
    unit_code: null,
    params: null,

    filters: {
      prnt_army_name: '',
      // sortBy: 'mil_no',
      // sortDir: 'asc',
    },

    pagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
    personsReportPagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
    unitsReportPagination: {
      page: 1,
      pageSize: 20,
      total: 0,
    },
  }),

  actions: {
    async getPrntArmyUnitsReportDetails() {
      this.loading = true
      try {
        console.log('this.params', this.params)
        console.log('this.params', this.filters)
        const res = await lagnaService.fetchPrntArmyUnitsReportDetails(this.prnt_army_code, {
          ...this.params,
          ...this.filters,
          page: this.unitsReportPagination.page,
          page_size: this.unitsReportPagination.pageSize,
        })

        this.unitsReportData = res.results
        this.unitsReportPagination.total = res.count

        return res.results
        // this.pagination.total = res.count
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async getPrntArmyUnitsPersonsReportDetails() {
      this.loading = true
      try {
        const res = await lagnaService.fetchPrntArmyUnitsPersonsReportDetails(
          this.prnt_army_code,
          this.unit_code,
          {
            ...this.params,
            page: this.personsReportPagination.page,
            page_size: this.personsReportPagination.pageSize,
          },
        )

        this.personsReportData = res.results
        this.personsReportPagination.total = res.count

        return res.results
        // this.pagination.total = res.count
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async getPrntArmyPersonsReportDetails() {
      this.loading = true
      try {
        console.log('this.params', this.params)
        const res = await lagnaService.fetchPrntArmyPersonsReportDetails(this.prnt_army_code, {
          ...this.params,
          page: this.personsReportPagination.page,
          page_size: this.personsReportPagination.pageSize,
        })

        this.personsReportData = res.results
        this.personsReportPagination.total = res.count

        return res.results
        // this.pagination.total = res.count
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    filteredReportData(armyName = 'all') {
      return armyName === 'all'
        ? this.reportData
        : this.reportData.filter((r) => r.pern_name === armyName)
    },
    filteredCommitiReportData(armyName = 'all') {
      return armyName === 'all'
        ? this.commitiReportData
        : this.commitiReportData.filter((r) => r.pern_name === armyName)
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1
      console.log('this.filters', this.filters)
      this.connectReportSocket()
    },

    connectReportSocket() {
      const wsStore = useWebSocketStore()
      const reportSocket = wsStore.connect('report', '/photo/report/', {
        autoReconnect: true,
        heartbeatInterval: 8000,
      })

      reportSocket.socket.value.onmessage = (event) => {
        const data = JSON.parse(event.data)

        console.log('data ============>', event)
        // Ignore ping/pong
        if (data?.type === 'pong') return

        // Handle different event types
        if (data?.type === 'report:update') {
          // Optimistic UI: تحديث مباشر
          this.reportData = data.payload
          this.lastUpdate = new Date()
        } else if (data?.type === 'report:summary') {
          // ممكن نضيف summary أو أي بيانات إضافية
          this.reportData = data.payload
          this.lastUpdate = new Date()
        } else {
          this.reportData = data
        }

        this.isLoading = false
      }
    },
    disconnectReportSocket() {
      useWebSocketStore().disconnect('report')
    },

    setPage(page) {
      this.pagination.page = page
    },

    setPageSize(size) {
      this.pagination.pageSize = size
      this.pagination.page = 1
    },

    setPersonsPage(page) {
      console.log(page)
      this.personsReportPagination.page = page
      if (this.unit_code) {
        this.getPrntArmyUnitsPersonsReportDetails()
      } else {
        this.getPrntArmyPersonsReportDetails()
      }
    },

    setPersonsPageSize(size) {
      this.personsReportPagination.pageSize = size
      this.personsReportPagination.page = 1
      if (this.unit_code) {
        this.getPrntArmyUnitsPersonsReportDetails()
      } else {
        this.getPrntArmyPersonsReportDetails()
      }
    },

    setUnitsPage(page) {
      this.unitsReportPagination.page = page
      this.getPrntArmyUnitsReportDetails()
    },

    setUnitsPageSize(size) {
      this.unitsReportPagination.pageSize = size
      this.unitsReportPagination.page = 1
      this.getPrntArmyUnitsReportDetails()
    },

    setUnitsFilters(filters) {
      console.log('filters', filters)
      this.filters = { ...this.filters, ...filters }
      console.log('this.filters', this.filters)
      this.unitsReportPagination.page = 1
      this.getPrntArmyUnitsReportDetails()
    },
    resetPersonsPagination() {
      this.personsReportPagination = {
        page: 1,
        pageSize: 20,
        total: 0,
      }
    },

    resetUnitsPagination() {
      this.unitsReportPagination = {
        page: 1,
        pageSize: 20,
        total: 0,
      }
    },

    resetPersonsData() {
      this.personsReportData = []
    },

    resetUnitsData() {
      this.unitsReportData = []
    },

    setSort(column) {
      if (this.filters.sortBy === column) {
        this.filters.sortDir = this.filters.sortDir === 'asc' ? 'desc' : 'asc'
      } else {
        this.filters.sortBy = column
        this.filters.sortDir = 'asc'
      }
    },
  },
  getters: {},
})
