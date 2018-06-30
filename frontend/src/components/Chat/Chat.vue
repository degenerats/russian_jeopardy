<template>
  <div class="chat">
    <div ref="messages" class="chat__messages">
      <Message
        v-for="messageData in messages"
        v-bind:key="messageData.id"
        v-bind:messageData="messageData"
      />
    </div>
    <Input :sendMessage = "sendMessage" />
  </div>
</template>

<script>
import uuid from 'uuid';
import Input from './Input';
import Message from './Message';

export default {
  name: 'Chat',
  components: {
    Input,
    Message,
  },
  data() {
    return {
      messages: [
        {
          id: uuid(),
          author: 'Tamara Vasiliyevna',
          time: 1530316568116,
          text: 'Test Message',
        },
        {
          id: uuid(),
          author: 'Tamara Vasiliyevna',
          time: 1530316601923,
          text: 'Test Message 2',
        },
        {
          id: uuid(),
          author: 'Lorem',
          time: 1530316618734,
          text: 'Stop this madness!',
        },
        {
          id: uuid(),
          author: 'Tamara Vasiliyevna',
          time: 1530316631328,
          text: 'MADNESS??!',
        },
        {
          id: uuid(),
          author: 'Lorem',
          time: 1530316642989,
          text: 'Oh, god...',
        },
      ],
    };
  },
  methods: {
    sendMessage(message) {
      this.messages.push(message);
    },
  },
  updated() {
    this.$refs.messages.scrollTop = this.$refs.messages.scrollHeight;
  }
};
</script>

<style scoped>
  .chat__messages {
    height: 600px;
    overflow: auto;
  }
</style>
