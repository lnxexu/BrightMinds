<template>
  <div class="dashboard-container">
    <div class="section-header">
      <h2 class="section-title">Parent <span class="title-accent">Dashboard</span></h2>
      <p class="section-description">Monitor and support your child's learning journey</p>
    </div>

    <div class="dashboard-grid">
      <!-- Progress Overview Card -->
      <div class="dashboard-card overview">
        <div class="card-header">
          <h3 class="card-title">
            <i class="fas fa-chart-line"></i>
            Learning Progress
          </h3>
          <select v-model="selectedChild" class="select-input">
            <option value="child1">John Doe</option>
            <option value="child2">Jane Doe</option>
          </select>
        </div>
        <div class="progress-stats">
          <div class="stat-item">
            <div class="stat-value">85%</div>
            <div class="stat-label">Overall Progress</div>
            <div class="progress-bar">
              <div class="progress" style="width: 85%"></div>
            </div>
          </div>
          <div class="stat-grid">
            <div class="stat-box">
              <i class="fas fa-book"></i>
              <span class="stat-number">8</span>
              <span class="stat-label">Active Courses</span>
            </div>
            <div class="stat-box">
              <i class="fas fa-trophy"></i>
              <span class="stat-number">12</span>
              <span class="stat-label">Achievements</span>
            </div>
            <div class="stat-box">
              <i class="fas fa-clock"></i>
              <span class="stat-number">24h</span>
              <span class="stat-label">Study Time</span>
            </div>
            <div class="stat-box">
              <i class="fas fa-star"></i>
              <span class="stat-number">4.8</span>
              <span class="stat-label">Avg. Score</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activities Card -->
      <div class="dashboard-card">
        <h3 class="card-title">
          <i class="fas fa-history"></i>
          Recent Activities
        </h3>
        <div class="activity-list">
          <div v-for="(activity, index) in recentActivities" 
               :key="index" 
               class="activity-item">
            <div class="activity-icon">
              <i :class="activity.icon"></i>
            </div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Tasks Card -->
      <div class="dashboard-card">
        <h3 class="card-title">
          <i class="fas fa-tasks"></i>
          Upcoming Tasks
        </h3>
        <div class="task-list">
          <div v-for="(task, index) in upcomingTasks" 
               :key="index" 
               class="task-item">
            <div class="task-status">
              <i :class="['fas', task.completed ? 'fa-check-circle' : 'fa-circle']"></i>
            </div>
            <div class="task-content">
              <div class="task-title">{{ task.title }}</div>
              <div class="task-due">Due: {{ task.dueDate }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Academic Performance Card -->
      <div class="dashboard-card">
        <h3 class="card-title">
          <i class="fas fa-graduation-cap"></i>
          Academic Performance
        </h3>
        <div class="subject-list">
          <div v-for="(subject, index) in subjects" 
               :key="index" 
               class="subject-item">
            <div class="subject-info">
              <span class="subject-name">{{ subject.name }}</span>
              <span class="subject-score">{{ subject.score }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress" :style="{ width: subject.score + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ParentDashboard",
  data() {
    return {
      selectedChild: 'child1',
      recentActivities: [
        {
          icon: 'fas fa-check-circle',
          title: 'Completed Math Quiz - Chapter 5',
          time: '2 hours ago'
        },
        {
          icon: 'fas fa-play-circle',
          title: 'Started Science Course - Unit 3',
          time: '4 hours ago'
        },
        {
          icon: 'fas fa-trophy',
          title: 'Earned "Math Master" Badge',
          time: 'Yesterday'
        },
        {
          icon: 'fas fa-book',
          title: 'Submitted English Assignment',
          time: 'Yesterday'
        }
      ],
      upcomingTasks: [
        {
          title: 'Science Project Submission',
          dueDate: 'Tomorrow',
          completed: false
        },
        {
          title: 'Math Practice Test',
          dueDate: 'In 2 days',
          completed: false
        },
        {
          title: 'Reading Assignment',
          dueDate: 'Completed',
          completed: true
        }
      ],
      subjects: [
        { name: 'Mathematics', score: 85 },
        { name: 'Science', score: 78 },
        { name: 'English', score: 92 },
        { name: 'History', score: 88 }
      ]
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  max-width: 1440px;
  margin: 2rem auto;
  padding: 0 2rem;
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
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.dashboard-card {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.dashboard-card.overview {
  grid-column: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-title i {
  color: #4f46e5;
}

.select-input {
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f8fafc;
  color: #1f2937;
}

.progress-stats {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #4f46e5;
}

.stat-label {
  color: #6b7280;
  margin-top: 0.25rem;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.stat-box {
  background: #f8fafc;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stat-box i {
  font-size: 1.5rem;
  color: #4f46e5;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.progress-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.progress {
  height: 100%;
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  border-radius: 999px;
  transition: width 0.3s ease;
}

.activity-list, .task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item, .task-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
}

.activity-icon, .task-status {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e0e7ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4f46e5;
}

.activity-content, .task-content {
  flex: 1;
}

.activity-title, .task-title {
  color: #1f2937;
  font-weight: 500;
}

.activity-time, .task-due {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.subject-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.subject-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.subject-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subject-name {
  color: #1f2937;
  font-weight: 500;
}

.subject-score {
  color: #4f46e5;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-card.overview {
    grid-column: span 1;
  }

  .stat-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .section-title {
    font-size: 2rem;
  }

  .dashboard-container {
    padding: 0 1rem;
  }

  .stat-grid {
    grid-template-columns: 1fr;
  }
}
</style>