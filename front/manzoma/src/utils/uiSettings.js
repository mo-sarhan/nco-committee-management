/**
 * Turns a UI settings row (section or field) into a plain style object that can
 * be bound with :style. Every value is optional - anything the admin did not
 * set stays untouched so the original CSS keeps winning.
 */

const has = (v) => v !== null && v !== undefined && v !== ''

/** border / background / text of a box (section container or field card) */
export function toBoxStyle(cfg) {
  const style = {}
  if (!cfg) return style

  if (has(cfg.background_color)) style.background = cfg.background_color
  if (has(cfg.text_color)) style.color = cfg.text_color

  if (has(cfg.border_color) || has(cfg.border_width)) {
    const width = has(cfg.border_width) ? cfg.border_width : 1
    const type = has(cfg.border_style) ? cfg.border_style : 'solid'
    const color = has(cfg.border_color) ? cfg.border_color : '#dddddd'
    style.border = `${width}px ${type} ${color}`
  }
  if (has(cfg.border_radius)) style.borderRadius = `${cfg.border_radius}px`
  if (has(cfg.font_size)) style.fontSize = `${cfg.font_size}px`
  if (has(cfg.font_weight)) style.fontWeight = cfg.font_weight

  return style
}

/** the label half of a field card */
export function toLabelStyle(cfg) {
  const style = {}
  if (!cfg) return style
  if (has(cfg.label_background)) style.backgroundColor = cfg.label_background
  if (has(cfg.label_color)) style.color = cfg.label_color
  return style
}

/** the value half of a field card */
export function toValueStyle(cfg) {
  const style = {}
  if (!cfg) return style
  if (has(cfg.value_background)) style.backgroundColor = cfg.value_background
  if (has(cfg.value_color)) style.color = cfg.value_color
  return style
}

/** grid of a section */
export function toGridStyle(cfg) {
  const style = {}
  if (!cfg) return style

  if (has(cfg.columns_count)) {
    style.gridTemplateColumns = `repeat(${cfg.columns_count}, minmax(0, 1fr))`
  } else if (has(cfg.min_column_width)) {
    style.gridTemplateColumns = `repeat(auto-fit, minmax(${cfg.min_column_width}px, 1fr))`
  }
  if (has(cfg.gap_size)) style.gap = `${cfg.gap_size}px`

  return style
}

/** header (spliter) of a section */
export function toTitleStyle(cfg) {
  const style = {}
  if (!cfg) return style
  if (has(cfg.title_background)) style.backgroundColor = cfg.title_background
  if (has(cfg.title_color)) style.color = cfg.title_color
  return style
}

/**
 * Applies the saved order / visibility / label to the field list a page builds.
 * Fields the admin never registered keep their place at the end of the list.
 */
export function applyFieldConfig(fields, fieldConfigs) {
  if (!fieldConfigs || !fieldConfigs.length) return fields

  const byKey = new Map(fieldConfigs.map((c) => [c.field_key, c]))
  // screens that show the same block without carrying a key are matched on the
  // wording the code uses, so one setting drives all of them
  const byLabel = new Map(
    fieldConfigs.filter((c) => c.default_label).map((c) => [c.default_label, c]),
  )

  return fields
    .map((field, index) => {
      const cfg = (field.key && byKey.get(field.key)) || byLabel.get(field.label) || null
      return { field, cfg, index }
    })
    .filter(({ cfg }) => !cfg || cfg.visible_flag)
    .sort((a, b) => {
      const aOrder = a.cfg ? a.cfg.display_order : 1000 + a.index
      const bOrder = b.cfg ? b.cfg.display_order : 1000 + b.index
      return aOrder - bOrder || a.index - b.index
    })
    .map(({ field, cfg }) => {
      if (!cfg) return field

      // the page can still force a style per row; it wins over the settings.
      // an empty result stays undefined - fieldShow uses the absence of a label
      // style to decide whether a clickable field gets the orange button look.
      const merge = (fromCfg, fromPage) => {
        const merged = { ...fromCfg, ...(fromPage || {}) }
        return Object.keys(merged).length ? merged : undefined
      }

      return {
        ...field,
        label: cfg.label || field.label,
        colSpan: cfg.col_span,
        fieldShowStyle: merge(toBoxStyle(cfg), field.fieldShowStyle),
        fieldShowLabelStyle: merge(toLabelStyle(cfg), field.fieldShowLabelStyle),
        fieldShowDataStyle: merge(toValueStyle(cfg), field.fieldShowDataStyle),
      }
    })
}
