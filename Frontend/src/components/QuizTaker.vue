<template>
  <div class="quiz-taker">
    <div class="quiz-header" v-if="quiz">
      <h2 class="quiz-title">{{ quiz.title }}</h2>
      <div class="quiz-info">
        <span class="course">{{ quiz.course_name }}</span>
        <span class="topic">{{ quiz.topic_name }}</span>
        <span class="question-count">{{ questions.length }} Questions</span>
      </div>
    </div>

    <div class="quiz-content" v-if="currentQuestion">
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { supabase } from '@/lib/supabaseClient';
import { useToast } from 'vue-toastification';

const route = useRoute();
const toast = useToast();

const quiz = ref(null);
const questions = ref([]);
const currentQuestionIndex = ref(0);
const answers = ref({});

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value]);

const isQuizComplete = computed(() => {
  return questions.value.every((_, index) => answers.value[index] !== undefined);
});

const fetchQuiz = async () => {
  try {
    const { data: quizData, error: quizError } = await supabase
      .from('quizzes')
      .select('*')
      .eq('id', route.params.quizId)
      .single();

    if (quizError) throw quizError;
    quiz.value = quizData;

    const { data: questionData, error: questionError } = await supabase
      .from('questions')
      .select('*')
      .eq('quiz_id', route.params.quizId)
      .order('order_number');

    if (questionError) throw questionError;
    questions.value = questionData;
  } catch (error) {
    console.error('Error fetching quiz:', error);
    toast.error('Failed to load quiz');
  }
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

const submitQuiz = async () => {
  try {
    const submission = {
      quiz_id: quiz.value.id,
      student_id: await getCurrentUser(),
      answers: answers.value,
      submitted_at: new Date().toISOString()
    };

    const { error } = await supabase
      .from('quiz_submissions')
      .insert(submission);

    if (error) throw error;

    toast.success('Quiz submitted successfully!');
    // Redirect to results or dashboard
  } catch (error) {
    console.error('Error submitting quiz:', error);
    toast.error('Failed to submit quiz');
  }
};

const getCurrentUser = async () => {
  const { data: { user }, error } = await supabase.auth.getUser();
  if (error) throw error;
  return user.id;
};

onMounted(() => {
  fetchQuiz();
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

@media (max-width: 640px) {
  .quiz-title {
    font-size: 1.5rem;
  }

  .question-container {
    padding: 1rem;
  }
}
</style>
