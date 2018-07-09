import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Chat from '@/components/Chat/Chat';
import Auth from '@/components/Auth/Auth';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
    },
    {
      path: '/chatroom',
      name: 'Chatroom',
      component: Chat,
    },
    {
      path: '/login',
      name: 'Auth',
      component: Auth,
    },
  ],
});
