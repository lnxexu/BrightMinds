<template>
  <div class="login-container">
    <div class="login-card">
      <div class="card-header">
        <h2 class="card-title">Welcome Back!</h2>
        <p class="card-subtitle">Log in to continue your learning journey</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">

        <div class="form-group">
          <label for="email">Email</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope"></i>
            <input v-model="email" type="email" id="email" placeholder="Enter your email" required />
          </div>
        </div>

        <div class="form-group">
          <div class="password-label">
            <label for="password">Password</label>
            <a href="#" class="forgot-link">Forgot Password?</a>
          </div>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input v-model="password" :type="showPassword ? 'text' : 'password'" id="password"
              placeholder="Enter your password" required />
            <button type="button" class="toggle-password" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>

        <div class="remember-group">
          <label class="remember-label">
            <input type="checkbox" v-model="rememberMe" />
            <span class="checkmark"></span>
            Remember me
          </label>
        </div>

        <button type="submit" class="login-button" :disabled="loading">
          <span>{{ loading ? 'Logging in...' : 'Log In' }}</span>
          <i class="fas fa-arrow-right"></i>
        </button>

        <div class="divider">
          <span>OR</span>
        </div>

        <div class="social-login">
          <p class="divider">Or continue with</p>
          <div class="social-buttons">
            <button type="button" @click="loginWithGoogle" class="google-btn">
              <i class="fab fa-google"></i>
              <span>Google</span>
            </button>
            <button type="button" @click="loginWithFacebook" class="facebook-btn">
              <i class="fab fa-facebook-f"></i>
              <span>Facebook</span>
            </button>
          </div>
        </div>
      </form>

      <p class="signup-text">
        Don't have an account?
        <router-link to="/register" class="signup-link">Sign up</router-link>
      </p>
    </div>
  </div>

  <div v-if="loading" class="loading-spinner">
    Loading...
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { supabase } from '../lib/supabaseClient.js'
import { useToast } from 'vue-toastification';

const router = useRouter();
const store = useStore();
const toast = useToast();

// Form data
const email = ref('');
const password = ref('');
const rememberMe = ref(false);
const showPassword = ref(false);
const loading = ref(false);
const error = ref(null);

const loadGoogleAPI = () => {
  const script = document.createElement('script');
  script.src = 'https://accounts.google.com/gsi/client';
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
};

const initFacebookSDK = () => {
  window.fbAsyncInit = function() {
    FB.init({
      appId: 'YOUR_FACEBOOK_APP_ID', // Replace with your Facebook App ID
      cookie: true,
      xfbml: true,
      version: 'v12.0'
    });
  };

  // Load Facebook SDK
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
};

const loginWithGoogle = async () => {
  // use supabase for Google login
  const { user, session, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: 'http://localhost:3000/courses'
    }
  });

  if (error) {
    console.error('Google login error:', error);
    toast.error('Google login failed. Please try again.');
  } else {
    // Store user data and token in localStorage
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('token', session.access_token);

    // Update Vuex store
    store.commit('setUser', user);
    store.commit('setLoggedIn', true);

    // Navigate to courses page
    router.push('/courses');
  }

};

const loginWithFacebook = async () => {
  // use supabase for Facebook login
  const { user, session, error } = await supabase.auth.signInWithOAuth({
    provider: 'facebook',
    options: {
      redirectTo: 'http://localhost:3000/courses'
    }
  });

  if (error) {
    console.error('Facebook login error:', error);
    toast.error('Facebook login failed. Please try again.');
  } else {
    // Store user data and token in localStorage
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('token', session.access_token);

    // Update Vuex store
    store.commit('setUser', user);
    store.commit('setLoggedIn', true);

    // Navigate to courses page
    router.push('/');
  }

};

const handleLogin = async () => {
  loading.value = true;
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value
    });

    if (error) {
      console.error('Login error:', error);
      toast.error('Login failed. Please check your credentials and try again.');
      return;
    }

    if (data.user && data.session) {
      // Store user data and token in localStorage
      localStorage.setItem('user', JSON.stringify(data.user));
      localStorage.setItem('token', data.session.access_token);

      // Update Vuex store
      store.commit('setUser', data.user);
      store.commit('setLoggedIn', true);

      // Store email if remember me is checked
      if (rememberMe.value) {
        localStorage.setItem('email', email.value);
      }

      // Navigate to courses page
      router.push('/courses');
    }
  } catch (err) {
    console.error('Login error:', err);
    toast.error('An unexpected error occurred. Please try again.');
  } finally {
    loading.value = false;
  }
};

// Load remembered email if exists
if (localStorage.getItem('email')) {
  email.value = localStorage.getItem('email');
  rememberMe.value = true;
}

// Initialize social login SDKs
loadGoogleAPI();
initFacebookSDK();
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.card-header {
  text-align: center;
  margin-bottom: 30px;
}

.card-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
}

.card-subtitle {
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background-color: #fff;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 0 12px;
  transition: border-color 0.3s ease;
}

.input-wrapper i {
  color: #666;
  margin-right: 10px;
}

.input-wrapper input {
  flex: 1;
  border: none;
  padding: 12px 0;
  font-size: 14px;
  background: transparent;
  outline: none;
}

.toggle-password {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: color 0.3s ease;
}

.toggle-password:hover {
  color: #4a90e2;
}

.toggle-password i {
  margin: 0;
  font-size: 16px;
}

.password-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.forgot-link {
  color: #4CAF50;
  font-size: 14px;
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
}

.remember-group {
  display: flex;
  align-items: center;
  margin: 16px 0;
}

.remember-label {
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 28px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  user-select: none;
}

.remember-label input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  left: 0;
  height: 18px;
  width: 18px;
  background-color: #fff;
  border: 2px solid #ddd;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.remember-label:hover input ~ .checkmark {
  border-color: #4a90e2;
}

.remember-label input:checked ~ .checkmark {
  background-color: #4a90e2;
  border-color: #4a90e2;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.remember-label input:checked ~ .checkmark:after {
  display: block;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #45a049;
}

.login-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #4CAF50;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.divider {
  position: relative;
  text-align: center;
  margin: 20px 0;
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

.social-buttons {
  display: flex;
  gap: 1rem;
}

.google-btn, .facebook-btn {
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
}

.google-btn:hover, .facebook-btn:hover {
  background: #f8fafc;
  transform: translateY(-2px);
}

.google-btn i, .facebook-btn i {
  font-size: 1.25rem;
}

.google-btn i {
  color: #ea4335;
}

.facebook-btn i {
  color: #1877f2;
}

.signup-text {
  text-align: center;
  color: #6b7280;
  margin-top: 2rem;
}

.signup-link {
  color: #4f46e5;
  font-weight: 500;
  text-decoration: none;
}

.signup-link:hover {
  text-decoration: underline;
}

.loading-spinner {
  text-align: center;
  color: #4f46e5;
  margin-bottom: 1rem;
}
</style>