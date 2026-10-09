import http from '../http';

export const getPersonImagesTypes = () => http.get('photo/');
export const postPersonImages = (payload,config={}) => http.post('photo/', payload,config);

export const persons = {
    getPersonImagesTypes,
    postPersonImages,
};
