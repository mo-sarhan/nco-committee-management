<template>
  <div :class="['error-wrapper', { dark }]">
    <!-- Particle background -->
    <div class="particles"></div>

    <div class="card">
      <!-- Animated SVG -->
      <div class="svg-wrapper">
        <span class="error-icon" v-html="currentIcon"></span>
      </div>

      <h1 class="code">{{ code }}</h1>
      <h2>{{ title }}</h2>
      <p v-if="message">{{ message }}</p>

      <slot />

      <button v-if="buttonText" @click="$emit('onClick')">
        {{ buttonText }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { icons } from '../../../public/icons'

const props = defineProps({
  code: String,
  title: String,
  message: String,
  buttonText: String,
  dark: Boolean,
})
defineEmits(['onClick'])

const currentIcon = computed(() => {
  if (props.code === '404') return icons.Briefcase
  if (props.code === '401' || props.code === '403') return icons.Briefcase
  if (props.code === '500') return icons.Briefcase
  return icons.Briefcase // maintenance default
})

// ----- PARTICLES -----
onMounted(() => {
  const particleCount = 35
  const container = document.querySelector('.particles')

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div')
    particle.classList.add('particle')
    const size = Math.random() * 10 + 5
    particle.style.width = `${size}px`
    particle.style.height = `${size}px`
    particle.style.left = `${Math.random() * 100}%`
    particle.style.animationDuration = `${Math.random() * 10 + 5}s`
    particle.style.animationDelay = `${Math.random() * 5}s`
    container.appendChild(particle)
  }
})
</script>

<style scoped>
.error-wrapper {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(-45deg, #f8f9fa, #e3f2fd, #e9ecef, #f1f3f5);
  background-size: 400% 400%;
  animation: gradientMove 12s ease infinite;
  overflow: hidden;
  padding: 20px;
  transition: 0.4s ease;
}

.error-wrapper.dark {
  background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c1c1c);
  background-size: 400% 400%;
  animation: gradientMove 12s ease infinite;
  color: white;
}

/* Particle background */
.particles {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  animation: floatParticles linear infinite;
}
.error-wrapper.dark .particle {
  background: rgba(255, 255, 255, 0.1);
}
@keyframes floatParticles {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0.6;
  }
  50% {
    opacity: 0.3;
  }
  100% {
    transform: translateY(-200px) scale(1.2);
    opacity: 0;
  }
}

/* Glass Card */
.card {
  position: relative;
  z-index: 2;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.75);
  padding: 50px 60px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  text-align: center;
  max-width: 500px;
  width: 100%;
  animation: floatCard 6s ease-in-out infinite;
  transition: 0.3s ease;
}
.error-wrapper.dark .card {
  background: rgba(30, 30, 30, 0.6);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
}

/* Icon */
.error-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
  display: inline-block;
  animation: iconFloat 4s ease-in-out infinite;
}

/* Code */
.code {
  font-size: 90px;
  font-weight: 700;
  margin: 10px 0;
  letter-spacing: 3px;
  background: linear-gradient(45deg, #007bff, #00c6ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Title */
h2 {
  font-size: 24px;
  margin-bottom: 10px;
  font-weight: 600;
}

/* Message */
p {
  font-size: 16px;
  opacity: 0.8;
  margin-bottom: 20px;
}

/* Button */
button {
  margin-top: 20px;
  padding: 10px 30px;
  border-radius: 50px;
  border: none;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  background: linear-gradient(45deg, var(--mainColor, #007bff), var(--disableColor, #00c6ff));
  color: white;
  transition: 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
}
button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 123, 255, 0.6);
}
button:active {
  transform: scale(0.97);
}

/* Animations */
@keyframes floatCard {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-8px);
  }
}
@keyframes iconFloat {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-6px);
  }
}
@keyframes gradientMove {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Responsive */
@media (max-width: 600px) {
  .card {
    padding: 35px 25px;
  }
  .code {
    font-size: 60px;
  }
  h2 {
    font-size: 20px;
  }
}
</style>
