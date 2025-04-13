<template>
  <div class="course-details" v-if="course">
    <div class="section-header animate-fade-in">
      <h2 class="section-title">
        {{ course.name }} <span class="title-accent">Details</span>
      </h2>
      <p class="section-description">{{ course.description }}</p>
    </div>

    <!-- Course Info Card -->
    <div class="course-info-card animate-slide-up">
      <div class="info-header">
        <div class="course-icon">
          <i class="fas fa-book-open"></i>
        </div>
        <div>
          <h3>Course Overview</h3>
          <p>Select topics by grade level to explore course content</p>
        </div>
      </div>

      <!-- Grade Level Selector -->
      <div class="filter-container">
        <label for="grade-select">Filter by Grade:</label>
        <div class="select-wrapper">
          <select id="grade-select" v-model="selectedGrade">
            <option value="all">All Grades</option>
            <option v-for="grade in uniqueGrades" :key="grade" :value="grade">
              {{ grade }}
            </option>
          </select>
          <i class="fas fa-chevron-down"></i>
        </div>
      </div>
    </div>

    <!-- Add topic button that will show a modal -->
    <!-- Add this after the Course Info Card and before the Topics List -->
    <div class="action-buttons">
      <button @click="showTopicMaterial({})" class="action-btn add-btn">
        <i class="fas fa-plus"></i> Add Topic
      </button>
    </div>

    <!-- Add topic Modal -->
    <div
      v-if="showAddTopicModal"
      class="modal-overlay"
      @click="closeAddTopicModal"
    >
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedTopic?.id ? "Modify Topic" : "Add New Topic" }}</h3>
          <button class="close-button" @click="closeAddTopicModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleAddTopic" class="topic-form">
            <div class="form-group">
              <label for="topicName">Topic Name</label>
              <input
                id="topicName"
                v-model="newTopic.topic_name"
                type="text"
                required
                placeholder="Enter topic name"
              />
            </div>
            <div class="form-group">
              <label for="gradeLevel">Grade Level</label>
              <div class="select-wrapper">
                <select
                  id="gradeLevel"
                  v-model="newTopic.grade_level"
                  required
                  class="form-select"
                >
                  <option value="" disabled selected>Select grade level</option>
                  <option value="K">Kinder</option>
                  <option
                    v-for="grade in availableGrades"
                    :key="grade"
                    :value="grade"
                  >
                    Grade {{ grade }}
                  </option>
                </select>
                <i class="fas fa-chevron-down"></i>
              </div>
            </div>
            <div class="form-group">
              <label for="topicContent">Topic Content</label>
              <div class="file-upload-container">
                <div
                  class="file-upload-area"
                  @drop.prevent="handleFileDrop"
                  @dragover.prevent="dragover = true"
                  @dragleave.prevent="dragover = false"
                  :class="{ dragging: dragover }"
                >
                  <input
                    type="file"
                    id="fileUpload"
                    ref="fileInput"
                    @change="handleFileSelect"
                    multiple
                    accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.mp4,.mp3"
                    class="file-input"
                  />
                  <div class="upload-content">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>Drag and drop files here or click to browse</p>
                    <span class="file-types"
                      >Supported files: PDF, DOC, Images, Videos, etc.</span
                    >
                  </div>
                </div>
                <div class="form-group">
                  <label for="topicDescription">Description (Optional)</label>
                  <textarea
                    id="topicDescription"
                    v-model="newTopic.description"
                    placeholder="Enter topic description"
                    rows="3"
                  ></textarea>
                  <small class="helper-text"
                    >Provide additional details about this topic to help users
                    identify it.</small
                  >
                </div>
                <!-- Preview uploaded files -->
                <div v-if="selectedFiles.length" class="selected-files">
                  <div
                    v-for="(file, index) in selectedFiles"
                    :key="index"
                    class="file-item"
                  >
                    <i :class="getFileIcon(file.type)"></i>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click="removeFile(index)" class="remove-file">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-submit" :disabled="isSubmitting">
                <i v-if="isSubmitting" class="fas fa-spinner fa-spin"></i>
                {{ isSubmitting ? "Adding..." : "Add Topic" }}
              </button>
              <button
                type="button"
                class="btn-cancel"
                @click="closeAddTopicModal"
                :disabled="isSubmitting"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Topics List -->
    <div class="topics-container">
      <h3 class="topics-title animate-fade-in">Course Topics</h3>
      <div v-if="filteredTopics.length === 0" class="no-topics">
        <i class="fas fa-search"></i>
        <p>No topics found for the selected grade</p>
      </div>
      <TransitionGroup v-else name="topic-list" tag="div" class="topics-grid">
        <div
          v-for="(topic, index) in filteredTopics"
          :key="topic.id"
          class="topic-card"
          :style="{ animationDelay: `${index * 100}ms` }"
          @click="showTopicMaterial(topic)"
        >
          <div class="topic-icon">
            <i class="fas fa-book"></i>
          </div>
          <div class="topic-content">
            <h4 class="topic-title">{{ topic.topic_name }}</h4>
            <span class="topic-grade">{{
              topic.grade_level === "Kindergarten"
                ? "Kindergarten"
                : `Grade
              ${topic.grade_level}`
            }}</span>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <Transition name="modal">
      <!-- Replace the existing modal content -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>
              {{ selectedTopic?.topic_name }} ({{
                selectedTopic?.grade_level === "Kindergarten"
                  ? "Kindergarten"
                  : `Grade ${selectedTopic?.grade_level}`
              }})
            </h3>
            <div class="modal-actions">
              <button
                @click="handleModifyTopic(selectedTopic)"
                class="action-btn edit-btn"
              >
                <i class="fas fa-edit"></i> Edit Topic
              </button>
              <button
                @click="showDeleteConfirmation"
                class="action-btn delete-btn"
              >
                <i class="fas fa-trash"></i> Delete Topic
              </button>
              <button class="close-button" @click="closeModal">
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
          <div class="modal-body">
            <div v-if="topicMaterial" class="material-content">
              <div v-if="topicMaterial?.materials" class="material-files">
                <h4>Topic Materials:</h4>
                <div class="files-grid">
                  <a
                    v-for="file in topicMaterial.materials"
                    :key="file.url"
                    :href="file.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="file-link"
                  >
                    <i :class="getFileIcon(file.type)"></i>
                    <span>{{ file.name }}</span>
                    <span class="file-size"
                      >({{ formatFileSize(file.size) }})</span
                    >
                  </a>
                </div>
              </div>
              <div v-else class="no-materials">
                <p>No materials available for this topic.</p>
              </div>
            </div>
            <div v-else class="loading-state">
              <i class="fas fa-spinner fa-spin"></i>
              <p>Loading material...</p>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <router-link to="/courses" class="back-button animate-fade-in">
      <i class="fas fa-arrow-left"></i> Back to Courses
    </router-link>
  </div>
  <div v-else class="loading-state animate-pulse">
    <i class="fas fa-spinner fa-spin"></i>
    <p>Loading course details...</p>
  </div>
  
  <Transition name="modal">
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content delete-confirmation" @click.stop>
        <div class="modal-header">
          <h3>Delete Topic</h3>
          <button class="close-button" @click="closeDeleteModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p class="delete-warning">
            <i class="fas fa-exclamation-triangle"></i>
            This action cannot be undone. To confirm deletion, please type the
            topic name below:
          </p>
          <div class="form-group">
            <input
              v-model="deleteConfirmation"
              type="text"
              class="form-input"
              :placeholder="selectedTopic?.topic_name"
            />
          </div>
          <div class="form-actions">
            <button
              @click="handleDeleteTopic"
              class="btn-delete"
              :disabled="deleteConfirmation !== selectedTopic?.topic_name"
            >
              <i v-if="isDeleting" class="fas fa-spinner fa-spin"></i>
              {{ isDeleting ? "Deleting..." : "Delete Topic" }}
            </button>
            <button
              type="button"
              class="btn-cancel"
              @click="closeDeleteModal"
              :disabled="isDeleting"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { supabase } from "../lib/supabaseClient";
import { useToast } from "vue-toastification";

const showDeleteModal = ref(false);
const deleteConfirmation = ref("");
const isDeleting = ref(false);
const fileInput = ref(null);
const dragover = ref(false);
const selectedFiles = ref([]);
const route = useRoute();
const course = ref(null);
const selectedGrade = ref("all");
const topics = ref([]);
const showModal = ref(false);
const selectedTopic = ref(null);
const topicMaterial = ref(null);
const showAddTopicModal = ref(false);
const isSubmitting = ref(false);
const toast = useToast();
const newTopic = ref({
  topic_name: "",
  grade_level: "",
  content: "",
  description: "",
});

const showDeleteConfirmation = () => {
  showDeleteModal.value = true;
  showModal.value = false;
  deleteConfirmation.value = "";
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  deleteConfirmation.value = "";
};

const handleDeleteTopic = async () => {
  if (
    !selectedTopic.value ||
    deleteConfirmation.value !== selectedTopic.value.topic_name
  ) {
    return;
  }

  try {
    isDeleting.value = true;

    // Delete associated materials first
    if (topicMaterial.value?.materials) {
      for (const material of topicMaterial.value.materials) {
        const filePath = material.url.split("/").pop();
        await supabase.storage
          .from("materials")
          .remove([`${selectedTopic.value.id}/${filePath}`]);
      }
    }

    // Delete the topic
    const { error } = await supabase
      .from("topics")
      .delete()
      .eq("id", selectedTopic.value.id);

    if (error) throw error;

    toast.success("Topic deleted successfully");
    closeDeleteModal();
    closeModal();
    await fetchCourseDetails();
  } catch (error) {
    console.error("Error deleting topic:", error);
    toast.error(error.message || "Error deleting topic");
  } finally {
    isDeleting.value = false;
  }
};

const formatFileSize = (bytes) => {
  if (!bytes) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

const fetchTopicMaterial = async () => {
  try {
    const { data, error } = await supabase
      .from("topics")
      .select("materials")
      .eq("id", selectedTopic.value.id)
      .single();

    if (error) throw error;

    // If materials exist and is an array, return it directly
    if (data?.materials && Array.isArray(data.materials)) {
      return data;
    }

    // If materials is a string, try to parse it
    if (data?.materials && typeof data.materials === "string") {
      try {
        const parsedMaterials = JSON.parse(data.materials);
        return { materials: parsedMaterials };
      } catch (e) {
        console.error("Error parsing materials:", e);
      }
    }

    return data;
  } catch (error) {
    console.error("Error fetching topic material:", error);
    return null;
  }
};

const handleFileDrop = (e) => {
  dragover.value = false;
  const files = Array.from(e.dataTransfer.files);
  addFiles(files);
};

const handleFileSelect = (e) => {
  const files = Array.from(e.target.files);
  addFiles(files);
};

const addFiles = (files) => {
  files.forEach((file) => {
    // Check if file is already selected
    if (!selectedFiles.value.some((f) => f.name === file.name)) {
      selectedFiles.value.push(file);
    }
  });
};

const removeFile = (index) => {
  selectedFiles.value.splice(index, 1);
};

const getFileIcon = (fileType) => {
  if (fileType.includes("image")) return "fas fa-image";
  if (fileType.includes("video")) return "fas fa-video";
  if (fileType.includes("pdf")) return "fas fa-file-pdf";
  if (fileType.includes("word")) return "fas fa-file-word";
  return "fas fa-file";
};

const handleAddTopic = async () => {
  try {
    // Input validation
    if (!newTopic.value.topic_name?.trim() || !newTopic.value.grade_level) {
      throw new Error("Topic name and grade level are required");
    }

    // File validation for new files
    const MAX_FILE_SIZE = 50 * 1024 * 1024;
    const ALLOWED_TYPES = [
      "image/",
      "video/",
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    for (const file of selectedFiles.value) {
      if (file.size > MAX_FILE_SIZE) {
        throw new Error(`File ${file.name} exceeds 50MB size limit`);
      }
      if (!ALLOWED_TYPES.some((type) => file.type.startsWith(type))) {
        throw new Error(`File ${file.name} has unsupported format`);
      }
    }

    let topicData;
    const topicPayload = {
      topic_name: newTopic.value.topic_name.trim(),
      grade_level: newTopic.value.grade_level,
      course: course.value.name,
      description: newTopic.value.description, // Add this line
    };

    if (newTopic.value.id) {
      // Update existing topic
      const { data, error: topicError } = await supabase
        .from("topics")
        .update(topicPayload)
        .eq("id", newTopic.value.id)
        .select()
        .single();

      if (topicError) throw topicError;
      topicData = data;
    } else {
      // Insert new topic
      const { data, error: topicError } = await supabase
        .from("topics")
        .insert([topicPayload])
        .select()
        .single();

      if (topicError) throw topicError;
      topicData = data;
    }

    // Handle file uploads if there are new files
    if (selectedFiles.value.length > 0) {
      const uploadedUrls = await Promise.all(
        selectedFiles.value.map(async (file) => {
          const fileExt = file.name.split(".").pop();
          const safeFileName = `${
            topicData.id
          }/${Date.now()}-${file.name.replace(
            /[^a-zA-Z0-9.-]/g,
            "_"
          )}.${fileExt}`;

          const { data, error } = await supabase.storage
            .from("materials")
            .upload(safeFileName, file, {
              cacheControl: "3600",
              upsert: false,
            });

          if (error) throw error;

          const {
            data: { publicUrl },
          } = supabase.storage.from("materials").getPublicUrl(safeFileName);

          return {
            url: publicUrl,
            type: file.type,
            name: file.name,
            size: file.size,
          };
        })
      );

      // Combine existing materials with new ones if modifying
      const materials = newTopic.value.id
        ? [...(newTopic.value.existingMaterials || []), ...uploadedUrls]
        : uploadedUrls;

      // Update materials
      const { error: materialError } = await supabase
        .from("topics")
        .update({
          materials: materials,
        })
        .eq("id", topicData.id);

      if (materialError) throw materialError;
    }

    // Show success message
    toast.success(
      newTopic.value.id
        ? "Topic updated successfully!"
        : "Topic added successfully!",
      {
        position: "top-right",
        timeout: 3000,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      }
    );

    // Reset form and close modal
    resetForm();
    showAddTopicModal.value = false;

    // Refresh the topics list
    await fetchCourseDetails();
  } catch (error) {
    console.error("Error handling topic:", error);
    throw error;
  }
};

// Add this helper function to keep the code DRY
const resetForm = () => {
  newTopic.value = {
    topic_name: "",
    grade_level: "",
    content: "",
    description: "",
  };
  selectedFiles.value = [];
};

const closeAddTopicModal = () => {
  showAddTopicModal.value = false;
  newTopic.value = {
    topic_name: "",
    grade_level: "",
    content: "",
  };
};

const showTopicMaterial = async (topic) => {
  if (Object.keys(topic).length === 0) {
    showAddTopicModal.value = true;
    return;
  }
  selectedTopic.value = topic;
  showModal.value = true;
  topicMaterial.value = null;

  const material = await fetchTopicMaterial(topic.id);
  if (material) {
    topicMaterial.value = material;
  }
};

const closeModal = () => {
  showModal.value = false;
  selectedTopic.value = null;
  topicMaterial.value = null;
};

const handleModifyTopic = async (topic) => {
  if (!topic) return;

  // Close the view modal
  showModal.value = false;

  // Pre-fill the form with existing topic data
  newTopic.value = {
    id: topic.id,
    topic_name: topic.topic_name,
    grade_level: topic.grade_level,
    content: topic.content || "",
  };

  // Get existing materials
  const material = await fetchTopicMaterial(topic.id);
  if (material?.materials) {
    // Store existing materials for reference
    newTopic.value.existingMaterials = material.materials;
  }

  showAddTopicModal.value = true;
};

// Fetch course details from Supabase
const fetchCourseDetails = async () => {
  try {
    const { data: courseData, error: courseError } = await supabase
      .from("courses")
      .select("*")
      .eq("course_id", route.params.course_id) // Changed from id to course_id
      .single();

    if (courseError) {
      console.error("Error fetching course:", courseError);
      return;
    }

    course.value = courseData;

    // Fetch topics for this course
    const { data: topicsData, error: topicsError } = await supabase
      .from("topics")
      .select("id, topic_name, grade_level")
      .eq("course", course.value.name);

    if (topicsError) {
      console.error("Error fetching topics:", topicsError);
      return;
    }
    topics.value = topicsData;
  } catch (error) {
    console.error("Error:", error);
  }
};

// Add this computed property after your existing computed properties
const availableGrades = computed(() => {
  // Generate array of grades 1-12
  return Array.from({ length: 6 }, (_, i) => i + 1);
});

const uniqueGrades = computed(() => {
  if (!topics.value?.length) return [];
  const grades = new Set(topics.value.map((topic) => topic.grade_level));
  return Array.from(grades).sort((a, b) => {
    if (a === "K") return -1;
    if (b === "K") return 1;
    return a - b;
  });
});

const filteredTopics = computed(() => {
  if (!topics.value?.length) return [];
  if (selectedGrade.value === "all") return topics.value;
  return topics.value.filter(
    (topic) => topic.grade_level === selectedGrade.value
  );
});

onMounted(() => {
  fetchCourseDetails();
});
</script>

<style scoped>
.course-details {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.title-accent {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-description {
  color: #6b7280;
  font-size: 1.1rem;
  max-width: 600px;
  margin: 0 auto;
}

/* Course Info Card */
.course-info-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
  margin-bottom: 2rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  padding: 2rem;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.course-icon {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-header .edit-btn {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.modal-header .close-button {
  padding: 0.5rem;
}

.course-icon i {
  font-size: 1.5rem;
}

.info-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem;
}

.info-header p {
  color: #6b7280;
  margin: 0;
}

/* Grade Filter */
.filter-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

label {
  font-weight: 600;
  color: #374151;
}

.select-wrapper {
  position: relative;
  display: inline-block;
}

select {
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  font-size: 1rem;
  cursor: pointer;
  appearance: none;
  background-color: white;
  min-width: 180px;
  color: #1f2937;
  font-weight: 500;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.select-wrapper i {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #4f46e5;
  pointer-events: none;
}

/* Topics */
.topics-container {
  margin-bottom: 2rem;
}

.topics-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.topic-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  animation: slideIn 0.6s ease-out forwards;
  opacity: 0;
}

.topic-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: #d1d5db;
}

.file-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: #f9fafb;
  color: #374151;
  text-decoration: none;
  transition: all 0.2s;
}

.file-size {
  font-size: 0.75rem;
  color: #6b7280;
  margin-left: auto;
}

.topic-icon {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: white;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease-in-out;
}

.topic-card:hover .topic-icon {
  transform: scale(1.1);
}

.topic-icon i {
  font-size: 1.25rem;
}

.topic-content {
  padding: 1rem 1.5rem;
  flex: 1;
}

.topic-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  color: #1f2937;
}

.topic-grade {
  display: inline-block;
  font-size: 0.85rem;
  background-color: #f3f4f6;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-weight: 500;
}

.no-topics {
  text-align: center;
  padding: 3rem 0;
  color: #6b7280;
}

.no-topics i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #d1d5db;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #4f46e5;
  color: white;
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s;
  font-weight: 600;
}

.back-button:hover {
  background: #4338ca;
  transform: translateY(-2px);
}

.back-button i {
  transition: transform 0.3s ease;
}

.back-button:hover i {
  transform: translateX(-4px);
}

/* Add these styles in your <style> section */
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 0 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  color: white;
}

.add-btn {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
}

.add-btn:hover {
  background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%);
  transform: translateY(-2px);
}

.edit-btn {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
}

.edit-btn:hover {
  background: linear-gradient(135deg, #047857 0%, #059669 100%);
  transform: translateY(-2px);
}

.action-btn i {
  font-size: 1rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #6b7280;
}

.loading-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

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
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.close-button {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.3s;
}

.close-button:hover {
  color: #1f2937;
}

.topic-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  font-size: 1rem;
  width: 100%;
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-submit,
.btn-cancel {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit {
  background: #4f46e5;
  color: white;
  border: none;
}

.btn-submit:hover {
  background: #4338ca;
}

.btn-cancel {
  background: #f3f4f6;
  color: #4b5563;
  border: 1px solid #e5e7eb;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.modal-body {
  padding: 1.5rem;
}

.material-content {
  line-height: 1.6;
  color: #374151;
  padding: 1rem;
}

.content-text {
  line-height: 1.6;
  color: #374151;
  margin-bottom: 1.5rem;
}

.material-files {
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
}

.material-files h4 {
  margin-bottom: 1rem;
  color: #374151;
}

.helper-text {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.form-group textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.file-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: #f9fafb;
  color: #374151;
  text-decoration: none;
  transition: all 0.2s;
}

.file-link:hover {
  background: #f3f4f6;
  transform: translateY(-2px);
}

.file-link i {
  color: #4f46e5;
  font-size: 1.25rem;
}

.file-link span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Make topic cards clickable */
.topic-card {
  cursor: pointer;
}

.topic-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: #4f46e5;
}

.file-upload-container {
  margin-top: 0.5rem;
}

.file-upload-area {
  position: relative;
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  background: #f9fafb;
  cursor: pointer;
}

.file-upload-area:hover,
.file-upload-area.dragging {
  border-color: #4f46e5;
  background: #f5f3ff;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.upload-content i {
  font-size: 2rem;
  color: #4f46e5;
}

.upload-content p {
  margin: 0;
  font-weight: 500;
  color: #374151;
}

.file-types {
  font-size: 0.875rem;
  color: #6b7280;
}

.selected-files {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  gap: 0.5rem;
}

.file-item i {
  color: #4f46e5;
}

.file-name {
  flex: 1;
  font-size: 0.875rem;
  color: #374151;
}

.remove-file {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-file:hover {
  background: #fee2e2;
}

/* Add these new animation styles */
.animate-fade-in {
  animation: fadeIn 0.8s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.8s ease-out;
}

.animate-pulse {
  animation: pulse 2s infinite;
}

/* Topic list transitions */
.topic-list-move,
.topic-list-enter-active,
.topic-list-leave-active {
  transition: all 0.5s ease;
}

.topic-list-enter-from,
.topic-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.topic-list-leave-active {
  position: absolute;
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content {
  transform: translateY(20px);
}

.form-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  font-size: 1rem;
  cursor: pointer;
  appearance: none;
  background-color: white;
  color: #1f2937;
  font-weight: 500;
  transition: all 0.3s ease;
}

.form-select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}

.form-group .select-wrapper {
  position: relative;
  width: 100%;
}

.form-group .select-wrapper i {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #4f46e5;
  pointer-events: none;
  transition: transform 0.3s ease;
}

.form-group .select-wrapper:hover i {
  transform: translateY(-50%) translateY(1px);
}

.delete-btn {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.delete-btn:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
}

.delete-confirmation {
  max-width: 500px;
}

.delete-warning {
  color: #dc2626;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.delete-warning i {
  font-size: 1.25rem;
}

.btn-delete {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #dc2626;
  color: white;
  border: none;
}

.btn-delete:disabled {
  background: #f87171;
  cursor: not-allowed;
}

.btn-delete:not(:disabled):hover {
  background: #b91c1c;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #dc2626;
  box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1);
}

/* Animation keyframes */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    opacity: 1;
  }

  50% {
    opacity: 0.5;
  }

  100% {
    opacity: 1;
  }
}

/* Enhance existing hover animations */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }

  .topics-grid {
    grid-template-columns: 1fr;
  }

  .course-details {
    padding: 1rem;
  }
}
</style>
