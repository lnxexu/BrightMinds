<template>
  <div class="course-list">
    <div class="section-header">
      <h2 class="section-title">Available <span class="title-accent">Courses</span></h2>
      <p class="section-description">Explore our interactive learning programs designed for young minds</p>
    </div>

    <div class="course-grid">
      <div v-for="course in courses" :key="course.id" class="course-card">
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
              <span>{{ course.students }}+ Students</span>
            </div>
          </div>
          <button class="card-button">
            View Course
            <i class="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseList',
  setup() {
    const courses = [
      {
        id: 1,
        name: "Math Basics",
        description: "Master fundamental mathematics through interactive lessons and fun problem-solving activities.",
        icon: "fas fa-square-root-alt",
        duration: "8 weeks",
        students: 125
      },
      {
        id: 2,
        name: "Science Explorations",
        description: "Discover the wonders of science through hands-on experiments and engaging virtual labs.",
        icon: "fas fa-flask",
        duration: "10 weeks",
        students: 98
      },
      {
        id: 3,
        name: "English Literacy",
        description: "Develop strong reading and writing skills with our comprehensive English program.",
        icon: "fas fa-book-reader",
        duration: "12 weeks",
        students: 156
      }
    ];
    return { courses };
  },
};
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

.card-icon {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.card-icon i {
  font-size: 2.5rem;
}

.card-content {
  padding: 2rem;
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