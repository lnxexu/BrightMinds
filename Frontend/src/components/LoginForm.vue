<template>
  <div class="login-container">
    <div class="login-card">
      <div class="card-header">
        <h2 class="card-title">Welcome Back!</h2>
        <p class="card-subtitle">Log in to continue your learning journey</p>
      </div>

      <form @submit.prevent="login" class="login-form">
        <!-- Removed old error display div since we're using Toast now -->

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

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'LoginForm',
  setup() {
    const router = useRouter();
    const store = useStore();
    
    // Form data
    const email = ref('');
    const password = ref('');
    const rememberMe = ref(false);
    const showPassword = ref(false);
    const loading = ref(false);
    
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
                store.commit('setUser', data.user);
                store.commit('setLoggedIn', true);
                router.push('/courses');
              } else {
                // Removed local toast handling
              }
            }
          },
        });
        client.requestAccessToken();
      } catch (err) {
        // Removed local toast handling
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
              store.commit('setUser', data.user);
              store.commit('setLoggedIn', true);
              router.push('/courses');
            } else {
              // Removed local toast handling
            }
          } else {
            // Removed local toast handling
          }
        }, { scope: 'public_profile,email' });
      } catch (err) {
        // Removed local toast handling
        console.error(err);
      }
    };

    const login = async () => {
      try {
        // Reset states
        loading.value = true;

        // Basic validation
        if (!email.value || !password.value) {
          // Removed local toast handling
          return;
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
          // Removed local toast handling
          return;
        }

        // Make API call to backend
        const response = await fetch(`http://127.0.0.1:8000/login/${encodeURIComponent(email.value)}/${encodeURIComponent(password.value)}`);
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.detail || "Invalid email or password");
        }

        // Get user's full name and split to get first name
        const fullName = data.user.full_name || '';
        const firstName = fullName.split(' ')[0];

        // Update Vuex store with user data including first name
        store.commit('setUser', { ...data.user, firstName });
        store.commit('setLoggedIn', true);

        // Store email if remember me is checked
        if (rememberMe.value) {
          localStorage.setItem('email', email.value);
        } else {
          localStorage.removeItem('email');
        }

        // Navigate to courses page
        router.push('/courses');

      } catch (err) {
        // Removed local toast handling
        console.error('Login error:', err);
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

    return {
      email,
      password,
      showPassword,
      loading,
      rememberMe,
      login,
      loginWithGoogle,
      loginWithFacebook
    };
  }
});
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
}

.input-wrapper i {
  position: absolute;
  left: 12px;
  color: #666;
}

input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
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

.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
}

.remember-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.remember-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
  color: #666;
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