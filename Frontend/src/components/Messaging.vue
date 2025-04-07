<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messageContainer">
      <div v-if="messages.length" class="messages-list">
        <div v-for="message in messages" 
             :key="message.id" 
             :class="['message', message.sender_id === currentUserId ? 'sent' : 'received']">
          <div class="message-content">
            <p>{{ message.content }}</p>
            <span class="message-time">{{ formatTime(message.created_at) }}</span>
          </div>
        </div>
      </div>
      <div v-else class="no-messages">
        No messages yet. Start the conversation!
      </div>
    </div>
    
    <div class="message-input">
      <input 
        v-model="newMessage" 
        @keyup.enter="sendMessage"
        placeholder="Type your message..."
        type="text"
      />
      <button @click="sendMessage" :disabled="!newMessage.trim()">
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { supabase } from '../lib/supabaseClient.js';

const route = useRoute();
const router = useRouter();
const messages = ref([]);
const newMessage = ref('');
const messageContainer = ref(null);
const currentUserId = ref(null);
const teacherId = ref(null);

// Initialize Supabase subscription
const subscription = ref(null);

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

const scrollToBottom = () => {
  if (messageContainer.value) {
    setTimeout(() => {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }, 50);
  }
};

const fetchMessages = async () => {
  const { data, error } = await supabase
    .from('messages')
    .select('*')
    .or(`sender_id.eq.${currentUserId.value},recipient_id.eq.${currentUserId.value}`)
    .order('created_at', { ascending: true });

  if (error) {
    console.error('Error fetching messages:', error);
    return;
  }

  messages.value = data;
  scrollToBottom();
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  const { data, error } = await supabase
    .from('messages')
    .insert([{
      sender_id: currentUserId.value,
      recipient_id: teacherId.value,
      content: newMessage.value.trim(),
    }]);

  if (error) {
    console.error('Error sending message:', error);
    return;
  }

  newMessage.value = '';
  await fetchMessages();
};

const subscribeToMessages = () => {
  subscription.value = supabase
    .channel('messages')
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'messages',
        filter: `sender_id=eq.${currentUserId.value} OR recipient_id=eq.${currentUserId.value}`
      },
      () => {
        fetchMessages();
      }
    )
    .subscribe();
};

onMounted(async () => {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    router.push('/login');
    return;
  }
  
  currentUserId.value = user.id;
  teacherId.value = route.params.teacherId;
  
  await fetchMessages();
  subscribeToMessages();
});

onUnmounted(() => {
  if (subscription.value) {
    subscription.value.unsubscribe();
  }
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: 80vh;
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  max-width: 70%;
  padding: 10px;
  border-radius: 12px;
  margin: 4px 0;
}

.sent {
  align-self: flex-end;
  background-color: #007bff;
  color: white;
}

.received {
  align-self: flex-start;
  background-color: #e9ecef;
  color: #212529;
}

.message-content {
  position: relative;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.8;
  margin-top: 4px;
  display: block;
}

.message-input {
  display: flex;
  padding: 15px;
  background: white;
  border-top: 1px solid #dee2e6;
  gap: 10px;
}

.message-input input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  outline: none;
}

.message-input button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.message-input button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.no-messages {
  text-align: center;
  color: #6c757d;
  padding: 20px;
}
</style>