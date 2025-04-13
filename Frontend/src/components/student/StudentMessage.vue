<template>
    <div class="student-dashboard">
      <!-- Student Navigation Bar -->
      <StudentNavBar />
  
      <!-- Messaging Section -->
      <div class="messaging-container">
        <!-- Recipient Dropdown Selector -->
        <div class="recipient-selector">
          <label for="recipient">Select Recipient:</label>
          <select
            id="recipient"
            v-model="selectedRecipient"
            @change="updateRecipient"
          >
            <option disabled value="">-- Select a recipient --</option>
            <option v-for="r in filteredRecipients" :key="r.id" :value="r.id">
              {{ r.full_name }}
            </option>
          </select>
        </div>
  
        <!-- Messaging Header -->
        <div class="messaging-header">
          <h2 class="heading">Messages</h2>
          <div class="active-status">
            <span class="status-dot"></span>
            Online
          </div>
        </div>
  
        <!-- Messages Section -->
        <div class="messages-section" ref="messageContainer">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="[
              'message-item',
              message.sender === 'You' ? 'outgoing' : 'incoming',
            ]"
          >
            <div class="message-content">
              <div class="message-info">
                <span class="sender">{{ message.sender }}</span>
                <span class="time">{{ message.time || "12:00 PM" }}</span>
              </div>
              <p class="message-text">{{ message.text }}</p>
            </div>
            <div class="avatar">
              <i
                :class="
                  message.sender === 'You' ? 'fas fa-user' : 'fas fa-user-tie'
                "
              ></i>
            </div>
          </div>
        </div>
  
        <!-- Message Form -->
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
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, nextTick, computed } from "vue";
  import { supabase } from "@/lib/supabaseClient";
  import StudentNavBar from "./StudentNavBar.vue";
  
  // Props (for v-model)
  const props = defineProps({
    modelValue: {
      type: String,
      required: true,
    },
  });
  
  const emit = defineEmits(["update:modelValue"]);
  
  const messages = ref([]);
  const newMessage = ref("");
  const messageContainer = ref(null);
  const subscription = ref(null);
  const currentUserId = ref(null);
  const selectedRecipient = ref(props.modelValue);
  const recipientOptions = ref([]);
  
  const updateRecipient = (event) => {
    emit("update:modelValue", event.target.value);
    fetchMessages();
  };
  
  const filteredRecipients = computed(() =>
    recipientOptions.value.filter((r) => r.id !== currentUserId.value)
  );
  
  const scrollToBottom = async () => {
    await nextTick();
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  };
  
  const fetchMessages = async () => {
    if (!currentUserId.value || !selectedRecipient.value) return;
  
    const { data, error } = await supabase
      .from("messages")
      .select("*")
      .or(
        `sender_id.eq.${currentUserId.value},recipient_id.eq.${currentUserId.value}`
      )
      .order("created_at", { ascending: true });
  
    if (error) {
      console.error("Error fetching messages:", error);
      return;
    }
  
    messages.value = data
      .filter(
        (msg) =>
          (msg.sender_id === currentUserId.value &&
            msg.recipient_id === selectedRecipient.value) ||
          (msg.sender_id === selectedRecipient.value &&
            msg.recipient_id === currentUserId.value)
      )
      .map((msg) => ({
        id: msg.id,
        sender: msg.sender_id === currentUserId.value ? "You" : "Recipient",
        text: msg.content,
        time: new Date(msg.created_at).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      }));
  
    await scrollToBottom();
  };
  
  const sendMessage = async () => {
    if (
      !newMessage.value.trim() ||
      !currentUserId.value ||
      !selectedRecipient.value
    )
      return;
  
    const { error } = await supabase.from("messages").insert([
      {
        sender_id: currentUserId.value,
        recipient_id: selectedRecipient.value,
        content: newMessage.value.trim(),
        created_at: new Date().toISOString(),
      },
    ]);
  
    if (!error) newMessage.value = "";
  };
  
  const subscribeToMessages = () => {
    if (!currentUserId.value) return;
  
    subscription.value = supabase
      .channel("messages")
      .on(
        "postgres_changes",
        {
          event: "INSERT",
          schema: "public",
          table: "messages",
        },
        (payload) => {
          const msg = payload.new;
          const relevant =
            (msg.sender_id === currentUserId.value &&
              msg.recipient_id === selectedRecipient.value) ||
            (msg.sender_id === selectedRecipient.value &&
              msg.recipient_id === currentUserId.value);
  
          if (relevant) {
            messages.value.push({
              id: msg.id,
              sender: msg.sender_id === currentUserId.value ? "You" : "Recipient",
              text: msg.content,
              time: new Date(msg.created_at).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              }),
            });
            scrollToBottom();
          }
        }
      )
      .subscribe();
  };
  
  onMounted(async () => {
    const { data, error } = await supabase.auth.getUser();
    if (error || !data?.user) {
      console.error("Unable to fetch authenticated user", error);
      return;
    }
  
    currentUserId.value = data.user.id;
  
    const { data: users } = await supabase.from("users").select("id, full_name");
    recipientOptions.value = users || [];
  
    await fetchMessages();
    subscribeToMessages();
  });
  
  onUnmounted(() => {
    if (subscription.value) subscription.value.unsubscribe();
  });
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
  .chat-head {
    position: fixed;
    bottom: 1.5rem;
    right: 1.5rem;
    max-width: 320px;
    z-index: 999;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
  
  .chat-head .messaging-header {
    background: #4f46e5;
    border-radius: 24px 24px 0 0;
  }
  
  .chat-head .messages-section {
    max-height: 300px;
    overflow-y: auto;
  }
  </style>
  