<template>
  <div class="stream-container">
    <h2 class="stream-title">Class Stream</h2>
    
    <!-- Post Form - Only visible for non-students -->
    <div v-if="canCreatePosts" class="post-form">
      <textarea
        v-model="newPostContent"
        placeholder="Share an announcement or task..."
        rows="2"
      ></textarea>
      <div class="form-actions">
        <select v-model="newPostType">
          <option value="announcement">Announcement</option>
          <option value="task">Task</option>
        </select>
        <select v-model="newPostGradeLevel" class="grade-select">
          <option value="all">All Grades</option>
          <option value="kindergarten">Kindergarten</option>
          <option value="grade1">Grade 1</option>
          <option value="grade2">Grade 2</option>
          <option value="grade3">Grade 3</option>
          <option value="grade4">Grade 4</option>
          <option value="grade5">Grade 5</option>
          <option value="grade6">Grade 6</option>
        </select>
        <button @click="toggleTaskOptions" v-if="newPostType === 'task'">
          Task Options
        </button>
        <button @click="addPost" :disabled="!newPostContent.trim()">
          Post
        </button>
      </div>

      <!-- Task Options -->
      <div v-if="showTaskOptions" class="task-options">
        <div class="form-row">
          <div class="form-group">
          <label for="attachment">Attachment</label>
          <input type="file" id="attachment" @change="handleFileUpload" />
          <p v-if="attachmentFileName" class="attachment-preview">
            <strong>Attached File:</strong> {{ attachmentFileName }}
          </p>
        </div>
        <div class="form-group">
          <label for="deadline">Deadline</label>
          <input type="datetime-local" id="deadline" v-model="taskDeadline" />
        </div>
        </div>
        <div class="form-row">
          <div class="form-group">
          <label for="acceptLate">Accept Late Submissions</label>
          <div class="checkbox-label">
            <input
              type="checkbox"
              id="acceptLate"
              v-model="acceptLateSubmissions"
            />
            <span>Allow late submissions</span>
          </div>
        </div>
        </div>
      </div>
    </div>
    
    <!-- Message for students -->
    <div v-else class="student-message">
      <p>Welcome to the class stream! Here you can view announcements and tasks from your teachers.</p>
    </div>

    <!-- Grade Filter Dropdown -->
    <div class="filter-container">
      <div class="filter-label">Filter by Grade:</div>
      <div class="filter-dropdown-container">
        <select v-model="gradeFilter" class="filter-dropdown">
          <option value="all">All Grades</option>
          <option value="kindergarten">Kindergarten</option>
          <option value="grade1">Grade 1</option>
          <option value="grade2">Grade 2</option>
          <option value="grade3">Grade 3</option>
          <option value="grade4">Grade 4</option>
          <option value="grade5">Grade 5</option>
          <option value="grade6">Grade 6</option>
        </select>
      </div>
    </div>

    <div class="posts">
      <div 
        v-for="post in filteredPosts" 
        :key="post.id" 
        class="post-card"
        @click="openPostModal(post)"
      >
      <div class="post-header">
  <span class="post-type">
    <i
      :class="
        post.type === 'announcement'
          ? 'fas fa-bullhorn'
          : 'fas fa-tasks'
      "
      class="post-icon"
    ></i>
    {{ post.type }}
  </span>
  <span class="post-grade-level">{{ formatGradeLevel(post.grade_level) }}</span>
  <span class="post-author">Posted by: {{ post.created_by }}</span>
  <span class="post-timestamp">{{
    formatTimestamp(post.timestamp)
  }}</span>
</div>
        <p class="post-content post-preview">{{ truncateContent(post.content) }}</p>
        <p class="read-more">Click to view details</p>
      </div>
      <div v-if="filteredPosts.length === 0" class="no-posts-message">
        No posts available for the selected grade level.
      </div>
    </div>

    <!-- Post Modal -->
    <div v-if="selectedPost" class="modal-overlay" @click="closeModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <span class="post-type">
              <i
                :class="
                  selectedPost.type === 'announcement'
                    ? 'fas fa-bullhorn'
                    : 'fas fa-tasks'
                "
                class="post-icon"
              ></i>
              {{ selectedPost.type }}
            </span>
            <span class="post-grade-level">{{ formatGradeLevel(selectedPost.grade_level) }}</span>
          </div>
          <button class="modal-close" @click="closeModal">×</button>
        </div>
        <div class="modal-content">
  <p class="post-content">{{ selectedPost.content }}</p>
  <div v-if="selectedPost.type === 'task'" class="task-details">
    <p><strong>Deadline:</strong> {{ formatTimestamp(selectedPost.deadline) }}</p>
    <p>
      <strong>Accept Late Submissions:</strong>
      {{ selectedPost.acceptLate ? "Yes" : "No" }}
    </p>
    <p v-if="selectedPost.attachment">
      <strong>Attachment:</strong>
      <a
        :href="selectedPost.attachment"
        :download="attachmentFileName"
        target="_blank"
        >Download</a
      >
    </p>
  </div>
  <div class="modal-footer">
    <div class="post-author-info">
      <strong>Posted by:</strong> {{ selectedPost.created_by }}
    </div>
    <div class="modal-timestamp">
      Posted: {{ formatTimestamp(selectedPost.timestamp) }}
    </div>
  </div>
</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { supabase, getPosts } from "@/lib/supabaseClient.js"; 
import { useToast } from "vue-toastification"; // Import toast library

const toast = useToast(); // Initialize toast
const posts = ref([]);
const newPostContent = ref("");
const newPostType = ref("announcement");
const newPostGradeLevel = ref("all");
const showTaskOptions = ref(false);
const taskDeadline = ref("");
const acceptLateSubmissions = ref(false);
const attachmentFile = ref(null);
const attachmentFileName = ref("");
const gradeFilter = ref("all");
const selectedPost = ref(null);
const userRole = ref(""); // Store the user's role

// Check if user can create posts based on role
const canCreatePosts = computed(() => {
  // Students cannot create posts
  return userRole.value !== "student";
});

const toggleTaskOptions = () => {
  showTaskOptions.value = !showTaskOptions.value;
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    attachmentFileName.value = file.name; // Store the file name
    const reader = new FileReader();
    reader.onload = () => {
      attachmentFile.value = reader.result; // Store the Base64 string
    };
    reader.readAsDataURL(file);
  }
};

const fetchPosts = async () => {
  const { data, error } = await getPosts();
  if (error) {
    console.error("Error fetching posts:", error.message);
    return;
  }
  posts.value = data;
};

const fetchUserRole = async () => {
  try {
    const { data: { user }, error: userError } = await supabase.auth.getUser();
    
    if (userError || !user) {
      console.error("Error fetching user:", userError?.message || "User not found");
      return;
    }
    
    const { data, error } = await supabase
      .from("profiles")
      .select("role")
      .eq("id", user.id)
      .single();
      
    if (error) {
      console.error("Error fetching user role:", error.message);
      return;
    }
    
    userRole.value = data.role || "";
    console.log("User role:", userRole.value);
  } catch (error) {
    console.error("Error in fetchUserRole:", error);
  }
};

const filteredPosts = computed(() => {
  if (gradeFilter.value === 'all') {
    return posts.value;
  }
  return posts.value.filter(post => post.grade_level === gradeFilter.value || post.grade_level === 'all');
});

const setGradeFilter = (grade) => {
  gradeFilter.value = grade;
};

const formatGradeLevel = (gradeLevel) => {
  if (!gradeLevel || gradeLevel === 'all') return 'All Grades';
  if (gradeLevel === 'kindergarten') return 'Kindergarten';
  
  // Convert "grade1" to "Grade 1"
  return gradeLevel.replace('grade', 'Grade ');
};

const addPost = async () => {
  if (!newPostContent.value.trim()) return;

  try {
    // Additional role check before posting
    if (!canCreatePosts.value) {
      toast.error("You don't have permission to create posts", {
        position: "top-right",
        timeout: 3000,
      });
      return;
    }

    // get the current user
    const { data: { user }, userError } = await supabase.auth.getUser()
    if (userError) {
      toast.error("Error fetching user: " + userError.message, {
        position: "top-right",
        timeout: 2000,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      throw new Error("Failed to fetch user");
    }
    // get from profiles using the user id
    const { data: profileData, error: profileError } = await supabase
      .from("profiles")
      .select("full_name")
      .eq("id", user.id)
      .single();

    if (profileError) {
      toast.error("Error fetching profile: " + profileError.message, {
        position: "top-right",
        timeout: 2000,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      throw new Error("Failed to fetch profile");
    }

    const newPost = {
      type: newPostType.value,
      content: newPostContent.value.trim(),
      deadline: newPostType.value === "task" ? taskDeadline.value : null,
      accept_late: newPostType.value === "task" ? acceptLateSubmissions.value : false,
      attachment: attachmentFile.value,
      grade_level: newPostGradeLevel.value,
      created_by: profileData.full_name,
    };

    const { error } = await supabase.from("posts").insert(newPost);
    if (error) {
      toast.error("Error adding post: " + error.message, {
        position: "top-right",
        timeout: 2000,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      throw new Error("Failed to add post");

    }

    // Reset form
    newPostContent.value = "";
    newPostType.value = "announcement";
    newPostGradeLevel.value = "all";
    showTaskOptions.value = false;
    taskDeadline.value = "";
    acceptLateSubmissions.value = false;
    attachmentFile.value = null;
    attachmentFileName.value = "";

    // toast notification
    toast.success("Post added successfully!", {
      position: "top-right",
      timeout: 2000,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });


    // Fetch updated posts
    fetchPosts();
  } catch (error) {
    toast.error("Error creating post: " + error.message);
  }
};

// Truncate the post content for preview
const truncateContent = (content) => {
  if (content.length <= 150) return content;
  return content.substring(0, 150) + '...';
};

// Open modal with selected post
const openPostModal = (post) => {
  selectedPost.value = post;
  // Add class to prevent scrolling when modal is open
  document.body.classList.add('modal-open');
};

// Close the modal
const closeModal = () => {
  selectedPost.value = null;
  // Remove class to re-enable scrolling
  document.body.classList.remove('modal-open');
};

// Close modal when pressing escape key
onMounted(() => {
  fetchPosts();
  fetchUserRole(); // Get the user's role when component mounts

  const handleEscape = (e) => {
    if (e.key === 'Escape' && selectedPost.value) {
      closeModal();
    }
  };

  window.addEventListener('keydown', handleEscape);

  const subscription = supabase
    .channel("public:posts") // Use the correct channel name
    .on(
      "postgres_changes",
      { event: "INSERT", schema: "public", table: "posts" },
      (payload) => {
        posts.value.unshift(payload.new);
      }
    )
    .subscribe();

  onUnmounted(() => {
    supabase.removeChannel(subscription);
    window.removeEventListener('keydown', handleEscape);
  });
});

const formatTimestamp = (timestamp) => {
  if (!timestamp) return "No deadline";
  return new Date(timestamp).toLocaleString();
};
</script>

<style scoped>
.stream-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2.5rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.stream-title {
  font-size: 2.25rem;
  font-weight: 800;
  margin-bottom: 2.5rem;
  text-align: center;
  color: #111827;
  border-bottom: none;
  background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.post-form {
  margin-bottom: 2.5rem;
  background: #ffffff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f3f4f6;
}

textarea {
  width: 100%;
  padding: 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1.1rem;
  margin-bottom: 1.25rem;
  resize: vertical;
  min-height: 80px;
  background: #ffffff;
  color: #1f2937;
  transition: all 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-actions {
  display: flex;
  gap: 1.25rem;
}

select {
  padding: 0.75rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  background: #ffffff;
  color: #1f2937;
  flex: 1;
  transition: all 0.3s ease;
  cursor: pointer;
}

select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

button {
  padding: 0.75rem 1.75rem;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
}

button:disabled {
  background: #e5e7eb;
  box-shadow: none;
}

.task-options {
  margin-top: 1.5rem;
  padding: 1.75rem;
  border-radius: 12px;
  background: #f8fafc;
  border: 2px solid #e5e7eb;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.post-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f3f4f6;
  transition: all 0.3s ease;
  margin-bottom: 16px;
  cursor: pointer;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f3f4f6;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.post-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  color: #4f46e5;
}

.post-type i {
  font-size: 1.2rem;
}

.post-content {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #1f2937;
  margin: 1rem 0;
}

.task-details {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px solid #f3f4f6;
}

.task-details p {
  margin: 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.task-details a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.task-details a:hover {
  color: #7c3aed;
  text-decoration: underline;
}

/* Add smooth scrolling to the container */
html {
  scroll-behavior: smooth;
}

/* Modern scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c7d2fe;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #4f46e5;
}

.filter-container {
  margin-bottom: 2rem;
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f3f4f6;
}

.filter-label {
  font-weight: 600;
  margin-bottom: 1rem;
  color: #374151;
  font-size: 1.1rem;
}

.filter-dropdown-container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.filter-dropdown {
  width: 100%;
  padding: 0.75rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  background: #ffffff;
  color: #1f2937;
  transition: all 0.3s ease;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%234b5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
}

.filter-dropdown:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.post-preview {
  position: relative;
  overflow: hidden;
}

.read-more {
  text-align: right;
  color: #4f46e5;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 0.75rem;
  cursor: pointer;
}

.post-grade-level {
  font-size: 0.9rem;
  background: #f3f4f6;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  color: #4b5563;
  font-weight: 500;
}

.no-posts-message {
  text-align: center;
  padding: 2rem;
  background: #f9fafb;
  border-radius: 12px;
  color: #6b7280;
  font-size: 1.1rem;
  font-style: italic;
}

.form-group {
  margin-bottom: 1.5rem;
}
.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #374151;
}
.form-group input[type="datetime-local"] {
  padding: 0.75rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  background: #ffffff;
  color: #1f2937;
  transition: all 0.3s ease;
}

.form-group input[type="datetime-local"]:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  color: #374151;
}
.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}
.attachment-preview {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #4b5563;
  font-style: italic;
}
.task-options .form-group {
  margin-bottom: 1.5rem;
}
.task-options .form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #374151;
}

.task-options .form-group input[type="file"] {
  padding: 0.75rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  background: #ffffff;
  color: #1f2937;
  transition: all 0.3s ease;
}

.form-row {
  display: flex;;
  flex-direction: row;
  justify-content: space-between;
}

.form-row .form-group {
  flex: 1;
  margin-right: 1rem;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
  overflow-y: auto;
}

.modal-container {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
  animation: modal-appear 0.3s ease-out forwards;
  transform-origin: bottom;
}

@keyframes modal-appear {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 2px solid #f3f4f6;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  transition: color 0.2s ease;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: none;
}

.modal-close:hover {
  color: #ef4444;
  background: #f3f4f6;
  transform: none;
  box-shadow: none;
}

.modal-content {
  padding: 2rem;
}

.modal-timestamp {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
  font-size: 0.9rem;
  color: #6b7280;
  text-align: right;
  font-style: italic;
}

/* Prevent scrolling on body when modal is open */
:global(body.modal-open) {
  overflow: hidden;
}

.post-author {
  font-size: 0.9rem;
  color: #4b5563;
  font-weight: 500;
}

.modal-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.post-author-info {
  font-size: 0.9rem;
  color: #4b5563;
}

/* Update existing style to fit in modal-footer */
.modal-footer .modal-timestamp {
  margin-top: 0;
  padding-top: 0;
  border-top: none;
}

.student-message {
  background: #f0f9ff;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2.5rem;
  border-left: 4px solid #4f46e5;
  color: #1e40af;
  font-size: 1.1rem;
  line-height: 1.6;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}
</style>
