import { defineStore } from 'pinia'
import glopal from '@/services/glopal'
import router from '@/router'
import swal from 'sweetalert'

export const useGlopalStore = defineStore('useGlopalStore', {
  state: () => ({
    armyRanks: [],
    allArmyNames: [],
    ImageRejectionReasons: [],
    ponsCons: [],
    commanderJobs: [],
    lagnaStatus: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchArmyRanks() {
      this.loading = true
      try {
        const res = await glopal.fetchArmyRanks()

        this.armyRanks = res
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async fetchArmys(params) {
      console.log('fetch army paramms ', params)
      this.loading = true
      try {
        if (
          params &&
          (params['army_code'] ||
            params['mil_ser__army_code'] ||
            params['mil_ser__prnt_army_code'] ||
            params['prnt_army_code'])
        ) {
          if (params['army_code']) {
            console.log('+++++++++1')
            params = {
              ...params,
              ['army_name']: params['army_code'],
            }
          }
          if (params['mil_ser__army_code']) {
            console.log('+++++++++2')
            params = {
              ...params,
              ['army_name']: params['mil_ser__army_code'],
            }
          }
          if (params['prnt_army_code']) {
            console.log('+++++++++3')
            params = {
              ...params,
              ['army_name']: params['prnt_army_code'],
            }
          }
          if (params['mil_ser__prnt_army_code']) {
            console.log('+++++++++4')
            params = {
              ...params,
              ['army_name']: params['mil_ser__prnt_army_code'],
            }
          }
          delete params.army_code
        }

        console.log('paramsparamsparamsparamsparams+++', params)
        const res = await glopal.getAllArmyNames(params)

        console.log('res', res)
        this.allArmyNames = res
        console.log('allArmyNames', this.allArmyNames)
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async fetchAllImageRejectionReasons() {
      this.loading = true
      try {
        const res = await glopal.fetchAllImageRejectionReasons()

        this.ImageRejectionReasons = res
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async fetchAllPonsCons() {
      this.loading = true
      try {
        const res = await glopal.fetchAllPonsCons()

        this.ponsCons = res
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async fetchAllCommanderJobs() {
      this.loading = true
      try {
        const res = await glopal.getCommanderJob()

        this.commanderJobs = res
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
    async fetchLagnaSpecificsPersonStutus() {
      this.loading = true
      try {
        const res = await glopal.getLagnaSpecificsPersonStutus()

        this.lagnaStatus = res
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
  },
  getters: {
    getArmyRanks: (state) => state.armyRanks,
    getImageRejectionReasons: (state) => state.ImageRejectionReasons,
    getPonsCons: (state) => state.ponsCons,
  },
})
