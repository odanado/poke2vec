<template>
  <Visualizer2dCanvas
    :poke2vec="poke2vec"
  />
</template>

<script>

import Visualizer2dCanvas from '@/components/Visualizer2dCanvas';

const poke2vec = require('@/data/pca_2d_gen7battlespotsingles_ns_64_poke2vec');

export default {
  components: {
    Visualizer2dCanvas,
  },
  data: () => ({
    poke2vec,
  }),
};
</script>
