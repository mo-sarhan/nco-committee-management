import http from '../http'

export const getAllArmyRanks = () => http.get('rank/')
export const getAllArmyNames = (params) => http.get('army/', params)
export const getAllImageRejectionReasons = () => http.get('rejection-reasons/')
export const getAllPonsCons = () => http.get('pons-cons/')
export const getCommanderJobs = () => http.get(`commander-job/`) // get comander's job
export const getLagnaSpecificsPersonStutus = (params) => http.get(`lagna/person-status/`, params)
export const glopal = {
  getAllArmyRanks,
  getAllArmyNames,
  getAllImageRejectionReasons,
  getAllPonsCons,
  getCommanderJobs,
  getLagnaSpecificsPersonStutus,
}
