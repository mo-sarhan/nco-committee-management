import http from '../http';

export const getSpecificsPersonReasons = (committe_code,spacific_id,person_id) => http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/reasons/`);
export const postSpecificsPersonReasons = (committe_code,spacific_id,person_id,params) => http.post(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/reasons/add/`,params);
export const deleteSpecificsPersonReasons = (committe_code,spacific_id,person_id,reason_id,params) => http.delete(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/reasons/${reason_id}/delete/`,params);

// ----------------- سبب العرض (one free text stored on the snap) ------------------
export const getSpecificsPersonAddReason = (committe_code,spacific_id,person_id) => http.get(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/add-reason/`);
export const patchSpecificsPersonAddReason = (committe_code,spacific_id,person_id,params) => http.patch(`lagna/${committe_code}/lagna-spacific/${spacific_id}/persons/${person_id}/add-reason/`,params,{ headers: { 'Content-Type': 'application/json' } });

export const reasons = {
    // ----------------- Reason ------------------
    getSpecificsPersonReasons,
    postSpecificsPersonReasons,
    deleteSpecificsPersonReasons,

    // ----------------- سبب العرض ------------------
    getSpecificsPersonAddReason,
    patchSpecificsPersonAddReason,
};