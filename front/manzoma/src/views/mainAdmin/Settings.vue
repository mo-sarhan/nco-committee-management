<template>
  <div class="ui-settings rtl-container">
    <!-- ================= HEADER ================= -->
    <div class="panel-head">
      <div>
        <h3>إعدادات شكل الصفحات</h3>
        <p class="hint">
          تحكم في ترتيب الأقسام والحقول وألوان الخلفية والإطار والعناوين، ثم اضغط حفظ.
        </p>
      </div>

      <div class="head-actions">
        <select v-model="pageKey" class="form-select page-select" @change="reload">
          <option v-for="page in PAGES" :key="page.key" :value="page.key">{{ page.label }}</option>
        </select>

        <button class="btn btn-outline-secondary" :disabled="busy" @click="reload">
          <i class="fa-solid fa-rotate-right"></i>
          تحديث
        </button>
        <button class="btn btn-primary" :disabled="busy || !dirtyCount" @click="saveAll">
          <i class="fa-solid fa-floppy-disk"></i>
          حفظ ({{ dirtyCount }})
        </button>
      </div>
    </div>

    <!-- ================= STATES ================= -->
    <div v-if="loading" class="state-box">... جاري التحميل</div>

    <div v-else-if="!sections.length" class="state-box">
      لا توجد أقسام مسجلة لهذه الصفحة.
      <div class="hint">
        شغل الأمر التالي على السيرفر مرة واحدة: <code>python manage.py seed_ui_settings</code>
      </div>
    </div>

    <!-- ================= SECTIONS ================= -->
    <div v-else class="sections">
      <div
        v-for="(section, sIndex) in sections"
        :key="section.section_id"
        class="section-card"
        :class="{ hidden: !section.visible_flag }"
      >
        <!-- ---------- section head ---------- -->
        <div class="section-head">
          <div class="order-btns">
            <button class="mini" :disabled="sIndex === 0" @click="moveSection(sIndex, -1)">
              <i class="fa-solid fa-chevron-up"></i>
            </button>
            <span class="order-no">{{ sIndex + 1 }}</span>
            <button
              class="mini"
              :disabled="sIndex === sections.length - 1"
              @click="moveSection(sIndex, 1)"
            >
              <i class="fa-solid fa-chevron-down"></i>
            </button>
          </div>

          <!-- left empty the screen picks the name itself (it may vary per committee) -->
          <input
            v-model="section.title"
            class="form-control title-input"
            :placeholder="section.section_key"
          />

          <label class="switch">
            <input type="checkbox" v-model="section.visible_flag" />
            <span>ظاهر</span>
          </label>

          <label class="switch">
            <input type="checkbox" v-model="section.expanded_flag" />
            <span>مفتوح</span>
          </label>

          <button class="btn btn-sm btn-outline-secondary" @click="toggleOpen(section.section_id)">
            {{ opened === section.section_id ? 'إخفاء الحقول' : 'الحقول (' + fieldsOf(section).length + ')' }}
          </button>

          <span v-if="isDirty(section)" class="dirty-dot" title="غير محفوظ"></span>
        </div>

        <!-- ---------- section style ---------- -->
        <div class="style-row">
          <color-input v-model="section.title_background" label="خلفية العنوان" />
          <color-input v-model="section.title_color" label="لون العنوان" />
          <color-input v-model="section.background_color" label="خلفية القسم" />
          <color-input v-model="section.border_color" label="لون الإطار" />

          <num-input v-model="section.border_width" label="سمك الإطار" :max="20" />
          <num-input v-model="section.border_radius" label="استدارة" :max="60" />
          <num-input v-model="section.columns_count" label="عدد الأعمدة" :max="6" />
          <num-input v-model="section.min_column_width" label="أقل عرض للعمود" :max="900" />
          <num-input v-model="section.gap_size" label="المسافة" :max="60" />

          <select v-model="section.border_style" class="form-select mini-select">
            <option :value="null">نوع الإطار</option>
            <option value="solid">متصل</option>
            <option value="dashed">متقطع</option>
            <option value="dotted">منقط</option>
            <option value="double">مزدوج</option>
          </select>
        </div>

        <!-- ---------- fields ---------- -->
        <div v-if="opened === section.section_id" class="fields">
          <div
            v-for="(field, fIndex) in fieldsOf(section)"
            :key="field.field_id"
            class="field-row"
            :class="{ hidden: !field.visible_flag }"
          >
            <div class="order-btns">
              <button class="mini" :disabled="fIndex === 0" @click="moveField(section, fIndex, -1)">
                <i class="fa-solid fa-chevron-up"></i>
              </button>
              <span class="order-no">{{ fIndex + 1 }}</span>
              <button
                class="mini"
                :disabled="fIndex === fieldsOf(section).length - 1"
                @click="moveField(section, fIndex, 1)"
              >
                <i class="fa-solid fa-chevron-down"></i>
              </button>
            </div>

            <code class="field-key" :title="field.field_key">{{
              field.default_label || field.field_key
            }}</code>

            <input
              v-model="field.label"
              class="form-control label-input"
              :placeholder="field.default_label || field.field_key"
            />

            <label class="switch">
              <input type="checkbox" v-model="field.visible_flag" />
              <span>ظاهر</span>
            </label>

            <color-input v-model="field.label_background" label="خلفية الاسم" />
            <color-input v-model="field.label_color" label="لون الاسم" />
            <color-input v-model="field.value_background" label="خلفية القيمة" />
            <color-input v-model="field.value_color" label="لون القيمة" />
            <color-input v-model="field.border_color" label="الإطار" />
            <num-input v-model="field.border_width" label="سمك" :max="20" />
            <num-input v-model="field.border_radius" label="استدارة" :max="60" />
            <num-input v-model="field.col_span" label="اتساع" :max="6" />

            <!-- live preview of the card -->
            <div class="preview" :style="previewBox(field)">
              <span class="preview-label" :style="previewLabel(field)">
                {{ field.label || field.default_label || field.field_key }}
              </span>
              <span class="preview-value" :style="previewValue(field)">---</span>
            </div>

            <button class="mini danger" title="إرجاع الألوان الافتراضية" @click="clearStyle(field)">
              <i class="fa-solid fa-eraser"></i>
            </button>

            <span v-if="isDirty(field)" class="dirty-dot" title="غير محفوظ"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import swal from 'sweetalert'
import { uiSettings as api } from '@/api/modules/uiSettings'
import { useUiSettingsStore } from '@/stores/uiSettings'
import { toBoxStyle, toLabelStyle, toValueStyle } from '@/utils/uiSettings'

/* ================= small inline inputs ================= */
const ColorInput = {
  props: { modelValue: { type: String, default: null }, label: String },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    return () =>
      h('label', { class: 'color-input', title: props.label }, [
        h('input', {
          type: 'color',
          value: props.modelValue || '#ffffff',
          onInput: (e) => emit('update:modelValue', e.target.value),
        }),
        h('span', { class: 'color-caption' }, props.label),
        props.modelValue
          ? h(
              'button',
              {
                class: 'color-clear',
                type: 'button',
                title: 'إلغاء اللون',
                onClick: () => emit('update:modelValue', null),
              },
              '×',
            )
          : null,
      ])
  },
}

const NumInput = {
  props: { modelValue: { type: Number, default: null }, label: String, max: Number },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    return () =>
      h('label', { class: 'num-input', title: props.label }, [
        h('span', { class: 'color-caption' }, props.label),
        h('input', {
          type: 'number',
          min: 0,
          max: props.max,
          value: props.modelValue ?? '',
          onInput: (e) =>
            emit('update:modelValue', e.target.value === '' ? null : Number(e.target.value)),
        }),
      ])
  },
}

/* ================= state ================= */
const PAGES = [
  { key: 'afr_person_profile', label: 'ملف الفرد - الراتب العالي' },
  { key: 'lagna_presenting', label: 'شاشة عرض اللجنة' },
]

const store = useUiSettingsStore()
const pageKey = ref(PAGES[0].key)
const sections = ref([])
const original = ref({}) // { 'section:3': '<json>', 'field:9': '<json>' }
const opened = ref(null)
const loading = ref(false)
const busy = ref(false)

const fieldsOf = (section) => section.fields || []

/* ================= dirty tracking ================= */
const snapshotKey = (row) =>
  row.section_id !== undefined ? `section:${row.section_id}` : `field:${row.field_id}`

function takeSnapshot() {
  const snap = {}
  sections.value.forEach((section) => {
    snap[snapshotKey(section)] = JSON.stringify({ ...section, fields: undefined })
    fieldsOf(section).forEach((field) => {
      snap[snapshotKey(field)] = JSON.stringify(field)
    })
  })
  original.value = snap
}

function isDirty(row) {
  const current = JSON.stringify(
    row.section_id !== undefined ? { ...row, fields: undefined } : row,
  )
  return original.value[snapshotKey(row)] !== current
}

const dirtyCount = computed(() => {
  let count = 0
  sections.value.forEach((section) => {
    if (isDirty(section)) count += 1
    fieldsOf(section).forEach((field) => {
      if (isDirty(field)) count += 1
    })
  })
  return count
})

/* ================= load / save ================= */
async function reload() {
  loading.value = true
  opened.value = null // the expanded section belongs to the page we are leaving
  try {
    const res = await api.getSections(pageKey.value)
    sections.value = (res.data || []).map((section) => ({
      ...section,
      fields: [...(section.fields || [])].sort((a, b) => a.display_order - b.display_order),
    }))
    sections.value.sort((a, b) => a.display_order - b.display_order)
    takeSnapshot()
  } catch (error) {
    swal('خطأ', 'تعذر تحميل الإعدادات', 'error')
  } finally {
    loading.value = false
  }
}

async function saveAll() {
  busy.value = true
  try {
    for (const section of sections.value) {
      if (isDirty(section)) {
        const { fields, ...body } = section
        await api.updateSection(section.section_id, body)
      }
      for (const field of fieldsOf(section)) {
        if (isDirty(field)) await api.updateField(field.field_id, field)
      }
    }
    takeSnapshot()
    // the pages read from the store, refresh it so the change shows at once
    await store.loadPage(pageKey.value, { force: true })
    swal('تم', 'تم حفظ الإعدادات', 'success')
  } catch (error) {
    swal('خطأ', 'تعذر حفظ الإعدادات', 'error')
  } finally {
    busy.value = false
  }
}

/* ================= ordering ================= */
function reindex(list) {
  list.forEach((row, index) => {
    row.display_order = index
  })
}

function moveSection(index, step) {
  const target = index + step
  if (target < 0 || target >= sections.value.length) return
  const list = sections.value
  ;[list[index], list[target]] = [list[target], list[index]]
  reindex(list)
}

function moveField(section, index, step) {
  const list = fieldsOf(section)
  const target = index + step
  if (target < 0 || target >= list.length) return
  ;[list[index], list[target]] = [list[target], list[index]]
  reindex(list)
}

/* ================= misc ================= */
function toggleOpen(sectionId) {
  opened.value = opened.value === sectionId ? null : sectionId
}

function clearStyle(field) {
  Object.assign(field, {
    label_background: null,
    label_color: null,
    value_background: null,
    value_color: null,
    background_color: null,
    text_color: null,
    border_color: null,
    border_width: null,
    border_style: null,
    border_radius: null,
    font_size: null,
    font_weight: null,
    col_span: null,
  })
}

const previewBox = (field) => toBoxStyle(field)
const previewLabel = (field) => toLabelStyle(field)
const previewValue = (field) => toValueStyle(field)

onMounted(reload)
</script>

<style scoped>
.rtl-container {
  direction: rtl;
  text-align: right;
}

.ui-settings {
  padding: 18px;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.panel-head h3 {
  margin: 0;
  font-weight: 800;
}

.hint {
  color: #6b7280;
  font-size: 13px;
  margin: 4px 0 0;
}

.head-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-select {
  min-width: 240px;
}

.state-box {
  background: #fff;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
  padding: 28px;
  text-align: center;
  color: #6b7280;
}

/* ---------- sections ---------- */
.sections {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px 14px;
}

.section-card.hidden {
  opacity: 0.55;
}

.section-head {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.title-input {
  max-width: 260px;
  font-weight: 700;
}

.style-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #eee;
}

/* ---------- fields ---------- */
.fields {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  flex-wrap: wrap;
  background: #f9fafb;
  border: 1px solid #eef0f3;
  border-radius: 10px;
  padding: 8px 10px;
}

.field-row.hidden {
  opacity: 0.5;
}

.field-key {
  background: #eef2ff;
  color: #3730a3;
  border-radius: 6px;
  padding: 3px 6px;
  font-size: 11px;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.label-input {
  max-width: 210px;
}

/* ---------- controls ---------- */
.order-btns {
  display: flex;
  align-items: center;
  gap: 4px;
}

.order-no {
  min-width: 22px;
  text-align: center;
  font-size: 12px;
  color: #6b7280;
}

.mini {
  border: 1px solid #d1d5db;
  background: #fff;
  border-radius: 6px;
  width: 26px;
  height: 26px;
  line-height: 1;
  font-size: 12px;
  cursor: pointer;
}

.mini:disabled {
  opacity: 0.4;
  cursor: default;
}

.mini.danger {
  color: #b91c1c;
  border-color: #fecaca;
}

.mini-select {
  width: 120px;
}

.switch {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #374151;
  white-space: nowrap;
}

.dirty-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #f59e0b;
  display: inline-block;
}

/* ---------- preview ---------- */
.preview {
  display: flex;
  align-items: stretch;
  min-width: 190px;
  height: 34px;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  border: 1px solid #e5e7eb;
  font-size: 12px;
}

.preview-label {
  background: #8080804d;
  padding: 0 8px;
  display: flex;
  align-items: center;
  font-weight: 700;
  white-space: nowrap;
}

.preview-value {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<style>
/* the two inline helper components render outside scoped styles */
.color-input,
.num-input {
  display: flex;
  flex-direction: column;
  gap: 2px;
  position: relative;
  font-size: 11px;
  color: #6b7280;
}

.color-input input[type='color'] {
  width: 46px;
  height: 28px;
  padding: 0;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: none;
  cursor: pointer;
}

.num-input input {
  width: 78px;
  height: 28px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 0 6px;
  font-size: 12px;
}

.color-caption {
  white-space: nowrap;
}

.color-clear {
  position: absolute;
  top: -6px;
  inset-inline-start: -6px;
  width: 16px;
  height: 16px;
  line-height: 14px;
  border-radius: 50%;
  border: 1px solid #d1d5db;
  background: #fff;
  color: #b91c1c;
  font-size: 11px;
  padding: 0;
  cursor: pointer;
}
</style>
