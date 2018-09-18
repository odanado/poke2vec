// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import 'babel-polyfill';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons/iconfont/material-icons.css';
import VueAnalytics from 'vue-analytics';


import { VueHammer } from 'vue2-hammer';
import App from './App';
import router from './router';


Vue.use(Vuetify);
Vue.use(VueHammer);
Vue.use(VueAnalytics, {
  id: 'UA-49269757-15',
  router,
});

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
