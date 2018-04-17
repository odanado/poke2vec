<template>
  <div>
    <v-layout
      justify-center
      text-xs-center
      row
      wrap
    >

      <v-flex
        xs12>
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

const poke2vec = require('@/data/gen7vgc2018_ns_64_poke2vec.json');

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
    topN: 100,
    polarityPokemons: [],
    // range(10, 101, 10)
    topNRange: [...Array(10).keys()].map(x => (x + 1) * 10),
  }),
  computed: {
    inputPokemons() {
      let ret = poke2vec.map(x => ({ text: translate(x.name, 'Japanese'), value: x.name }));
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
      const { vocab } = convertPoke2vec(poke2vec);
      return vocab;
    },
    unitVec() {
      const { unitVec } = convertPoke2vec(poke2vec);
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

</style>
