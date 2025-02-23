<template>
  <div class="messaging-container">
    <div class="messaging-header">
      <h2 class="heading">Messages</h2>
      <div class="active-status">
        <span class="status-dot"></span>
        Online
      </div>
    </div>

    <div class="messages-section" ref="messageContainer">
      <div v-for="message in messages" 
           :key="message.id" 
           :class="['message-item', message.sender === 'You' ? 'outgoing' : 'incoming']">
        <div class="message-content">
          <div class="message-info">
            <span class="sender">{{ message.sender }}</span>
            <span class="time">{{ message.time || '12:00 PM' }}</span>
          </div>
          <p class="message-text">{{ message.text }}</p>
        </div>
        <div class="avatar">
          <i :class="message.sender === 'You' ? 'fas fa-user' : 'fas fa-user-tie'"></i>
        </div>
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="message-form">
      <div class="input-wrapper">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          class="message-input"
          required
        />
        <div class="input-actions">
          <button type="button" class="action-button">
            <i class="fas fa-paperclip"></i>
          </button>
          <button type="button" class="action-button">
            <i class="far fa-smile"></i>
          </button>
        </div>
      </div>
      <button type="submit" class="send-button">
        <i class="fas fa-paper-plane"></i>
      </button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from "vue";

export default {
  name: "MessagingComponent",
  setup() {
    const messages = ref([
      { 
        id: 1, 
        sender: "Teacher", 
        text: "Welcome to the course! How can I help you today?",
        time: "11:30 AM" 
      },
      { 
        id: 2, 
        sender: "You", 
        text: "Thank you! I have a question about the latest assignment.",
        time: "11:32 AM" 
      },
      { 
        id: 3, 
        sender: "Teacher", 
        text: "Of course! What would you like to know?",
        time: "11:33 AM" 
      }
    ]);

    const newMessage = ref("");
    const messageContainer = ref(null);

    const scrollToBottom = async () => {
      await nextTick();
      if (messageContainer.value) {
        messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
      }
    };

    const sendMessage = () => {
      if (newMessage.value.trim()) {
        messages.value.push({
          id: messages.value.length + 1,
          sender: "You",
          text: newMessage.value.trim(),
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        });
        newMessage.value = "";
        scrollToBottom();
      }
    };

    onMounted(scrollToBottom);

    return { messages, newMessage, sendMessage, messageContainer };
  },
};
</script>

<style scoped>
.messaging-container {
  max-width: 800px;
  margin: 2rem auto;
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.messaging-header {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.heading {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.active-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  display: inline-block;
}

.messages-section {
  height: 400px;
  overflow-y: auto;
  padding: 1.5rem;
  background: #f8fafc;
}

.message-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: flex-start;
}

.message-content {
  max-width: 70%;
  background: white;
  padding: 1rem;
  border-radius: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.outgoing {
  flex-direction: row-reverse;
}

.outgoing .message-content {
  background: #4f46e5;
  color: white;
}

.outgoing .message-info {
  color: rgba(255, 255, 255, 0.9);
}

.message-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.sender {
  font-weight: 600;
}

.avatar {
  width: 40px;
  height: 40px;
  background: #e0e7ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4f46e5;
}

.outgoing .avatar {
  background: #4f46e5;
  color: white;
}

.message-form {
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  background: white;
  border-top: 1px solid #e5e7eb;
}

.input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f8fafc;
  border-radius: 12px;
  padding: 0.5rem 1rem;
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.5rem;
  font-size: 1rem;
  color: #1f2937;
}

.message-input:focus {
  outline: none;
}

.input-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  background: none;
  border: none;
  color: #6b7280;
  padding: 0.5rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.action-button:hover {
  color: #4f46e5;
}

.send-button {
  background: #4f46e5;
  color: white;
  border: none;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-button:hover {
  background: #4338ca;
  transform: translateY(-2px);
}

@media (max-width: 640px) {
  .messaging-container {
    margin: 1rem;
    border-radius: 16px;
  }

  .messages-section {
    height: calc(100vh - 200px);
  }

  .message-content {
    max-width: 85%;
  }
}
</style>