import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/pages/Home';
import MostSimilar from '@/pages/MostSimilar';
import Visualizer2d from '@/pages/Visualizer2d';

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
    {
      path: '/Visualizer2d',
      name: '2D Visualizer',
      component: Visualizer2d,
    },
  ],
});
