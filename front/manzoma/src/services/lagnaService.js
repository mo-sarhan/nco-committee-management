import {
  getMainLagnas,
  getLagnaReport,
  getLagnaPhotoReport,
  getLagnas,
  getMemberLagnas,
  postLagnas,
  editLagnaByid,
  deleteLagnaByid,
  getLagnaByid,
  getLagnaCategory,
  getLagnaType,
  getLagnaMembersUsers,
  getLagnaMembersTypes,
  getLagnaSpecifics,
  getOneLagnaSpecific,
  addLagnaSpecifics,
  updateLagnaSpecifics,
  deleteLagnaSpecifics,
  getLagnaSpecificsMembers,
  postLagnaSpecificsMembers,
  deleteLagnaSpecificsMembers,
  getOneLagnaSpecificsPerson,
  getLagnaSpecificsPersons,
  postLagnaSpecificsPersons,
  deleteLagnaSpecificsPersons,
  getPrntArmyUnitsReportDetails,
  getPrntArmyPersonsReportDetails,
  getPrntArmyUnitsPersonsReportDetails,

  // getLagnaSpecificsPersonsDecision,
  // postLagnaSpecificsPersonsDecision,
  // deleteLagnaSpecificsPersonsDecision,
  getLagnaSpecificsPersonShow,
  getLagnaSpecificsPersonPopupShow,
  postLagnaSpecificsPersonStutus,

  // getLagnaSpecificsPersonsReady,
  getLagnaSpecificsPersonSnap,
  postLagnaSpecificsPersonSnap,
  getPsychologicPerson,
  postPsychologicPerson,
  getCommitiReportData,

  // getLagnaMembers,
  // postLagnaMember,
  // putLagnaMember,
  // deleteLagnaMember,

  // getLagnaPersons,
  // postLagnaPerson,
  // putLagnaPerson,
  // deleteLagnaPerson,
} from '@/api/modules/lagna'
import { getPersons } from '@/api/modules/persons'
import { withLoading } from '@/api/utils/apiWrapper'

import { handleApiError } from '@/utils/handleApiError'

export default {
  // -------------------------------lagna /committ api,s ------------------------------------------
  async fetchMainLagnas() {
    try {
      const response = await withLoading(() => getMainLagnas())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchLagnaReport(committe_code, lagna_type_id, params) {
    try {
      const response = await withLoading(() =>
        getLagnaReport(committe_code, lagna_type_id, { params }),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchLagnaPhotoReport(committe_code, lagna_type_id, params) {
    try {
      const response = await withLoading(() =>
        getLagnaPhotoReport(committe_code, lagna_type_id, { params }),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchLagnas(params) {
    try {
      const response = await withLoading(() => getLagnas({ params }))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchMemberLagnas(params) {
    try {
      const response = await withLoading(() => getMemberLagnas({ params }))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async addNewLagna(params) {
    try {
      const response = await withLoading(() => postLagnas(params))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async updateLagna(committe_code, params) {
    try {
      const response = await withLoading(() => editLagnaByid(committe_code, params))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async deleteLagna(committe_code) {
    try {
      const response = await withLoading(() => deleteLagnaByid(committe_code))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async getLagnaByid(committe_code) {
    try {
      const response = await withLoading(() => getLagnaByid(committe_code))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  // ----------------------- fetch lagna specifics ------------------------------------
  async fetchLagnaSpecifics(committe_code, params) {
    try {
      const response = await withLoading(() => getLagnaSpecifics(committe_code, params))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchOneLagnaSpecific(committe_code, spacific_id) {
    try {
      const response = await withLoading(() => getOneLagnaSpecific(committe_code, spacific_id))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async addNewLagnaSpecifics(committe_code, params) {
    try {
      const response = await withLoading(() => addLagnaSpecifics(committe_code, params))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async updateLagnaSpecifics(committe_code, spacific_id, params) {
    try {
      const response = await withLoading(() =>
        updateLagnaSpecifics(committe_code, spacific_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async deleteLagnaSpecifics(committe_code, spacific_id, params) {
    try {
      const response = await withLoading(() =>
        deleteLagnaSpecifics(committe_code, spacific_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  async getAlowedLagnaSpecificPerson(params) {
    try {
      const response = await withLoading(() => getPersons({ params }))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  // -------------------------------lagna Persons api,s ------------------------------------------
  async fetchOneLagnaSpecificsPerson(committe_code, spacific_id, person_id, params) {
    try {
      const response = await withLoading(() =>
        getOneLagnaSpecificsPerson(committe_code, spacific_id, person_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchSpecificLagnaPersons(committe_code, spacific_id, params) {
    try {
      const response = await withLoading(() =>
        getLagnaSpecificsPersons(committe_code, spacific_id, { params }),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async addNewSpecificLagnaPerson(committe_code, spacific_id, params) {
    try {
      const response = await withLoading(() =>
        postLagnaSpecificsPersons(committe_code, spacific_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async deleteLagnaSpecificsPersons(committe_code, spacific_id, person_id) {
    try {
      const response = await withLoading(() =>
        deleteLagnaSpecificsPersons(committe_code, spacific_id, person_id),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  // -------------------------------lagna Members api,s ------------------------------------------
  async fetchSpecificLagnaMembers(committe_code, spacific_id, params) {
    try {
      const response = await withLoading(() =>
        getLagnaSpecificsMembers(committe_code, spacific_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async addNewSpecificLagnaMember(committe_code, spacific_id, params) {
    try {
      const response = await withLoading(() =>
        postLagnaSpecificsMembers(committe_code, spacific_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async deleteSpecificLagnaMember(committe_code, spacific_id, member_id) {
    try {
      const response = await withLoading(() =>
        deleteLagnaSpecificsMembers(committe_code, spacific_id, member_id),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  // -------------------------------lagna category & types api,s ------------------------------------------
  async fetchLagnaCategory() {
    try {
      const response = await withLoading(() => getLagnaCategory())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchLagnaType() {
    try {
      const response = await withLoading(() => getLagnaType())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  async fetchLagnaMembersUsers() {
    try {
      const response = await withLoading(() => getLagnaMembersUsers())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchLagnaMembersTypes() {
    try {
      const response = await withLoading(() => getLagnaMembersTypes())
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  // ----------------------------- reports -----------------------------
  async fetchPrntArmyUnitsReportDetails(prnt_army_code, params) {
    try {
      console.log('prnt_army_code ======================>', prnt_army_code, params)
      const response = await withLoading(() =>
        getPrntArmyUnitsReportDetails(prnt_army_code, { params }),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchPrntArmyPersonsReportDetails(prnt_army_code, params = null) {
    try {
      console.log('prnt_army_code ======================>', prnt_army_code, params)
      const response = await withLoading(() =>
        getPrntArmyPersonsReportDetails(prnt_army_code, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchPrntArmyUnitsPersonsReportDetails(prnt_army_code, unit_code, params = null) {
    try {
      console.log('prnt_army_code ======================>', prnt_army_code, params)
      const response = await withLoading(() =>
        getPrntArmyUnitsPersonsReportDetails(prnt_army_code, unit_code, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchCommitiReportData(params = {}) {
    try {
      const response = await withLoading(() => getCommitiReportData(params))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  async changeLagnaSpecificsPersonStutus(committe_code, spacific_id, person_id, params) {
    try {
      const response = await withLoading(() =>
        postLagnaSpecificsPersonStutus(committe_code, spacific_id, person_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchLagnaSpecificsPersonShow(committe_code, spacific_id, person_id, params) {
    try {
      const response = await withLoading(() =>
        getLagnaSpecificsPersonShow(committe_code, spacific_id, person_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async fetchLagnaSpecificsPersonPopupShow(committe_code, specific_code, params) {
    try {
      const response = await withLoading(() =>
        getLagnaSpecificsPersonPopupShow(committe_code, specific_code, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async addLagnaSpecificsPersonSnap(committe_code, spacific_id, person_id, params) {
    try {
      const response = await withLoading(() =>
        postLagnaSpecificsPersonSnap(committe_code, spacific_id, person_id, params),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async getLagnaSpecificsPersonSnap(committe_code, spacific_id, person_id) {
    try {
      const response = await withLoading(() =>
        getLagnaSpecificsPersonSnap(committe_code, spacific_id, person_id),
      )
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },

  async addPsychologicPerson(mil_sir, params) {
    try {
      const response = await withLoading(() => postPsychologicPerson(mil_sir, params))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
  async getPsychologicPerson(mil_sir) {
    try {
      const response = await withLoading(() => getPsychologicPerson(mil_sir))
      return response.data
    } catch (error) {
      handleApiError(error)
    }
  },
}
