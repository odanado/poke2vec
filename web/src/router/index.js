import Vue from 'vue';
import Router from 'vue-router';
// import Home from '@/pages/Home';
import MostSimilar from '@/pages/MostSimilar';
import Visualizer2d from '@/pages/Visualizer2d';
import Visualizer3d from '@/pages/Visualizer3d';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'MostSimilar',
      component: MostSimilar,
    },
    {
      path: '/visualizer-2d',
      name: '2D Visualizer',
      component: Visualizer2d,
    },
    {
      path: '/visualizer-3d',
      name: '3D Visualizer',
      component: Visualizer3d,
    },
  ],
});
