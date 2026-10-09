// src/api/modules/auth.js
import http, { cancelRequest } from '../http';

export const authApi = {
  login: (credentials) => http.post('/login/', credentials),
  // register: (data) => http.post('/register', data),
  logout: () => http.post('/logout'),
  getProfile: () => http.get('/me'),

  // Example with cancellation
  getProfileCancelable: () => {
    const requestConfig = {};
    const promise = http.get('/me', requestConfig);
    return { promise, cancel: () => cancelRequest(requestConfig) };
  },
};
