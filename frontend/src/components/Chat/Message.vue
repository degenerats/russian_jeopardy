<template>
  <div class="message">
    <div class="message__info">
      <span class="message__author">{{ messageData.author }}</span>
      <span class="message__time">{{ formattedDate }}</span>
    </div>
    <div class="message__text">{{ messageData.text }}</div>
  </div>
</template>

<script>
export default {
  name: 'Message',
  props: ['messageData'],
  computed: {
    formattedDate() {
      let date = new Date();
      date.setTime(this.messageData.time);

      const hours = date.getHours();
      const minutes = date.getMinutes();
      const seconds = date.getSeconds();

      return `${hours}:${minutes}:${seconds}`;
    },
  },
};
</script>

<style scoped>
  .message {
    text-align: left;
    margin-bottom: 17px;
    word-wrap: break-word;
  }
  .message.you {
    text-align: right;
  }
  .message__info {
    font-size: 14px;
    margin-bottom: 7px;
  }
  .message__text {
    font-size: 18px;
  }
</style>
