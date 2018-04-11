import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import MostSimilar from '@/components/MostSimilar';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/MostSimilar',
      name: 'MostSimilar',
      component: MostSimilar,
    },
  ],
});
