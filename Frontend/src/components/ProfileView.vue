<template>
  <div class="profile-container">
    <div class="profile-card" v-motion-slide-bottom>
      <div class="profile-header">
        <div class="profile-avatar">
          <img :src="profileImage" alt="Profile" v-if="profileImage" />
          <div class="avatar-placeholder" v-else>{{ initials }}</div>
        </div>
        <h1 class="profile-name">{{ fullName }}</h1>
      </div>

      <div class="profile-content">
        <div class="info-section" v-motion-slide-right>
          <h2>Personal Information</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>Email</label>
              <p>{{ email }}</p>
            </div>
            <div class="info-item">
              <label>Role</label>
              <p>{{ role }}</p>
            </div>
            <div class="info-item">
              <label>Member Since</label>
              <p>{{ formatDate(memberSince) }}</p>
            </div>
          </div>
        </div>

        <div class="actions" v-motion-slide-up>
          <button class="edit-button" @click="editProfile">
            Edit Profile
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// User data
const profileImage = ref('')
const firstName = ref('John')
const lastName = ref('Doe')
const email = ref('john.doe@example.com')
const role = ref('Student')
const memberSince = ref(new Date())

// Computed properties
const fullName = computed(() => `${firstName.value} ${lastName.value}`)
const initials = computed(() => 
  `${firstName.value[0]}${lastName.value[0]}`.toUpperCase()
)

// Methods
const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const editProfile = () => {
  // Implement edit profile logic
}

</script>

<style scoped>
.profile-container {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 60px;
  overflow: hidden;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
}

.profile-name {
  font-size: 2.5rem;
  color: #1f2937;
  margin: 0;
}

.info-section {
  margin-top: 2rem;
}

.info-section h2 {
  color: #4b5563;
  margin-bottom: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.info-item {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.info-item:hover {
  background: #f1f5f9;
}

.info-item label {
  color: #6b7280;
  font-size: 0.875rem;
  display: block;
  margin-bottom: 0.5rem;
}

.info-item p {
  color: #1f2937;
  font-size: 1rem;
  margin: 0;
}

.actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
}

.edit-button {
  background: #6366f1;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.edit-button:hover {
  background: #4f46e5;
}

/* Transitions */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>