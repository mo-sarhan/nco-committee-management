import { defineStore } from 'pinia'

export const useLoadingStore = defineStore('loading', {
    state: () => ({
        isLoading: false,
        activeRequests: 0,
    }),
    actions: {
        startLoading() {
            this.activeRequests++
            this.isLoading = this.activeRequests > 0
        },
        stopLoading() {
            this.activeRequests = Math.max(0, this.activeRequests - 1)
            this.isLoading = this.activeRequests > 0
        },
    },
    getters: {
        isGlobalLoading: (state) => state.isLoading,
    },
})