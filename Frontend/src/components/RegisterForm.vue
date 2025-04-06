<template>
  <div class="register-container">
    <div class="register-card">
      <div class="card-header">
        <h2 class="card-title">Create Account</h2>
        <p class="card-subtitle">Join us to start your learning journey</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <!-- Name Field -->
        <div class="form-group">
          <label for="name">Full Name</label>
          <div class="input-wrapper" :class="{ 'error': validationErrors.name }">
            <i class="fas fa-user"></i>
            <input v-model.trim="name" type="text" id="name" placeholder="Enter your full name" required />
          </div>
          <span v-if="validationErrors.name" class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            {{ validationErrors.name }}
          </span>
        </div>

        <!-- Email Field -->
        <div class="form-group">
          <label for="email">Email Address</label>
          <div class="input-wrapper" :class="{ 'error': validationErrors.email }">
            <i class="fas fa-envelope"></i>
            <input v-model.trim="email" type="email" id="email" placeholder="Enter your email" required />
          </div>
          <span v-if="validationErrors.email" class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            {{ validationErrors.email }}
          </span>
        </div>

        <!-- Password Field -->
        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-wrapper" :class="{ 'error': validationErrors.password }">
            <i class="fas fa-lock"></i>
            <input v-model="password" :type="showPassword ? 'text' : 'password'" id="password"
              placeholder="Create a strong password" required />
            <button type="button" class="toggle-password" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span v-if="validationErrors.password" class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            {{ validationErrors.password }}
          </span>
        </div>

        <!-- Confirm Password Field -->
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <div class="input-wrapper" :class="{ 'error': passwordMismatch }">
            <i class="fas fa-lock"></i>
            <input v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" id="confirmPassword"
              placeholder="Re-enter your password" required />
            <button type="button" class="toggle-password" @click="showConfirmPassword = !showConfirmPassword">
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span v-if="passwordMismatch" class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            Passwords do not match
          </span>
        </div>

        <!-- Password Requirements -->
        <div class="password-requirements">
          <p class="requirements-title">Password must contain:</p>
          <ul>
            <li :class="{ 'met': password.length >= 8 }">
              <i :class="password.length >= 8 ? 'fas fa-check' : 'fas fa-times'"></i>
              At least 8 characters
            </li>
            <li :class="{ 'met': /[A-Z]/.test(password) }">
              <i :class="/[A-Z]/.test(password) ? 'fas fa-check' : 'fas fa-times'"></i>
              One uppercase letter
            </li>
            <li :class="{ 'met': /[a-z]/.test(password) }">
              <i :class="/[a-z]/.test(password) ? 'fas fa-check' : 'fas fa-times'"></i>
              One lowercase letter
            </li>
            <li :class="{ 'met': /\d/.test(password) }">
              <i :class="/\d/.test(password) ? 'fas fa-check' : 'fas fa-times'"></i>
              One number
            </li>
            <li :class="{ 'met': /[@$!%*?&]/.test(password) }">
              <i :class="/[@$!%*?&]/.test(password) ? 'fas fa-check' : 'fas fa-times'"></i>
              One special character
            </li>
          </ul>
        </div>

        <!-- General Error Message -->
        <div v-if="error" class="general-error">
          <i class="fas fa-exclamation-triangle"></i>
          {{ error }}
        </div>

        <!-- Submit Button -->
        <button type="submit" class="submit-button" :disabled="isLoading || passwordMismatch">
          <span v-if="isLoading">
            <i class="fas fa-spinner fa-spin"></i>
            Creating Account...
          </span>
          <span v-else>
            Create Account
            <i class="fas fa-arrow-right"></i>
          </span>
        </button>

        <div class="divider">
          <span>OR</span>
        </div>

        <!-- Social Login Buttons -->
        <div class="social-login">
          <button type="button" class="social-button google" @click="registerWithGoogle" :disabled="isLoading">
            <i class="fab fa-google"></i>
            <span>Continue with Google</span>
          </button>
          <button type="button" class="social-button facebook" @click="registerWithFacebook" :disabled="isLoading">
            <i class="fab fa-facebook-f"></i>
            <span>Continue with Facebook</span>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { supabase } from '../lib/supabaseClient.js'; 
import { useToast } from 'vue-toastification'; 
// Reactive state
const toast = useToast();
const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const isLoading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const error = ref(null);
const validationErrors = ref({
  name: null,
  email: null,
  password: null
});

// Computed properties
const passwordMismatch = computed(() => {
  return password.value !== confirmPassword.value && confirmPassword.value.length > 0;
});

// Methods
const validateForm = () => {
  let isValid = true;
  validationErrors.value = {
    name: null,
    email: null,
    password: null
  };

  // Name validation
  if (name.value.trim().length < 2) {
    validationErrors.value.name = "Name must be at least 2 characters long";
    isValid = false;
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    validationErrors.value.email = "Please enter a valid email address";
    isValid = false;
  }

  // Password validation
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  if (!passwordRegex.test(password.value)) {
    validationErrors.value.password = "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character";
    isValid = false;
  }

  // Confirm password validation
  if (passwordMismatch.value) {
    isValid = false;
  }

  return isValid;
};

const handleRegister = async () => {
  if (!validateForm()) {
    return;
  }

  try {
    isLoading.value = true;
    const { user, error: signUpError } = await supabase.auth.signUp({
      email: email.value,
      password: password.value,
      options: {
        data: {
          full_name: name.value
        }
      }
    });

    if (signUpError) {
       toast.error(signUpError.message, {
        position: 'top-right',
        timeout: 5000,
      });
    }

    // Handle successful registration (e.g., redirect to login page or show success message)
    toast.success('Registration successful! Please check your email for confirmation.', {
      position: 'top-right',
      timeout: 5000,
    });

    // goes to the login page after successful registration
    router.push('/login');
  } catch (err) {
    toast.error('An error occurred during registration. Please try again.', {
      position: 'top-right',
      timeout: 5000,
    });
    console.log(email.value, password.value, name.value);
    error.value = 'Failed to register. Please try again.';
  } finally {
    isLoading.value = false;
  }


};

const registerWithGoogle = async () => {
  try {
    isLoading.value = true;
    // Implement Google OAuth registration
    console.log('Google registration not implemented');
  } catch (err) {
    console.error('Google registration error:', err);
    error.value = 'Failed to register with Google';
  } finally {
    isLoading.value = false;
  }
};

const registerWithFacebook = async () => {
  try {
    isLoading.value = true;
    // Implement Facebook OAuth registration
    console.log('Facebook registration not implemented');
  } catch (err) {
    console.error('Facebook registration error:', err);
    error.value = 'Failed to register with Facebook';
  } finally {
    isLoading.value = false;
  }
};

// Define emits
const emit = defineEmits(['register-success']);

</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-card {
  background: white;
  border-radius: 24px;
  padding: 2.5rem;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.card-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.input-wrapper i {
  color: #6b7280;
  margin-right: 0.75rem;
}

.input-wrapper input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 1rem;
  color: #1f2937;
}

.input-wrapper input:focus {
  outline: none;
}

.toggle-password {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.submit-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 45%;
  height: 1px;
  background: #e5e7eb;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background: white;
  padding: 0 1rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.social-login {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.social-button {
  width: 100%;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
  background: white;
  color: #374151;
  cursor: pointer;
}

.social-button:hover {
  background: #f8fafc;
  transform: translateY(-2px);
}

.social-button i {
  font-size: 1.25rem;
}

.social-button.google i {
  color: #ea4335;
}

.social-button.facebook i {
  color: #1877f2;
}

.login-link {
  text-align: center;
  color: #6b7280;
  margin-top: 2rem;
}

.login-link a {
  color: #4f46e5;
  font-weight: 500;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

.general-error {
  background-color: #fef2f2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-message {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-message i {
  font-size: 1rem;
}

.input-wrapper.error {
  border-color: #dc2626;
  background-color: #fef2f2;
}

.password-requirements {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #f8fafc;
  border-radius: 8px;
}

.requirements-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 0.5rem;
}

.password-requirements ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.password-requirements li {
  font-size: 0.875rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.password-requirements li.met {
  color: #059669;
}

.password-requirements li i {
  font-size: 0.75rem;
}

.password-requirements li.met i {
  color: #059669;
}

.general-error {
  background-color: #fef2f2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.fa-spinner {
  margin-right: 0.5rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.social-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 640px) {
  .register-card {
    padding: 2rem;
    margin: 1rem;
  }

  .card-title {
    font-size: 1.75rem;
  }
}
</style>