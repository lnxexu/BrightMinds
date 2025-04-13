<template>
  <div class="quiz-creator">
    <div class="section-header">
      <h2 class="section-title">
        Create a <span class="title-accent">Quiz</span>
      </h2>
      <p class="section-description">
        Design engaging quizzes for your students
      </p>
    </div>

    <!-- Add course and topic selection -->

    <div v-if="!showQuizForm" class="selection-container">
      <div class="form-section">
        <div class="form-group">
          <label for="course">Select Course</label>
          <select
            id="course"
            v-model="selectedCourse"
            @change="handleCourseChange"
            class="select-input"
            required
          >
            <option value="">Choose a course</option>
            <option
              v-for="course in courses"
              :key="course.name"
              :value="course.name"
            >
              {{ course.name }}
            </option>
          </select>
        </div>

        <div class="form-group" v-if="selectedCourse">
          <label for="topic">Select Topic</label>
          <select
            id="topic"
            v-model="selectedTopic"
            class="select-input"
            required
          >
            <option value="" disabled selected>Choose a topic</option>
            <option
              v-for="topic in topics"
              :key="topic.topic_name"
              :value="topic.topic_name"
            >
              {{ topic.topic_name }}
            </option>
          </select>
        </div>

        <button
          @click="handleTopicSelection"
          :disabled="!selectedCourse || !selectedTopic"
          class="primary-button"
        >
          <i class="fas fa-arrow-right"></i>
          Continue to Quiz Creation
        </button>
      </div>
    </div>

    <div v-else class="quiz-container">
      <div class="form-section">
        <form @submit.prevent="addQuestion" class="quiz-form">
          <div class="form-group">
            <label for="quizTitle">Quiz Title</label>
            <div class="input-wrapper">
              <i class="fas fa-heading"></i>
              <input
                v-model="quizTitle"
                type="text"
                id="quizTitle"
                placeholder="Enter quiz title..."
                class="text-input"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="questionType">Question Type</label>
            <select
              v-model="questionType"
              id="questionType"
              class="select-input"
            >
              <option value="multiple_choice">Multiple Choice</option>
              <option value="identification">Identification</option>
              <option value="essay">Essay</option>
            </select>
          </div>

          <div class="form-group">
            <label for="question">Question Text</label>
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

          <div class="form-group">
            <label for="questionImage">Question Image (Optional)</label>
            <div class="image-upload-wrapper">
              <input
                type="file"
                id="questionImage"
                @change="handleImageUpload"
                accept="image/*"
                class="image-input"
              />
              <div class="image-preview" v-if="imagePreview">
                <img :src="imagePreview" alt="Question image preview" />
                <button type="button" @click="removeImage" class="remove-image">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>

          <div v-if="questionType === 'multiple_choice'" class="form-group">
            <label>Answer Options</label>
            <div class="options-container">
              <div
                v-for="(option, index) in options"
                :key="index"
                class="option-group"
              >
                <div class="input-wrapper">
                  <input
                    v-model="options[index]"
                    type="text"
                    :placeholder="'Option ' + (index + 1)"
                    class="text-input"
                    required
                  />
                  <button
                    v-if="index > 1"
                    type="button"
                    @click="removeOption(index)"
                    class="remove-option"
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <input
                  type="radio"
                  :value="index"
                  v-model="correctAnswer"
                  name="correct-answer"
                  required
                />
              </div>
            </div>
            <button
              v-if="options.length < 6"
              type="button"
              @click="addOption"
              class="secondary-button"
            >
              <i class="fas fa-plus"></i>
              Add Option
            </button>
          </div>

          <div v-else-if="questionType === 'identification'" class="form-group">
            <label for="correctAnswer">Correct Answer</label>
            <div class="input-wrapper">
              <i class="fas fa-check-circle"></i>
              <input
                v-model="correctAnswer"
                type="text"
                id="correctAnswer"
                placeholder="Enter the correct answer..."
                class="text-input"
                required
              />
            </div>
          </div>

          <button type="submit" class="primary-button">
            <i class="fas fa-plus"></i>
            Add Question
          </button>
        </form>

        <div class="button-group">
          <button
            @click="saveQuiz"
            class="save-button"
            :disabled="!questions.length"
          >
            <i class="fas fa-save"></i>
            Save Quiz
          </button>
        </div>
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
          <div
            v-for="(question, index) in questions"
            :key="index"
            class="question-card"
          >
            <div class="question-header">
              <span class="question-number">Q{{ index + 1 }}</span>
              <div class="question-actions">
                <button class="action-button" @click="editQuestion(index)">
                  <i class="fas fa-edit"></i>
                </button>
                <button
                  class="action-button delete"
                  @click="deleteQuestion(index)"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
            <div class="question-content">
              <img
                v-if="question.imageUrl"
                :src="question.imageUrl"
                alt="Question image"
                class="question-image"
              />
              <p v-else class="question-text">{{ question.text }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "vue-toastification";
import { supabase } from "@/lib/supabaseClient";

const quizTitle = ref("");
const toast = useToast();
const newQuestion = ref("");
const questions = ref([]);
const questionType = ref("multiple");
const options = ref(["", "", "", ""]);
const correctAnswer = ref(null);
const useImage = ref(false);
const imageFile = ref(null);
const imagePreview = ref(null);
const selectedCourse = ref(null);
const selectedTopic = ref(null);
const courses = ref([]);
const topics = ref([]);
const showQuizForm = ref(false);
const user = ref(null);

const fetchCourses = async () => {
  try {
    const { data, error } = await supabase
      .from("courses")
      .select("name")
      .order("name", { ascending: true });

    if (error) {
      console.error("Error fetching courses:", error);
      return;
    }

    courses.value = data || [];
    console.log("Fetched courses:", courses.value);
  } catch (error) {
    console.error("Error fetching courses:", error);
  }
};

const fetchTopics = async (courseId) => {
  if (!courseId) return;

  try {
    const { data, error } = await supabase
      .from("topics")
      .select("id, topic_name")
      .eq("course", courseId)
      .order("topic_name", { ascending: true });

    if (error) {
      console.error("Error fetching topics:", error);
      return;
    }

    topics.value = data || [];
    console.log("Fetched topics:", topics.value);
  } catch (error) {
    console.error("Error in fetchTopics:", error);
  }
};

const handleCourseChange = async () => {
  console.log("Course changed to:", selectedCourse.value);
  selectedTopic.value = null;
  topics.value = [];

  if (selectedCourse.value) {
    await fetchTopics(selectedCourse.value);
  }
};

// Handle topic selection
const handleTopicSelection = () => {
  if (selectedCourse.value && selectedTopic.value) {
    showQuizForm.value = true;
  }
};

const removeOption = (index) => {
  options.value.splice(index, 1);
  if (correctAnswer.value === index) {
    correctAnswer.value = null;
  }
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
  }
};

const removeImage = () => {
  imageFile.value = null;
  imagePreview.value = null;
};

const uploadImage = async (file) => {
  try {
    const fileExt = file.name.split(".").pop();
    const fileName = `${Math.random()}.${fileExt}`;
    const filePath = `quiz-images/${fileName}`;

    // Upload the file
    const { error: uploadError } = await supabase.storage
      .from("quiz-images")
      .upload(filePath, file);

    if (uploadError) throw uploadError;

    // Get the public URL
    const { data } = supabase.storage
      .from("quiz-images")
      .getPublicUrl(filePath);

    if (!data.publicUrl) {
      throw new Error("Could not get public URL for uploaded image");
    }

    console.log("Image uploaded, public URL:", data.publicUrl);
    return data.publicUrl;
  } catch (error) {
    console.error("Error uploading image:", error);
    throw error;
  }
};

const addQuestion = async () => {
  try {
    let questionData = {
      type: questionType.value,
      text: newQuestion.value.trim(),
      imageUrl: null,
      imageFile: null, // Add this to store the file temporarily
      options: questionType.value === "multiple_choice" ? options.value : null,
      correctAnswer:
        questionType.value !== "essay" ? correctAnswer.value : null,
    };

    // If there's an image file, store it and its preview URL
    if (imageFile.value) {
      try {
        const imageUrl = await uploadImage(imageFile.value);
        questionData.imageUrl = imageUrl;
        console.log("Image URL set:", imageUrl); // Debug log
      } catch (error) {
        console.error("Error uploading image:", error);
        toast.error("Failed to upload image");
        return;
      }
    }

    questions.value.push(questionData);
    console.log("Added question with data:", questionData); // Debug log

    // Reset form
    newQuestion.value = "";
    imageFile.value = null;
    imagePreview.value = null;
    useImage.value = false;
    options.value = ["", "", "", ""];
    correctAnswer.value = null;

    toast.success("Question added successfully");
  } catch (error) {
    console.error("Error adding question:", error);
    toast.error("Failed to add question");
  }
};

const saveQuiz = async () => {
  try {
    if (!quizTitle.value || !questions.value.length) {
      console.error("Quiz title or questions are missing.");
      return;
    }

    if (useImage.value && imageFile.value) {
      const imageUrl = await uploadImage(imageFile.value);
      questions.value[questions.value.length - 1].imageUrl = imageUrl;
    }

    for (const question of questions.value) {
      if (question.imageFile && !question.imageUrl) {
        try {
          const imageUrl = await uploadImage(question.imageFile);
          question.imageUrl = imageUrl;
          delete question.imageFile; // Remove the file object after upload
        } catch (error) {
          console.error("Error uploading image:", error);
          toast.error("Failed to upload image");
          return;
        }
      }
    }

    const { data: quiz, error: quizError } = await supabase
      .from("quizzes")
      .insert({
        title: quizTitle.value,
        created_by: user.value,
        created_at: new Date().toISOString(),
        course_name: selectedCourse.value,
        topic_name: selectedTopic.value,
      })
      .select();

    if (quizError) {
      console.error("Error saving quiz:", quizError);
      return;
    }
    const questionsData = questions.value.map((q, index) => ({
      quiz_id: quiz[0].id,
      question_type: q.type,
      question_text: q.text,
      question_image_url: q.imageUrl || null,
      options: q.type === "multiple_choice" ? q.options : null,
      correct_answer: q.type !== "essay" ? q.correctAnswer : null,
      order_number: index + 1,
    }));

    const { error: questionsError } = await supabase
      .from("questions")
      .insert(questionsData);

    if (questionsError) {
      console.error("Error saving questions:", questionsError);
      toast.error("Failed to save questions");
      return;
    }

    // Reset form after successful save
    quizTitle.value = "";
    questions.value = [];
    showQuizForm.value = false;
    toast.success("Quiz saved successfully!");
  } catch (error) {
    console.error("Error saving quiz:", error);
    toast.error("Failed to save quiz");
  }
};

const getCurrentUser = async () => {
  try {
    const {
      data: { user: currentUser },
      error,
    } = await supabase.auth.getUser();
    if (error) throw error;
    user.value = currentUser.id;
    console.log("Current user:", user.value);
  } catch (error) {
    console.error("Error getting user:", error);
    toast.error("Error getting user information");
  }
};

const addOption = () => {
  options.value.push("");
};

const deleteQuestion = (index) => {
  questions.value.splice(index, 1);
};

const editQuestion = (index) => {
  const question = questions.value[index];
  questionType.value = question.type;
  useImage.value = !!question.imageUrl;

  if (question.imageUrl) {
    imagePreview.value = question.imageUrl;
  } else {
    newQuestion.value = question.text;
  }

  if (question.type === "multiple_choice") {
    options.value = [...question.options];
    correctAnswer.value = question.correctAnswer;
  } else if (question.type === "identification") {
    correctAnswer.value = question.correctAnswer;
  }

  questions.value.splice(index, 1);
};

onMounted(() => {
  fetchCourses();
  getCurrentUser();
});
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
  margin-bottom: 1rem;
}

.option-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.option-group .input-wrapper {
  flex: 1;
}

.remove-option {
  color: #ef4444;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.primary-button,
.secondary-button {
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

.primary-button:hover,
.secondary-button:hover {
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

.image-upload-wrapper {
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
}

.image-input {
  width: 100%;
  padding: 1rem;
}

.image-preview {
  position: relative;
  margin-top: 1rem;
}

.image-preview img {
  max-width: 100%;
  border-radius: 8px;
}

.remove-image {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.toggle-group {
  display: flex;
  gap: 0.5rem;
}

.toggle-btn {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #6b7280;
}

.toggle-btn.active {
  background: #4f46e5;
  color: white;
  border-color: #4f46e5;
}

.question-image {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 1rem;
}

.selection-container {
  max-width: 600px;
  margin: 0 auto;
}

.selection-container .form-section {
  background: white;
  padding: 2rem;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.selection-container .primary-button {
  margin-top: 2rem;
}

.selection-container .primary-button:disabled {
  background: #e5e7eb;
  cursor: not-allowed;
  transform: none;
}

.button-group {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.save-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem 1.5rem;
  background: #059669;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-button:hover {
  background: #047857;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.2);
}

.save-button:disabled {
  background: #e5e7eb;
  cursor: not-allowed;
  transform: none;
}

.save-button i {
  font-size: 1.1rem;
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

  .form-section,
  .preview-section {
    padding: 1rem;
  }
}
</style>
