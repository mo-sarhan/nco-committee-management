<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">

      <div v-if="loading" class="loading-overlay">
        جاري التحميل...
      </div>

      <div class="modal-header">
        <h2>تقرير العمل النفسى</h2>
      </div>

      <form @submit.prevent="submitForm">

        <!-- ================= BASIC INFO ================= -->
        <div class="section">
          <div class="section-title">البيانات الأساسية عن ضابط الصف</div>

          <div class="grid-2">
            <div class="field">
              <label>الرقم العسكري</label>
              <div class="display-value">{{ form.military_no }}</div>
            </div>

            <div class="field">
              <label>الدرجة</label>
              <div class="display-value">{{ form.degree }}</div>
            </div>

            <div class="field">
              <label>الاسم</label>
              <div class="display-value">{{ form.name }}</div>
            </div>
          </div>
        </div>

        <!-- ================= REPORTS ================= -->
        <div class="section">
          <div class="action-header">
            <div class="section-title">عرض جهاز العمل النفسي</div>

            <!-- Add only if no new report exists -->
            <div
              v-if="!hasNewReport"
              class="action-btn"
              @click="addPsychRow"
            >
              + إضافة عرض جديد
            </div>
          </div>

          <div
            v-for="(report, index) in form.psych_reports"
            :key="index"
            class="accordion-item"
          >

            <!-- Header -->
            <div
              class="accordion-header"
              @click="toggleAccordion(index)"
            >
              <div>
                عرض رقم {{ index + 1 }}
                <span v-if="report.isOld" class="old-badge">
                  (تقرير سابق)
                </span>
              </div>

              <div class="accordion-actions">
                <span v-if="report.date" class="date-badge">
                  {{ report.date }}
                </span>

                <!-- Allow delete only for new report -->
                <button
                  v-if="!report.isOld"
                  type="button"
                  class="remove-btn"
                  @click.stop="removePsychRow(index)"
                >
                  حذف
                </button>

                <span class="arrow">
                  <i v-if="report.open" class="fa-solid fa-chevron-up"></i>
                  <i v-else class="fa-solid fa-chevron-down"></i>
                </span>
              </div>
            </div>

            <!-- Body -->
            <transition name="fade">
              <div v-show="report.open" class="accordion-body">

                <div class="grid-2">

                  <!-- Recommendation -->
                  <div class="field">
                    <label>توصية الجهاز</label>

                    <!-- OLD REPORT (READ ONLY) -->
                    <div
                      v-if="report.isOld"
                      class="display-value"
                    >
                      {{ report.recommendation }}
                    </div>

                    <!-- NEW REPORT (EDITABLE) -->
                    <textarea
                      v-else
                      v-model="report.recommendation"
                    ></textarea>
                  </div>

                  <!-- Date -->
                  <div class="field">
                    <label>تاريخ العرض</label>

                    <div
                      v-if="report.isOld"
                      class="display-value"
                    >
                      {{ report.date }}
                    </div>

                    <input
                      v-else
                      type="date"
                      v-model="report.date"
                    />
                  </div>

                  <!-- Attachment -->
                  <div class="field full-width">
                    <label>المرفقات</label>

                    <!-- Upload only for new -->
                    <input
                      v-if="!report.isOld"
                      type="file"
                      @change="handleFileUpload($event, index)"
                    />

                    <div v-if="report.preview" class="file-preview">

                      <div class="file-name">
                        📎 {{ report.attachment?.name || 'ملف مرفوع سابقاً' }}
                      </div>

                      <img
                        v-if="isImagePreview(report.preview)"
                        :src="report.preview"
                        class="image-preview"
                      />

                      <!-- Remove file only for new -->
                      <button
                        v-if="!report.isOld"
                        type="button"
                        class="remove-file"
                        @click="removeFile(index)"
                      >
                        حذف المرفق
                      </button>

                    </div>
                  </div>

                </div>

              </div>
            </transition>

          </div>
        </div>

        <!-- ================= ACTIONS ================= -->
        <div class="actions">
          <button
            v-if="hasNewReport"
            type="submit"
            class="btn btn-success"
            :disabled="loading"
          >
            حفظ
          </button>

          <button
            type="button"
            class="btn btn-danger"
            @click="$emit('close')"
          >
            إغلاق
          </button>
        </div>

      </form>

    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted, ref, computed } from 'vue'
import lagnaService from '@/services/lagnaService'
import { getWsUrl } from '@/utils/glopal'

const props = defineProps({
  person: { type: Object, required: true },
  person_id: { type: Number, required: true }
})

const emit = defineEmits(['close', 'saved'])

/* ================= STATE ================= */

const loading = ref(false)

const form = reactive({
  military_no: '',
  degree: '',
  name: '',
  psych_reports: []
})

const hasNewReport = computed(() =>
  form.psych_reports.some(r => !r.isOld)
)

/* ================= LOAD ================= */

onMounted(async () => {
  form.military_no = props.person?.mil_no || ''
  form.degree = props.person?.degree_name || ''
  form.name = props.person?.person_name || ''

  await loadExistingReports()
})

async function loadExistingReports() {
  try {
    loading.value = true

    const response = await lagnaService.getPsychologicPerson(
      props.person.mil_ser
    )

    console.log("response",response)
    if (response.length) {
      form.psych_reports = response.map(r => ({
        recommendation: r.psych_notes,
        date: r.report_date,
        attachment: null,
        preview: getWsUrl(r.psych_attach) || null,
        open: false,
        isOld: true
      }))

      form.psych_reports[0].open = true
    }

  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

/* ================= METHODS ================= */

function addPsychRow() {
  form.psych_reports.push({
    recommendation: '',
    date: '',
    attachment: null,
    preview: null,
    open: true,
    isOld: false
  })
}

function removePsychRow(index) {
  form.psych_reports.splice(index, 1)
}

function toggleAccordion(index) {
  form.psych_reports[index].open =
    !form.psych_reports[index].open
}

function handleFileUpload(event, index) {
  const file = event.target.files[0]
  if (!file) return

  form.psych_reports[index].attachment = file
  form.psych_reports[index].preview = URL.createObjectURL(file)
}

function removeFile(index) {
  form.psych_reports[index].attachment = null
  form.psych_reports[index].preview = null
}

function isImagePreview(preview) {
  return preview?.startsWith('blob:') || preview?.includes('http')
}

/* ================= SUBMIT ================= */

async function submitForm() {
  try {
    loading.value = true

    const newReport = form.psych_reports.find(r => !r.isOld)

    if (!newReport) return

    const payload = new FormData()

    payload.append(`psych_notes`, newReport.recommendation)
    payload.append(`report_date`, newReport.date)

    if (newReport.attachment) {
      payload.append(`psych_attach`, newReport.attachment)
    }

    await lagnaService.addPsychologicPerson(
      props.person_id,
      payload
    )

    emit('saved')
    emit('close')

  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-container {
  width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  background: white;
  padding: 25px;
  border-radius: 8px;
  direction: rtl;
  font-family: 'Cairo', sans-serif;
}

.section {
  margin-top: 25px;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 6px;
}

.section-title {
  font-weight: bold;
  margin-bottom: 15px;
  color: #003366;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.field label {
  display: block;
  font-size: 13px;
  margin-bottom: 5px;
}

input, textarea {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  min-height: 80px;
}

.full-width {
  grid-column: span 2;
}

.action-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.action-btn {
  cursor: pointer;
  background: #1e88e5;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
}

.accordion-item {
  border: 1px dashed #ccc;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 6px;
  background: #fafafa;
}

.accordion-header {
   display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: bold;
  background: #f1f3f6;
  padding: 10px;
  border-radius: 6px;
}

.accordion-body {
  padding: 15px;
  background: #fff;
}
.actions{
  margin-top:15px;
  gap: 20px;
}

.accordion-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.remove-btn {
  background: red;
  color: white;
  border: none;
  padding: 3px 8px;
  cursor: pointer;
  border-radius: 4px;
}

.file-preview {
  margin-top: 10px;
}

.image-preview {
  margin-top: 10px;
  max-width: 200px;
  border-radius: 6px;
}

.remove-file {
  margin-top: 5px;
  background: #777;
  color: white;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
  border-radius: 4px;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
}

.display-value {
  padding: 8px 10px;
  background-color: #f5f7fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 34px;
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #2c3e50;
}
</style>