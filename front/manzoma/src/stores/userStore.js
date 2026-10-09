import { defineStore } from 'pinia';
import { usersApi } from '@/api/modules/users';

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
  }),
  actions: {
    async fetchUsers() {
      this.users = await usersApi.getAll();
    },
  },
});
