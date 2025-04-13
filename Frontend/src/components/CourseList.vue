<template>
  <div class="course-list">
    <div class="section-header animate-fade-in">
      <h2 class="section-title">
        Available <span class="title-accent">Courses</span>
      </h2>
      <p class="section-description">
        Explore our interactive learning programs designed for young minds
      </p>
    </div>

    <TransitionGroup 
      name="course-list"
      tag="div"
      class="course-grid"
    >
      <div v-for="(course, index) in courses" 
           :key="course.course_id" 
           class="course-card"
           :style="{ animationDelay: `${index * 100}ms` }">
        <div class="card-icon">
          <i :class="course.icon"></i>
        </div>
        <div class="card-content">
          <h3 class="card-title">{{ course.name }}</h3>
          <p class="card-description">{{ course.description }}</p>
          <div class="card-stats">
            <div class="stat">
              <i class="fas fa-clock"></i>
              <span>{{ course.duration }}</span>
            </div>
            <div class="stat">
              <i class="fas fa-users"></i>
              <span>{{ course.student_count }}+ Students</span>
            </div>
          </div>
          <button class="card-button" @click="navigateToCourse(course.course_id)">
            <i class="fas fa-arrow-right"></i> View Course
          </button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { supabase } from "../lib/supabaseClient";
import { useRouter } from 'vue-router';

const router = useRouter();
const courses = ref([]);

const navigateToCourse = (course_id) => {
  if (course_id) {
    router.push({
      name: "CourseDetails",
      params: { course_id: course_id.toString() }, // Match the route parameter name
    });
  }
};

const fetchCourses = async () => {
  try {
    const { data, error } = await supabase.from("courses").select("*")
    //arrange by course_id in descending order
    .order("course_id", { ascending: false });

    if (error) {
      console.error("Error fetching courses:", error);
      return;
    }

    courses.value = data;
  } catch (error) {
    console.error("Error:", error);
  }
};

onMounted(() => {
  fetchCourses();
});
</script>

<style scoped>
.course-list {
  padding: 2rem 0;
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

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

/* Animation for header */
.animate-fade-in {
  animation: fadeIn 0.8s ease-out;
}

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

/* Transition group animations */
.course-list-move,
.course-list-enter-active,
.course-list-leave-active {
  transition: all 0.5s ease;
}

.course-list-enter-from,
.course-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.course-list-leave-active {
  position: absolute;
}

/* Card animation on mount */
.course-card {
  animation: slideIn 0.6s ease-out forwards;
  opacity: 0;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  height: 100%;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.course-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* Enhanced hover animations */
.course-card:hover .card-icon {
  transform: scale(1.05);
}

.card-icon {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s ease-in-out;
}

.card-icon i {
  font-size: 2.5rem;
}

.card-content {
  padding: 2rem;
  transition: transform 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.course-card:hover .card-content {
  transform: translateY(-5px);
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.card-description {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.card-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  margin-top: auto;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
}

.stat i {
  color: #4f46e5;
}

.card-button {
  width: 100%;
  padding: 1rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.card-button:hover {
  background: #4338ca;
  transform: translateY(-2px);
}

.card-button i {
  transition: transform 0.3s ease;
}

.card-button:hover i {
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }

  .course-grid {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
}
</style>
