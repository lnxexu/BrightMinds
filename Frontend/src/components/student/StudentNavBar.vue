<template>
    <nav class="student-nav-bar">
      <!-- Logo -->
      <div class="logo">
        <router-link to="/" class="logo-link">
          <i class="fas fa-graduation-cap"></i>
          <span>Bright <span class="text-gradient">Minds</span></span>
        </router-link>
      </div>
  
      <!-- Navigation Links -->
      <div class="nav-links">
        <!-- Courses Button -->
        <router-link to="/courses" class="nav-link" :class="{ active: isActive('/courses') }">
          <i class="fas fa-book"></i>
          <span>Courses</span>
        </router-link>
  
        <!-- Messaging Button -->
        <router-link to="/student-message" class="nav-link" :class="{ active: isActive('/messages') }">
          <i class="fas fa-comments"></i>
          <span>Messaging</span>
        </router-link>
  
        <!-- Quizzes Button -->
        <router-link to="/quizzes" class="nav-link" :class="{ active: isActive('/quizzes') }">
          <i class="fas fa-clipboard-list"></i>
          <span>Quizzes</span>
        </router-link>
      </div>
  
      <!-- User Profile Dropdown -->
      <div class="user-profile" @click="toggleProfileMenu">
        <img :src="userAvatar" alt="User Avatar" class="avatar" />
        <span class="username">{{ username }}</span>
        <i class="fas fa-chevron-down"></i>
  
        <!-- Dropdown Menu -->
        <div v-show="showProfileMenu" class="profile-dropdown">
          <router-link to="/profile" class="dropdown-item">
            <i class="fas fa-user"></i>My Profile
          </router-link>
          <router-link to="/settings" class="dropdown-item">
            <i class="fas fa-cog"></i>Settings
          </router-link>
          <button @click="logout" class="dropdown-item logout">
            <i class="fas fa-sign-out-alt"></i>Logout
          </button>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRoute } from 'vue-router';
  
  // Get the current route
  const route = useRoute();
  
  // Function to check if the current route is active
  const isActive = (path) => {
    return route.path === path;
  };
  
  // Mocked user data for demonstration purposes
  const userAvatar = '/default-avatar.png'; // Replace with actual avatar URL
  const username = 'User'; // Replace with actual username
  
  // Profile menu logic
  const showProfileMenu = ref(false);
  const toggleProfileMenu = () => {
    showProfileMenu.value = !showProfileMenu.value;
  };
  
  // Logout logic
  const logout = () => {
    console.log('User logged out');
  };
  </script>
  
  <style scoped>
  .student-nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    background-color: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .logo-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: #374151;
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  .text-gradient {
    background: linear-gradient(135deg, #4f46e5, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .nav-links {
    display: flex;
    gap: 1rem;
  }
  
  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    text-decoration: none;
    color: #374151;
    font-size: 1rem;
    font-weight: 600;
    transition: background-color 0.3s, color 0.3s;
  }
  
  .nav-link i {
    font-size: 1.2rem;
  }
  
  .nav-link:hover {
    background-color: #e5e7eb;
  }
  
  .nav-link.active {
    background-color: #4f46e5;
    color: white;
  }
  
  .user-profile {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    position: relative;
  }
  
  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .username {
    font-size: 1rem;
    font-weight: 600;
    color: #374151;
  }
  
  .profile-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    margin-top: 0.5rem;
    z-index: 10;
    display: flex;
    flex-direction: column;
    width: 200px;
  }
  
  .dropdown-item {
    padding: 0.75rem 1rem;
    text-decoration: none;
    color: #374151;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .dropdown-item:hover {
    background-color: #f3f4f6;
  }
  
  .logout {
    color: #ef4444;
  }
  
  .logout:hover {
    background-color: #fee2e2;
  }
  </style>