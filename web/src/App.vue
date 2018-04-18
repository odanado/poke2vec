<template>
  <v-app id="inspire">
    <NaviGationDrawer />
    <v-content>
      <v-container
        fluid
        grid-list-md>
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

<style scoped>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.container {
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

@media (min-width: 768px) {
  .container {
    width: 750px;
  }
}

</style>
