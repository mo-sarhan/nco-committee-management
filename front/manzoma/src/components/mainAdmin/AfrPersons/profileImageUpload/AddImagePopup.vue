<template>
  <ModalOverlay @close="$emit('close')">
    <h3 class="title">{{ title }}</h3>

    <div class="upload-container">
      <label class="upload-box" v-if="newImage.typeCode">
        <input type="file" hidden accept="image/*" @change="$emit('uploadNewImage', $event)" />
        <span v-if="!newImage.preview">اضغط لاختيار صورة</span>
        <img v-else :src="newImage.preview" class="preview cover" @click="zoomImage(newImage.preview)" />
      </label>

      <div v-if="progress > 0" class="progress-container">
        <div class="progress-bar" :style="{ width: `${progress}%` }"></div>
      </div>

      <div class="select-options">
        <!-- Select for Photo Type -->
        <div class="select-group">
          <label for="photoType">اختيار نوع الصورة</label>
          <select v-model="newImage.typeCode" id="photoType" @change="$emit('updateUploadNewImage')">
            <option v-for="type in imagesTypes" :key="type.photo_type_code" :value="type.photo_type_code">
              {{ type.photo_type_name }}
            </option>
          </select>
        </div>


        <div v-if="newImage.typeCode === 3" class="select-group">
          <label for="familySerial">اختيار الترتيب العائلي</label>
          <select v-model="newImage.familySerial" id="familySerial" @change="$emit('updateUploadNewImage')">
            <option v-for="serial in photoFamilySerials" :key="serial.id" :value="serial.id">
              {{ serial.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <slot name="actions"></slot>
  </ModalOverlay>

  <ImageZoomOverlay :showZoomOverlay="showZoomOverlay" :zoomedImage="zoomedImage" @closeZoom="showZoomOverlay = false"/>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import ModalOverlay from '@/components/global/ModalOverlay.vue'
import ImageZoomOverlay from './ImageZoomOverlay.vue'

defineEmits(['close', 'uploadNewImage', 'updateUploadNewImage'])
const props = defineProps({
  imagesTypes: Array,
  newImage: Object,
  title: String,
  progress: Number,
  photoFamilySerials: Array,
})

const zoomedImage = ref('')
const showZoomOverlay = ref(false)

function zoomImage(src) {
  zoomedImage.value = src
  showZoomOverlay.value = true
}


</script>



<style>
.review-container {
  display: grid;
  grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
  gap: 16px;
  margin-bottom: 16px;
}
.select-options{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.title {
  margin-bottom: 30px;
  font-size: 20px;
  text-align: center;
}

.upload-box {
  border: 2px dashed #aaa;
  border-radius: 12px;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-bottom: 12px;
  background: #fafafa;
  transition: background 0.2s;
}

.upload-box:hover {
  background: #f0f0f0;
}

.pending-preview h4 {
  margin-bottom: 8px;
  text-align: center;
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

.select-group {
  margin: 12px 0;
  display: flex;
  flex-direction: column;
  width: 350px;
}

.select-group label {
  margin-bottom: 6px;
}

.select-group select {
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ddd;
}
.progress-container {
  width: 100%;
  background-color: #f3f3f3;
  height: 5px;
  border-radius: 10px;
  margin: 20px;
}

.progress-bar {
  height: 100%;
  background-color: #4caf50;
  border-radius: 10px;
}
</style>