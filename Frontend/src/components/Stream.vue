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
          <button @click="toggleTaskOptions" v-if="newPostType === 'task'">Task Options</button>
          <button @click="addPost" :disabled="!newPostContent.trim()">Post</button>
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
      <input type="checkbox" id="acceptLate" v-model="acceptLateSubmissions" />
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
      :class="post.type === 'announcement' ? 'fas fa-bullhorn' : 'fas fa-tasks'"
      class="post-icon"
    ></i>
    {{ post.type }}
  </span>
  <span class="post-timestamp">{{ formatTimestamp(post.timestamp) }}</span>
</div>
          <p class="post-content">{{ post.content }}</p>
          <div v-if="post.type === 'task'" class="task-details">
            <p><strong>Deadline:</strong> {{ formatTimestamp(post.deadline) }}</p>
            <p><strong>Accept Late Submissions:</strong> {{ post.acceptLate ? 'Yes' : 'No' }}</p>
            <p v-if="post.attachment">
            <strong>Attachment:</strong>
            <a :href="post.attachment" :download="attachmentFileName" target="_blank">Download</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { supabase } from '@/lib/supabaseClient.js'; // Import supabase client
import { getPosts } from '@/lib/supabaseClient.js';

const posts = ref([]);
const newPostContent = ref('');
const newPostType = ref('announcement');
const showTaskOptions = ref(false);
const taskDeadline = ref('');
const acceptLateSubmissions = ref(false);
const attachmentFile = ref(null);
const attachmentFileName = ref('');

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
    console.error('Error fetching posts:', error.message);
    return;
  }
  posts.value = data;
};

const addPost = async () => {
  if (!newPostContent.value.trim()) return;

  const newPost = {
    type: newPostType.value,
    content: newPostContent.value.trim(),
    deadline: newPostType.value === 'task' ? taskDeadline.value : null,
    accept_late: newPostType.value === 'task' ? acceptLateSubmissions.value : false,
    attachment: attachmentFile.value,
  };

  const { error } = await supabase.from('posts').insert(newPost);
  if (error) {
    console.error('Error adding post:', error.message);
    return;
  }

  // Reset form
  newPostContent.value = '';
  newPostType.value = 'announcement';
  showTaskOptions.value = false;
  taskDeadline.value = '';
  acceptLateSubmissions.value = false;
  attachmentFile.value = null;
  attachmentFileName.value = '';

  // Fetch updated posts
  fetchPosts();
};

onMounted(() => {
  fetchPosts();

  const subscription = supabase
    .channel('public:posts') // Use the correct channel name
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'posts' }, (payload) => {
      posts.value.unshift(payload.new);
    })
    .subscribe();

  onUnmounted(() => {
    supabase.removeChannel(subscription);
  });
});

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'No deadline';
  return new Date(timestamp).toLocaleString();
};
</script>
  
  <style scoped>
/* Container */
.stream-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: #f3f4f6;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

/* Title */
.stream-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
  color: #1f2937;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

/* Post Form */
.post-form {
  margin-bottom: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
  resize: none;
  background: #f9fafb;
  color: #374151;
}

textarea::placeholder {
  color: #9ca3af;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  background: #f9fafb;
  color: #374151;
  flex: 1;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #4338ca;
  transform: translateY(-2px);
}

/* Task Options */
.task-options {
  margin-top: 1rem;
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.task-options .form-group {
  margin-bottom: 1rem;
}

.task-options label {
display: block;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.task-options input[type="file"],
.task-options input[type="datetime-local"],
.task-options input[type="checkbox"] {
    width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  background: #f9fafb;
  color: #374151;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.task-options input[type="file"]:focus,
.task-options input[type="datetime-local"]:focus,
.task-options input[type="checkbox"]:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 5px rgba(79, 70, 229, 0.4);
}
.task-options input[type="checkbox"] {
  width: auto;
  margin-right: 0.5rem;
}
.task-options .checkbox-label {
  display: flex;
  align-items: center;
  font-size: 1rem;
  color: #374151;
}

.task-options .form-group:last-child {
  margin-bottom: 0;
}

/* Posts */
.posts {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #6b7280;
}

.post-type {
  font-weight: bold;
  text-transform: capitalize;
  color: #4f46e5;
}

.post-timestamp {
  font-size: 0.8rem;
  color: #9ca3af;
}

.post-content {
  font-size: 1rem;
  color: #374151;
  line-height: 1.6;
}

.task-details {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #374151;
}

.task-details p {
  margin: 0.5rem 0;
}

.task-details a {
  color: #4f46e5;
  text-decoration: underline;
}

.task-details a:hover {
  color: #4338ca;
  text-decoration: none;
}
</style>