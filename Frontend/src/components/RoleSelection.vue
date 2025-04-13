<template>
  <div class="role-selection-container">
    <h2 class="title">Welcome! What is your role?</h2>
    <p class="subtitle">Please select your role to continue:</p>

    <div class="form-group">
      <label for="role">Select Role</label>
      <select v-model="selectedRole" id="role" class="role-dropdown">
        <option value="" disabled>Select your role</option>
        <option value="Student">Student</option>
        <option value="Teacher">Teacher</option>
        <option value="Parent">Parent</option>
      </select>
    </div>

    <button :disabled="!selectedRole" @click="proceed" class="next-button">
      Next
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const selectedRole = ref('');

const proceed = () => {
  if (selectedRole.value === 'Teacher') {
    router.push({ name: 'TeacherRegister' }); // Redirect to teacher registration form
  } else {
    router.push({ name: 'Register', query: { role: selectedRole.value } }); // Redirect to the original form with role
  }
};
</script>

<style scoped>
.role-selection-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f5f5f5;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
  width: 100%;
  max-width: 400px;
}

.role-dropdown {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

.next-button {
  padding: 0.75rem 1.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.next-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.next-button:hover:not(:disabled) {
  background-color: #45a049;
}
</style>