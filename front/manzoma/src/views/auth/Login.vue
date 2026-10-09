<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore.js'
import { useLoadingStore } from '@/stores/loadingStore.js'

const authStore = useAuthStore()
const loadingStore = useLoadingStore()

const credentials = ref({
  username: '',
  password: '',
})

const handleLogin = async () => {
  try {
    await authStore.login(credentials.value)
  } catch (error) {
    console.error('Login component caught error:', error)
  }
}
</script>

<template>
  <div class="loginPage">
    <main style="height: 100%">
      <form @submit.prevent="handleLogin">
        <div class="logo">
          <img src="@/assets/Images/logo.png" alt="logo" width="90px" />
          <h1>هيئـــة التنظيـــم والادارة ق.م</h1>
        </div>
        <h3>تســـجـيـل دخــول المـســتـخـدم</h3>
        <div class="for-inputs">
          <div class="userN">
            <label for="userName">اسم المستخدم</label>
            <input
              type="text"
              name="userName"
              id="userName"
              class="input-field"
              v-model="credentials.username"
              :disabled="loadingStore.isGlobalLoading"
            />
          </div>

          <div class="userN">
            <label for="Password">كـلـمـة الســر</label>
            <input
              type="Password"
              name="Password"
              id="Password"
              class="input-field"
              v-model="credentials.password"
              :disabled="loadingStore.isGlobalLoading"
            />
          </div>

          <button type="submit" :disabled="loadingStore.isGlobalLoading">
            <span>دخول</span>
          </button>
        </div>
      </form>
    </main>
  </div>
</template>

<style scoped>
.loginPage {
  height: 90vh;
}
.err {
  padding: 10px;
  color: white;
  width: 300px;
  position: absolute;
  top: 80%;
  left: 50%;
  background: #ff0000ba;
  transform: translateX(-50%);
  height: 100px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
form {
  width: 451px;
  height: 55vh;
  margin: auto;
  position: relative;
  top: 50%;
  transform: translateY(-50%);
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 40px #b1b1b1a6;
  min-height: 500px !important;
}
.logo {
  display: flex;
  flex-direction: column;
  /* gap: 5px; */
  align-items: center;
  background: transparent;
  place-content: flex-end;
}
p {
  font-weight: 600;
  text-align: center;
  margin: 2px;
  font-size: 15px;
}
h1 {
  color: var(--secondColor);
  margin: 0;
  font-size: 25px;
}
h3 {
  text-align: center;
  font-size: 16px;
}
.userN {
  display: flex;
  align-items: center;
  gap: 10px;
}
.userN label {
  width: 24%;
}

.for-inputs {
  display: flex;
  flex-direction: column;
  height: 55%;
  justify-content: center;
  gap: 50px;
}

button {
  background: var(--secondColor);
  width: 30%;
  margin: 0 auto;
  padding: 5px;
  border-radius: 10px;
  color: white;
  font-size: 25px;
  border: none;
}
button:hover {
  background-color: #d48e19;
}
</style>
