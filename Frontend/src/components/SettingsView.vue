<template>
  <div class="settings-page">
    <header class="settings-header">
      <h1>Account Settings</h1>
      <p class="settings-subtitle">Manage your account preferences and personal information</p>
    </header>

    <div class="settings-container">
      <aside class="settings-sidebar">
        <nav>
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['tab-button', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            <i :class="tab.icon"></i>
            {{ tab.name }}
          </button>
        </nav>
      </aside>

      <main class="settings-content">
        <!-- Notifications Section -->
        <div v-show="activeTab === 'notifications'" class="settings-panel">
          <div class="panel-header">
            <h2>Notification Preferences</h2>
            <p>Choose how you want to receive updates and alerts</p>
          </div>

          <form @submit.prevent="updateNotificationSettings" class="settings-form">
            <div class="toggle-group">
              <div class="toggle-item">
                <div class="toggle-content">
                  <label>Email Notifications</label>
                  <p>Receive important updates via email</p>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="notifications.email_notifications">
                  <span class="slider"></span>
                </label>
              </div>

              <div class="toggle-item">
                <div class="toggle-content">
                  <label>Assignment Reminders</label>
                  <p>Get notified about upcoming assignments</p>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="notifications.assignment_reminders">
                  <span class="slider"></span>
                </label>
              </div>

              <div class="toggle-item">
                <div class="toggle-content">
                  <label>Course Updates</label>
                  <p>Stay informed about course changes</p>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="notifications.course_updates">
                  <span class="slider"></span>
                </label>
              </div>
            </div>

            <div class="form-footer">
              <button type="submit" class="btn-save" :disabled="loading">
                <i class="fas fa-save"></i>
                {{ loading ? 'Saving Changes...' : 'Save Preferences' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Privacy Section -->
        <div v-show="activeTab === 'privacy'" class="settings-panel">
          <div class="panel-header">
            <h2>Privacy Settings</h2>
            <p>Control your privacy and visibility preferences</p>
          </div>

          <form @submit.prevent="updatePrivacySettings" class="settings-form">
            <div class="toggle-group">
              <div class="toggle-item">
                <div class="toggle-content">
                  <label>Profile Visibility</label>
                  <p>Allow other users to view your profile</p>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="privacy.profile_visible">
                  <span class="slider"></span>
                </label>
              </div>

              <div class="toggle-item">
                <div class="toggle-content">
                  <label>Learning Progress</label>
                  <p>Show your course progress to others</p>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="privacy.show_progress">
                  <span class="slider"></span>
                </label>
              </div>
            </div>

            <div class="form-footer">
              <button type="submit" class="btn-save" :disabled="loading">
                <i class="fas fa-save"></i>
                {{ loading ? 'Saving Changes...' : 'Save Settings' }}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  </div>
</template>
<script setup>
import { supabase } from "../lib/supabaseClient";
import { ref, onMounted } from 'vue';

const loading = ref(false);
const activeTab = ref('notifications');

const tabs = [
  { id: 'notifications', name: 'Notifications', icon: 'fas fa-bell' },
  { id: 'privacy', name: 'Privacy', icon: 'fas fa-shield-alt' }
];

const profile = ref({
  username: '',
  email: '',
  full_name: ''
});

const notifications = ref({
  email_notifications: true,
  assignment_reminders: true,
  course_updates: true
});

const privacy = ref({
  profile_visible: true,
  show_progress: true
});


const updateProfile = async () => {
  try {
    loading.value = true;
    const { error } = await supabase
      .from('profiles')
      .update({
        username: profile.value.username,
        full_name: profile.value.full_name,
        updated_at: new Date()
      })
      .eq('id', store.state.currentUser.id);

    if (error) throw error;
  } catch (error) {
    console.error('Error updating profile:', error.message);
  } finally {
    loading.value = false;
  }
};

const updateNotificationSettings = async () => {
  try {
    loading.value = true;
    const { error } = await supabase
      .from('profiles')
      .update({
        settings: {
          notifications: notifications.value,
          privacy: privacy.value
        }
      })
      .eq('id', store.state.currentUser.id);

    if (error) throw error;
  } catch (error) {
    console.error('Error updating notification settings:', error.message);
  } finally {
    loading.value = false;
  }
};

const updatePrivacySettings = async () => {
  try {
    loading.value = true;
    const { error } = await supabase
      .from('profiles')
      .update({
        settings: {
          notifications: notifications.value,
          privacy: privacy.value
        }
      })
      .eq('id', store.state.currentUser.id);

    if (error) throw error;
  } catch (error) {
    console.error('Error updating privacy settings:', error.message);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
});
</script>

<style scoped>
:root {
  --primary: #4f46e5;
  --primary-light: #818cf8;
  --primary-dark: #4338ca;
  --secondary: #f8fafc;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}
.settings-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-header {
  margin-bottom: 2rem;
  text-align: center;
  background: var(--primary);
  padding: 2rem;
  border-radius: 16px;
  color: var(--secondary);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.settings-header h1 {
  font-size: 2.5rem;
  color: var(--secondary);
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.settings-subtitle {
  color: var(--secondary);
  font-size: 1.1rem;
}

.settings-container {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.settings-sidebar {
  background: #f8f9fa;
  padding: 1.5rem;
  border-right: 1px solid #eee;
}

.tab-button {
  width: 100%;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.tab-button:hover {
  background: var(--secondary);
}

.tab-button.active {
  background: var(--primary);
  color: var(--secondary);
}

.settings-panel {
  padding: 2rem;
}

.panel-header {
  margin-bottom: 2rem;
}

.panel-header h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.panel-header p {
  color: var(--text-secondary);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.full-width {
  grid-column: 1 / -1;
}

.input-with-icon {
  position: relative;
}

.input-with-icon i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.input-with-icon input {
  padding-left: 2.5rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  color: var(--text-primary);
  background-color: white;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-control:disabled {
  background-color: #f8fafc;
  cursor: not-allowed;
  color: var(--text-secondary);
}

.form-control::placeholder {
  color: var(--text-secondary);
  opacity: 0.8;
}

.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.toggle-content label {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.toggle-content p {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--primary);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.form-footer {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
}

.btn-save {
  background: var(--primary);
  color: var(--secondary);
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.btn-save:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .settings-container {
    grid-template-columns: 1fr;
  }
  
  .settings-sidebar {
    border-right: none;
    border-bottom: 1px solid #eee;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .settings-page {
    padding: 1rem;
  }
}
</style>