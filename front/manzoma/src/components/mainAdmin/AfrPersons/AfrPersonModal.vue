<template>
    <!-- Add/Edit Modal -->
    <div v-if="isModalOpen" class="modal-overlay">
        <div class="modal-content">
            <h2>{{ isEditMode ? "تعديل مستخدم" : "إضافة مستخدم" }}</h2>

            <form @submit.prevent="emit('save')">

                <div class="form-group">
                    <label>الاسم</label>
                    <input type="text" :value="currentAfrPerson.name"
                           @input="update('name', $event.target.value)" required>
                </div>

                <div class="form-group">
                    <label>البريد الإلكتروني</label>
                    <input type="unit" :value="currentAfrPerson.unit"
                           @input="update('unit', $event.target.value)" required>
                </div>

                <div class="form-group">
                    <label>الهاتف</label>
                    <input type="tel" :value="currentAfrPerson.milNo"
                           @input="update('milNo', $event.target.value)" required>
                </div>

                <div class="form-group">
                    <label>الحالة</label>
                    <select :value="currentAfrPerson.lastLagna"
                            @change="update('lastLagna', $event.target.value)">
                        <option value="نشط">نشط</option>
                        <option value="غير نشط">غير نشط</option>
                    </select>
                </div>

                <div class="modal-actions">
                    <button class="btn btn-primary" type="submit">
                        {{ isEditMode ? "حفظ" : "إضافة" }}
                    </button>

                    <button class="btn cancel-btn" type="button" @click="emit('close')">إلغاء</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Delete Confirm -->
    <div v-if="isDeleteConfirmOpen" class="modal-overlay">
        <div class="modal-content confirm-box">
            <h2>تأكيد الحذف</h2>

            <p>هل تريد حذف المستخدم {{ AfrPersonToDeleteName }} ؟</p>

            <div class="modal-actions">
                <button class="btn btn-danger" @click="emit('confirmDelete')">حذف</button>
                <button class="btn cancel-btn" @click="emit('cancelDelete')">إلغاء</button>
            </div>
        </div>
    </div>

</template>

<script setup>
const props = defineProps({
    isModalOpen: Boolean,
    isEditMode: Boolean,
    currentAfrPerson: Object,
    isDeleteConfirmOpen: Boolean,
    AfrPersonToDeleteName: String
})

const emit = defineEmits([
    "close", "save",
    "confirmDelete", "cancelDelete",
    "update:currentAfrPerson"
])

function update(field, value) {
    emit("update:currentAfrPerson", { ...props.currentAfrPerson, [field]: value })
}
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
}

.modal-content {
    background: white;
    padding: 30px;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    text-align: right;
}

.modal-content h2 {
    margin: 0 0 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    color: var(--dark-blue);
}

.form-group {
    margin-bottom: 15px;
}

label {
    font-weight: bold;
    margin-bottom: 5px;
    display: block;
}

input, select {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #ddd;
}

.modal-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

.cancel-btn {
    background: #f1f1f1;
    color: var(--secondary-color);
}

.confirm-box {
    max-width: 400px;
}
</style>
