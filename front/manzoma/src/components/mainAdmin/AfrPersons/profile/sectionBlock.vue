<template>
  <secSpliter :splitTitle="resolvedTitle" :splitTitleStyle="titleStyle" @expand="$emit('sectionOpen')" />

  <div
    class="sec-data"
    :class="{ withoutResponsiveGrid: withoutGrid }"
    :style="{ ...gridStyle, ...boxStyle }"
    v-if="sectionExpand"
  >
    <div
      v-for="(field, i) in resolvedFields"
      :key="field.key || i"
      class="section-field-wrapper"
      :style="field.colSpan ? { gridColumn: `span ${field.colSpan}` } : null"
    >
      <fieldShow
        :fieldShowLabel="field.label"
        :fieldShowData="field.value"
        :fieldShowLabelStyle="field.fieldShowLabelStyle"
        :fieldShowDataStyle="field.fieldShowDataStyle"
        :fieldShowStyle="field.fieldShowStyle"
        :fieldShowClickable="!!field.click"
        @click="field.click && field.click()"
      />

      <!-- OPTIONAL EXTRA DATA -->
      <div v-if="field.subValue" class="field-sub">
        {{ field.subValue }}
      </div>

      <div v-if="field.meta" class="field-meta">
        {{ field.meta }}
      </div>

      <div v-if="field.date" class="field-date">
        {{ field.date }}
      </div>
    </div>
    <slot name="additionFields"></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import secSpliter from '@/components/mainAdmin/AfrPersons/profile/secSpliter.vue'
import fieldShow from '@/components/mainAdmin/AfrPersons/profile/fieldShow.vue'
import { useUiSettingsStore } from '@/stores/uiSettings'
import {
  applyFieldConfig,
  toBoxStyle,
  toGridStyle,
  toTitleStyle,
} from '@/utils/uiSettings'

const props = defineProps({
  title: { type: String, required: true },
  sectionExpand: {
    type: Boolean,
    default: true,
  },
  withoutGrid: {
    type: Boolean,
    default: false,
  },
  fields: {
    type: Array,
    default: () => [],
  },
  // keys used to look the block up in the settings screen; when they are not
  // given the block renders exactly as it did before the settings existed
  pageKey: {
    type: String,
    default: '',
  },
  sectionKey: {
    type: String,
    default: '',
  },
})
defineEmits(['sectionOpen'])

const uiSettings = useUiSettingsStore()

const config = computed(() =>
  props.pageKey && props.sectionKey ? uiSettings.sectionOf(props.pageKey, props.sectionKey) : null,
)

const resolvedTitle = computed(() => config.value?.title || props.title)
const resolvedFields = computed(() =>
  applyFieldConfig(props.fields, config.value?.fields || []),
)

const boxStyle = computed(() => {
  const style = toBoxStyle(config.value)
  // a bare grid with a border/background looks cramped, give it some room
  if (style.border || style.background) style.padding = '12px'
  return style
})
const gridStyle = computed(() => toGridStyle(config.value))
const titleStyle = computed(() => toTitleStyle(config.value))
</script>

<style scoped>
.section {
  background: #fff;
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 16px;
}

.section-title {
  font-weight: 700;
  margin-bottom: 12px;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.field {
  padding: 10px;
  border-radius: 8px;
  background: #f6f7f9;
}

.field.clickable {
  cursor: pointer;
  transition: 0.2s;
}
.field.clickable:hover {
  background: #e9eef5;
}

.field.danger {
  background: #ffecec;
}

.label {
  font-size: 13px;
  color: #666;
}

.value {
  font-weight: 600;
}

.sec-data {
  display: grid;
  flex-wrap: wrap;
  align-items: center;
  gap: 19px;
  margin: 10px 0;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}
.withoutResponsiveGrid {
  display: grid;
  flex-wrap: wrap;
  align-items: center;
  gap: 19px;
  margin: 10px 0;
  grid-template-columns: repeat(5, minmax(320px, 1fr));
}
.section-field-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-sub {
  font-size: 13px;
  color: #444;
  padding: 4px 6px;
}

.field-meta {
  font-size: 12px;
  color: #666;
}

.field-date {
  font-size: 11px;
  color: #888;
}
</style>
