<template>
  <div class="settings-page">
    <h1>My Settings</h1>
    <div class="settings-container">
      <div class="settings-sections">
        <div class="settings-section">
          <h2>
            <i class="fas fa-user"></i>
            Profile Settings
          </h2>
          <form @submit.prevent="updateProfile" class="settings-form">
            <div class="form-group">
              <label for="username">Username</label>
              <input 
                type="text" 
                id="username" 
                v-model="profile.username" 
                class="form-control"
                placeholder="Enter username"
              >
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input 
                type="email" 
                id="email" 
                v-model="profile.email" 
                class="form-control" 
                disabled
              >
            </div>
            <div class="form-group">
              <label for="full_name">Full Name</label>
              <input 
                type="text" 
                id="full_name" 
                v-model="profile.full_name" 
                class="form-control"
                placeholder="Enter your full name"
              >
            </div>
            <button type="submit" class="btn-save" :disabled="loading">
              <i class="fas fa-save"></i>
              {{ loading ? 'Saving...' : 'Save Profile Changes' }}
            </button>
          </form>
        </div>

        <div class="settings-section">
          <h2>
            <i class="fas fa-bell"></i>
            Notification Settings
          </h2>
          <form @submit.prevent="updateNotificationSettings" class="settings-form">
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="notifications.email_notifications">
                <span>Receive email notifications</span>
              </label>
            </div>
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="notifications.assignment_reminders">
                <span>Assignment reminders</span>
              </label>
            </div>
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="notifications.course_updates">
                <span>Course updates</span>
              </label>
            </div>
            <button type="submit" class="btn-save" :disabled="loading">
              <i class="fas fa-save"></i>
              {{ loading ? 'Saving...' : 'Save Notification Settings' }}
            </button>
          </form>
        </div>

        <div class="settings-section">
          <h2>
            <i class="fas fa-shield-alt"></i>
            Privacy Settings
          </h2>
          <form @submit.prevent="updatePrivacySettings" class="settings-form">
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="privacy.profile_visible">
                <span>Make profile visible to other users</span>
              </label>
            </div>
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="privacy.show_progress">
                <span>Show my learning progress</span>
              </label>
            </div>
            <button type="submit" class="btn-save" :disabled="loading">
              <i class="fas fa-save"></i>
              {{ loading ? 'Saving...' : 'Save Privacy Settings' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { supabase } from "../lib/supabaseClient";
import { ref, onMounted } from 'vue';
const loading = ref(false);

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
.settings-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.settings-page h1 {
  font-size: 2.5rem;
  color: #1a1a1a;
  margin-bottom: 2rem;
  font-weight: 600;
}

.settings-container {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.settings-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.settings-section {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.settings-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

.settings-section h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
  background: white;
}

.form-control:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.form-control:disabled {
  background: #f1f1f1;
  cursor: not-allowed;
}

.checkbox-group {
  background: white;
  padding: 0.75rem;
  border-radius: 8px;
  border: 2px solid #e2e8f0;
  transition: border-color 0.2s;
}

.checkbox-group:hover {
  border-color: #4CAF50;
}

.checkbox-group label {
  font-weight: normal;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.btn-save {
  width: 100%;
  background: #4CAF50;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
}

btn-save:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.btn-save:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .settings-sections {
    grid-template-columns: 1fr;
  }
  
  .settings-page {
    padding: 1rem;
  }
}
</style>