<template>
  <div class="profile-container">
    <div class="profile-layout" v-motion-slide-bottom>
      <!-- Left Column -->
      <div class="profile-sidebar">
        <div class="profile-avatar-section">
          <div class="profile-avatar">
            <img :src="profileImage" alt="Profile" v-if="profileImage" />
            <div class="avatar-placeholder" v-else>{{ initials }}</div>
          </div>
          <input
            type="file"
            ref="fileInput"
            @change="handleFileChange"
            accept="image/*"
            style="display: none"
          />
          <button class="change-avatar-btn" @click="triggerFileInput">Change Photo</button>
        </div>
        <div class="quick-actions">
          <button class="primary-button" @click="editProfile">
            <i class="fas fa-edit"></i>
            Edit Profile
          </button>
          <button class="secondary-button">
            <i class="fas fa-cog"></i>
            Settings
          </button>
        </div>
      </div>

      <!-- Right Column -->
      <div class="profile-main">
        <div class="profile-header">
          <h1 class="profile-name">{{ fullName }}</h1>
          <span class="profile-badge">{{ role }}</span>
        </div>

        <div class="profile-sections">
          <section class="info-section" v-motion-slide-right>
            <h2><i class="fas fa-user"></i> Personal Information</h2>
            <div class="info-grid">
              <div class="info-item">
                <label>Username</label>
                <p>{{ username }}</p>
              </div>
              <div class="info-item">
                <label>Full Name</label>
                <p>{{ fullName }}</p>
              </div>
              <div class="info-item">
                <label>Email</label>
                <p>{{ email }}</p>
              </div>
              <div class="info-item">
                <label>Age</label>
                <p>{{ age }}</p>
              </div>
              <div class="info-item">
                <label>Gender</label>
                <p>{{ gender }}</p>
              </div>
              <div class="info-item">
                <label>Phone</label>
                <p>{{ phone }}</p>
              </div>
              <div class="info-item">
                <label>Date of Birth</label>
                <p>{{ formatDate(dateOfBirth) }}</p>
              </div>
              <div class="info-item">
                <label>Address</label>
                <p>{{ address }}</p>
              </div>
            </div>
          </section>

          <section class="info-section" v-motion-slide-right>
            <h2><i class="fas fa-shield-alt"></i> Account Security</h2>
            <div class="security-items">
              <div class="security-item">
                <div>
                  <h3>Two-Factor Authentication</h3>
                  <p>Secure your account with 2FA</p>
                </div>
                <button class="toggle-button">Enable</button>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Profile Modal -->
  <div class="modal" v-if="showEditModal" @click.self="closeModal">
    <div class="modal-content" v-motion-pop>
      <h2>Edit Profile</h2>
      <form @submit.prevent="saveProfile" class="edit-form">
        <div class="form-grid">
          <div class="form-group">
            <label>Username</label>
            <input type="text" v-model="editForm.username" required />
          </div>
          <div class="form-group">
            <label>Age</label>
            <input type="number" v-model="editForm.age" required />
          </div>
          <div class="form-group">
            <label>Gender</label>
            <select v-model="editForm.gender" required>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input type="tel" v-model="editForm.phone" required />
          </div>
          <div class="form-group">
            <label>Date of Birth</label>
            <input type="date" v-model="editForm.dateOfBirth" required />
          </div>
          <div class="form-group full-width">
            <label>Address</label>
            <textarea v-model="editForm.address" required></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeModal">Cancel</button>
          <button type="submit" class="primary-button" :disabled="loading">
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeMount, onBeforeUnmount} from 'vue'
import { supabase } from '@/lib/supabaseClient'
import { useToast } from 'vue-toastification'

const toast = useToast()
const loading = ref(false)
const showEditModal = ref(false)

// Extended user data
const username = ref('')
const fullName = ref('John Doe')
const email = ref('john.doe@example.com')
const role = ref('Student')
const memberSince = ref(new Date())
const timezone = ref('Pacific Time (US & Canada)')
const age = ref(null)
const gender = ref('')
const phone = ref('')
const profileImage = ref(null)
const dateOfBirth = ref(null)
const address = ref('')

const initials = computed(() => {
  if (!fullName.value) return ''
  const names = fullName.value.split(' ')
  return names.map(name => name.charAt(0).toUpperCase()).join('')
})

const formatDate = (date) => {
  if (!date) return 'Not set'
  try {
    const dateObj = new Date(date)
    if (isNaN(dateObj.getTime())) return 'Invalid date'
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(dateObj)
  } catch (error) {
    console.error('Date formatting error:', error)
    return 'Invalid date'
  }
}

// Edit form state
const editForm = ref({
  username: '',
  firstName: '',
  lastName: '',
  age: null,
  gender: '',
  phone: '',
  dateOfBirth: '',
  address: ''
})

const fileInput = ref(null)
const uploadingPhoto = ref(false)

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    toast.error('Please select an image file')
    return
  }

  uploadingPhoto.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('No user logged in')

    // Upload the file
    const fileExt = file.name.split('.').pop()
    const filepath = `public/${user.id}.${fileExt}`

    const { error: uploadError } = await supabase.storage
      .from('avatars')
      .upload(filepath, file, {
        upsert: true,
        contentType: file.type
      })

    if (uploadError) throw uploadError

      
    // Get the public URL of the uploaded image
    const { data: { publicUrl } } = supabase.storage
      .from('avatars')
      .getPublicUrl(filepath)

    if (!publicUrl) throw new Error('Failed to get public URL')

    // Update the database with the new image URL
    const { error: updateError } = await supabase
      .from('users')
      .update({ avatar_url: publicUrl })
      .eq('id', user.id)

    if (updateError) throw updateError

    // Update the profile image URL
    profileImage.value = publicUrl

    toast.success('Profile photo updated successfully!')
  } catch (error) {
    console.error('Error uploading photo:', error)
    toast.error('Failed to update profile photo')
  } finally {
    uploadingPhoto.value = false
    // Reset the file input
    event.target.value = ''
  }
}

// Update loadUserData function to use getPublicUrl
const loadUserData = async () => {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) {
      toast.error('No user logged in')
      return
    }

    // Load user profile data
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('id', user.id)
      .single()

    if (error) throw error

    if (data) {
      // Update user data
      username.value = data.username
      fullName.value = data.full_name
      age.value = data.age
      gender.value = data.gender
      phone.value = data.phone
      dateOfBirth.value = data.date_of_birth
      profileImage.value = data.avatar_url
      address.value = data.address
      email.value = user.email
      role.value = data.role || 'Student'
      memberSince.value = new Date(user.created_at)
      timezone.value = Intl.DateTimeFormat().resolvedOptions().timeZone

      // Update profile image loading
      try {
        const { data: { publicUrl } } = supabase.storage
          .from('avatars')
          .getPublicUrl(`public/${user.id}.${data.avatar_url.split('.').pop()}`)

        profileImage.value = publicUrl
      } catch (imageError) {
        console.error('Error loading profile image:', imageError)
        profileImage.value = null
      }
    }
  } catch (error) {
    console.error('Error loading user data:', error)
    toast.error('Failed to load profile data')
  }
}

const editProfile = () => {
  editForm.value = {
    age: age.value,
    gender: gender.value,
    phone: phone.value,
    dateOfBirth: dateOfBirth.value,
    address: address.value
  }
  showEditModal.value = true
}

const closeModal = () => {
  showEditModal.value = false
}

const saveProfile = async () => {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('No user logged in')

    const { error } = await supabase
      .from('users')
      .update({
        username: editForm.value.username,
        age: editForm.value.age,
        gender: editForm.value.gender,
        phone: editForm.value.phone,
        date_of_birth: editForm.value.dateOfBirth,
        address: editForm.value.address,
        updated_at: new Date()
      })
      .eq('id', user.id)

    if (error) throw error

    // Update local state
    username.value = editForm.value.username
    firstName.value = editForm.value.firstName
    lastName.value = editForm.value.lastName
    age.value = editForm.value.age
    gender.value = editForm.value.gender
    phone.value = editForm.value.phone
    dateOfBirth.value = editForm.value.dateOfBirth
    address.value = editForm.value.address

    toast.success('Profile updated successfully!')
    closeModal()
  } catch (error) {
    console.error('Error updating profile:', error)
    toast.error('Failed to update profile')
  } finally {
    loading.value = false
  }
}

// Load user data on component mount
onMounted(() => {
  loadUserData()
});

onBeforeMount(() => {
  loadUserData()
})

onBeforeUnmount(() => {
  if (profileImage.value) {
    URL.revokeObjectURL(profileImage.value)
  }
})
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.profile-sidebar {
  padding: 2rem;
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
}

.profile-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.profile-avatar {
  width: 180px;
  height: 180px;
  border-radius: 90px;
  overflow: hidden;
  border: 4px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e5e7eb;
  color: #6366f1;
  font-size: 3rem;
  font-weight: 600;
}

.change-avatar-btn {
  color: #6366f1;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
}

.quick-actions {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.primary-button, .secondary-button {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.primary-button {
  background: #6366f1;
  color: white;
}

.secondary-button {
  background: white;
  color: #4b5563;
  border: 1px solid #e5e7eb;
}

.profile-main {
  padding: 2rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.profile-badge {
  background: #e0e7ff;
  color: #6366f1;
  padding: 0.25rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.profile-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.info-item label {
  font-weight: 500;
  color: #374151;
}

.info-item p {
  color: #6b7280;
  margin: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.info-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-section h2 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1f2937;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.security-items {
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.security-item {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.security-item h3 {
  font-size: 1rem;
  color: #1f2937;
  margin: 0;
}

security-item p {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.toggle-button {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: span 2;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.875rem;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }
  
  .profile-sidebar {
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group.full-width {
    grid-column: span 1;
  }
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