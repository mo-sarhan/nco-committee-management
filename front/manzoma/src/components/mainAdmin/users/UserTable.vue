<template>
  <div class="table-responsive">
    <table class="user-table">
      <thead>
        <tr>
          <th class="sortable" @click="$emit('sort', 'name')">
            الاسم
            <span class="sort-icon">{{ icon('name') }}</span>
          </th>

          <th class="sortable" @click="$emit('sort', 'email')">
            البريد الإلكتروني
            <span class="sort-icon">{{ icon('email') }}</span>
          </th>

          <th class="sortable" @click="$emit('sort', 'phone')">
            الهاتف
            <span class="sort-icon">{{ icon('phone') }}</span>
          </th>

          <th class="sortable" @click="$emit('sort', 'status')">
            الحالة
            <span class="sort-icon">{{ icon('status') }}</span>
          </th>

          <th style="text-align: left">الإجراءات</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.phone }}</td>

          <td>
            <span
              :class="[
                'status-badge',
                user.status === 'نشط' ? 'status-active' : 'status-inactive',
              ]"
            >
              {{ user.status }}
            </span>
          </td>

          <td style="text-align: left">
            <div class="action-btns">
              <button @click="$emit('editUser', user)" class="action-btn edit">
                <i class="fa-solid fa-pencil"></i>
              </button>

              <button @click="$emit('deleteUser', user.id)" class="action-btn delete">
                <i class="fa-regular fa-trash-can"></i>
              </button>
            </div>
          </td>
        </tr>

        <tr v-if="users.length === 0">
          <td colspan="5" class="empty-row">لا توجد بيانات مطابقة.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  users: { type: Array, required: true },
  sortBy: { type: String, required: true },
  sortDir: { type: String, required: true },
})

defineEmits(['sort', 'editUser', 'deleteUser'])

// Recreate the icon function locally for display logic
function icon(column) {
  if (props.sortBy !== column) return '↕'
  return props.sortDir === 'asc' ? '↑' : '↓'
}
</script>

<style scoped>
/* Only include styles relevant to the table, sorting, and actions, such as .user-table, .sortable, .status-badge, .action-btns, etc. */
/* Sorting */
.sortable {
  cursor: pointer;
  user-select: none;
}
.sort-icon {
  margin-right: 6px;
  opacity: 0.6;
  font-size: 13px;
}
.user-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}
.user-table th,
.user-table td {
  padding: 15px;
  text-align: right;
  border-bottom: 1px solid #f0f0f0;
}
.user-table th {
  background-color: #f7f9fc;
  color: var(--dark-blue);
  font-weight: 600;
  font-size: 15px;
}
.user-table tr:hover {
  background-color: #fcfcfc;
}
.status-badge {
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
}
.status-active {
  background-color: #d4edda;
  color: var(--success-color);
}
.status-inactive {
  background-color: #f8d7da;
  color: var(--danger-color);
}
.action-btns {
  display: flex;
  gap: 5px;
  justify-content: flex-end;
}
.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--secondary-color);
  font-size: 16px;
}
.action-btn:hover {
  color: var(--primary-color);
}
.action-btn.edit:hover {
  color: var(--success-color);
}
.action-btn.delete:hover {
  color: var(--danger-color);
}
.empty-row {
  text-align: center;
  color: var(--secondary-color);
}
</style>