import http from '../http';

export const getPersons = (params ) => http.get('persons/',params);
export const getUnits = () => http.get('units/');
export const getImagesReport = () => http.get('get_images_report/');
export const getPersonDetails = (mil_ser, op) => http.get(`person/${mil_ser}/?op=${op}`);
export const getPersonInfo = (mil_ser) => http.get(`persons/${mil_ser}/`);
export const getLaganPersonInfo = (mil_ser) => http.get(`persons/${mil_ser}/?prnt_army=true`);
export const fetchBasicPersonInfo = (mil_ser) => http.get(`persons/${mil_ser}/?basic=1`);
export const postAttendance = (mil_ser, payload) => http.post(`attend_person/${mil_ser}/`, payload);
export const checkPhotoReview = (mil_ser,photo_id,payload) => http.post(`persons/${mil_ser}/photos/${photo_id}/check/`, payload);
export const getVote = (mil_ser,vote_type,final_decision) => http.get(`vote/${mil_ser}/?vote_type=${vote_type}&final_decision=${final_decision}`);
export const getLagnaStatistics = (lagna_date) => http.get(`get_lagna_statistics/?lagna_date=${lagna_date}`);

// -------------------------- reports --------------------------

export const getUploadedImagesReport = (params ) => http.get('report/',params);
export const getReviewedImagesReport = (params ) => http.get('report/',params);


// ----------------------------- opinions --------------------------

export const persons = {
    getPersons,
    getImagesReport,
    getPersonDetails,
    getPersonInfo,
    getLaganPersonInfo,
    fetchBasicPersonInfo,
    postAttendance,
    getVote,
    getLagnaStatistics,
    checkPhotoReview,
    // ------------------ reports ----------------
    getUploadedImagesReport,
    getReviewedImagesReport,

};
