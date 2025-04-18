<template>
  <div id="app" class="min-h-screen flex flex-col bg-gradient">
    <header class="header">
      <div class="navbar">
        <!-- Logo -->
        <div class="logo">
          <router-link to="/" class="logo-link">
            <i class="fas fa-graduation-cap"></i>
            <span>Bright <span class="text-gradient">Minds</span></span>
          </router-link>
        </div>

        <!-- Navigation Links - Only Visible When Logged In -->
        <nav v-if="isLoggedIn" class="nav-links">
          <router-link to="/courses" class="nav-link">
            <i class="fas fa-book"></i>
            <span>Courses</span>
          </router-link>
          <router-link to="/messages" class="nav-link">
            <i class="fas fa-comments"></i>
            <span>Messaging</span>
          </router-link>
          <router-link to="/quiz-creator" class="nav-link">
            <i class="fas fa-tasks"></i>
            <span>Quiz Creator</span>
          </router-link>
          <router-link to="/parent" class="nav-link">
            <i class="fas fa-user-shield"></i>
            <span>Parent Dashboard</span>
          </router-link>
          <router-link to="/stream" class="nav-link">
            <i class="fas fa-bullhorn"></i>
            <span>Stream</span>
          </router-link>
        </nav>

        <!-- Auth Buttons -->
        <div class="nav-buttons">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="auth-button login"><i class="fas fa-sign-in-alt"></i><span>Login</span></router-link>
            <router-link to="/register" class="auth-button register"><i class="fas fa-user-plus"></i><span>Register</span></router-link>
          </template>
          <template v-else>
            <div class="user-profile" @click="toggleProfileMenu">
              <img :src="userAvatar" alt="User Avatar" class="avatar" />
              <span class="username">{{ username }}</span>
              <i class="fas fa-chevron-down"></i>

              <!-- Dropdown Menu -->
              <div v-show="showProfileMenu" class="profile-dropdown">
                <router-link to="/profile" class="dropdown-item"><i class="fas fa-user"></i>My Profile</router-link>
                <router-link to="/settings" class="dropdown-item"><i class="fas fa-cog"></i>Settings</router-link>
                <button @click="logout" class="dropdown-item logout"><i class="fas fa-sign-out-alt"></i>Logout</button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <div><component :is="Component" /></div>
        </transition>
      </router-view>

      <!-- Floating Chat Head - Now visible everywhere when logged in -->
      <div v-if="isLoggedIn && $route.path !== '/messages'" class="chat-head">
        <button class="chat-toggle" @click="toggleChatHead">
          <i class="fas fa-comments"></i>
          <span v-if="hasUnreadMessage && !showChat" class="notification-dot"></span>
        </button>
        <MessagingComponent
          v-if="showChat"
          class="chat-box"
          v-model="chatRecipient"
          @opened="clearUnread"
        />
      </div>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p class="copyright">
          © 2025 Bright Minds Elementary School. All Rights Reserved.
        </p>
        <div class="social-links">
          <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
          <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
          <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { mapState } from "vuex";
import MessagingComponent from "./components/MessagingComponent.vue";

export default {
  name: "App",
  components: { MessagingComponent },
  data() {
    return {
      showProfileMenu: false,
      userAvatar: "/default-avatar.png", // Add a default avatar path
      username: "User", // Add a default username
      showChat: false, // Chat visibility state
      hasUnreadMessage: false, // Unread message state
      chatRecipient: null, // Chat recipient state
    };
  },
  computed: {
    ...mapState({
      isLoggedIn: (state) => state.isLoggedIn,
    }),
  },
  methods: {
    toggleProfileMenu() {
      this.showProfileMenu = !this.showProfileMenu;
    },
    logout() {
      this.$store.dispatch("logout");
      this.showProfileMenu = false;
      this.$router.push("/login");
    },
    toggleChatHead() {
      this.showChat = !this.showChat;
    },
    clearUnread() {
      this.hasUnreadMessage = false;
    },
  },
  created() {
    // Check auth state when app loads
    this.$store.dispatch("checkAuthState").then(() => {
      // If user is on a protected route and not logged in, redirect to login
      if (this.$route.meta.requiresAuth && !this.isLoggedIn) {
        this.$router.push("/login");
      }
      // If user is on a guest route and logged in, redirect to home
      else if (this.$route.meta.requiresGuest && this.isLoggedIn) {
        this.$router.push("/");
      }
    });

    // Retrieve the user's first name from localStorage
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const user = JSON.parse(storedUser);
      this.username = user.user_metadata?.full_name?.split(" ")[0] || "User";
    }
  },
};
</script>


<style>


/* Modern color variables */
:root {
  --primary: #4f46e5;
  --primary-light: #818cf8;
  --primary-dark: #4338ca;
  --secondary: #f8fafc;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}

/* Global styles */
body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
  margin: 0;
  padding: 0;
}

.bg-gradient {
  background: var(--bg-gradient);
}

/* Header styles */
.header {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar {
  width: 100%;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo styles */
.logo-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-primary);
}

.logo-link i {
  font-size: 1.75rem;
  color: var(--primary);
  filter: drop-shadow(0 2px 4px rgba(79, 70, 229, 0.2));
}

.text-gradient {
  background: linear-gradient(135deg,
      var(--primary) 0%,
      var(--primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Navigation links */
.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link i {
  font-size: 1.1rem;
  transition: transform 0.3s ease;
}

.nav-link:hover {
  color: var(--primary);
  background: rgba(79, 70, 229, 0.08);
  transform: translateY(-1px);
}

.nav-link:hover i {
  transform: scale(1.1);
}

.router-link-active {
  color: var(--primary);
  font-weight: 600;
}

/* Auth buttons */
.nav-buttons {
  display: flex;
  gap: 1rem;
}

.auth-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
}

.auth-button.login {
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.auth-button.register {
  background: var(--primary);
  color: white;
  border: none;
}

.auth-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
}

.auth-button.login:hover {
  background: rgba(79, 70, 229, 0.08);
}

.auth-button.register:hover {
  background: var(--primary-dark);
}

.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.user-profile:hover {
  background: rgba(79, 70, 229, 0.08);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  font-weight: 600;
  color: var(--text-primary);
}

.profile-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  margin-top: 0.5rem;
  z-index: 100;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s ease;
}

.dropdown-item:hover {
  background: rgba(79, 70, 229, 0.08);
  color: var(--primary);
}

.dropdown-item.logout {
  border-top: 1px solid #e5e7eb;
  color: #ef4444;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
}

.dropdown-item.logout:hover {
  background: #fef2f2;
}

/* Responsive adjustments for profile */
@media (max-width: 640px) {
  .username {
    display: none;
  }

  .user-profile {
    padding: 0.5rem;
  }
}

/* Main content */
.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1440px;
  margin: 0 auto;
  width: 100%;
}

/* Footer styles */
.footer {
  background: white;
  border-top: 1px solid rgba(79, 70, 229, 0.1);
  padding: 2rem 0;
}

.footer-content {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.copyright {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.social-links {
  display: flex;
  gap: 1.5rem;
}

.social-link {
  color: var(--text-secondary);
  font-size: 1.25rem;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--secondary);
}

.social-link:hover {
  color: var(--primary);
  background: rgba(79, 70, 229, 0.08);
  transform: translateY(-2px);
}

/* Page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive design */
@media (max-width: 1024px) {
  .navbar {
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-buttons {
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .nav-link span {
    display: none;
  }

  .nav-link {
    padding: 0.75rem;
  }

  .nav-link i {
    font-size: 1.25rem;
  }

  .auth-button span {
    display: none;
  }

  .auth-button {
    padding: 0.75rem;
  }

  .auth-button i {
    margin: 0;
    font-size: 1.25rem;
  }

  .footer-content {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }

  .social-links {
    justify-content: center;
  }
}
.chat-head {
  position: fixed;
  bottom: 100px;
  right: 30px;
  z-index: 1000;
}

.chat-toggle {
  background: var(--primary);
  border: none;
  color: white;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s ease;
}

.chat-toggle:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.notification-dot {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 10px;
  height: 10px;
  background: red;
  border-radius: 50%;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.chat-box {
  margin-top: 1rem;
  width: 400px;
  max-height: 600px;
}
</style>
