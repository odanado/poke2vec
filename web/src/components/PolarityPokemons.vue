<template>
  <v-flex xs12>
    <v-list>
      <template v-for="(item, index) in items">
        <PolarityPokemon
          :item="item"
          :key="index" />
        <v-divider
          v-if="items.length !== index + 1"
          :key="'divider_' + index" />
      </template>
    </v-list>
  </v-flex>
</template>

<script>


import PolarityPokemon from '@/components/PolarityPokemon';

export default {
  components: {
    PolarityPokemon,
  },
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>
