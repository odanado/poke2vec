<template>
  <v-layout
    row
    wrap>

    <v-flex xs10>
      <v-select
        :items="items"
        v-model="selectedName"
        return-object
        label="ポケモン名"/>
    </v-flex>

    <v-flex xs1>
      <v-btn
        @click="add('+')"
        dark
        small
        fab
        :style="{ 'background-color': 'deeppink'}">
        <v-icon>add</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs1>
      <v-btn
        @click="add('-')"
        dark
        small
        fab
        :style="{ 'background-color': 'blue'}">
        <v-icon>remove</v-icon>
      </v-btn>
    </v-flex>

  </v-layout>
</template>


<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
  methods: {
    add(polarity) {
      this.$emit('addPokemon', { polarity, ...this.selectedName });
      this.selectedName = null;
    },
  },
  data: () => ({
    selectedName: null,
  }),
};
</script>

<style scoped>
.icon {
  display: inline-flex
}
</style>
