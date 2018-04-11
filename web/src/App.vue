<template>
  <v-app id="inspire">
    <NaviGationDrawer />
    <v-content>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-content>
    <Footer />
  </v-app>
</template>

<script>

import NaviGationDrawer from '@/components/NavigationDrawer';
import Footer from '@/components/Footer';

export default {
  name: 'App',
  components: {
    NaviGationDrawer,
    Footer,
  },
};
</script>

<style>
@import url(https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons);

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
