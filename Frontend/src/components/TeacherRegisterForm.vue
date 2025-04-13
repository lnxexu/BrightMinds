<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="card-title">Teacher Registration</h2>
      <p class="card-subtitle">Join us and share your expertise with students!</p>
      <form @submit.prevent="handleTeacherRegister" class="register-form">
        <!-- Full Name -->
        <div class="form-group">
          <label for="name">Full Name</label>
          <div class="input-wrapper">
            <i class="fas fa-user"></i>
            <input v-model="name" type="text" id="name" placeholder="Enter your full name" required />
          </div>
        </div>

        <!-- Email -->
        <div class="form-group">
          <label for="email">Email</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope"></i>
            <input v-model="email" type="email" id="email" placeholder="Enter your email" required />
          </div>
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input v-model="password" type="password" id="password" placeholder="Create a password" required />
          </div>
        </div>

        <!-- Subject Expertise -->
        <div class="form-group">
          <label for="subject">Subject Expertise</label>
          <div class="input-wrapper">
            <i class="fas fa-book"></i>
            <select v-model="subject" id="subject" required>
              <option value="" disabled>Select your subject expertise</option>
              <option v-for="course in courses" :key="course.id" :value="course.name">
                {{ course.name }}
              </option>
            </select>
          </div>
        </div>

        <!-- Register Button -->
        <div class="form-group">
          <button type="submit" class="register-button" :disabled="isLoading">
            {{ isLoading ? 'Registering...' : 'Register' }}
          </button>
        </div>
      </form>

      <p class="login-link">
        Already have an account?
        <router-link to="/login">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '../lib/supabaseClient.js';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const name = ref('');
const email = ref('');
const password = ref('');
const subject = ref('');
const courses = ref([]);
const isLoading = ref(false);
const toast = useToast();
const router = useRouter();

const fetchCourses = async () => {
  try {
    const { data, error } = await supabase.from('courses').select('course_id, name');
    if (error) {
      console.error('Error fetching courses:', error.message, error.details);
      return;
    }
    courses.value = data.map(course => ({
      id: course.course_id,
      name: course.name,
    }));
  } catch (err) {
    console.error('Unexpected error fetching courses:', err);
  }
};

onMounted(() => {
  fetchCourses();
});

const handleTeacherRegister = async () => {
  if (!name.value || !email.value || !password.value || !subject.value) {
    toast.error('Please fill in all fields.');
    return;
  }

  try {
    isLoading.value = true;

    const { user, error: signUpError } = await supabase.auth.signUp({
      email: email.value,
      password: password.value,
      options: {
        data: {
          full_name: name.value,
          subject_expertise: subject.value,
          role: 'Teacher',
        },
      },
    });

    if (signUpError) {
      toast.error(signUpError.message, {
        position: 'top-right',
        timeout: 5000,
      });
      return;
    }

    toast.success('Registration successful! Please check your email for confirmation.', {
      position: 'top-right',
      timeout: 5000,
    });

    router.push('/login');
  } catch (err) {
    toast.error('An error occurred during registration. Please try again.', {
      position: 'top-right',
      timeout: 5000,
    });
    console.error('Registration error:', err);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #f9fafb;
}

.register-card {
  background: white;
  border-radius: 24px;
  padding: 2.5rem;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
  text-align: center;
}

.card-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  background: #f9fafb;
}

.input-wrapper i {
  margin-right: 0.5rem;
  color: #9ca3af;
}

input,
select {
  border: none;
  outline: none;
  background: transparent;
  flex: 1;
  font-size: 1rem;
  color: #374151;
}

.register-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.register-button:hover:not(:disabled) {
  background-color: #4338ca;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.login-link a {
  color: #4f46e5;
  font-weight: 600;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>