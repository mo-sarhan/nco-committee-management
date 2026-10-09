import { defineStore } from 'pinia'
import { uiSettings as api } from '@/api/modules/uiSettings'
import { handleApiError } from '@/utils/handleApiError'

/**
 * Holds the layout the admin saved for each page.
 * Pages read it through the getters, the settings screen writes it.
 */
export const useUiSettingsStore = defineStore('uiSettings', {
  state: () => ({
    // { [page_key]: [section, ...] }
    pages: {},
    loading: false,
    saving: false,
    error: null,
  }),

  getters: {
    /** every section of a page, already ordered by the backend */
    sectionsOf: (state) => (pageKey) => state.pages[pageKey] || [],

    /** one section config, or null when the admin never registered it */
    sectionOf: (state) => (pageKey, sectionKey) =>
      (state.pages[pageKey] || []).find((s) => s.section_key === sectionKey) || null,

    /** the field rows of one section */
    fieldsOf() {
      return (pageKey, sectionKey) => {
        const section = this.sectionOf(pageKey, sectionKey)
        return section ? section.fields || [] : []
      }
    },

    /** css order value, so a page can reorder its blocks without restructuring */
    sectionOrder() {
      return (pageKey, sectionKey) => {
        const section = this.sectionOf(pageKey, sectionKey)
        return section ? section.display_order : 0
      }
    },

    isSectionVisible() {
      return (pageKey, sectionKey) => {
        const section = this.sectionOf(pageKey, sectionKey)
        return section ? section.visible_flag : true
      }
    },
  },

  actions: {
    async loadPage(pageKey, { force = false } = {}) {
      if (!force && this.pages[pageKey]) return this.pages[pageKey]

      this.loading = true
      this.error = null
      try {
        const res = await api.getPageConfig(pageKey)
        this.pages[pageKey] = res.data.sections || []
        return this.pages[pageKey]
      } catch (error) {
        // a missing layout must never break the page it decorates
        this.error = error
        this.pages[pageKey] = this.pages[pageKey] || []
        return this.pages[pageKey]
      } finally {
        this.loading = false
      }
    },

    async saveSection(section) {
      this.saving = true
      try {
        const res = await api.updateSection(section.section_id, section)
        this.mergeSection(res.data)
        return res.data
      } catch (error) {
        handleApiError(error)
        throw error
      } finally {
        this.saving = false
      }
    },

    async saveField(field) {
      this.saving = true
      try {
        const res = await api.updateField(field.field_id, field)
        this.mergeField(res.data)
        return res.data
      } catch (error) {
        handleApiError(error)
        throw error
      } finally {
        this.saving = false
      }
    },

    async saveSectionOrder(pageKey, sections) {
      this.saving = true
      try {
        await api.reorderSections(
          sections.map((s, i) => ({ id: s.section_id, display_order: i })),
        )
        await this.loadPage(pageKey, { force: true })
      } catch (error) {
        handleApiError(error)
        throw error
      } finally {
        this.saving = false
      }
    },

    async saveFieldOrder(pageKey, fields) {
      this.saving = true
      try {
        await api.reorderFields(fields.map((f, i) => ({ id: f.field_id, display_order: i })))
        await this.loadPage(pageKey, { force: true })
      } catch (error) {
        handleApiError(error)
        throw error
      } finally {
        this.saving = false
      }
    },

    mergeSection(section) {
      const list = this.pages[section.page_key]
      if (!list) return
      const index = list.findIndex((s) => s.section_id === section.section_id)
      if (index === -1) return
      // the detail response carries no nested fields on PATCH, keep the old ones
      list[index] = { ...list[index], ...section, fields: section.fields || list[index].fields }
    },

    mergeField(field) {
      for (const list of Object.values(this.pages)) {
        for (const section of list) {
          const index = (section.fields || []).findIndex((f) => f.field_id === field.field_id)
          if (index !== -1) {
            section.fields[index] = { ...section.fields[index], ...field }
            return
          }
        }
      }
    },
  },
})
