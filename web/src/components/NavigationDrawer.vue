<template>
  <div>
    <v-navigation-drawer
      app
      v-model="drawer"
      :clipped="$vuetify.breakpoint.lgAndUp"
    >
      <v-list dense>
        <div
          v-for="item in items"
          :key="item.path">
          <v-list-tile @click="routePush(item.path)">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ item.text }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </div>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      color="red accent-2"
      dark
      fixed
      app
      :clipped-left="$vuetify.breakpoint.lgAndUp"
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"/>
      <v-toolbar-title>poke2vec Visualization</v-toolbar-title>
    </v-toolbar>
  </div>
</template>

<script>
export default {
  data: () => ({
    drawer: false,
    items: [
      { icon: 'home', text: 'Home', path: '/' },
      { icon: 'compare_arrows', text: 'Most Similar', path: '/MostSimilar' },
      { icon: 'apps', text: '2D Visualizer', path: '/Visualizer2d' },
      { icon: '3d_rotation', text: '3D Visualizer', path: '/3DVisualizer' },
    ],
  }),
  methods: {
    routePush(path) {
      this.$router.push(path);
    },
  },
};
</script>
