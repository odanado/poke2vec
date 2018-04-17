<template>
  <div>
    <v-layout
      justify-center
      text-xs-center
      row
      wrap
    >
      <v-flex
        xs4>
        <v-select
          :items="poke2vecItems"
          v-model="selectedPoke2vec"
          return-object
          label="ルール"
          class="selecte-poke2vec"/>
      </v-flex>

      <v-flex
        xs4>
        <v-select
          :items="topNRange"
          v-model="topN"
          label="上位N匹"
          @change="changeTopN"/>
      </v-flex>

      <InputPokemon
        :items="inputPokemons"
        @addPokemon="addPokemon"/>

      <PolarityPokemons
        :items="polarityPokemons"
        @deletePokemon="deletePokemon"/>

      <ShowSimiliar
        :items="showPokemons"/>
    </v-layout>
  </div>
</template>

<script>

import InputPokemon from '@/components/InputPokemon';
import PolarityPokemons from '@/components/PolarityPokemons';
import ShowSimiliar from '@/components/ShowSimiliar';

import translate from '@/modules/translate';
import { mostSimilar, convertPoke2vec } from '@/modules/poke2vec';


/* eslint-disable global-require */
const poke2vecs = new Map(Object.entries({
  gen7vgc2018_ns_64: require('@/data/gen7vgc2018_ns_64_poke2vec.json'),
  gen7battlespotsingles_ns_64: require('@/data/gen7battlespotsingles_ns_64_poke2vec.json'),
}));
/* eslint-enable global-require */

export default {
  components: {
    InputPokemon,
    PolarityPokemons,
    ShowSimiliar,
  },
  methods: {
    addPokemon(pokemon) {
      this.polarityPokemons.push({ index: this.polarityPokemons.length, ...pokemon });
    },
    changeTopN(topN) {
      this.topN = topN;
    },
    deletePokemon(index) {
      this.polarityPokemons.splice(index, 1);
    },
  },
  data: () => ({
    polarityPokemons: [],
    topN: 50,
    // range(10, 101, 10)
    topNRange: [...Array(10).keys()].map(x => (x + 1) * 10),
    poke2vecItems: [
      { text: 'VGC2018 64次元', value: 'gen7vgc2018_ns_64' },
      { text: 'シングルバトル 64次元', value: 'gen7battlespotsingles_ns_64' },
    ],
    selectedPoke2vec: null,
  }),
  computed: {
    poke2vec() {
      const { value } = this.selectedPoke2vec;
      if (poke2vecs.has(value)) {
        return poke2vecs.get(value);
      }
      return [];
    },
    inputPokemons() {
      let ret = this.poke2vec.map(x => ({ text: translate(x.name, 'Japanese'), value: x.name }));
      ret = ret.slice(0, this.topN);
      ret.sort((a, b) => {
        if (a.text < b.text) return -1;
        if (a.text > b.text) return 1;
        return 0;
      });
      return ret;
    },
    showPokemons() {
      const positive = this.polarityPokemons.filter(x => x.polarity === '+').map(x => x.value);
      const negative = this.polarityPokemons.filter(x => x.polarity === '-').map(x => x.value);
      if (positive.length > 0 || negative.length > 0) {
        const results = mostSimilar(this.unitVec, this.vocab, positive, negative, this.topN);
        return results.slice(0, 5).map(x => ({ text: translate(x.id, 'Japanese'), ...x }));
      }
      return [];
    },
    vocab() {
      const { vocab } = convertPoke2vec(this.poke2vec);
      return vocab;
    },
    unitVec() {
      const { unitVec } = convertPoke2vec(this.poke2vec);
      return unitVec;
    },
  },
};
</script>


<style scoped>

.module-title {
  border-bottom: 2px solid #eee;
  margin-bottom: 20px;
}

.selecte-poke2vec {
  white-space: nowrap
}
</style>
