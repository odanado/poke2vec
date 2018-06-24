<template>
  <div>
    <SelectPoke2vecModel
      :poke2vec-models="poke2vecModels"
      @changeModel="changePoke2vecModel"
    />
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
import SelectPoke2vecModel from '@/components/SelectPoke2vecModel';

/* eslint-disable global-require */
const poke2vecs = new Map(Object.entries({
  pca_2d_gen7battlespotsingles_ns_64: require('@/data/pca_2d_gen7battlespotsingles_ns_64_poke2vec.json'),
  pca_2d_gen7vgc2018_ns_64: require('@/data/pca_2d_gen7vgc2018_ns_64_poke2vec.json'),
}));
/* eslint-enable global-require */
export default {
  created() {
    this.selectedPoke2vecModel = this.poke2vecModels[1];
  },
  components: {
    Visualizer2dCanvas,
    SelectPoke2vecModel,
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
    changePoke2vecModel(model) {
      this.selectedPoke2vecModel = model;
      // FIXME: dataのupdateに少し時間がかかるため、直後にdrawを呼び出すと前のdataでdrawしてしまう
      setInterval(this.$refs.canvas.draw, 100);
    },
  },
  computed: {
    poke2vec() {
      const { value } = this.selectedPoke2vecModel;
      if (poke2vecs.has(value)) {
        return poke2vecs.get(value);
      }
      return [];
    },
  },
  data: () => ({
    selectedPoke2vecModel: null,
    canvasScaleFactor: 1,
    poke2vecModels: [
      { text: 'VGC2018 64次元', value: 'pca_2d_gen7vgc2018_ns_64' },
      { text: 'シングルバトル 2次元', value: 'pca_2d_gen7battlespotsingles_ns_64' },
    ],
  }),
};
</script>
