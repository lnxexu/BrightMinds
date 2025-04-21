<template>
  <div class="quiz-taker">
    <!-- Course Selection Section -->
    <div v-if="!quizStarted && !quizCompleted" class="course-selection">
      <h2>Available Quizzes</h2>
      <div v-if="loading" class="loading-spinner">
        <div class="spinner"></div>
        <p>Loading quizzes...</p>
      </div>
      <div v-else-if="availableQuizzes.length === 0" class="no-quizzes">
        No quizzes available for this course.
      </div>
      <div v-else class="quiz-list">
        <div 
          v-for="quizItem in availableQuizzes" 
          :key="quizItem.id" 
          class="quiz-item"
          @click="selectQuiz(quizItem.id)"
        >
          <h3>{{ quizItem.title }}</h3>
          <div class="quiz-meta">
            <span><i class="fas fa-question-circle"></i> {{ quizItem.question_count }} questions</span>
            <span v-if="quizItem.time_limit"><i class="fas fa-clock"></i> {{ quizItem.time_limit }} minutes</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quiz Header Section -->
    <div class="quiz-header" v-if="quiz && quizStarted && !quizCompleted">
      <h2 class="quiz-title">{{ quiz.title }}</h2>
      <div class="quiz-info">
        <span class="course">{{ quiz.course_name }}</span>
        <span class="topic">{{ quiz.topic_name }}</span>
        <span class="question-count">{{ questions.length }} Questions</span>
        <span v-if="timeRemaining !== null" class="timer" :class="{'timer-warning': timeRemaining < 60}">
          <i class="fas fa-clock"></i> {{ formatTime(timeRemaining) }}
        </span>
      </div>
    </div>

    <!-- Quiz Content Section -->
    <div class="quiz-content" v-if="currentQuestion && quizStarted && !quizCompleted">
      <div class="question-navigation">
        <div 
          v-for="(q, index) in questions" 
          :key="index"
          :class="['question-dot', {
            'active': currentQuestionIndex === index,
            'answered': answers[index] !== undefined
          }]"
          @click="navigateToQuestion(index)"
        >
          {{ index + 1 }}
        </div>
      </div>

      <div class="question-container">
        <div class="question-header">
          <span class="question-number">Question {{ currentQuestionIndex + 1 }}</span>
        </div>

        <div class="question-content">
          <p class="question-text">{{ currentQuestion.question_text }}</p>
          <img 
            v-if="currentQuestion.question_image_url" 
            :src="currentQuestion.question_image_url" 
            alt="Question image"
            class="question-image"
          />
        </div>

        <div class="answer-section">
          <template v-if="currentQuestion.question_type === 'multiple_choice'">
            <div 
              v-for="(option, index) in currentQuestion.options" 
              :key="index"
              class="option"
            >
              <input 
                type="radio" 
                :id="'option-' + index"
                :value="index"
                v-model="answers[currentQuestionIndex]"
                :name="'question-' + currentQuestionIndex"
              />
              <label :for="'option-' + index">{{ option }}</label>
            </div>
          </template>

          <template v-else-if="currentQuestion.question_type === 'identification'">
            <input 
              type="text"
              v-model="answers[currentQuestionIndex]"
              class="text-input"
              placeholder="Enter your answer..."
            />
          </template>

          <template v-else-if="currentQuestion.question_type === 'essay'">
            <textarea
              v-model="answers[currentQuestionIndex]"
              class="essay-input"
              placeholder="Write your answer..."
              rows="6"
            ></textarea>
          </template>
        </div>

        <div class="navigation-buttons">
          <button 
            @click="previousQuestion" 
            class="nav-button"
            :disabled="currentQuestionIndex === 0"
          >
            <i class="fas fa-arrow-left"></i> Previous
          </button>
          <button 
            v-if="currentQuestionIndex < questions.length - 1"
            @click="nextQuestion" 
            class="nav-button"
          >
            Next <i class="fas fa-arrow-right"></i>
          </button>
          <button 
            v-else
            @click="submitQuiz" 
            class="submit-button"
            :disabled="!isQuizComplete"
          >
            Submit Quiz
          </button>
        </div>
      </div>
    </div>

    <!-- Quiz Results Section -->
    <div class="quiz-results" v-if="quizCompleted">
      <div class="results-container">
        <h2>Quiz Completed!</h2>
        <div class="score-display">
          <div class="score-circle" :class="getScoreColorClass()">
            <span class="score-percentage">{{ Math.round(quizScore.percentage) }}%</span>
          </div>
          <div class="score-details">
            <p>You scored <strong>{{ quizScore.correctAnswers }}</strong> out of <strong>{{ quizScore.totalQuestions }}</strong></p>
            <p class="score-message" :class="getScoreColorClass()">{{ scoreMessage }}</p>
          </div>
        </div>
        
        <div class="results-summary">
          <h3>Performance Summary</h3>
          <div class="summary-stats">
            <div class="stat-item">
              <span class="stat-value">{{ formatTime(quizScore.timeTaken) }}</span>
              <span class="stat-label">Time Taken</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ Math.round(quizScore.correctAnswers / quizScore.timeTaken * 60) }}</span>
              <span class="stat-label">Points/Min</span>
            </div>
          </div>
        </div>

        <div class="results-actions">
          <button @click="reviewQuiz" class="review-button">
            <i class="fas fa-search"></i> Review Answers
          </button>
          <button @click="returnToDashboard" class="dashboard-button">
            <i class="fas fa-home"></i> Return to Dashboard
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { supabase } from '@/lib/supabaseClient';
import { useToast } from 'vue-toastification';

const route = useRoute();
const router = useRouter();
const toast = useToast();

// State management
const loading = ref(false);
const availableQuizzes = ref([]);
const courseId = ref("Fifth Grade Writing Workshop");
const quiz = ref(null);
const questions = ref([]);
const currentQuestionIndex = ref(0);
const answers = ref({});
const quizStarted = ref(false);
const quizCompleted = ref(false);
const quizScore = ref({
  correctAnswers: 0,
  totalQuestions: 0,
  percentage: 0,
  timeTaken: 0
});
const timeRemaining = ref(null);
const timer = ref(null);
const startTime = ref(null);

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value]);

const isQuizComplete = computed(() => {
  return questions.value.every((_, index) => answers.value[index] !== undefined);
});

const scoreMessage = computed(() => {
  const percentage = quizScore.value.percentage;
  if (percentage >= 90) return "Excellent work!";
  if (percentage >= 80) return "Great job!";
  if (percentage >= 70) return "Good effort!";
  if (percentage >= 60) return "You passed!";
  return "Keep practicing!";
});

// Quiz functionality
const fetchAvailableQuizzes = async () => {
  loading.value = true;
  try {
    const { data, error } = await supabase
      .from('quizzes')
      .select(`
        id, 
        title, 
        course_name, 
        topic_name, 
        time_limit,
        course_id
      `)
      .eq('course_id', courseId.value);

    if (error) throw error;
    
    // Get question counts for each quiz
    if (data.length > 0) {
      const quizIds = data.map(q => q.id);
      const { data: questionCounts, error: countError } = await supabase
        .from('questions')
        .select('quiz_id, count(*)')
        .in('quiz_id', quizIds)
        .group('quiz_id');
        
      if (countError) throw countError;
      
      availableQuizzes.value = data.map(quiz => {
        const countData = questionCounts.find(q => q.quiz_id === quiz.id);
        return {
          ...quiz,
          question_count: countData ? countData.count : 0
        };
      });
    } else {
      availableQuizzes.value = [];
    }
  } catch (error) {
    console.error('Error fetching available quizzes:', error);
    toast.error('Failed to load quizzes');
  } finally {
    loading.value = false;
  }
};

const selectQuiz = async (quizId) => {
  try {
    loading.value = true;
    const { data: quizData, error: quizError } = await supabase
      .from('quizzes')
      .select('*')
      .eq('id', quizId)
      .single();

    if (quizError) throw quizError;
    quiz.value = quizData;

    const { data: questionData, error: questionError } = await supabase
      .from('questions')
      .select('*')
      .eq('quiz_id', quizId)
      .order('order_number');

    if (questionError) throw questionError;
    questions.value = questionData;
    
    quizStarted.value = true;
    startTime.value = new Date();
    
    // Start timer if the quiz has a time limit
    if (quiz.value.time_limit) {
      timeRemaining.value = quiz.value.time_limit * 60; // Convert minutes to seconds
      startTimer();
    }
  } catch (error) {
    console.error('Error fetching quiz:', error);
    toast.error('Failed to load quiz');
  } finally {
    loading.value = false;
  }
};

const startTimer = () => {
  timer.value = setInterval(() => {
    timeRemaining.value--;
    if (timeRemaining.value <= 0) {
      clearInterval(timer.value);
      timeRemaining.value = 0;
      submitQuiz(true); // Auto submit when time's up
    }
  }, 1000);
};

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${minutes}:${secs < 10 ? '0' + secs : secs}`;
};

const navigateToQuestion = (index) => {
  currentQuestionIndex.value = index;
};

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++;
  }
};

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
  }
};

const calculateScore = () => {
  let correct = 0;
  const total = questions.value.length;
  
  questions.value.forEach((question, index) => {
    const userAnswer = answers.value[index];
    
    if (question.question_type === 'multiple_choice' && 
        userAnswer === question.correct_option_index) {
      correct++;
    } else if (question.question_type === 'identification' && 
              userAnswer?.toLowerCase().trim() === question.correct_answer?.toLowerCase().trim()) {
      correct++;
    }
    // Essay questions would need manual grading
  });

  // Calculate time taken
  const endTime = new Date();
  const timeTaken = startTime.value ? 
    Math.floor((endTime - startTime.value) / 1000) : 
    (quiz.value.time_limit * 60) - timeRemaining.value;
  
  return {
    correctAnswers: correct,
    totalQuestions: total,
    percentage: (correct / total) * 100,
    timeTaken: timeTaken
  };
};

const getScoreColorClass = () => {
  const percentage = quizScore.value.percentage;
  if (percentage >= 80) return 'score-excellent';
  if (percentage >= 60) return 'score-good';
  return 'score-needs-improvement';
};

const submitQuiz = async (autoSubmit = false) => {
  try {
    if (autoSubmit) {
      toast.info('Time\'s up! Quiz has been automatically submitted.');
    }
    
    // Calculate the score
    quizScore.value = calculateScore();
    
    const submission = {
      quiz_id: quiz.value.id,
      student_id: await getCurrentUser(),
      answers: answers.value,
      score: quizScore.value.percentage,
      correct_answers: quizScore.value.correctAnswers,
      total_questions: quizScore.value.totalQuestions,
      submitted_at: new Date().toISOString(),
      time_taken: quizScore.value.timeTaken
    };

    const { error } = await supabase
      .from('quiz_submissions')
      .insert(submission);

    if (error) throw error;
    
    // Clear the timer if it's running
    if (timer.value) {
      clearInterval(timer.value);
      timer.value = null;
    }
    
    quizCompleted.value = true;
    toast.success('Quiz submitted successfully!');
  } catch (error) {
    console.error('Error submitting quiz:', error);
    toast.error('Failed to submit quiz');
  }
};

const reviewQuiz = () => {
  // Toggle back to quiz view in review mode
  quizStarted.value = true;
  quizCompleted.value = false;
  // You would typically add a reviewMode state here
};

const returnToDashboard = () => {

};

const getCurrentUser = async () => {
  const { data: { user }, error } = await supabase.auth.getUser();
  if (error) throw error;
  return user.id;
};

onMounted(() => {
  if (route.params.courseId) {
    courseId.value = route.params.courseId;
    fetchAvailableQuizzes();
  } else if (route.params.quizId) {
    selectQuiz(route.params.quizId);
  } else {
    toast.error('No course or quiz specified');
    router.push('/home');
  }
});

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value);
  }
});
</script>

<style scoped>
.quiz-taker {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.quiz-header {
  text-align: center;
  margin-bottom: 2rem;
}

.quiz-title {
  font-size: 2rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.quiz-info {
  display: flex;
  gap: 1rem;
  justify-content: center;
  color: #6b7280;
}

.question-navigation {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.question-dot {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.question-dot.active {
  background: #4f46e5;
  color: white;
}

.question-dot.answered {
  background: #059669;
  color: white;
}

.question-container {
  background: white;
  padding: 2rem;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.question-content {
  margin-bottom: 2rem;
}

.question-text {
  font-size: 1.25rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.question-image {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 1rem;
}

.answer-section {
  margin-bottom: 2rem;
}

.option {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option:hover {
  background: #f3f4f6;
}

.text-input, .essay-input {
  width: 100%;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  color: #1f2937;
}

.essay-input {
  resize: vertical;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.nav-button, .submit-button {
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.nav-button {
  background: #f3f4f6;
  color: #4b5563;
}

.nav-button:hover {
  background: #e5e7eb;
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-button {
  background: #059669;
  color: white;
}

.submit-button:hover {
  background: #047857;
}

.submit-button:disabled {
  background: #e5e7eb;
  cursor: not-allowed;
}

/* Course selection styles */
.course-selection {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.quiz-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.quiz-item {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.quiz-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  border-color: #e0e0e0;
}

.quiz-item h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #1f2937;
}

.quiz-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.9rem;
  color: #6b7280;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border-left-color: #4f46e5;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-quizzes {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Timer styles */
.timer {
  font-weight: 600;
  color: #059669;
  background: #ecfdf5;
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
}

.timer-warning {
  color: #dc2626;
  background: #fef2f2;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

/* Results styles */
.quiz-results {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.results-container {
  background: white;
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.results-container h2 {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  color: #1f2937;
}

.score-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2.5rem;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.score-excellent {
  background: #ecfdf5;
  color: #059669;
}

.score-good {
  background: #eef2ff;
  color: #4f46e5;
}

.score-needs-improvement {
  background: #fef2f2;
  color: #dc2626;
}

.score-percentage {
  font-size: 3rem;
  font-weight: 700;
}

.score-details {
  text-align: center;
  font-size: 1.25rem;
}

.score-message {
  font-weight: 600;
  margin-top: 0.75rem;
}

.results-summary {
  background: #f9fafb;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.results-summary h3 {
  text-align: center;
  margin-bottom: 1rem;
  color: #4b5563;
  font-size: 1.2rem;
}

.summary-stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.stat-label {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.results-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.review-button, .dashboard-button {
  padding: 0.85rem 1.75rem;
  border-radius: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.review-button {
  background: #f3f4f6;
  color: #4b5563;
}

.review-button:hover {
  background: #e5e7eb;
}

.dashboard-button {
  background: #4f46e5;
  color: white;
}

.dashboard-button:hover {
  background: #4338ca;
}

@media (max-width: 640px) {
  .quiz-title {
    font-size: 1.5rem;
  }

  .question-container {
    padding: 1rem;
  }
  
  .score-circle {
    width: 120px;
    height: 120px;
  }
  
  .score-percentage {
    font-size: 2.5rem;
  }
  
  .summary-stats {
    gap: 1.5rem;
  }
  
  .results-actions {
    flex-direction: column;
  }
}
</style>
