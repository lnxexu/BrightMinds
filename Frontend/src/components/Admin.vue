<template>
  <div class="admin-container">
    <!-- Admin Sidebar -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <h2 v-if="!sidebarCollapsed">BrightMinds</h2>
        <div class="logo-icon">BM</div>
        <button class="toggle-sidebar" @click="toggleSidebar">
          <i :class="sidebarCollapsed ? 'fas fa-angle-right' : 'fas fa-angle-left'"></i>
        </button>
      </div>

      <div class="sidebar-menu">
        <div 
          v-for="(item, index) in sidebarItems" 
          :key="index" 
          class="sidebar-item" 
          :class="{ active: currentView === item.id }"
          @click="changeView(item.id)"
        >
          <i :class="item.icon"></i>
          <span v-if="!sidebarCollapsed">{{ item.label }}</span>
        </div>
      </div>

      <div class="sidebar-footer" v-if="!sidebarCollapsed">
        <div class="admin-profile">
          <img :src="adminProfile.avatar_url || 'https://via.placeholder.com/40'" alt="Admin" class="admin-avatar" />
          <div class="admin-info">
            <p class="admin-name">{{ adminProfile.full_name }}</p>
            <p class="admin-role">Administrator</p>
          </div>
        </div>
        <button class="logout-button" @click="logout">
          <i class="fas fa-sign-out-alt"></i> Logout
        </button>
      </div>
      
      <div class="sidebar-footer-collapsed" v-else>
        <button class="logout-button-icon" @click="logout">
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </div>
    </div>

    <!-- Admin Main Content -->
    <div class="main-content">
      <!-- Header -->
      <header class="admin-header">
        <div class="search-container">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            placeholder="Search..." 
            v-model="searchQuery"
            @keyup.enter="handleSearch"
          />
        </div>
        <div class="header-actions">
          <button class="action-button">
            <i class="fas fa-bell"></i>
            <span class="notification-badge" v-if="notifications.length > 0">{{ notifications.length }}</span>
          </button>
          <button class="action-button" @click="refreshData">
            <i class="fas fa-sync-alt"></i>
          </button>
        </div>
      </header>

      <!-- Main Views -->
      <div class="content-wrapper">
        <!-- Dashboard View -->
        <div v-if="currentView === 'dashboard'" class="dashboard-view">
          <h1>Admin Dashboard</h1>
          
          <div class="stats-cards">
            <div class="stat-card">
              <div class="stat-icon users-icon">
                <i class="fas fa-users"></i>
              </div>
              <div class="stat-details">
                <h3>{{ loading ? '...' : userStats.totalUsers }}</h3>
                <p>Total Users</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon courses-icon">
                <i class="fas fa-book"></i>
              </div>
              <div class="stat-details">
                <h3>{{ loading ? '...' : courseStats.totalCourses }}</h3>
                <p>Active Courses</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon quizzes-icon">
                <i class="fas fa-question-circle"></i>
              </div>
              <div class="stat-details">
                <h3>{{ loading ? '...' : quizStats.totalQuizzes }}</h3>
                <p>Published Quizzes</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon submissions-icon">
                <i class="fas fa-clipboard-check"></i>
              </div>
              <div class="stat-details">
                <h3>{{ loading ? '...' : submissionStats.totalSubmissions }}</h3>
                <p>Quiz Submissions</p>
              </div>
            </div>
          </div>
          
          <div class="dashboard-charts">
            <div class="chart-container">
              <h2>User Registration</h2>
              <div class="chart-placeholder">
                <p>User growth chart would display here</p>
                <!-- In a real implementation, you would integrate a chart library like Chart.js -->
              </div>
            </div>
            
            <div class="chart-container">
              <h2>Recent Activity</h2>
              <div class="recent-activity">
                <div v-if="loading" class="loading-spinner">Loading...</div>
                <div v-else-if="recentActivity.length === 0" class="no-data">
                  No recent activity to display
                </div>
                <div v-else class="activity-list">
                  <div v-for="(activity, index) in recentActivity" :key="index" class="activity-item">
                    <div class="activity-icon">
                      <i :class="getActivityIcon(activity.type)"></i>
                    </div>
                    <div class="activity-details">
                      <p class="activity-text">{{ activity.description }}</p>
                      <p class="activity-time">{{ formatActivityTime(activity.timestamp) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Users Management View -->
        <div v-if="currentView === 'users'" class="users-view">
          <div class="view-header">
            <h1>User Management</h1>
            <div class="view-actions">
              <button class="add-button">
                <i class="fas fa-plus"></i> Add User
              </button>
              <div class="filter-dropdown">
                <button class="filter-button">
                  <i class="fas fa-filter"></i> Filter
                </button>
                <div class="dropdown-content">
                  <label>
                    <input type="checkbox" v-model="filters.showAdmins" /> Admins
                  </label>
                  <label>
                    <input type="checkbox" v-model="filters.showStudents" /> Students
                  </label>
                  <label>
                    <input type="checkbox" v-model="filters.showInstructors" /> Instructors
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <div class="search-filters">
            <div class="search-box">
              <i class="fas fa-search"></i>
              <input 
                type="text" 
                placeholder="Search users..." 
                v-model="userSearchQuery"
              />
            </div>
            <div class="filter-tags">
              <div class="filter-tag" v-if="filters.showAdmins">
                Admins <i class="fas fa-times" @click="filters.showAdmins = false"></i>
              </div>
              <div class="filter-tag" v-if="filters.showStudents">
                Students <i class="fas fa-times" @click="filters.showStudents = false"></i>
              </div>
              <div class="filter-tag" v-if="filters.showInstructors">
                Instructors <i class="fas fa-times" @click="filters.showInstructors = false"></i>
              </div>
            </div>
          </div>
          
          <div class="users-table">
            <div v-if="loading" class="loading-spinner">Loading users...</div>
            <div v-else-if="filteredUsers.length === 0" class="no-data">
              No users found matching your criteria
            </div>
            <table v-else>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>{{ user.id.slice(0, 8) }}...</td>
                  <td class="user-name-cell">
                    <img :src="user.avatar_url || 'https://via.placeholder.com/30'" alt="User" class="user-avatar" />
                    <span>{{ user.full_name }}</span>
                  </td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span class="role-badge" :class="'role-' + user.role">
                      {{ user.role }}
                    </span>
                  </td>
                  <td>
                    <span class="status-indicator" :class="user.active ? 'active' : 'inactive'"></span>
                    {{ user.active ? 'Active' : 'Inactive' }}
                  </td>
                  <td>{{ formatDate(user.created_at) }}</td>
                  <td>
                    <div class="action-buttons">
                      <button class="table-action edit-action" @click="editUser(user)">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button class="table-action delete-action" @click="confirmDeleteUser(user)">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="pagination">
            <button 
              class="pagination-button" 
              @click="changePage(currentPage - 1)" 
              :disabled="currentPage === 1"
            >
              <i class="fas fa-chevron-left"></i>
            </button>
            
            <div class="page-numbers">
              <button 
                v-for="page in displayedPages" 
                :key="page"
                class="page-number"
                :class="{ active: currentPage === page }"
                @click="changePage(page)"
              >
                {{ page }}
              </button>
            </div>
            
            <button 
              class="pagination-button" 
              @click="changePage(currentPage + 1)" 
              :disabled="currentPage === totalPages"
            >
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
        
        <!-- Courses View -->
        <div v-if="currentView === 'courses'" class="courses-view">
          <h1>Course Management</h1>
          <p>Manage all courses and their content here.</p>
          <!-- Course management functionality would be implemented here -->
        </div>
        
        <!-- Quizzes View -->
        <div v-if="currentView === 'quizzes'" class="quizzes-view">
          <h1>Quiz Management</h1>
          <p>Create, edit and analyze quiz performance here.</p>
          <!-- Quiz management functionality would be implemented here -->
        </div>
        
        <!-- Settings View -->
        <div v-if="currentView === 'settings'" class="settings-view">
          <h1>System Settings</h1>
          <p>Configure application settings and preferences.</p>
          <!-- Settings functionality would be implemented here -->
        </div>
      </div>
    </div>
    
    <!-- Modals -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Confirm Deletion</h2>
          <button class="close-button" @click="showDeleteModal = false">×</button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete user <strong>{{ userToDelete?.full_name }}</strong>?</p>
          <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button class="cancel-button" @click="showDeleteModal = false">Cancel</button>
          <button class="delete-button" @click="deleteUser">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { supabase } from '@/lib/supabaseClient';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();

// State
const sidebarCollapsed = ref(false);
const currentView = ref('dashboard');
const loading = ref(true);
const showDeleteModal = ref(false);
const userToDelete = ref(null);
const adminProfile = ref({
  full_name: 'Admin User',
  avatar_url: null
});
const searchQuery = ref('');
const userSearchQuery = ref('');
const users = ref([]);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const notifications = ref([]);

const sidebarItems = [
  { id: 'dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt' },
  { id: 'users', label: 'Users', icon: 'fas fa-users' },
  { id: 'courses', label: 'Courses', icon: 'fas fa-book' },
  { id: 'quizzes', label: 'Quizzes', icon: 'fas fa-question-circle' },
  { id: 'settings', label: 'Settings', icon: 'fas fa-cog' }
];

// Stats
const userStats = reactive({
  totalUsers: 0,
  newUsersToday: 0
});

const courseStats = reactive({
  totalCourses: 0,
  activeCourses: 0
});

const quizStats = reactive({
  totalQuizzes: 0,
  submissionsToday: 0
});

const submissionStats = reactive({
  totalSubmissions: 0,
  averageScore: 0
});

const recentActivity = ref([]);

// Filters
const filters = reactive({
  showAdmins: true,
  showStudents: true,
  showInstructors: true
});

// Computed Properties
const filteredUsers = computed(() => {
  return users.value
    .filter(user => {
      // Filter by search query
      if (userSearchQuery.value) {
        const query = userSearchQuery.value.toLowerCase();
        return (
          user.full_name?.toLowerCase().includes(query) ||
          user.email?.toLowerCase().includes(query)
        );
      }
      return true;
    })
    .filter(user => {
      // Filter by role
      if (user.role === 'admin' && !filters.showAdmins) return false;
      if (user.role === 'student' && !filters.showStudents) return false;
      if (user.role === 'instructor' && !filters.showInstructors) return false;
      return true;
    })
    .slice(
      (currentPage.value - 1) * itemsPerPage.value,
      currentPage.value * itemsPerPage.value
    );
});

const totalPages = computed(() => {
  return Math.ceil(users.value.length / itemsPerPage.value);
});

const displayedPages = computed(() => {
  const pages = [];
  const maxDisplayPages = 5;
  
  if (totalPages.value <= maxDisplayPages) {
    // Show all pages if there are fewer than maxDisplayPages
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i);
    }
  } else {
    // Always include first page
    pages.push(1);
    
    // Middle pages
    const middleStart = Math.max(2, currentPage.value - 1);
    const middleEnd = Math.min(totalPages.value - 1, currentPage.value + 1);
    
    // Show ellipsis after first page if necessary
    if (middleStart > 2) {
      pages.push('...');
    }
    
    // Add middle pages
    for (let i = middleStart; i <= middleEnd; i++) {
      pages.push(i);
    }
    
    // Show ellipsis before last page if necessary
    if (middleEnd < totalPages.value - 1) {
      pages.push('...');
    }
    
    // Always include last page
    pages.push(totalPages.value);
  }
  
  return pages;
});

// Functions
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value;
};

const changeView = (view) => {
  currentView.value = view;
};

const logout = async () => {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    toast.success('Logged out successfully');
    router.push('/login');
  } catch (error) {
    toast.error('Error logging out');
    console.error('Logout error:', error);
  }
};

const handleSearch = () => {
  console.log('Searching for:', searchQuery.value);
  // Implement global search functionality here
};

const fetchCurrentAdmin = async () => {
  try {
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) throw error;
    
    if (user) {
      const { data, error: profileError } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user.id)
        .single();
        
      if (profileError) throw profileError;
      adminProfile.value = data;
    }
  } catch (error) {
    console.error('Error fetching admin profile:', error);
    toast.error('Error loading admin profile');
  }
};

const fetchUsers = async () => {
  try {
    loading.value = true;
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .order('created_at', { ascending: false });
      
    if (error) throw error;
    users.value = data.map(user => ({
      ...user,
      role: user.role || 'student', // Default role if not set
      active: user.active !== false // Default to active if not set
    }));
    
    userStats.totalUsers = users.value.length;
    
    // Count new users today
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    userStats.newUsersToday = users.value.filter(user => {
      const createdDate = new Date(user.created_at);
      return createdDate >= today;
    }).length;
  } catch (error) {
    console.error('Error fetching users:', error);
    toast.error('Error loading users');
  } finally {
    loading.value = false;
  }
};

const fetchCourseStats = async () => {
  try {
    const { data, error } = await supabase
      .from('courses')
      .select('*');
      
    if (error) throw error;
    courseStats.totalCourses = data.length;
    courseStats.activeCourses = data.filter(course => course.active !== false).length;
  } catch (error) {
    console.error('Error fetching course stats:', error);
  }
};

const fetchQuizStats = async () => {
  try {
    const { data, error } = await supabase
      .from('quizzes')
      .select('*');
      
    if (error) throw error;
    quizStats.totalQuizzes = data.length;
  } catch (error) {
    console.error('Error fetching quiz stats:', error);
  }
};

const fetchSubmissionStats = async () => {
  try {
    const { data, error } = await supabase
      .from('quiz_submissions')
      .select('*');
      
    if (error) throw error;
    submissionStats.totalSubmissions = data.length;
    
    // Calculate average score
    if (data.length > 0) {
      const totalScore = data.reduce((sum, submission) => sum + (submission.score || 0), 0);
      submissionStats.averageScore = Math.round(totalScore / data.length);
    }
  } catch (error) {
    console.error('Error fetching submission stats:', error);
  }
};

const fetchRecentActivity = async () => {
  try {
    // This would be replaced with actual activity logging from your database
    // For now, just mocking some data
    recentActivity.value = [
      {
        type: 'login',
        description: 'John Smith logged in',
        timestamp: new Date(Date.now() - 15 * 60000) // 15 minutes ago
      },
      {
        type: 'course',
        description: 'New course "Advanced Mathematics" created',
        timestamp: new Date(Date.now() - 2 * 3600000) // 2 hours ago
      },
      {
        type: 'quiz',
        description: 'Quiz "Physics Fundamentals" was submitted by 5 students',
        timestamp: new Date(Date.now() - 5 * 3600000) // 5 hours ago
      },
      {
        type: 'user',
        description: 'New user Maria Garcia registered',
        timestamp: new Date(Date.now() - 8 * 3600000) // 8 hours ago
      }
    ];
  } catch (error) {
    console.error('Error fetching recent activity:', error);
  }
};

const getActivityIcon = (type) => {
  switch (type) {
    case 'login': return 'fas fa-sign-in-alt';
    case 'course': return 'fas fa-book';
    case 'quiz': return 'fas fa-question-circle';
    case 'user': return 'fas fa-user-plus';
    default: return 'fas fa-info-circle';
  }
};

const formatActivityTime = (timestamp) => {
  const now = new Date();
  const diff = (now - new Date(timestamp)) / 1000; // difference in seconds
  
  if (diff < 60) return 'Just now';
  if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
  return `${Math.floor(diff / 86400)} days ago`;
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

const refreshData = () => {
  fetchUsers();
  fetchCourseStats();
  fetchQuizStats();
  fetchSubmissionStats();
  fetchRecentActivity();
  toast.success('Data refreshed');
};

const changePage = (page) => {
  if (typeof page === 'number' && page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

const editUser = (user) => {
  // Implementation for edit user functionality
  toast.info(`Editing user: ${user.full_name}`);
};

const confirmDeleteUser = (user) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};

const deleteUser = async () => {
  if (!userToDelete.value) return;
  
  try {
    // In a real app, you might want to archive rather than delete
    const { error } = await supabase
      .from('profiles')
      .delete()
      .eq('id', userToDelete.value.id);
      
    if (error) throw error;
    
    toast.success(`User ${userToDelete.value.full_name} deleted successfully`);
    await fetchUsers(); // Refresh user list
    showDeleteModal.value = false;
  } catch (error) {
    console.error('Error deleting user:', error);
    toast.error('Failed to delete user');
  }
};

// Initialize
onMounted(async () => {
  try {
    await fetchCurrentAdmin();
    await Promise.all([
      fetchUsers(),
      fetchCourseStats(),
      fetchQuizStats(),
      fetchSubmissionStats(),
      fetchRecentActivity()
    ]);
  } catch (error) {
    console.error('Error initializing admin dashboard:', error);
  }
});
</script>

<style scoped>
/* Base Styles */
:root {
  --primary: #4f46e5;
  --primary-light: #818cf8;
  --primary-dark: #4338ca;
  --secondary: #f8fafc;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
  --danger: #dc2626;
  --danger-light: #fee2e2;
  --success: #059669;
  --warning: #f59e0b;
  --purple: #8b5cf6;
}

.admin-container {
  display: flex;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
  background-color: var(--secondary);
  color: var(--text-primary);
}

/* Sidebar Styles */
.sidebar {
  width: 260px;
  background-color: var(--primary);
  color: white;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--primary-light);
}

.sidebar-collapsed .sidebar-header {
  justify-content: center;
  padding: 1.5rem 0;
}

.sidebar h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: white;
  color: var(--primary);
  border-radius: 8px;
  font-weight: bold;
  font-size: 1.2rem;
}

.sidebar-collapsed h2 {
  display: none;
}

.toggle-sidebar {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
}

.sidebar-collapsed .toggle-sidebar {
  position: absolute;
  right: -12px;
  top: 20px;
  background-color: var(--primary);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.sidebar-menu {
  flex: 1;
  padding: 1.5rem 0;
}

.sidebar-item {
  padding: 0.75rem 1.5rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.sidebar-collapsed .sidebar-item {
  padding: 0.75rem 0;
  justify-content: center;
  margin: 0.5rem 0;
}

.sidebar-item:hover {
  background-color: var(--primary-dark);
}

.sidebar-item.active {
  background-color: var(--primary-dark);
  border-left-color: white;
}

.sidebar-collapsed .sidebar-item.active {
  border-left: none;
  position: relative;
}

.sidebar-collapsed .sidebar-item.active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: white;
}

.sidebar-item i {
  margin-right: 1rem;
  font-size: 1.2rem;
  width: 20px;
  text-align: center;
}

.sidebar-collapsed .sidebar-item i {
  margin-right: 0;
}

.sidebar-item span {
  font-weight: 500;
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--primary-light);
}

.admin-profile {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.admin-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 1rem;
}

.admin-info {
  flex: 1;
}

.admin-name {
  font-weight: 600;
  margin: 0;
  font-size: 0.95rem;
}

.admin-role {
  color: rgba(255, 255, 255, 0.75);
  margin: 0;
  font-size: 0.85rem;
}

.logout-button {
  width: 100%;
  padding: 0.7rem;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  transition: background-color 0.2s;
}

.sidebar-footer-collapsed {
  padding: 1.5rem 0;
  display: flex;
  justify-content: center;
  border-top: 1px solid var(--primary-light);
}

.logout-button-icon {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.logout-button:hover,
.logout-button-icon:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Main Content Styles */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.admin-header {
  background-color: white;
  height: 70px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.search-container {
  position: relative;
  width: 300px;
}

.search-container i {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.search-container input {
  padding: 0.6rem 0.8rem 0.6rem 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9rem;
  width: 100%;
  transition: border-color 0.2s;
}

.search-container input:focus {
  outline: none;
  border-color: var(--primary);
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.action-button {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: var(--secondary);
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: var(--danger);
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-wrapper {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

/* Dashboard Styles */
.dashboard-view h1 {
  margin-top: 0;
  margin-bottom: 2rem;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--text-primary);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  flex-shrink: 0;
}

.stat-icon i {
  font-size: 1.5rem;
  color: white;
}

.users-icon {
  background-color: var(--primary);
}

.courses-icon {
  background-color: green;
}

.quizzes-icon {
  background-color:orange;
}

.submissions-icon {
  background-color: purple;
}

.stat-details {
  flex: 1;
}

.stat-details h3 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-details p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.dashboard-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.chart-container {
  background-color: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.chart-container h2 {
  margin-top: 0;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e5e7eb;
  color: var(--text-primary);
}

.chart-placeholder {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--secondary);
  border-radius: 8px;
  color: var(--text-secondary);
}

.activity-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  padding: 1rem 0;
  border-bottom: 1px solid var(--secondary);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  flex-shrink: 0;
}

.activity-details {
  flex: 1;
}

.activity-text {
  margin: 0;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.activity-time {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

/* User Management Styles */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.view-header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--text-primary);
}

.view-actions {
  display: flex;
  gap: 0.75rem;
}

.add-button, .filter-button {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.add-button {
  background-color: var(--primary);
  color: white;
  border: none;
}

.add-button:hover {
  background-color: var(--primary-dark);
}

.filter-button {
  background-color: white;
  border: 1px solid #e5e7eb;
  color: var(--text-secondary);
}

.filter-button:hover {
  background-color: var(--secondary);
}

.filter-dropdown {
  position: relative;
}

.dropdown-content {
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 0.5rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  padding: 0.75rem;
  z-index: 10;
  min-width: 150px;
}

.dropdown-content label {
  display: block;
  padding: 0.5rem;
  cursor: pointer;
  color: var(--text-primary);
}

.search-filters {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-box {
  position: relative;
  max-width: 500px;
}

.search-box i {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.search-box input {
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
  transition: border-color 0.2s;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary);
}

.filter-tags {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background-color: var(--secondary);
  border-radius: 20px;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.filter-tag i {
  cursor: pointer;
}

.users-table {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 1rem;
  font-weight: 600;
  background-color: var(--secondary);
  color: var(--text-secondary);
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  color: var(--text-primary);
}

tr:last-child td {
  border-bottom: none;
}

.user-name-cell {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 0.75rem;
}

.role-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.role-admin {
  background-color: #fef3c7;
  color: #92400e;
}

.role-student {
  background-color: #e0e7ff;
  color: var(--primary-dark);
}

.role-instructor {
  background-color: #d1fae5;
  color: #065f46;
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.status-indicator.active {
  background-color: var(--success);
}

.status-indicator.inactive {
  background-color: var(--danger);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.table-action {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.edit-action {
  background-color: var(--secondary);
  color: var(--text-secondary);
}

.edit-action:hover {
  background-color: #e5e7eb;
}

.delete-action {
  background-color: var(--danger-light);
  color: var(--danger);
}

.delete-action:hover {
  background-color: #fecaca;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.pagination-button {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button:not(:disabled):hover {
  background-color: var(--secondary);
}

.page-numbers {
  display: flex;
  gap: 0.5rem;
}

.page-number {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.page-number:hover {
  background-color: var(--secondary);
}

.page-number.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.close-button {
  border: none;
  background: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
}

.modal-body {
  padding: 1.5rem;
  color: var(--text-primary);
}

.warning-text {
  color: var(--danger);
  font-weight: 500;
}

.modal-footer {
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  border-top: 1px solid #e5e7eb;
}

.cancel-button, .delete-button {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-button {
  background-color: var(--secondary);
  border: 1px solid #e5e7eb;
  color: var(--text-primary);
}

.cancel-button:hover {
  background-color: #e5e7eb;
}

.delete-button {
  background-color: var(--danger);
  border: none;
  color: white;
}

.delete-button:hover {
  background-color: #b91c1c;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  color: var(--text-secondary);
}

.no-data {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 50;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .sidebar-collapsed {
    transform: translateX(0);
    width: 80px;
  }

  .admin-header {
    padding: 0 1rem;
  }

  .stats-cards,
  .dashboard-charts {
    grid-template-columns: 1fr;
  }

  .search-container,
  .search-box {
    width: 100%;
    max-width: none;
  }

  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .action-buttons {
    justify-content: center;
  }
}
</style>
