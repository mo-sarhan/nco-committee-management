<template>
  <ModalOverlay @close="$emit('close')">

  <div class="images-update">
    <h3 class="title">{{ title }}</h3>

    <div class="review-container">
      <ImageItem
        v-for="item in imagesConfig"
        :key="item.key"
        :item="item"
        :preview="previews[item.key]"
        :reviewMode="true"
        :allowReviewImage="allowReviewImage"
        :rejectReasons="glopalStore.ImageRejectionReasons"
        @decisionChange="emit('decisionChange', item)"
        @zoom="previews[item.key] && zoomImage(previews[item.key])"
      />
    </div>

    <div class="actions">
      <slot name="actions"></slot>
    </div>
  </div>
  </ModalOverlay>

  <ImageZoomOverlay :showZoomOverlay="showZoomOverlay" :zoomedImage="zoomedImage" @closeZoom="showZoomOverlay = false"/>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import ModalOverlay from '@/components/global/ModalOverlay.vue'
import ImageItem from './ImageItem.vue'
import ImageZoomOverlay from './ImageZoomOverlay.vue'
import { useGlopalStore } from '@/stores/glopal'

let glopalStore = useGlopalStore()

const emit = defineEmits(['decisionChange', 'close'])

const props = defineProps({
  imagesConfig: Array,
  previews: Object,
  title: String,
  allowReviewImage: Boolean,
})

const zoomedImage = ref('')
const showZoomOverlay = ref(false)

function zoomImage(src) {
  zoomedImage.value = src
  showZoomOverlay.value = true
}
  onMounted(()=>{
    // console.log("imagesConfig",props.imagesConfig)
  })
</script>

<style>

.review-container {
  display: grid;
  grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
  gap: 16px;
  margin-bottom: 16px;
}
.title{
    margin-bottom: 30px;
    font-size: 20px;
    text-align: center;
}
.actions{
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>