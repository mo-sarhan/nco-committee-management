<template>
  <div class="table-responsiv">
    <table class="base-table">
      <thead :class="{ stiky_table_head: stikyHeader }">
        <tr v-for="(row, rIndex) in headerRows" :key="rIndex">
          <th v-if="selectable"></th>

          <th
            v-for="col in row"
            :key="col.key || col.label"
            :class="{ sortable: col.sortable }"
            @click="col.sortable && emitSort(col.key)"
            :rowspan="col.hRowspan"
            :colspan="col.hColspan"
          >
            {{ col.label }}
            <span v-if="col.sortable" class="sort-icon">
              {{ sortIcon(col.key) }}
            </span>
          </th>

          <th v-if="$slots.actions" style="text-align: center">الإجراءات</th>
        </tr>
      </thead>

      <!-- BODY -->
      <tbody>
        <tr
          v-for="(row, index) in rows"
          :key="row[idKey] ?? index"
          class="clickable-row"
          :class="{ total: isTotalRow(index) }"
        >
          <!-- SELECT -->
          <td v-if="selectable">
            <input
              :type="multiSelect ? 'checkbox' : 'radio'"
              :name="row.mil_ser"
              @change="toggleRow(row)"
            />
          </td>

          <td
            v-for="col in leafColumns"
            :key="col.key"
            :colspan="col.colColspan ? col.colColspan(row, index, isTotalRow(index)) : 1"
            :rowspan="col.colRowspan ? col.colRowspan(row, index, isTotalRow(index)) : 1"
            :class="{
              rowClickable: col.rowClickable,
              clickable: col.onClick,
              hide: col.hide ? col.hide(row, index, isTotalRow(index)) : false,
              markRow: col.mark ? col.mark(row, index, isTotalRow(index)) : false,
            }"
            @click="handleCellClick(row, col)"
            :style="col.style"
            class="copyable-cell"
          >
            <!-- @click="col.onClick && col.onClick(row)" -->
            <!-- {{ col.value(row, index, isTotalRow(index)) }} -->

            <template v-if="col.render">
              <component :is="col.render(row, index, isTotalRow(index))" />
            </template>

            <template v-else>
              {{ col.value(row, index, isTotalRow(index)) }}
            </template>
          </td>
          <td v-if="$slots.actions" @click.stop>
            <slot name="actions" :row="row" />
          </td>
        </tr>

        <tr v-if="!rows || rows.length === 0">
          <td :colspan="leafColumns.length" class="empty-row">لا توجد بيانات</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  rows: Array,
  columns: Array,
  sortBy: String,
  sortDir: String,
  idKey: { type: String, default: 'id' },

  selectable: Boolean,
  stikyHeader: Boolean,
  totalRows: Boolean,
  multiSelect: Boolean,
  selectedRows: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['sort', 'rowClick', 'update:selectedRows'])

function emitSort(key) {
  emit('sort', key)
}

function sortIcon(column) {
  if (props.sortBy !== column) return '↕'
  return props.sortDir === 'asc' ? '↑' : '↓'
}

function isSelected(row) {
  return props.selectedRows.some((r) => r[props.idKey] === row[props.idKey])
}

/* ---------- HEADER BUILDING ---------- */

const headerRows = computed(() => {
  const rows = [[], [], []]

  function walk(cols, level = 0) {
    cols.forEach((col) => {
      const hasChildren = col.children?.length

      rows[level].push({
        ...col,
        colspan: hasChildren ? col.children.length : 1,
        rowspan: hasChildren ? 1 : 3 - level,
      })

      if (hasChildren) {
        walk(col.children, level + 1)
      }
    })
  }

  walk(props.columns)
  return rows.filter((r) => r.length)
})

const leafColumns = computed(() => {
  const leaves = []

  function walk(cols) {
    cols.forEach((col) => {
      if (col.children?.length) {
        walk(col.children)
      } else {
        leaves.push(col)
      }
    })
  }

  walk(props.columns)
  return leaves
})

function isTotalRow(index) {
  return index + 1 === props.rows.length && props.totalRows
}
function toggleRow(row) {
  let selected = [...props.selectedRows]

  if (props.multiSelect) {
    if (isSelected(row)) {
      selected = selected.filter((r) => r[props.idKey] !== row[props.idKey])
    } else {
      selected.push(row)
    }
  } else {
    selected = [row]
  }

  emit('update:selectedRows', selected)
}

function handleCellClick(row, col) {
  console.log('col', col)
  if (col.onClick) {
    console.log('onClick')
    col.onClick(row)
  }
  if (!col.copyable && !col.notRowClick) {
    console.log('copyable')
    emit('rowClick', row)
    return
  }

  // navigator.clipboard.writeText(String(col.value(row)))
}
</script>

<style scoped>
.base-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}
.base-table th,
.base-table td {
  padding: 15px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
}
.base-table th {
  background: #f7f9fc;
  font-weight: 500;
}

tbody tr td.markRow {
  background: #d19e39;
}
/* tbody tr td.markRow:nth-child() {
  border-radius: 20px;
} */
tbody tr.total {
  background: #ce9d53;
  font-weight: bold;
  color: #f0f0f0;
}
.clickable {
  cursor: pointer;
  /* color: #0047ab; */
}
.container .hide {
  display: none !important;
}
.sortable {
  cursor: pointer;
}
.rowClickable {
  cursor: pointer;
}
.sort-icon {
  margin-right: 6px;
  font-size: 13px;
  opacity: 0.6;
}
.clickable-row:hover {
  background: #f5f7fa;
}
tbody tr.total:hover {
  background: #ce9d53;
  color: white;
}
.empty-row {
  text-align: center;
  color: #999;
}
.copyable-cell {
  user-select: text !important;
  cursor: text;
}
/* .copyable-cell:hover::after {
  content: 'اضغط للنسخ';
  position: absolute;
  font-size: 11px;
  opacity: 0.6;
} */

/* .clickable:hover {
  text-decoration: underline;
} */

.base-table th,
.base-table td {
  padding: 7px 10px;
  border-bottom: 1px solid #e0e0e0;
  text-align: center;
  /* vertical-align: middle; */
  /* word-break: break-word; */
}

.base-table th {
  background-color: #f3f4f6;
  color: #1f2937;
  font-weight: 600;
  /* position: sticky; */
  top: 0;
  z-index: 2;
}

.base-table th.sortable {
  cursor: pointer;
}

.base-table th.sortable:hover {
  background-color: #e5e7eb;
}

.base-table td {
  background-color: #ffffff;
  color: #000000;
  font-size: 0.9rem;
}

tbody tr:nth-child(even) td.clickable {
  background-color: #f9fafb;
}

tbody tr:hover td.clickable {
  background-color: #eef2f7;
}

tbody tr.total {
  background-color: #f59e0b;
  color: #ffffff;
  font-weight: bold;
}

tbody tr.total:hover td {
  background-color: #d97706;
  color: #ffffff;
}

.copyable-cell {
  user-select: text !important;
  cursor: text;
}

.rowClickable {
  cursor: pointer;
}

.clickable {
  cursor: pointer;
  color: #1d4ed8;
  font-weight: 500;
}

/* .clickable:hover {
  text-decoration: underline;
} */

.sort-icon {
  margin-left: 4px;
  font-size: 0.75rem;
  opacity: 0.7;
}

.empty-row {
  text-align: center;
  color: #9ca3af;
  font-style: italic;
}

/* Responsive scroll for small screens */
.table-responsiv {
  /* overflow-x: auto; */
  -webkit-overflow-scrolling: touch;
}

/* Sticky first column (index) if needed */
.base-table td:first-child,
.base-table th:first-child {
  /* position: sticky; */
  left: 0;
  background-color: #f7f7f7;
  z-index: 1;
  box-shadow: 2px 0 5px -2px rgba(0, 0, 0, 0.1);
}

/* Hover shadow effect for rows */
tbody tr {
  transition:
    background-color 0.2s,
    transform 0.15s;
}

tbody tr:hover {
  transform: translateY(-1px);
}

/* Rounded table */
.base-table {
  border-radius: 8px;
  /* overflow: hidden; */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}
.stiky_table_head {
  position: sticky;
  top: 0;
  z-index: 1;
}
</style>
