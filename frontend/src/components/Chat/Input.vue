<template>
  <div class="input-wrap">
    <input
      type="text"
      class="chat__input"
      placeholder="I want to say..."
      v-model.trim="typedText"
      @keyup.enter="onSendMessage"
    >
    <button
      class="chat__send-button"
      @click="onSendMessage"
    >
      SEND
    </button>
  </div>
</template>

<script>
import uuid from 'uuid';

export default {
  name: 'Input',
  props: [
    'sendMessage',
  ],
  data() {
    return {
      typedText: '',
    };
  },
  methods: {
    onSendMessage() {
      if (this.typedText) {
        const messageData = {
          id: uuid(),
          author: 'Me',
          time: Date.now(),
          text: this.typedText,
        };
        console.log(messageData);
        this.sendMessage(messageData);
      }

      this.typedText = '';
    },
  },
};
</script>

<style scoped>
  .input-wrap {
    position: relative;
  }
  .chat__input {
    width: 100%;
    padding: 15px 115px 15px 10px;
    font-size: 24px;
    box-sizing: border-box;
  }
  .chat__send-button {
    position: absolute;
    top: 0;
    right: 0;
    display: block;
    width: 100px;
    height: 100%;
    font-size: 16px;
  }
</style>
