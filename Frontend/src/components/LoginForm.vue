<template>
  <div class="login-container">
    <div class="login-card">
      <div class="card-header">
        <h2 class="card-title">Welcome Back!</h2>
        <p class="card-subtitle">Log in to continue your learning journey</p>
      </div>

      <form @submit.prevent="login" class="login-form">
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

        <button type="submit" class="login-button">
          <span>Log In</span>
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
        <a href="#" class="signup-link">Sign up</a>
      </p>
    </div>
  </div>

  <div v-if="error" class="error-message">
    {{ error }}
  </div>

  <div v-if="loading" class="loading-spinner">
    Loading...
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'LoginForm',
  setup() {
    const store = useStore();
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const showPassword = ref(false);
    const error = ref('');
    const loading = ref(false);

    const isLoggedIn = computed(() => store.state.isLoggedIn);
    const currentUser = computed(() => store.state.currentUser);

    // Load the Google API
    const loadGoogleAPI = () => {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      document.head.appendChild(script);
    };

    // Initialize Facebook SDK
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
      try {
        const client = google.accounts.oauth2.initTokenClient({
          client_id: 'YOUR_GOOGLE_CLIENT_ID', // Replace with your Google Client ID
          scope: 'email profile',
          callback: async (response) => {
            if (response.access_token) {
              const result = await fetch('http://127.0.0.1:8000/oauth/auth/google', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  access_token: response.access_token,
                  provider: 'google'
                })
              });

              const data = await result.json();
              if (data.success) {
                store.commit('setToken', data.token);
                store.commit('setUser', data.user);
                store.commit('setLoggedIn', true);
                router.push('/courses');
              } else {
                error.value = data.error_message || 'Failed to login with Google';
              }
            }
          },
        });
        client.requestAccessToken();
      } catch (err) {
        error.value = 'Failed to initialize Google login';
        console.error(err);
      }
    };

    const loginWithFacebook = async () => {
      try {
        FB.login(async function(response) {
          if (response.authResponse) {
            const result = await fetch('http://127.0.0.1:8000/oauth/auth/facebook', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                access_token: response.authResponse.accessToken,
                provider: 'facebook'
              })
            });

            const data = await result.json();
            if (data.success) {
              store.commit('setToken', data.token);
              store.commit('setUser', data.user);
              store.commit('setLoggedIn', true);
              router.push('/courses');
            } else {
              error.value = data.error_message || 'Failed to login with Facebook';
            }
          } else {
            error.value = 'Facebook login was cancelled';
          }
        }, { scope: 'public_profile,email' });
      } catch (err) {
        error.value = 'Failed to initialize Facebook login';
        console.error(err);
      }
    };

    // Regular email/password login
    const login = async () => {
      try {
        // Reset error state
        error.value = null;

        // Basic validation
        if (!email.value || !password.value) {
          error.value = "Please fill in all fields";
          return;
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
          error.value = "Please enter a valid email address";
          return;
        }

        // Set loading state
        loading.value = true;

        // Make API call to backend
        const response = await axios.get('http://127.0.0.1:8000/users/verify', {
          params: {
            email: email.value,
            password: password.value
          }
        });

        const data = response.data;

        // Update Vuex store with correct mutations
        store.commit('login', data); // Sets currentUser
        store.commit('setLoginState', true); // Sets isLoggedIn

        // Store token if present
        if (data.token) {
          localStorage.setItem('token', data.token);
        }

        // Remember email if checkbox is checked
        if (rememberMe.value) {
          localStorage.setItem('email', email.value);
        }

        // Emit login event
        // this.$emit('login-success', data);

        // Redirect to courses page
        router.push('/courses');

      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'An error occurred during login';
        console.error('Login error:', err);
      } finally {
        loading.value = false;
      }
    };

    loadGoogleAPI();
    initFacebookSDK();

    return {
      email,
      password,
      showPassword,
      rememberMe: ref(false),
      error,
      loading,
      login,
      loginWithGoogle,
      loginWithFacebook
    };
  },
  mounted() {
    // Check if there's a remembered email
    const rememberedEmail = localStorage.getItem('email');
    if (rememberedEmail) {
      this.email = rememberedEmail;
      this.rememberMe = true;
    }
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
  padding: 2rem;
}

.login-card {
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

.password-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.forgot-link {
  color: #4f46e5;
  font-size: 0.875rem;
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
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

.remember-group {
  margin-bottom: 1.5rem;
}

.remember-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4b5563;
  cursor: pointer;
}

.login-button {
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
  transition: all 0.3s ease;
}

.login-button:hover {
  background: #4338ca;
  transform: translateY(-2px);
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

.error-message {
  background-color: #fef2f2;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}

.loading-spinner {
  text-align: center;
  color: #4f46e5;
  margin-bottom: 1rem;
}

.login-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 640px) {
  .login-card {
    padding: 2rem;
  }

  .card-title {
    font-size: 1.75rem;
  }
}
</style>