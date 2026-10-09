<template>
  <transition :name="transitionName">
    <div
      v-show="visible"
      :style="customStyle"
      class="back-to-ceiling"
      @click="backToTop"
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 17 17"
        xmlns="http://www.w3.org/2000/svg"
        class="Icon Icon--backToTopArrow"
        aria-hidden="true"
        style="height:16px;width:16px"
      >
        <path
          d="M12.036 15.59a1 1 0 0 1-.997.995H5.032a.996.996 0 0 1-.997-.996V8.584H1.03c-1.1 0-1.36-.633-.578-1.416L7.33.29a1.003 1.003 0 0 1 1.412 0l6.878 6.88c.782.78.523 1.415-.58 1.415h-3.004v7.004z"
        />
      </svg>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// ✅ Props
const props = defineProps({
  visibilityHeight: {
    type: Number,
    default: 400
  },
  backPosition: {
    type: Number,
    default: 0
  },
  customStyle: {
    type: Object,
    default: () => ({
      right: '50%',
      bottom: '50px',
      width: '40px',
      height: '40px',
      borderRadius: '4px',
      lineHeight: '45px',
      background: '#ffcb05'
    })
  },
  transitionName: {
    type: String,
    default: 'fade'
  }
})

// ✅ State
const visible = ref(false)
const interval = ref(null)
const isMoving = ref(false)

// ✅ Scroll handler
const handleScroll = () => {
  visible.value = window.pageYOffset > props.visibilityHeight
}

// ✅ Smooth scroll function
const easeInOutQuad = (t, b, c, d) => {
  if ((t /= d / 2) < 1) return (c / 2) * t * t + b
  return (-c / 2) * (--t * (t - 2) - 1) + b
}

const backToTop = () => {
  if (isMoving.value) return

  const start = window.pageYOffset
  let i = 0
  isMoving.value = true

  interval.value = setInterval(() => {
    const next = Math.floor(
      easeInOutQuad(10 * i, start, -start, 500)
    )

    if (next <= props.backPosition) {
      window.scrollTo(0, props.backPosition)
      clearInterval(interval.value)
      isMoving.value = false
    } else {
      window.scrollTo(0, next)
    }

    i++
  }, 16.7)
}

// ✅ Lifecycle
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  if (interval.value) clearInterval(interval.value)
})
</script>

<style scoped>
.back-to-ceiling {
  position: fixed;
  right: 40px;
  bottom: 40px;

  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;
  cursor: pointer;

  /* Modern Gradient */
  background: linear-gradient(135deg, #4f8cff, #6a5cff);

  /* Glass effect */
  backdrop-filter: blur(8px);

  /* Shadow */
  box-shadow:
    0 8px 20px rgba(0, 0, 0, 0.15),
    0 3px 6px rgba(0, 0, 0, 0.1);

  transition: all 0.3s ease;

  z-index: 999;
}

/* Hover effect */
.back-to-ceiling:hover {
  transform: translateY(-6px) scale(1.08);
  box-shadow:
    0 12px 28px rgba(0, 0, 0, 0.2),
    0 6px 12px rgba(0, 0, 0, 0.15);
}

/* Click effect */
.back-to-ceiling:active {
  transform: scale(0.95);
}

/* Icon styling */
.back-to-ceiling .Icon {
  fill: white;
  transition: transform 0.3s ease;
}

/* Icon animation on hover */
.back-to-ceiling:hover .Icon {
  transform: translateY(-3px);
}

/* Fade + Scale animation */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.35s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.8);
}

</style>