<template>
  <div>
    <router-view></router-view>
    <GlobalLoader />
  </div>
</template>

<script setup>
import GlobalLoader from './components/global/GlobalLoader.vue'
import { useGlopalStore } from '@/stores/glopal'

let glopalStore = useGlopalStore()

if (!localStorage.getItem('user_data')) {
  localStorage.clear()
}

if (localStorage.getItem('user_data')) {
  if (glopalStore.armyRanks.length <= 0) {
    glopalStore.fetchArmyRanks()
  }
  if (glopalStore.ponsCons.length <= 0) {
    glopalStore.fetchAllPonsCons()
  }
  if (glopalStore.commanderJobs.length <= 0) {
    glopalStore.fetchAllCommanderJobs()
  }
  if (glopalStore.lagnaStatus.length <= 0) {
    glopalStore.fetchLagnaSpecificsPersonStutus()
  }
  if (glopalStore.ImageRejectionReasons.length <= 0) {
    glopalStore.fetchAllImageRejectionReasons()
  }
}
</script>
