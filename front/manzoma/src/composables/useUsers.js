// composables/useUsers.js
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/store/userStore';

export function useUsers() {
  const userStore = useUserStore();
  const loading = ref(false);
  const error = ref(null);

  const loadUsers = async () => {
    loading.value = true;
    try {
      await userStore.fetchUsers();
    } catch (err) {
      error.value = err;
    } finally {
      loading.value = false;
    }
  };

  onMounted(loadUsers);

  return { users: userStore.users, loading, error, loadUsers };
}
