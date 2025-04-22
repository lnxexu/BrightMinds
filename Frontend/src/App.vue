<template>
  <div id="app" class="min-h-screen flex flex-col bg-gradient">
    <header class="header">
      <div class="navbar">
        <!-- Logo -->
        <div class="logo">
          <router-link to="/home" class="logo-link">
            <i class="fas fa-graduation-cap"></i>
            <span>Bright <span class="text-gradient">Minds</span></span>
          </router-link>
        </div>

        <!-- Navigation Links - Only Visible When Logged In -->
        <nav v-if="isLoggedIn" class="nav-links">
          <router-link 
            v-for="link in allowedNavLinks" 
            :key="link.path" 
            :to="link.path" 
            class="nav-link"
          >
            <i :class="link.icon"></i>
            <span>{{ link.label }}</span>
          </router-link>
        </nav>

        <!-- Login status indicator -->
        <div v-if="isLoggedIn" class="login-status">
          <span class="status-indicator"></span>
          <span class="status-text">{{ userRoleDisplay }}</span>
        </div>

        <!-- Auth Buttons -->
        <div class="nav-buttons">
          <template v-if="!isLoggedIn">
            <router-link to="/" class="auth-button login"><i class="fas fa-sign-in-alt"></i><span>Login</span></router-link>
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
      
      <!-- Logout Confirmation Modal -->
      <div v-if="showLogoutModal" class="modal-overlay" @click.self="cancelLogout">
        <div class="modal-container">
          <div class="modal-header">
            <h3>Confirm Logout</h3>
            <button class="close-button" @click="cancelLogout">&times;</button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to logout from your {{ userRoleDisplay }} account?</p>
          </div>
          <div class="modal-footer">
            <button class="cancel-button" @click="cancelLogout">Cancel</button>
            <button class="confirm-button" @click="confirmLogout">Logout</button>
          </div>
        </div>
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
import MessagingComponent from "./components/MessagingComponent.vue";
import { supabase } from "./lib/supabaseClient";
import router from "./router";

export default {
  name: "App",
  components: { MessagingComponent },
  data() {
    return {
      isLoggedIn: false,
      user: null,
      showProfileMenu: false,
      userAvatar: "/default-avatar.png",
      username: "User",
      userRole: "",
      showChat: false,
      hasUnreadMessage: false,
      chatRecipient: null,
      showLogoutModal: false,
      navLinks: [
        { 
          path: "/courses", 
          icon: "fas fa-book", 
          label: "Courses", 
          allowedRoles: ["student", "teacher", "admin"] 
        },
        { 
          path: "/messages", 
          icon: "fas fa-comments", 
          label: "Messaging", 
          allowedRoles: ["student", "teacher", "parent", "admin"] 
        },
        { 
          path: "/quiz-creator", 
          icon: "fas fa-tasks", 
          label: "Quiz Creator", 
          allowedRoles: ["teacher", "admin"] 
        },
        { 
          path: "/parent", 
          icon: "fas fa-user-shield", 
          label: "Parent Dashboard", 
          allowedRoles: ["parent", "admin"] 
        },
        { 
          path: "/stream", 
          icon: "fas fa-bullhorn", 
          label: "Stream", 
          allowedRoles: ["student", "teacher", "admin"] 
        },
        {
          path: "/admin", 
          icon: "fas fa-cogs", 
          label: "Admin Panel", 
          allowedRoles: ["admin"] 
        }
      ]
    };
  },
  computed: {
    allowedNavLinks() {
      // If no role is specified, show no links
      if (!this.userRole) return [];
      
      // Filter links based on user role
      return this.navLinks.filter(link => 
        link.allowedRoles.includes(this.userRole)
      );
    },
    userRoleDisplay() {
      // Capitalize first letter of role for display
      return this.userRole ? 
        this.userRole.charAt(0).toUpperCase() + this.userRole.slice(1) : 
        'User';
    }
  },
  methods: {
    async checkAuthStatus() {
      try {
        const { data: { session } } = await supabase.auth.getSession();
        
        if (session) {
          this.isLoggedIn = true;
          this.fetchUserData();
        } else {
          this.isLoggedIn = false;
          this.user = null;
        }
      } catch (error) {
        console.error("Error checking auth status:", error);
        this.isLoggedIn = false;
        this.user = null;
      }
    },
    
    async fetchUserData() {
      try {
        const { data: { user } } = await supabase.auth.getUser();
        
        if (!user) {
          console.error("User not found in Supabase");
          this.isLoggedIn = false;
          this.user = null;
          return;
        }
        
        // User exists in auth, update local state
        this.user = user;
        this.isLoggedIn = true;
        
        // Fetch profile details including role
        const { data, error } = await supabase
          .from("profiles")
          .select("avatar_url, full_name, role, username")
          .eq("id", user.id)
          .single();

        if (error) {
          console.error("Error fetching user data:", error);
        } else {
          this.userAvatar = data.avatar_url || "/default-avatar.png";
          this.username = data.username || data.full_name.split(" ")[0] || "User";
          this.userRole = data.role || "";
          
          console.log("User data fetched:", data);
        }
      } catch (error) {
        console.error("Error in fetchUserData:", error);
      }
    },
    
    toggleProfileMenu() {
      this.showProfileMenu = !this.showProfileMenu;
    },
    
    logout() {
      // Show the logout confirmation modal
      this.showLogoutModal = true;
      // Hide profile menu when showing logout modal
      this.showProfileMenu = false;
    },
    
    cancelLogout() {
      // Close the modal without logging out
      this.showLogoutModal = false;
    },
    
    async confirmLogout() {
      try {
        await supabase.auth.signOut();
        this.isLoggedIn = false;
        this.user = null;
        this.userRole = "";
        this.showLogoutModal = false;
        router.push("/");
      } catch (error) {
        console.error("Error logging out:", error);
      }
    },
    
    toggleChatHead() {
      this.showChat = !this.showChat;
    },
    
    clearUnread() {
      this.hasUnreadMessage = false;
    },
    
    // Method to check if user has access to a specific route
    hasRouteAccess(routePath) {
      const route = this.navLinks.find(link => link.path === routePath);
      if (!route) return true; // If route not in navLinks, assume it's public
      return this.userRole && route.allowedRoles.includes(this.userRole);
    }
  },
  
  async created() {
    // Set up auth state change listener
    supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_IN' && session) {
        this.isLoggedIn = true;
        this.fetchUserData();
      } else if (event === 'SIGNED_OUT') {
        this.isLoggedIn = false;
        this.user = null;
        this.userRole = "";
      }
    });
    
    // Initial auth check
    await this.checkAuthStatus();
  }
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
  width: 500px;
  max-height: 600px;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 400px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid rgba(79, 70, 229, 0.1);
}

.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.25rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
}

.modal-body {
  padding: 1.25rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 1.25rem;
  gap: 0.75rem;
  border-top: 1px solid rgba(79, 70, 229, 0.1);
}

.cancel-button {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: var(--secondary);
  color: var(--text-secondary);
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-button {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: #ef4444;
  color: white;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-button:hover {
  background: #e5e7eb;
}

.confirm-button:hover {
  background: #dc2626;
}

/* Add to the style section */

.login-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 1rem;
  background: rgba(79, 70, 229, 0.1);
  border-radius: 16px;
}

.status-indicator {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
}

.status-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--primary);
}
</style>
