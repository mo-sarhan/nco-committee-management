<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">

      <!-- Header -->
      <div class="modal-header">
        <h2>تقرير عرض لجنة (عدم الصلاحية)</h2>
      </div>

      <form @submit.prevent="submitForm">

        <!-- ================= 1. البيانات الأساسية ================= -->
        <div class="section">
          <div class="section-title">أولاً : البيانات الأساسية عن ضابط الصف</div>

          <div class="grid-2">
            <div class="field">
              <label>الرقم العسكري</label>
              <input v-model="form.military_no" readonly />
            </div>

            <div class="field">
              <label>الدرجة</label>
              <input v-model="form.degree" readonly />
            </div>

            <div class="field">
              <label>الاسم</label>
              <input v-model="form.name" readonly />
            </div>

            <div class="field">
              <label>السلاح</label>
              <input v-model="form.weapon" readonly />
            </div>

            <div class="field">
              <label>الوحدة</label>
              <input v-model="form.unit" readonly />
            </div>

            <div class="field">
              <label>تاريخ الضم على الوحدة</label>
              <input type="date" v-model="form.join_date" />
            </div>

            <div class="field">
              <label>اسم قائد الوحدة</label>
              <input v-model="form.commander_name" />
            </div>

            <div class="field">
              <label>رقم تليفون القائد / CDM</label>
              <input v-model="form.commander_phone" />
            </div>
          </div>
        </div>

        <!-- ================= 2. الملاحظات ================= -->
        <div class="section">
          <div class="action-header">
            <div class="section-title">الملاحظات (الإيجابية / السلبية)</div>
            <!-- <button @click="addLagnaMember" class="action-btn"> 
              <i class="fa-solid fa-plus"></i>
            </button> -->
          </div>
        
          
          <textarea v-model="form.notes" rows="4"></textarea>
        </div>

        <!-- ================= 3. عرض الجهاز النفسي ================= -->
        <div class="section">
          <div class="section-title">ثالثاً : عرض جهاز العمل النفسي</div>

          <div class="grid-2">
            <div class="field">
              <label>توصية الجهاز</label>
              <textarea v-model="form.psych_recommendation"></textarea>
            </div>

            <div class="field">
              <label>تاريخ العرض</label>
              <input type="date" v-model="form.psych_date" />
            </div>
          </div>
        </div>

        <!-- ================= 4. مدى الجدوى ================= -->
        <div class="section">
          <div class="section-title">رابعاً : مدى جدوى استمراره بالخدمة</div>

          <div class="radio-group">
            <label>
              <input type="radio" value="useful" v-model="form.service_status" />
              يعود بالنفع على القوات المسلحة
            </label>

            <label>
              <input type="radio" value="not_useful" v-model="form.service_status" />
              لا يعود بالنفع على القوات المسلحة
            </label>
          </div>
        </div>

        <!-- ================= 5. رأي القائد المباشر ================= -->
        <div class="section">
          <div class="section-title">خامساً : رأي القائد المباشر</div>

          <textarea v-model="form.direct_commander_opinion"></textarea>

          <div class="grid-3 signatures">
            <input v-model="form.direct_rank" placeholder="الرتبة" />
            <input v-model="form.direct_name" placeholder="الاسم" />
            <input v-model="form.direct_job" placeholder="الوظيفة" />
          </div>
        </div>

        <!-- ================= 6. رأي قائد التشكيل ================= -->
        <div class="section">
          <div class="section-title">سادساً : رأي قائد التشكيل</div>

          <textarea v-model="form.formation_commander_opinion"></textarea>

          <div class="grid-3 signatures">
            <input v-model="form.formation_rank" placeholder="الرتبة" />
            <input v-model="form.formation_name" placeholder="الاسم" />
            <input v-model="form.formation_job" placeholder="الوظيفة" />
          </div>
        </div>

        <!-- ================= 7. رأي مدير الإدارة ================= -->
        <div class="section">
          <div class="section-title">سابعاً : رأي مدير الإدارة</div>

          <textarea v-model="form.admin_opinion"></textarea>

          <div class="grid-3 signatures">
            <input v-model="form.admin_rank" placeholder="الرتبة" />
            <input v-model="form.admin_name" placeholder="الاسم" />
            <input v-model="form.admin_job" placeholder="الوظيفة" />
          </div>
        </div>

        <!-- Actions -->
        <div class="actions">
          <button type="submit" class="btn btn-success">
            حفظ وطباعة PDF
          </button>

          <button type="button" class="btn btn-danger" @click="$emit('close')">
            إغلاق
          </button>
        </div>

      </form>

    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
// import html2pdf from 'html2pdf.js'

/* ================= PROPS ================= */
const props = defineProps({
  person: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'saved'])

/* ================= FORM STATE ================= */
const form = reactive({
  military_no: '',
  degree: '',
  name: '',
  weapon: '',
  unit: '',
  join_date: '',
  commander_name: '',
  commander_phone: '',
  notes: '',
  psych_recommendation: '',
  psych_date: '',
  service_status: '',
  direct_commander_opinion: '',
  direct_rank: '',
  direct_name: '',
  direct_job: '',
  formation_commander_opinion: '',
  formation_rank: '',
  formation_name: '',
  formation_job: '',
  admin_opinion: '',
  admin_rank: '',
  admin_name: '',
  admin_job: ''
})

/* ================= LOAD PERSON DATA ================= */
onMounted(() => {
  form.military_no = props.person?.mil_no || ''
  form.degree = props.person?.degree_name || ''
  form.name = props.person?.person_name || ''
  form.weapon = props.person?.army_name || ''
  form.unit = props.person?.unit_name || ''
})

/* ================= SUBMIT ================= */
function submitForm() {
  generatePDF()
  emit('saved', form)
}

/* ================= GENERATE PDF ================= */
// function generatePDF() {

//   const element = document.createElement("div")

//   element.innerHTML = `
//     <div style="direction:rtl;font-family:Arial;padding:30px">
//       <h2 style="text-align:center">
//         تقرير عرض لجنة (عدم الصلاحية)
//       </h2>
//       <hr/>

//       <p><strong>الرقم العسكري:</strong> ${form.military_no}</p>
//       <p><strong>الدرجة:</strong> ${form.degree}</p>
//       <p><strong>الاسم:</strong> ${form.name}</p>
//       <p><strong>السلاح:</strong> ${form.weapon}</p>
//       <p><strong>الوحدة:</strong> ${form.unit}</p>
//       <p><strong>تاريخ الضم:</strong> ${form.join_date}</p>

//       <h3>الملاحظات</h3>
//       <p>${form.notes}</p>

//       <h3>رأي القائد المباشر</h3>
//       <p>${form.direct_commander_opinion}</p>
//     </div>
//   `

//   html2pdf()
//     .set({
//       margin: 10,
//       filename: `unfitness_report_${form.military_no}.pdf`,
//       html2canvas: { scale: 2 },
//       jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
//     })
//     .from(element)
//     .save()
// }
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

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
.action-header{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
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

.radio-group {
  display: flex;
  gap: 40px;
  margin-top: 10px;
}

.actions {
  margin-top: 30px;
  text-align: center;
}
</style>