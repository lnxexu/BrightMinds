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

    <!-- Topics List -->
    <div class="topics-container">
      <h3 class="topics-title animate-fade-in">Course Topics</h3>
      <div v-if="filteredTopics.length === 0" class="no-topics">
        <i class="fas fa-search"></i>
        <p>No topics found for the selected grade</p>
      </div>
      <TransitionGroup 
        v-else
        name="topic-list"
        tag="div"
        class="topics-grid"
      >
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
            <h4 class="topic-title">{{ topic.course }}</h4>
            <span class="topic-grade">Grade {{ topic.grade_level }}</span>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <Transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>
              {{ selectedTopic?.course }} - Grade {{ selectedTopic?.grade_level }}
            </h3>
            <button class="close-button" @click="closeModal">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div v-if="topicMaterial" class="material-content">
              {{ topicMaterial.content }}
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
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { supabase } from "../lib/supabaseClient";

const route = useRoute();
const router = useRouter();
const course = ref(null);
const selectedGrade = ref("all");
const topics = ref([]);
const showModal = ref(false)
const selectedTopic = ref(null)
const topicMaterial = ref(null)


const showTopicMaterial = async (topic) => {
  selectedTopic.value = topic
  showModal.value = true
  topicMaterial.value = null

  try {
    const { data, error } = await supabase
      .from('topic_materials')
      .select('*')
      .eq('topic_id', topic.id)
      .single()

    if (error) {
      console.error('Error fetching topic material:', error)
      return
    }

    topicMaterial.value = data
  } catch (error) {
    console.error('Error:', error)
  }
}

const closeModal = () => {
  showModal.value = false
  selectedTopic.value = null
  topicMaterial.value = null
}

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
      .select("*")
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

// Computed properties
const uniqueGrades = computed(() => {
  // use supabase to get unique grades from topics

  console.log("topics", topics.value);
  const grades = topics.value.map((topic) => topic.grade_level);
  return [...new Set(grades)].sort((a, b) => a - b);
});

const filteredTopics = computed(() => {
  if (!topics.value?.length) return [];
  if (selectedGrade.value === "all") return topics.value;
  return topics.value.filter((topic) => topic.grade == selectedGrade.value);
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

.modal-body {
  padding: 1.5rem;
}

.material-content {
  line-height: 1.6;
  color: #374151;
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
