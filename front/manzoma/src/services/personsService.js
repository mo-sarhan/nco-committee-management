import {
  getPersons,
  getImagesReport,
  getPersonDetails,
  getPersonInfo,
  getLaganPersonInfo,
  fetchBasicPersonInfo,
  postAttendance,
  checkPhotoReview,
  getVote,
  getLagnaStatistics,
} from '@/api/modules/persons'

import {
  getSpecificsPersonOpinions,
  postSpecificsPersonOpinions,
  deleteSpecificsPersonOpinions,
  postPersonFinalDecision,
  getLagnaOpinionTypes,
} from '@/api/modules/opinions'
import {
  getSpecificsPersonReasons,
  postSpecificsPersonReasons,
  deleteSpecificsPersonReasons,
} from '@/api/modules/reasons'

import { withLoading } from '@/api/utils/apiWrapper'

import { handleApiError } from '@/utils/handleApiError'

export default {
  async fetchPersons(params) {
    try {
      const response = await withLoading(() => getPersons({ params }))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchPersons_v_old() {
    try {
      const response = await withLoading(() => getPersons())
      console.log(response.data.results)
      return [
        ...response.data.filter((t) => t.committe_order != 0),
        ...response.data.filter((t) => t.committe_order == 0),
      ]
    } catch (error) {
      handleApiError(error)
    }
  },

  async fetchImagesReport() {
    try {
      return await getImagesReport()
    } catch (error) {
      handleApiError(error)
    }
  },

  async fetchPersonDetails(mil_ser, op) {
    try {
      return await getPersonDetails(mil_ser, op)
    } catch (error) {
      handleApiError(error)
    }
  },

  async fetchPersonInfo(mil_ser) {
    try {
      return await withLoading(() => getPersonInfo(mil_ser))
    } catch (error) {
      handleApiError(error)
    }
  },

  async fetchLaganPersonInfo(mil_ser) {
    try {
      return await withLoading(() => getLaganPersonInfo(mil_ser))
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchBasicPersonInfo(mil_ser) {
    try {
      return await withLoading(() => fetchBasicPersonInfo(mil_ser))
    } catch (error) {
      handleApiError(error)
    }
  },

  async updateAttendance(mil_ser, attended) {
    try {
      return await postAttendance(mil_ser, { attended })
    } catch (error) {
      handleApiError(error)
    }
  },
  async checkPhotoReview(mil_ser, photo_id, params) {
    try {
      return await checkPhotoReview(mil_ser, photo_id, params)
    } catch (error) {
      handleApiError(error)
    }
  },

  async updateDoneFlag(mil_ser, done_flag) {
    try {
      return await postAttendance(mil_ser, { done_flag })
    } catch (error) {
      handleApiError(error)
    }
  },

  async handleDecision(mil_ser, vote_type = 4, final_decision = 1) {
    try {
      return await getVote(mil_ser, vote_type, final_decision)
    } catch (error) {
      handleApiError(error)
    }
  },

  async getReport(lagna_date) {
    try {
      return await getLagnaStatistics(lagna_date)
    } catch (error) {
      handleApiError(error)
    }
  },

  async fetchLagnaOpinionTypes(person_id) {
    try {
      console.log('person_id=======>', person_id)
      const response = await withLoading(() => getLagnaOpinionTypes(person_id))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchSpecificsPersonOpinions(committe_code, spacific_id, person_id) {
    try {
      const response = await withLoading(() =>
        getSpecificsPersonOpinions(committe_code, spacific_id, person_id),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async addSpecificsPersonOpinions(committe_code, spacific_id, person_id, params) {
    try {
      return await withLoading(() =>
        postSpecificsPersonOpinions(committe_code, spacific_id, person_id, params),
      )
    } catch (error) {
      handleApiError(error)
    }
  },
  async addPersonFinalDecision(committe_code, spacific_id, person_id, params) {
    try {
      return await withLoading(() =>
        postPersonFinalDecision(committe_code, spacific_id, person_id, params),
      )
    } catch (error) {
      handleApiError(error)
    }
  },
  async deleteSpecificsPersonOpinions(committe_code, spacific_id, person_id, opinion_id, params) {
    try {
      return await withLoading(() =>
        deleteSpecificsPersonOpinions(committe_code, spacific_id, person_id, opinion_id, params),
      )
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchSpecificsPersonReasons(committe_code, spacific_id, person_id) {
    try {
      const response = await withLoading(() =>
        getSpecificsPersonReasons(committe_code, spacific_id, person_id),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async addSpecificsPersonReasons(committe_code, spacific_id, person_id, params) {
    try {
      return await withLoading(() =>
        postSpecificsPersonReasons(committe_code, spacific_id, person_id, params),
      )
    } catch (error) {
      handleApiError(error)
    }
  },
  async deleteSpecificsPersonReasons(committe_code, spacific_id, person_id, reason_id, params) {
    try {
      return await withLoading(() =>
        deleteSpecificsPersonReasons(committe_code, spacific_id, person_id, reason_id, params),
      )
    } catch (error) {
      handleApiError(error)
    }
  },
}
