<template>
  <div class="auth-form">
    <div class="auth-form__row">
      <p>Username:</p>
      <input type="text" v-model="username">
    </div>
    <div class="auth-form__row">
      <p>Password:</p>
      <input type="password" v-model="password">
    </div>
    <button class="auth-form__send-button">Login</button>
  </div>
</template>

<script>
export default {
  name: 'Auth',
  data() {
    return {
      username: '',
      password: '',
    };
  },
};
</script>

<style scoped>
  .auth-form {
    width: 380px;
    margin: 0 auto;
    padding: 50px 30px;
    border: 1px solid #2c3e50;
    box-sizing: border-box;
  }
  p {
    margin: 0;
  }
  .auth-form__row {
    margin-bottom: 25px;
    text-align: left;
  }
  .auth-form__row input {
    width: 100%;
    padding: 10px;
    font-size: 18px;
    box-sizing: border-box;
  }
  .auth-form__send-button {
    display: block;
    width: 180px;
    margin: 40px auto 0;
    padding: 10px;
    font-size: 20px;
    cursor: pointer;
  }
</style>
