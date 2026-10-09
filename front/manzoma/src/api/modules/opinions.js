import http from '../http'

export const getLagnaOpinionTypes = (person_id) => http.get(`opinion-types/?person_id=${person_id}`)

export const getSpecificsPersonOpinions = (committe_code, spacific_id, person_id) =>
  http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/opinions/`)
export const postSpecificsPersonOpinions = (committe_code, spacific_id, person_id, params) =>
  http.post(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/opinions/add/`,
    params,
  )
export const deleteSpecificsPersonOpinions = (
  committe_code,
  spacific_id,
  person_id,
  opinion_id,
  params,
) =>
  http.delete(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/opinions/${opinion_id}/delete/`,
    params,
  )

export const postPersonFinalDecision = (committe_code, spacific_id, person_id, params) =>
  http.post(
    `lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/votes/add/`,
    params,
  )
export const opinions = {
  // ----------------- opinion ------------------
  getSpecificsPersonOpinions,
  postSpecificsPersonOpinions,
  deleteSpecificsPersonOpinions,

  postPersonFinalDecision,

  getLagnaOpinionTypes,
}
