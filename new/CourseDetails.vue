<template>
  <div class="course-details">
    <div class="section-header">
      <h2 class="section-title">{{ course.name }} <span class="title-accent">Details</span></h2>
      <p class="section-description">{{ course.description }}</p>
    </div>

    <!-- Course Info Card -->
    <div class="course-info-card">
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
              Grade {{ grade }}
            </option>
          </select>
          <i class="fas fa-chevron-down"></i>
        </div>
      </div>
    </div>

    <!-- Topics List -->
    <div class="topics-container">
      <h3 class="topics-title">Course Topics</h3>
      <div v-if="filteredTopics.length" class="topics-grid">
        <div v-for="topic in filteredTopics" :key="topic.id" class="topic-card">
          <div class="topic-icon">
            <i class="fas fa-book"></i>
          </div>
          <div class="topic-content">
            <h4 class="topic-title">{{ topic.title }}</h4>
            <span class="topic-grade">Grade {{ topic.grade }}</span>
          </div>
        </div>
      </div>
      <div v-else class="no-topics">
        <i class="fas fa-search"></i>
        <p>No topics found for the selected grade</p>
      </div>
    </div>

    <router-link to="/courses" class="back-button">
      <i class="fas fa-arrow-left"></i> Back to Courses
    </router-link>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useRoute } from "vue-router";

export default {
  name: "CourseDetails",
  setup() {
    const route = useRoute();
    const selectedGrade = ref("all"); // Default to show all topics

    // Sample course data with topics grouped by grade
    const courses = [
      {
        id: 1,
        name: "Math Basics",
        description: "Master fundamental mathematics through interactive lessons.",
        topics: [
          { id: 1, title: "Counting and Numbers", grade: 1 },
          { id: 2, title: "Addition and Subtraction", grade: 2 },
          { id: 3, title: "Multiplication and Division", grade: 3 },
          { id: 4, title: "Fractions and Decimals", grade: 4 },
          { id: 5, title: "Algebra Basics", grade: 5 },
          { id: 6, title: "Geometry and Measurement", grade: 6 },
        ],
      },
      {
        id: 2,
        name: "Science Explorations",
        description: "Discover the wonders of science through experiments and virtual labs.",
        topics: [
          { id: 7, title: "Living and Non-Living Things", grade: 1 },
          { id: 8, title: "Human Body and Health", grade: 2 },
          { id: 9, title: "Earth and Space", grade: 3 },
          { id: 10, title: "Simple Machines", grade: 4 },
          { id: 11, title: "Ecosystems and Environment", grade: 5 },
          { id: 12, title: "Forces and Motion", grade: 6 },
        ],
      },
      {
        id: 3,
        name: "English Literacy",
        description: "Develop strong reading and writing skills with our English program.",
        topics: [
          { id: 13, title: "Alphabet and Phonics", grade: 1 },
          { id: 14, title: "Reading Short Stories", grade: 2 },
          { id: 15, title: "Sentence Structure", grade: 3 },
          { id: 16, title: "Writing Essays", grade: 4 },
          { id: 17, title: "Grammar and Vocabulary", grade: 5 },
          { id: 18, title: "Literature and Poetry", grade: 6 },
        ],
      },
    ];

    // Get the selected course using the route parameter
    const course = computed(() =>
      courses.find((c) => c.id === parseInt(route.params.id))
    );

    // Extract unique grade levels from topics for filtering
    const uniqueGrades = computed(() => {
      if (!course.value) return [];
      const grades = course.value.topics.map((topic) => topic.grade);
      return [...new Set(grades)].sort((a, b) => a - b);
    });

    // Filter topics based on selected grade
    const filteredTopics = computed(() => {
      if (!course.value) return [];
      if (selectedGrade.value === "all") return course.value.topics;
      return course.value.topics.filter((topic) => topic.grade == selectedGrade.value);
    });

    return { course, uniqueGrades, filteredTopics, selectedGrade };
  },
};
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