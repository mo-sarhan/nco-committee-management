<template>
    <div class="spliter-data" @click="$emit('expand')">
        <h4 :style="splitTitleStyle">{{splitTitle}}</h4>
        <hr style="background-color: black; font-weight: bolder" />
    </div>
</template>

<script setup>

defineProps({
  splitTitle: String,
  splitTitleStyle: {
    type: Object,
    default: () => ({}),
  },
})

defineEmits([
  'expand',
])


</script>

<style scoped>
.controls-container {
  margin-bottom: 15px;
}
.controles {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.fields {
  display: flex;
  align-items: center;
  gap: 20px;
}
.spliter-data {
  display: flex;
  align-items: center;
  cursor: pointer;
  /* height: 18px !important; */
}

.spliter-data h4 {
  font-size: 20px;
  padding: 5px;
}

hr {
  flex: 1;
}
</style>
