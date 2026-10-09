<template>
  <div class="fieldShow" :style="fieldShowStyle">
    <p
      class="fieldShowLabel"
      @click="$emit('click')"
      :style="fieldShowLabelStyle"
      :class="fieldShowClickable && !fieldShowLabelStyle ? 'data-btn' : ''"
    >
      {{ fieldShowLabel }}
    </p>
    <div v-if="actionFlag" class="fieldShowData" :style="fieldShowDataStyle">
      <slot name="actionData"> </slot>
    </div>
    <p v-else class="fieldShowData" :style="fieldShowDataStyle">{{ fieldShowData || '---' }}</p>
  </div>
</template>

<script setup>
defineProps({
  fieldShowLabel: String,
  fieldShowData: {
    type: [String, Number],
    default: '0',
    required: true,
  },
  actionFlag: Boolean,
  fieldShowClickable: Boolean,
  fieldShowColor: String,
  fieldShowLabelStyle: Object,
  fieldShowDataStyle: Object,
  fieldShowStyle: Object,
})

defineEmits(['click'])
</script>

<style scoped>
p {
  margin: 0;
}
.fieldShow {
  background: white;
  border-radius: 13px;
  /* gap: 13px; */
  display: flex;
  align-items: center;
  position: relative;
  font-weight: 800;
  height: 50px;
}

.fieldShowLabel {
  /* background-color: #8080804d;
  height: 43px;
  margin: 0;
  position: inherit;
  display: flex;
  align-items: center;
  border-radius: 25px 0px 10px 0px;
  text-align: center;
  place-content: center;
  min-width: 100px;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  padding: 1px 5px;
 */

  /* background-color: #8080804d;
  height: 43px;
  margin: 0;
  position: inherit;
  display: flex;
  border-radius: 25px 0px 10px 0px;
  text-align: center;
  place-content: center;
  min-width: 140px;
  font-size: 15px;
  font-weight: 800;
  line-height: 20px;
  padding: 1px 5px; */

  /* background-color: #8080804d;
  height: 43px;
  margin: 0;
  position: inherit;
  display: flex;
  border-radius: 25px 0px 10px 0px;
  text-align: center;
  place-content: center;
  min-width: 140px;
  
  font-weight: bold;
 
  padding: 8px 0px; */

  background-color: #8080804d;
  height: 50px;
  /* margin: 0; */
  /* position: inherit; */
  /* display: flex; */
  border-radius: 25px 0px 10px 0px;
  text-align: center;
  /* place-content: center; */
  min-width: 140px;
  /* font-size: 15px; */
  font-weight: bold;
  /* line-height: 20px; */
  padding: 8px 0px;
}

.fieldShowData {
  place-content: center;
  text-align: center;
  place-content: center;
  text-align: center;
  width: 100%;
  font-size: 14px;
  padding: 5px 10px;
}
.data-btn {
  transition: all 300ms;
  background-color: #f98d11d1 !important;
  color: rgb(5, 1, 1) !important;
  cursor: pointer !important;
}
.data-btn:hover {
  transform: scale(1.1);
}
</style>
