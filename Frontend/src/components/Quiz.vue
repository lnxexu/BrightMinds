<template>
    <div class="quiz-container">
        <div class="quiz-header">
            <div class="accent-bar"></div>
            <h1>Quiz</h1>
        </div>

        <div v-if="currentQuiz" class="quiz-content">
            <div class="quiz-info-card">
                <h2>{{ currentQuiz.title }}</h2>
                <p class="quiz-description">{{ currentQuiz.description }}</p>
            </div>

            <div v-for="(question, index) in questions" :key="index" class="question-card">
                <div class="question-number">Question {{ index + 1 }}</div>
                <p class="question-text">{{ question.question_text }}</p>
                
                <div v-if="question.type === 'multiple_choice'" class="options-container">
                    <div v-for="option in question.options" :key="option.id" class="option">
                        <label class="option-label">
                            <input 
                                type="radio" 
                                :name="'question' + index" 
                                :value="option.option_text"
                                v-model="answers[index]"
                            >
                            <span class="radio-custom"></span>
                            <span class="option-text">{{ option.option_text }}</span>
                        </label>
                    </div>
                </div>

                <div v-else class="essay-container">
                    <textarea
                        v-model="answers[index]"
                        :placeholder="question.type === 'essay' ? 'Write your essay here...' : 'Type your answer here...'"
                        :rows="question.type === 'essay' ? 6 : 2"
                        class="modern-textarea"
                    ></textarea>
                </div>
            </div>

            <div class="submit-container">
                <button @click="submitQuiz" class="submit-btn" :disabled="!isQuizComplete">
                    {{ submitButtonText }}
                </button>
            </div>
        </div>
        
        <div v-else-if="error" class="error-message">
            {{ error }}
        </div>
        <div v-else class="loading">
            <p>Loading quiz...</p>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { supabase } from '@/lib/supabaseClient'

const route = useRoute()
const router = useRouter()

const currentQuiz = ref(null)
const questions = ref([])
const answers = ref([])
const error = ref(null)
const isSubmitting = ref(false)

const isQuizComplete = computed(() => {
    return answers.value.length === questions.value.length && 
           !answers.value.includes(null)
})

const submitButtonText = computed(() => {
    return isSubmitting.value ? 'Submitting...' : 'Submit Quiz'
})

const fetchQuiz = async () => {
    try {
        const quizId = route.params.id
        console.log('Fetching quiz with ID:', quizId)
        const { data: quiz, error: quizError } = await supabase
            .from('quizzes')
            .select('*')

        if (quizError) {
            if (quizError.code === 'PGRST116') {
                error.value = 'Quiz not found. Please check the URL.'
            } else {
                error.value = 'Failed to load quiz. Please try again later.'
            }
            throw quizError
        }

        const { data: questionData, error: questionsError } = await supabase
            .from('questions')
            .select('*')
            .order('id', { ascending: true })


        if (questionsError) throw questionsError

        currentQuiz.value = quiz
        questions.value = questionData
        answers.value = new Array(questionData.length).fill(null)
    } catch (err) {
        error.value = 'Failed to load quiz. Please try again later.'
        console.error('Error fetching quiz:', err)
    }
}

const submitQuiz = async () => {
    if (!isQuizComplete.value) return

    isSubmitting.value = true
    try {
        const quizResults = {
            quiz_id: currentQuiz.value.id,
            answers: questions.value.map((question, index) => ({
                question_id: question.id,
                selected_answer: answers.value[index],
                is_correct: question.options.find(
                    opt => opt.option_text === answers.value[index]
                )?.is_correct || false
            })),
            submitted_at: new Date()
        }

        const { error: submitError } = await supabase
            .from('quiz_submissions')
            .insert([quizResults])

        if (submitError) throw submitError

        router.push(`/quiz-results/${currentQuiz.value.id}`)
    } catch (err) {
        error.value = 'Failed to submit quiz. Please try again.'
        console.error('Error submitting quiz:', err)
    } finally {
        isSubmitting.value = false
    }
}

onMounted(() => {
    fetchQuiz()
});
</script>

<style scoped>
.quiz-container {
    max-width: 768px;
    margin: 2rem auto;
    padding: 0 20px;
}

.quiz-header {
    position: relative;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 24px;
    margin-bottom: 24px;
}

.accent-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 10px;
    background: #673AB7;
    border-radius: 8px 8px 0 0;
}

.quiz-info-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 24px;
    margin-bottom: 24px;
}

.quiz-header h1 {
    color: #202124;
    font-size: 32px;
    margin: 8px 0;
}

.quiz-description {
    color: #5f6368;
    font-size: 14px;
    margin-top: 8px;
}

.question {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.option {
    margin: 10px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.submit-btn {
    background-color: #673AB7;
    color: white;
    padding: 10px 24px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
    background-color: #5c33a4;
}

.submit-btn:disabled {
    background-color: #dadce0;
    cursor: not-allowed;
}

.error-message {
    background: #fdeded;
    color: #5f6368;
    padding: 16px;
    border-radius: 8px;
    margin-top: 24px;
    text-align: center;
}

.loading {
    text-align: center;
    padding: 24px;
    color: #5f6368;
}

.question-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 24px;
    margin-bottom: 24px;
}

.question-number {
    color: #5f6368;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 16px;
}

.question-text {
    color: #202124;
    font-size: 16px;
    font-weight: 400;
    margin-bottom: 16px;
}

.options-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.option-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 12px;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.option-label:hover {
    background-color: #f8f9fa;
}

.radio-custom {
    width: 20px;
    height: 20px;
    border: 2px solid #5f6368;
    border-radius: 50%;
    margin-right: 12px;
    position: relative;
    transition: all 0.2s;
}

.option-label input[type="radio"] {
    display: none;
}

.option-label input[type="radio"]:checked + .radio-custom {
    border-color: #673AB7;
}

.option-label input[type="radio"]:checked + .radio-custom::after {
    content: '';
    position: absolute;
    top: 4px;
    left: 4px;
    width: 8px;
    height: 8px;
    background: #673AB7;
    border-radius: 50%;
}


.essay-container {
    margin-top: 1rem;
    width: 100%;
}

.option-text {
    color: #202124;
    font-size: 14px;
}

.modern-textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #dadce0;
    border-radius: 4px;
    font-size: 14px;
    line-height: 1.5;
    transition: all 0.2s;
    resize: vertical;
    min-height: 60px;
}

.modern-textarea:focus {
    outline: none;
    border-color: #673AB7;
    box-shadow: 0 0 0 2px rgba(103, 58, 183, 0.1);
}

.modern-textarea::placeholder {
    color: #5f6368;
}
</style>