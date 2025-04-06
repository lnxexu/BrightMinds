<template>
  <div class="quiz-creator">
    <div class="section-header">
      <h2 class="section-title">Create a <span class="title-accent">Quiz</span></h2>
      <p class="section-description">Design engaging quizzes for your students</p>
    </div>

    <div class="quiz-container">
      <div class="form-section">
        <form @submit.prevent="addQuestion" class="quiz-form">
          <div class="form-group">
            <label for="questionType">Question Type</label>
            <select v-model="questionType" id="questionType" class="select-input">
              <option value="multiple">Multiple Choice</option>z
              <option value="text">Text Answer</option>
              <option value="true-false">True/False</option>
            </select>
          </div>

          <div class="form-group">
            <label for="question">Question</label>
            <div class="input-wrapper">
              <i class="fas fa-question-circle"></i>
              <input
                v-model="newQuestion"
                type="text"
                id="question"
                placeholder="Enter your question here..."
                class="text-input"
                required
              />
            </div>
          </div>

          <div class="options-container" v-if="questionType === 'multiple'">
            <div class="option-group" v-for="(option, index) in options" :key="index">
              <div class="input-wrapper">
                <i class="fas fa-check-circle"></i>
                <input
                  v-model="options[index]"
                  type="text"
                  :placeholder="`Option ${index + 1}`"
                  class="text-input"
                />
              </div>
            </div>
            <button type="button" @click="addOption" class="secondary-button">
              <i class="fas fa-plus"></i>
              Add Option
            </button>
          </div>

          <button type="submit" class="primary-button">
            <i class="fas fa-plus"></i>
            Add Question
          </button>
        </form>
      </div>

      <div class="preview-section">
        <div class="preview-header">
          <h3 class="preview-title">
            <i class="fas fa-eye"></i>
            Quiz Preview
          </h3>
          <span class="question-count">{{ questions.length }} Questions</span>
        </div>

        <div class="questions-list" v-if="questions.length">
          <div v-for="(question, index) in questions" 
               :key="index" 
               class="question-card">
            <div class="question-header">
              <span class="question-number">Q{{ index + 1 }}</span>
              <div class="question-actions">
                <button class="action-button" @click="editQuestion(index)">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="action-button delete" @click="deleteQuestion(index)">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
            <p class="question-text">{{ question }}</p>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="fas fa-clipboard-list"></i>
          <p>No questions added yet</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const newQuestion = ref("");
const questions = ref([]);
const questionType = ref("multiple");
const options = ref(["", "", "", ""]);

const addQuestion = () => {
  if (newQuestion.value.trim()) {
    questions.value.push(newQuestion.value.trim());
    newQuestion.value = "";
    options.value = ["", "", "", ""];
  }
};

const addOption = () => {
  options.value.push("");
};

const deleteQuestion = (index) => {
  questions.value.splice(index, 1);
};

const editQuestion = (index) => {
  newQuestion.value = questions.value[index];
  questions.value.splice(index, 1);
};

</script>

<style scoped>
.quiz-creator {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
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

.quiz-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.form-section {
  background: white;
  padding: 2rem;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border-radius: 12px;
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
}

.input-wrapper i {
  color: #6b7280;
  margin-right: 0.75rem;
}

.text-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.5rem;
  font-size: 1rem;
  color: #1f2937;
}

.text-input:focus {
  outline: none;
}

.select-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #f8fafc;
  color: #1f2937;
  font-size: 1rem;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.option-group {
  display: flex;
  gap: 0.5rem;
}

.primary-button, .secondary-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.primary-button {
  background: #4f46e5;
  color: white;
  width: 100%;
}

.secondary-button {
  background: #e0e7ff;
  color: #4f46e5;
}

.primary-button:hover, .secondary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.preview-section {
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.preview-header {
  background: #f8fafc;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.question-count {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.questions-list {
  padding: 2rem;
  max-height: 500px;
  overflow-y: auto;
}

.question-card {
  background: #f8fafc;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e5e7eb;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  background: #4f46e5;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.question-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  background: white;
  border: 1px solid #e5e7eb;
  padding: 0.5rem;
  border-radius: 8px;
  color: #6b7280;
  transition: all 0.3s ease;
}

.action-button:hover {
  color: #4f46e5;
  border-color: #4f46e5;
}

.action-button.delete:hover {
  color: #ef4444;
  border-color: #ef4444;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

@media (max-width: 1024px) {
  .quiz-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .section-title {
    font-size: 2rem;
  }
  
  .form-section, .preview-section {
    padding: 1rem;
  }
}
</style>