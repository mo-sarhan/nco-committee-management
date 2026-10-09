import http from '../http'

// ------------------ lagna -------------------
export const getMainLagnas = () => http.get('lagna/main', { params: { committe_category: 2 } }) // get main langas
export const getLagnaReport = (committe_code, lagna_type_id, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${lagna_type_id}/report`, params) // get langas info
export const getLagnaPhotoReport = (committe_code, lagna_type_id, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${lagna_type_id}/photo-report`, params) // get langas info

export const getLagnas = (params) => http.get('lagna/', params) // get langas info
export const getMemberLagnas = (params) => http.get('accounts/comm', params) // get langas info
export const postLagnas = (params) => http.post('lagna/', params) // create new lagna params {committ_name ......}
export const getLagnaByid = (committe_code) => http.get(`lagna/${committe_code}/`) // to get one lagna by id
export const editLagnaByid = (committe_code, params) =>
  http.patch(`lagna/${committe_code}/`, params) // update get one lagna by id
export const deleteLagnaByid = (committe_code) => http.delete(`lagna/${committe_code}/`) // delete get one lagna by id

/* ------------------------- get lagna specifics ------------------------*/
export const getLagnaSpecifics = (committe_code, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific`, params)
export const getOneLagnaSpecific = (committe_code, spacific_id) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}`)
export const addLagnaSpecifics = (committe_code, params) =>
  http.post(`lagna/${committe_code}/lagna-spacific/add/`, params)
export const updateLagnaSpecifics = (committe_code, spacific_id, params) =>
  http.patch(`lagna/${committe_code}/lagna-spacific/${spacific_id}/`, params)
export const deleteLagnaSpecifics = (committe_code, spacific_id, params) =>
  http.delete(`lagna/${committe_code}/lagna-spacific/${spacific_id}/delete/`, params)

// ---------------------------- lagna members ------------------
export const getLagnaSpecificsMembers = (committe_code, spacific_id, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/members/`, params)
export const postLagnaSpecificsMembers = (committe_code, spacific_id, params) =>
  http.post(`lagna/${committe_code}/lagna-spacific/${spacific_id}/members/add/`, params)
export const deleteLagnaSpecificsMembers = (committe_code, spacific_id, member_id) =>
  http.delete(`lagna/ ${committe_code}/lagna-spacific/${spacific_id}/members/${member_id}/delete/`)

// ---------------------------- lagna persons ------------------
export const getLagnaSpecificsPersons = (committe_code, spacific_id, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons`, params)
export const getOneLagnaSpecificsPerson = (committe_code, spacific_id, person_id, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}`, params)
export const postLagnaSpecificsPersons = (committe_code, spacific_id, params) =>
  http.post(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/add/`, params)
export const deleteLagnaSpecificsPersons = (committe_code, spacific_id, person_id) =>
  http.delete(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/delete/`)

// ----------------------------- decicion --------------------------
export const getLagnaSpecificsPersonsDecision = (committe_code, spacific_id, person_id, params) =>
  http.get(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/decision`,
    params,
  )
export const postLagnaSpecificsPersonsDecision = (committe_code, spacific_id, person_id, params) =>
  http.post(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/decision/add`,
    params,
  )
export const deleteLagnaSpecificsPersonsDecision = (
  committe_code,
  spacific_id,
  person_id,
  params,
) =>
  http.delete(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/decision/delete`,
    params,
  )

// --------------------------- show --------------------------------

export const getLagnaSpecificsPersonShow = (committe_code, spacific_id, person_id, params) =>
  http.get(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/show/`,
    params,
  )
export const getLagnaSpecificsPersonPopupShow = (committe_code, specific_code, params) =>
  http.post(`lagna/${committe_code}/event/`, params)
export const postLagnaSpecificsPersonStutus = (committe_code, spacific_id, person_id, params) =>
  http.post(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/status/`,
    params,
  )

// ---------------------------- ready -------------------------------
export const getLagnaSpecificsPersonsReady = (committe_code, spacific_id, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/ready`, params)

// --------------- get lagna category && types --------------
export const getLagnaCategory = () => http.get('lagna/get-lagna-category/') // get langas category
export const getLagnaType = () => http.get('lagna/get-lagna-type/') // get langas types

export const getLagnaMembersUsers = () => http.get(`lagna-member/member-user/`)
export const getLagnaMembersTypes = () => http.get(`lagna-member/member-type/`)

// ------------------------------ snap =-------------------------------
export const getLagnaSpecificsPersonSnap = (committe_code, spacific_id, person_id, params) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/snap`)
export const postLagnaSpecificsPersonSnap = (committe_code, spacific_id, person_id, params) =>
  http.post(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/snap/`,
    params,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    },
  )

// ------------------------------ psychologic ---------------------------------
export const getPsychologicPerson = (mil_sir) => http.get(`persons/${mil_sir}/psychologic`)
export const postPsychologicPerson = (mil_sir, params) =>
  http.post(`persons/${mil_sir}/psychologic/add/`, params)

// ------------------- reports ------------------------
export const getPrntArmyUnitsReportDetails = (prnt_army_code, params) =>
  http.get(`/photo/report/${prnt_army_code}/units`, params)
export const getPrntArmyUnitsPersonsReportDetails = (prnt_army_code, unit_code, params = {}) => {
  const queryParams = {
    ...params,
  }
  return http.get(`/photo/report/${prnt_army_code}/units/${unit_code}/persons`, {
    params: queryParams,
  })
}
export const getPrntArmyPersonsReportDetails = (prnt_army_code, params = {}) => {
  const queryParams = {
    ...params,
  }
  return http.get(`/photo/report/${prnt_army_code}/persons`, { params: queryParams })
}

export const getCommitiReportData = (params = {}) => {
  return http.get(`/report/lagna/`, { params: params })
}

export const persons = {
  getMainLagnas,

  getLagnas,
  getMemberLagnas,
  postLagnas,
  getLagnaByid,
  editLagnaByid,
  deleteLagnaByid,

  getLagnaCategory,
  getLagnaType,

  getLagnaSpecifics,
  getOneLagnaSpecific,
  addLagnaSpecifics,
  updateLagnaSpecifics,
  deleteLagnaSpecifics,

  getLagnaSpecificsMembers,
  postLagnaSpecificsMembers,
  deleteLagnaSpecificsMembers,

  getLagnaSpecificsPersons,
  postLagnaSpecificsPersons,
  deleteLagnaSpecificsPersons,

  getLagnaSpecificsPersonsDecision,
  postLagnaSpecificsPersonsDecision,
  deleteLagnaSpecificsPersonsDecision,

  getLagnaSpecificsPersonShow,
  getLagnaSpecificsPersonPopupShow,
  postLagnaSpecificsPersonStutus,

  getLagnaSpecificsPersonsReady,

  getPrntArmyUnitsReportDetails,
  getPrntArmyUnitsPersonsReportDetails,
  getPrntArmyPersonsReportDetails,

  getCommitiReportData,
}
