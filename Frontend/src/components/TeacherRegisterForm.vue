<template>
    <div class="teacher-register-container">
      <h2>Teacher Registration</h2>
      <form @submit.prevent="handleTeacherRegister">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input v-model="name" type="text" id="name" placeholder="Enter your full name" required />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="email" type="email" id="email" placeholder="Enter your email" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" id="password" placeholder="Create a password" required />
        </div>
        <div class="form-group">
          <label for="subject">Subject Expertise</label>
          <select v-model="subject" id="subject" required>
            <option value="" disabled>Select your subject expertise</option>
            <option v-for="course in courses" :key="course.id" :value="course.name">
              {{ course.name }}
            </option>
          </select>
        </div>
        <button type="submit" class="register-button">Register</button>
      </form>
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
      // Fetch course_id and name from the courses table
      const { data, error } = await supabase.from('courses').select('course_id, name');
      if (error) {
        console.error('Error fetching courses:', error.message, error.details);
        return;
      }
      // Map course_id to id for consistency in the dropdown
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
  
      // Register the teacher with Supabase Auth
      const { user, error: signUpError } = await supabase.auth.signUp({
        email: email.value,
        password: password.value,
        options: {
          data: {
            full_name: name.value,
            subject_expertise: subject.value, // Add subject expertise to user metadata
            role: 'Teacher', // Add role to user metadata
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
  
      // Inform the user to verify their email
      toast.success('Registration successful! Please check your email for confirmation.', {
        position: 'top-right',
        timeout: 5000,
      });
  
      // Redirect to the login page
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
  .teacher-register-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
    background-color: #f5f5f5;
  }
  
  h2 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
    width: 100%;
    max-width: 400px;
  }
  
  input,
  select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
  }
  
  .register-button {
    padding: 0.75rem 1.5rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .register-button:hover {
    background-color: #45a049;
  }
  </style>