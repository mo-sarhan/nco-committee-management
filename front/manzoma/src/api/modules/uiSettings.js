import http from '../http'

// the shared client defaults to multipart (file uploads). These endpoints carry
// plain scalars including nulls and booleans, which multipart would flatten to
// strings, so they are sent as JSON instead. The reorder endpoints need it
// outright: they take a JSON array, which multipart cannot express.
const json = { headers: { 'Content-Type': 'application/json' } }

// ----------------- page config (runtime) ------------------
export const getPageConfig = (page_key) => http.get(`ui-settings/pages/${page_key}/`)

// ----------------- sections ------------------
export const getSections = (page_key) => http.get(`ui-settings/sections/?page_key=${page_key}`)
export const createSection = (params) => http.post(`ui-settings/sections/`, params, json)
export const updateSection = (section_id, params) =>
  http.patch(`ui-settings/sections/${section_id}/`, params, json)
export const deleteSection = (section_id) => http.delete(`ui-settings/sections/${section_id}/`)
export const reorderSections = (params) => http.post(`ui-settings/sections/reorder/`, params, json)

// ----------------- fields ------------------
export const getFields = (section_id) => http.get(`ui-settings/fields/?section=${section_id}`)
export const createField = (params) => http.post(`ui-settings/fields/`, params, json)
export const updateField = (field_id, params) =>
  http.patch(`ui-settings/fields/${field_id}/`, params, json)
export const deleteField = (field_id) => http.delete(`ui-settings/fields/${field_id}/`)
export const reorderFields = (params) => http.post(`ui-settings/fields/reorder/`, params, json)

export const uiSettings = {
  getPageConfig,

  getSections,
  createSection,
  updateSection,
  deleteSection,
  reorderSections,

  getFields,
  createField,
  updateField,
  deleteField,
  reorderFields,
}
