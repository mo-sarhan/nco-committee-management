import { useUiSettingsStore } from '@/stores/uiSettings'

/**
 * Wires a page to the layout saved from the settings screen.
 *
 *   const { pageKey, sectionOrder, isSectionVisible, loadUiSettings } =
 *     useUiSettingsPage('afr_person_profile')
 *
 * The section blocks that share the same wording share the same page key, so
 * one saved layout drives the profile, the committee profile and the
 * presentation screen at once.
 */
export function useUiSettingsPage(pageKey, splitterMap = {}) {
  const store = useUiSettingsStore()

  const sectionOrder = (sectionKey) => store.sectionOrder(pageKey, sectionKey)
  const isSectionVisible = (sectionKey) => store.isSectionVisible(pageKey, sectionKey)

  /**
   * loads the layout and, when a splitter map is given, seeds the expand state
   * ({ section_key: 'nameOfTheSplitterFlag' })
   */
  async function loadUiSettings(splitter) {
    const sections = await store.loadPage(pageKey)

    if (splitter) {
      sections.forEach((section) => {
        const flag = splitterMap[section.section_key]
        if (flag && flag in splitter) splitter[flag] = section.expanded_flag
      })
    }
    return sections
  }

  return { pageKey, sectionOrder, isSectionVisible, loadUiSettings }
}

/** the profile layout, shared by the profile and the committee profile screens */
export const PROFILE_PAGE_KEY = 'afr_person_profile'

export const PROFILE_SPLITTERS = {
  basic: 'primDataSpliter',
  punishment: 'punnDataSpliter',
  medical: 'medicalDataSpliter',
  custom_vacation: 'customVacationDataSpliter',
  travel: 'travelDataSpliter',
  family: 'famillyDataSpliter',
}

/**
 * The presentation screen has its own layout: it is a projector view with a
 * five column grid, a different field order, and two fields the profile does
 * not show (تبعية الوحدة, الموقف الامني). Keeping it on its own key lets it be
 * styled without dragging the profile screens along.
 */
export const PRESENTING_PAGE_KEY = 'lagna_presenting'

export const PRESENTING_SPLITTERS = {
  basic: 'primDataSpliter',
  punishment: 'punnDataSpliter',
  medical: 'medicalDataSpliter',
  custom_vacation: 'customVacationDataSpliter',
  travel: 'travelDataSpliter',
  presenting_reason: 'presentingReasonSpliter',
  reasons: 'reasonDataSpliter',
  family: 'famillyDataSpliter',
  lagna_decisions: 'priviousDecisionsDataSpliter',
}
