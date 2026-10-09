<template>
  <ReviewImagePopup
    :imagesConfig="imagesConfig"
    :allowReviewImage="allowReviewImage"
    @decisionChange="onDecisionChange"
    :previews="previews"
    title="مراجعة الصور"
    @close="$emit('close')"
  >
    <template v-slot:actions>
      <div class="footer-actions">
        <button class="add-btn" @click="showAddImagePopup = true" v-if="allowUploadImage">
          إضافة صورة
          <i class="fa-solid fa-upload search-icon"></i>
        </button>
        <button class="cancel-btn" @click="$emit('close')">إلغاء</button>
      </div>
    </template>
  </ReviewImagePopup>

  <AddImagePopup
    v-if="showAddImagePopup"
    :newImage="newImage"
    :imagesTypes="imagesTypes"
    :progress="progress"
    :photoFamilySerials="familySerials"
    title="اضافة صورة"
    @close="resetNewImage"
    @uploadNewImage="onNewImageChange"
    @updateUploadNewImage="updateUploadNewImage"
  >
    <template v-slot:actions>
      <div class="footer-actions">
        <!-- <button class="primary" :disabled="!canConfirmNewImage" @click="confirmAddImage">
          ➕ إضافة
        </button> -->
        <button
          class="upload-btn"
          :disabled="
            pendingImages.file == null || (newImage.typeCode === 3 && !newImage.familySerial)
          "
          @click="uploadImage"
        >
          رفع الصورة
        </button>
        <button class="cancel-btn" @click="resetNewImage">عودة</button>
      </div>
    </template>
  </AddImagePopup>

  <!-- IMAGE ZOOM OVERLAY -->
  <div v-if="showZoomOverlay" class="zoom-overlay" @click="closeZoom">
    <img :src="zoomedImage" class="zoomed-image" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { getWsUrl } from '@/utils/glopal'
import { getPersonImagesTypes, postPersonImages } from '@/api/modules/personPhoto'
import ImageItem from './profileImageUpload/ImageItem.vue'
import ReviewImagePopup from './profileImageUpload/ReviewImagePopup.vue'
import AddImagePopup from './profileImageUpload/AddImagePopup.vue'
import personsService from '@/services/personsService'
import swal from 'sweetalert'

const emit = defineEmits(['close'])
const props = defineProps({
  mil_sir: Number,
  allowUploadImage: Boolean,
  allowReviewImage: {
    type: Boolean,
    default: false,
  },
  photos: Array,
})

/* ===== STATE ===== */
const imagesTypes = ref([])
const imagesConfig = ref([])
const pendingImages = ref({})
const previews = reactive({})
const showAddImagePopup = ref(false)
const zoomedImage = ref('')
const showZoomOverlay = ref(false)
const progress = ref(0)
const familySerials = [
  { id: 1, name: 'كارت عائلى 1' },
  { id: 2, name: 'كارت عائلى 2' },
  { id: 3, name: 'كارت عائلى 3' },
  { id: 4, name: 'كارت عائلى 4' },
]

const newImage = reactive({
  file: null,
  preview: '',
  typeCode: '',
  familySerial: null,
})

/* ===== COMPUTED ===== */
const selectedType = computed(() =>
  imagesTypes.value.find((t) => t.photo_type_code === newImage.typeCode),
)

function onDecisionChange(item) {
  // already reactive — nothing special needed

  console.log(item.decision)
  console.log(props.mil_sir)
  if (item.decision == 0 && !item.reject_reason) {
    return
  } else {
    if (item.decision === 0 && item.reject_reason) {
      console.log('accept ===0 && reject_code', item.decision === 0, item.reject_reason)
      personsService.checkPhotoReview(props.mil_sir, item.photo_id, {
        accept: item.decision,
        reject_code: item.reject_reason,
      })
    }
    if (item.decision === 1) {
      personsService.checkPhotoReview(props.mil_sir, item.photo_id, {
        accept: item.decision,
        reject_code: item.reject_reason,
      })
    }
  }
  console.log('onDecisionChange', item)
}

const canConfirmNewImage = computed(() => {
  if (!newImage.file || !newImage.typeCode) return false
  if (selectedType.value?.family_flag && !newImage.familySerial) return false
  return true
})

/* ===== METHODS ===== */
function onNewImageChange(e) {
  const file = e.target.files[0]
  if (!file) return
  newImage.file = file
  newImage.preview = URL.createObjectURL(file)

  confirmAddImage()
}
function updateUploadNewImage() {
  // resetNewImage(false)
  confirmAddImage()
  // console.log(newImage)
}

function confirmAddImage() {
  const key = `${newImage.typeCode}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  const imageObj = {
    key,
    label: selectedType.value.photo_type_name,
    photo_code: newImage.typeCode,
    familySerial: newImage.familySerial,
    file: newImage.file,
  }

  // imagesConfig.value.push(imageObj)
  pendingImages.value = imageObj
  // previews[key] = newImage.preview
}

function resetNewImage(close = true) {
  if (close) showAddImagePopup.value = false
  pendingImages.value = {}
  progress.value = 0
  Object.assign(newImage, { file: null, preview: '', typeCode: '', familySerial: null })
}

async function uploadImage() {
  if (!pendingImages.value) return

  const formData = new FormData()
  formData.append('mil_ser', props.mil_sir)
  formData.append('photo_type_code', pendingImages.value.photo_code)
  formData.append('photo_family_serial', pendingImages.value.familySerial ?? '')
  formData.append('photo_path', pendingImages.value.file)

  try {
    const res = await postPersonImages(formData, {
      // Track progress
      onUploadProgress: (progressEvent) => {
        // console.log("progressEvent==============>",progressEvent)
        if (progressEvent.total) {
          progress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      },
    })

    imagesConfig.value = []
    pendingImages.value = {}
    progress.value = 0

    if (res.data) {
      // console.log("imagesTypes.value",imagesTypes.value)
      res.data.forEach((p) => {
        // console.log("p=============>",p)
        const matchingType = imagesTypes.value.find(
          (type) => type.photo_type_code === p.photo_type_code,
        )
        const label = matchingType ? matchingType.photo_type_name : 'Unknown Type'
        const key = `${newImage.typeCode}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
        imagesConfig.value.push({
          key,
          label,
          photo_type_code: p.photo_type_code,
          familySerial: p.photo_family_serial,
          decision: null,
          reject_reason: null,
        })
        previews[key] = getWsUrl(p.photo_path)
      })
      pendingImages.value = {}
      showAddImagePopup.value = false
      resetNewImage(false)

      // Success alert
      swal({
        title: 'تم الرفع بنجاح',
        text: 'تم الرفع بنجاح',
        icon: 'success',
        button: false,
        timer: 1000,
      })
    } else {
      swal({
        title: 'حدثت مشكلة',
        text: 'حدثت مشكلة اثناء الرفع',
        icon: 'error',
        confirmButtonText: 'حاول مره اخرى ',
      })
    }
  } catch (error) {
    swal({
      title: 'حدثت مشكلة',
      text: error,
      icon: 'error',
      confirmButtonText: 'حاول مره اخرى ',
    })
  }
}

async function submitReview() {
  const reviewPayload = imagesConfig.value.map((img) => ({
    photo_type_code: img.photo_type_code,
    decision: img.decision,
    reject_reason: img.reject_reason,
  }))

  console.log('Review Payload:', reviewPayload)

  // await apiCall(reviewPayload)
}
function zoomImage(src) {
  zoomedImage.value = src
  showZoomOverlay.value = true
}

function closeZoom() {
  zoomedImage.value = ''
  showZoomOverlay.value = false
}

onMounted(async () => {
  const res = await getPersonImagesTypes()
  imagesTypes.value = res.data

  console.log('props.photos', props.photos)
  props.photos?.forEach((p) => {
    const matchingType = imagesTypes.value.find(
      (type) => type.photo_type_code === p.photo_type_code,
    )

    // If a matching photo type is found, set the label from photo_type_name
    const label = matchingType ? matchingType.photo_type_name : 'Unknown Type'

    const key = `${newImage.typeCode}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    imagesConfig.value.push({
      key,
      label,
      photo_type_code: p.photo_type_code,
      photo_status: p.photo_status,
      reject_reason: p.reject_reason,
      familySerial: p.photo_family_serial,
      photo_id: p.photo_id,
    })
    previews[key] = getWsUrl(p.photo_path)
    console.log(previews[key])
  })
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  background: #fff;
  border-radius: 14px;
  padding: 24px;
  width: 720px;
  max-width: 95%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

.modal-content.add-image {
  width: 480px;
}

.pending-item {
  border: 1px dashed #ccc;
  border-radius: 10px;
  overflow: hidden;
  background: #f9f9f9;
  position: relative;
  transition: transform 0.2s;
}

.pending-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.preview {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.preview.cover {
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s;
}

.preview.cover:hover {
  transform: scale(1.05);
}

.radio-group {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  margin: 12px 0;
}

.radio-group label.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.serial label {
  flex: 1;
}

.pending-images {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.pending-item {
  width: 100px;
  text-align: center;
  position: relative;
}

.pending-item .remove-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  background: red;
  border: none;
  color: #fff;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  cursor: pointer;
  font-size: 12px;
}

.footer-actions {
  display: flex;
  justify-content: center;
  margin-top: 16px;
  flex-wrap: wrap;
  gap: 30px;
}

button.upload-btn {
  background: var(--mainColor);
  color: white;
  padding: 8px 18px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  transition: background 0.2s;
}

button.upload-btn:disabled {
  background: var(--disableColor);
  cursor: not-allowed;
}

button.upload-btn:hover:not(:disabled) {
  background: var(--secondColor);
}

button.add-btn {
  background: var(--success-color);
  padding: 8px 18px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  color: white;
}
button.add-btn:hover {
  background: var(--success-hover-color);
  box-shadow: 2px 3px #8ccaa0;
}
button.cancel-btn {
  background: var(--danger-color);
  padding: 8px 18px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  color: white;
}

button.cancel-btn:hover {
  background: var(--danger-color);
}
</style>
