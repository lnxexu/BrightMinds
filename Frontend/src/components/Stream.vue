<template>
  <div class="stream-container">
    <h2 class="stream-title">Class Stream</h2>
    <div class="post-form">
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
        <button @click="toggleTaskOptions" v-if="newPostType === 'task'">
          Task Options
        </button>
        <button @click="addPost" :disabled="!newPostContent.trim()">
          Post
        </button>
      </div>

      <!-- Task Options -->
      <!-- Task Options -->
      <div v-if="showTaskOptions" class="task-options">
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

    <div class="posts">
      <div v-for="post in posts" :key="post.id" class="post-card">
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
          <span class="post-timestamp">{{
            formatTimestamp(post.timestamp)
          }}</span>
        </div>
        <p class="post-content">{{ post.content }}</p>
        <div v-if="post.type === 'task'" class="task-details">
          <p><strong>Deadline:</strong> {{ formatTimestamp(post.deadline) }}</p>
          <p>
            <strong>Accept Late Submissions:</strong>
            {{ post.acceptLate ? "Yes" : "No" }}
          </p>
          <p v-if="post.attachment">
            <strong>Attachment:</strong>
            <a
              :href="post.attachment"
              :download="attachmentFileName"
              target="_blank"
              >Download</a
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { supabase, getPosts } from "@/lib/supabaseClient.js"; 

const posts = ref([]);
const newPostContent = ref("");
const newPostType = ref("announcement");
const showTaskOptions = ref(false);
const taskDeadline = ref("");
const acceptLateSubmissions = ref(false);
const attachmentFile = ref(null);
const attachmentFileName = ref("");

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

const addPost = async () => {
  if (!newPostContent.value.trim()) return;

  const newPost = {
    type: newPostType.value,
    content: newPostContent.value.trim(),
    deadline: newPostType.value === "task" ? taskDeadline.value : null,
    accept_late:
      newPostType.value === "task" ? acceptLateSubmissions.value : false,
    attachment: attachmentFile.value,
  };

  const { error } = await supabase.from("posts").insert(newPost);
  if (error) {
    console.error("Error adding post:", error.message);
    return;
  }

  // Reset form
  newPostContent.value = "";
  newPostType.value = "announcement";
  showTaskOptions.value = false;
  taskDeadline.value = "";
  acceptLateSubmissions.value = false;
  attachmentFile.value = null;
  attachmentFileName.value = "";

  // Fetch updated posts
  fetchPosts();
};

onMounted(() => {
  fetchPosts();

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
}

.post-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f3f4f6;
  transition: all 0.3s ease;
  margin-bottom: 16px;
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
</style>
