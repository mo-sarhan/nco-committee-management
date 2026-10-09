import {
  getAllArmyRanks,
  getAllArmyNames,
  getAllImageRejectionReasons,
  getAllPonsCons,
  getCommanderJobs,
  getLagnaSpecificsPersonStutus,
} from '@/api/modules/glopal'
import { withLoading } from '@/api/utils/apiWrapper'

import { handleApiError } from '@/utils/handleApiError'

export default {
  async fetchArmyRanks() {
    try {
      const response = await withLoading(() => getAllArmyRanks())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async getAllArmyNames(params) {
    try {
      const response = await getAllArmyNames({ params })
      console.log('response', response.data)
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchAllImageRejectionReasons() {
    try {
      const response = await withLoading(() => getAllImageRejectionReasons())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchAllPonsCons() {
    try {
      const response = await withLoading(() => getAllPonsCons())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async getCommanderJob() {
    try {
      const response = await withLoading(() => getCommanderJobs())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async getLagnaSpecificsPersonStutus() {
    try {
      const response = await withLoading(() => getLagnaSpecificsPersonStutus())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
}
