<template>
  <div>
    <v-layout>
      <v-slider
        v-model="canvasScaleFactor"
        @input="inputScaleFactor"
        label="ズーム"
        thumb-label
        min="1"
        max="10"
        step="0.1"/>
      <v-btn
        small
        @click="resetCanvas">リセット</v-btn>
    </v-layout>

    <Visualizer2dCanvas
      ref="canvas"
      :poke2vec="poke2vec"
      @changeScaleFactor="changeScaleFactor"
    />
  </div>
</template>

<script>

import Visualizer2dCanvas from '@/components/Visualizer2dCanvas';

const poke2vec = require('@/data/pca_2d_gen7battlespotsingles_ns_64_poke2vec');

export default {
  components: {
    Visualizer2dCanvas,
  },
  methods: {
    changeScaleFactor(scaleFactor) {
      this.canvasScaleFactor = scaleFactor;
    },
    inputScaleFactor(val) {
      this.$refs.canvas.changeScaleFactor(val, false);
      this.$refs.canvas.draw();
    },
    resetCanvas() {
      this.$refs.canvas.reset();
      this.$refs.canvas.draw();
    },
  },
  data: () => ({
    poke2vec,
    canvasScaleFactor: 1,
  }),
};
</script>
