<template>
  <div>
    <v-layout
      justify-center
      text-xs-center
      row
      wrap
    >
      <InputPokemon
        :items="inputPokemons"
        @addPokemon="addPokemon"/>
      <PolarityPokemons :items="polarityPokemons"/>
      <ShowSimiliar :items="showPokemons"/>
    </v-layout>
  </div>
</template>

<script>

import InputPokemon from '@/components/InputPokemon';
import PolarityPokemons from '@/components/PolarityPokemons';
import ShowSimiliar from '@/components/ShowSimiliar';

import translate from '@/lib/translate';
import { mostSimilar, convertPoke2vec } from '@/lib/poke2vec';

const poke2vec = require('@/data/gen7vgc2018_ns_64_poke2vec.json');

function initInputPokemons() {
  const ret = poke2vec.map(x => ({ text: translate(x.name, 'Japanese'), value: x.name }));
  ret.sort((a, b) => {
    if (a.text < b.text) return -1;
    if (a.text > b.text) return 1;
    return 0;
  });
  return ret;
}

export default {
  components: {
    InputPokemon,
    PolarityPokemons,
    ShowSimiliar,
  },
  methods: {
    addPokemon(pokemon) {
      this.polarityPokemons.push(pokemon);
    },
  },
  data: () => ({
    inputPokemons: initInputPokemons(),
    polarityPokemons: [],
  }),
  computed: {
    showPokemons() {
      const positive = this.polarityPokemons.filter(x => x.polarity === '+').map(x => x.value);
      const negative = this.polarityPokemons.filter(x => x.polarity === '-').map(x => x.value);
      if (positive.length > 0 || negative.length > 0) {
        const results = mostSimilar(this.unitVec, this.vocab, positive, negative);
        return results.slice(0, 5).map(x => ({ text: translate(x.id, 'Japanese'), ...x }));
      }
      return [];
    },
  },
  mounted() {
    const { vocab, unitVec } = convertPoke2vec(poke2vec);
    this.vocab = vocab;
    this.unitVec = unitVec;
  },
};
</script>


<style scoped>

.module-title {
  border-bottom: 2px solid #eee;
  margin-bottom: 20px;
}

</style>
