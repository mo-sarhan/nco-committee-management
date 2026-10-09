<template>
  <div class="stat-card" style="cursor: pointer;" :style="{ borderLeftColor: color }" @click="stCardClick">
    <div class="card-icon" :style="{ backgroundColor: color + '20', color: color }">
      <span class="material-icons-outlined" v-if="icon"><span v-html="icon"></span></span>
      <span class="material-icons-outlined" v-if="fontawesome"><i :class="fontawesome"></i> </span>
    </div>

    <div class="card-content">
      <p class="card-title">{{ title }}</p>
      <h3 class="card-value">{{ value }}</h3>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  title: { type: String, required: true },
  routeName: { type: String, required: true ,default : null},
  routeParams: { type: Object, required: true ,default : null},
  value: { type: [String, Number], required: true },
  icon: { type: String },
  fontawesome: { type: String},
  clickable: { type: Boolean},
  color: { type: String, default: '#3b82f6' },
})
const router = useRouter()

function stCardClick (){
  if(props.routeName != null){
    // console.log("props.routeName",props.routeName)
    router.push({
      name: props.routeName,
      params: props.routeParams,
    })
  }
}

onMounted(()=>{
  // console.log("fontawesome",props.fontawesome)
})
</script>

<style scoped>
.stat-card {
  display: flex;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s;
  border-left: 5px solid;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.card-content {
  flex-grow: 1;
  margin-right: 10px;
}

.card-title {
text-transform: uppercase;
    font-size: 1rem;
    color: #2f3031;
    margin: 0 0 5px 0;
    font-weight: 500;
}

.card-value {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #1f2937;
}

.material-icons,
.material-icons-outlined {
  font-family: 'Material Icons';
  font-weight: normal;
  font-style: normal;
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  -webkit-text-stroke-width: 0.2px;
}
</style>
