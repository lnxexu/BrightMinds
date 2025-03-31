<template>
  <Teleport to="body">
    <TransitionGroup name="toast">
      <div v-if="show" 
           :key="message"
           :class="['toast', `toast-${type}`]"
           @click="close">
        <div class="toast-content">
          <i :class="icon"></i>
          <span class="toast-message">{{ message }}</span>
        </div>
        <div class="progress">
          <div class="progress-bar" :style="{ animationDuration: `${duration}ms` }"></div>
        </div>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';

export default {
  name: 'Toast',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    duration: {
      type: Number,
      default: 3000
    }
  },
  setup(props, { emit }) {
    const show = ref(true);
    const timer = ref(null);

    const icon = computed(() => {
      switch (props.type) {
        case 'success':
          return 'fas fa-check-circle';
        case 'error':
          return 'fas fa-times-circle';
        case 'warning':
          return 'fas fa-exclamation-circle';
        default:
          return 'fas fa-info-circle';
      }
    });

    const close = () => {
      show.value = false;
      emit('close');
      if (timer.value) {
        clearTimeout(timer.value);
      }
    };

    onMounted(() => {
      timer.value = setTimeout(close, props.duration);
    });

    onUnmounted(() => {
      if (timer.value) {
        clearTimeout(timer.value);
      }
    });

    return {
      show,
      close,
      icon
    };
  }
};
</script>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  min-width: 300px;
  max-width: 400px;
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  z-index: 9999;
  overflow: hidden;
  transform-origin: right;
  will-change: transform, opacity;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.toast i {
  font-size: 20px;
}

.toast-message {
  font-size: 14px;
  font-weight: 500;
  flex: 1;
}

.progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: rgba(255, 255, 255, 0.3);
}

.progress-bar {
  height: 100%;
  background: currentColor;
  width: 100%;
  transform-origin: left;
  animation: progress linear forwards;
}

.toast-success {
  background: #4CAF50;
  color: white;
}

.toast-error {
  background: #f44336;
  color: white;
}

.toast-warning {
  background: #ff9800;
  color: white;
}

.toast-info {
  background: #2196f3;
  color: white;
}

/* Toast Animations */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.toast-enter-from {
  transform: translateX(120%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(120%);
  opacity: 0;
}

.toast-enter-to,
.toast-leave-from {
  transform: translateX(0);
  opacity: 1;
}

@keyframes progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}
</style>
