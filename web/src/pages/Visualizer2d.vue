<template>
  <div>
    <v-layout>
      <v-slider
        v-model="zoomScaleFactor"
        ref="zoomScaleFactorSlider"
        label="zoom"
        thumb-label
        min="1"
        max="5"
        step="0.5"/>
      <v-btn small>リセット</v-btn>
    </v-layout>

    <Visualizer2dCanvas
      :poke2vec="poke2vec"
      :scale-factor="zoomScaleFactor"
      @handleZoom="handleZoom"
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
    handleZoom({ isZoomIn }) {
      const { zoomScaleFactorSlider } = this.$refs;
      let factor = this.zoomScaleFactor;

      if (isZoomIn) {
        factor += Number(zoomScaleFactorSlider.step);
      } else {
        factor -= Number(zoomScaleFactorSlider.step);
      }

      factor = Math.max(factor, Number(zoomScaleFactorSlider.min));
      factor = Math.min(factor, Number(zoomScaleFactorSlider.max));

      this.zoomScaleFactor = factor;
    },
  },
  data: () => ({
    poke2vec,
    zoomScaleFactor: 1,
  }),
};
</script>
