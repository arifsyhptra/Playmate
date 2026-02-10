<template>
  <div class="chat-widget">

    <!-- Floating Button -->
    <div class="chat-button" v-if="!open" @click="open = true">
      💬
    </div>

    <!-- CHAT WINDOW -->
    <div class="chat-window" v-if="open">
      <div class="chat-header">
        <img
          src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png"
          class="bot-avatar-header"
        />
        <span>DMS AI Assistant</span>
        <button class="close-btn" @click="open = false">✕</button>
      </div>

      <div class="chat-box" ref="chatBox">

        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message-row', msg.sender]"
        >
          <!-- Avatar BOT -->
          <img
            v-if="msg.sender === 'bot'"
            class="avatar"
            src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png"
          />

          <div class="message-bubble">
            {{ msg.text }}
          </div>

          <!-- Avatar USER -->
          <img
            v-if="msg.sender === 'user'"
            class="avatar"
            src="https://cdn-icons-png.flaticon.com/512/3177/3177440.png"
          />
        </div>

        <!-- Loading -->
        <div v-if="loading" class="message-row bot">
          <img
            class="avatar"
            src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png"
          />
          <div class="message-bubble">...</div>
        </div>

      </div>

      <!-- INPUT -->
      <div class="input-area">
        <input
          v-model="inputText"
          @keyup.enter="sendMessage"
          placeholder="Ketik pesan..."
        />
        <button @click="sendMessage">Kirim</button>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChatView",

  data() {
    return {
      open: false,
      greeted: false,
      inputText: "",
      loading: false,
      messages: [],
    };
  },

  watch: {
    open(val) {
      if (val && !this.greeted) {
        this.messages.push({
          sender: "bot",
          text: "Halo, saya DMS AI — asisten AI Anda. Mau saya bantu apa hari ini?"
        });
        this.greeted = true;
        this.scrollToBottom();
      }
    }
  },

  methods: {
    async sendMessage() {
      if (!this.inputText.trim()) return;

      const userMsg = this.inputText;

      // tampilkan pesan user
      this.messages.push({
        sender: "user",
        text: userMsg,
      });

      this.inputText = "";
      this.scrollToBottom();
      this.loading = true;

      try {
        const res = await axios.post("http://localhost:8000/ask", {
          question: userMsg
        });

        this.messages.push({
          sender: "bot",
          text: res.data.answer,
        });

      } catch (err) {
        this.messages.push({
          sender: "bot",
          text: "Maaf, terjadi kesalahan saat memproses pesan."
        });
      }

      this.loading = false;
      this.scrollToBottom();
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.chatBox;
        if (el) el.scrollTop = el.scrollHeight;
      });
    }
  }
};
</script>

<style scoped>
.chat-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #2563eb;
  color: white;
  padding: 15px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 24px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.chat-window {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 320px;
  height: 450px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.25);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #ddd;
}

.chat-header {
  background: #2563eb;
  color: white;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.bot-avatar-header {
  width: 28px;
}

.close-btn {
  margin-left: auto;
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: white;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: #f9fafb;
}

.message-row {
  display: flex;
  align-items: flex-end;
  margin-bottom: 10px;
  gap: 8px;
}

.message-row.user {
  justify-content: flex-end;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.message-bubble {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
}

.bot .message-bubble {
  background: #e5e7eb;
}

.user .message-bubble {
  background: #bfdbfe;
  text-align: right;
}

.input-area {
  display: flex;
  border-top: 1px solid #ddd;
  padding: 8px;
  gap: 6px;
}

input {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

button {
  padding: 10px 14px;
  background: #2563eb;
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
}
</style>
