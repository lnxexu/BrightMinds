<template>
  <div class="home-page">
    <!-- Landing Page Hero - Always Visible -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">Transform Your Learning Journey</h1>
          <p class="hero-subtitle">with <span class="accent">Bright Minds</span></p>
          <p class="hero-description">
            Interactive courses, personalized learning paths, and expert guidance all in one place.
          </p>
          <div class="hero-buttons">
            <button v-if="isLoggedIn === false" @click="$router.push('/register')" class="button primary">
              Get Started
              <i class="fas fa-arrow-right"></i>
            </button>
            <button v-else @click="$router.push('/courses')" class="button primary">
              My Courses
              <i class="fas fa-book"></i>
            </button>
            <button v-if="isLoggedIn === false" @click="$router.push('/demo')" class="button secondary">
              Watch Demo
              <i class="fas fa-play"></i>
            </button>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">10K+</span>
              <span class="stat-label">Students</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">200+</span>
              <span class="stat-label">Courses</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">95%</span>
              <span class="stat-label">Success Rate</span>
            </div>
          </div>
        </div>
        <div class="hero-image">
          <img src="@/assets/learning-illustration.svg" alt="Online Learning" class="floating-animation" />
        </div>
      </div>
    </section>

    <!-- Features Section - Always Visible -->
    <section class="features">
      <h2 class="section-title">Why Choose <span class="title-accent">Bright Minds?</span></h2>
      <div class="feature-cards">
        <div class="card" v-for="(feature, index) in features" :key="index">
          <div class="card-icon-wrapper">
            <i :class="['fas', `fa-${feature.icon}`]"></i>
          </div>
          <h3 class="card-title">{{ feature.title }}</h3>
          <p class="card-description">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Logged In Content -->
    <template v-if="isLoggedIn === true">
      <section class="my-learning">
        <h2 class="section-title">My <span class="title-accent">Learning</span></h2>
        <div class="learning-dashboard">
          <div class="progress-cards">
            <div class="progress-card">
              <h3>Current Progress</h3>
              <div class="progress-bar">
                <div class="progress" style="width: 75%"></div>
              </div>
              <p>75% Complete</p>
            </div>
            <div class="upcoming-lessons">
              <h3>Next Lessons</h3>
              <ul>
                <li v-for="(lesson, index) in upcomingLessons" :key="index">
                  <i :class="['fas', lesson.icon]"></i>
                  <span>{{ lesson.title }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </template>

    <!-- Non-Logged In CTA -->
    <section v-else class="cta-section">
      <div class="cta-content">
        <h2>Ready to Start Your Learning Journey?</h2>
        <p>Join thousands of students already learning with Bright Minds</p>
        <div class="cta-buttons">
          <button @click="$router.push('/register')" class="button primary">
            Start Learning Now
            <i class="fas fa-arrow-right"></i>
          </button>
          <button @click="$router.push('/')" class="button secondary">
            Already a Member? Login
            <i class="fas fa-sign-in-alt"></i>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import { mapState } from 'vuex'

export default {
  name: "HomePage",
  data() {
    return {
      features: [
        {
          icon: "graduation-cap",
          title: "Personalized Learning",
          description: "Adaptive learning paths that adjust to your pace and style."
        },
        {
          icon: "chart-line",
          title: "Track Progress",
          description: "Real-time analytics and detailed performance insights."
        },
        {
          icon: "users",
          title: "Community Learning",
          description: "Connect with peers and learn together in study groups."
        },
        {
          icon: "award",
          title: "Certifications",
          description: "Earn recognized certificates upon course completion."
        }
      ],
      upcomingLessons: [
        { icon: "fa-book", title: "Mathematics - Chapter 5" },
        { icon: "fa-atom", title: "Science - Solar System" },
        { icon: "fa-language", title: "English - Grammar Basics" }
      ]
    }
  },


};
</script>

<style scoped>
.home-page {
  max-width: 1440px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  position: relative;
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  border-radius: 32px;
  padding: 4rem;
  overflow: hidden;
  margin-bottom: 4rem;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/pattern.svg') repeat;
  opacity: 0.1;
  pointer-events: none;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  position: relative;
  z-index: 1;
}

.hero-text {
  color: white;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.accent {
  background: linear-gradient(120deg, #f9fafb 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-accent {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
}

.hero-description {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
}

.button {
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  text-decoration: none;
}

.button.primary {
  background: white;
  color: #4f46e5;
}

.button.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  backdrop-filter: blur(10px);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.hero-stats {
  display: flex;
  gap: 3rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.8;
}

.hero-image {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-image img {
  width: 100%;
  max-width: 500px;
  height: auto;
}

.floating-animation {
  animation: floating 6s ease-in-out infinite;
}

@keyframes floating {
  0% { transform: translate(0, 0px); }
  50% { transform: translate(0, -20px); }
  100% { transform: translate(0, 0px); }
}

.my-learning {
  margin-top: 4rem;
}

.learning-dashboard {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.progress-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.progress-card {
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 16px;
}

.progress-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  margin: 1rem 0;
}

.progress {
  height: 100%;
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.upcoming-lessons ul {
  list-style: none;
  padding: 0;
}

.upcoming-lessons li {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.upcoming-lessons li:last-child {
  border-bottom: none;
}

.upcoming-lessons i {
  color: #4f46e5;
}

/* CTA Section styles */
.cta-section {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  border-radius: 32px;
  padding: 4rem;
  text-align: center;
  color: white;
  margin-top: 4rem;
}

.cta-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-content p {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .progress-cards {
    grid-template-columns: 1fr;
  }
  
  .cta-section {
    padding: 2rem;
  }
  
  .cta-content h2 {
    font-size: 2rem;
  }
}

.features {
  padding: 4rem 0;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
  color: #1f2937;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.card {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.card-icon-wrapper {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.card-icon-wrapper i {
  font-size: 1.5rem;
  color: white;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.card-description {
  color: #6b7280;
  line-height: 1.6;
}

@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-buttons {
    justify-content: center;
  }

  .hero-stats {
    justify-content: center;
  }

  .hero-image {
    order: -1;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 2rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 2rem;
  }

  .hero-stats {
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }
}
</style>