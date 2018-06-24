<template>
  <v-select
    :items="poke2vecModels"
    v-model="selectedModel"
    return-object
    label="モデル"
    class="selecte-poke2vec-model"
    @change="changeModel"/>
</template>

<script>
export default {
  props: {
    poke2vecModels: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    selectedModel: null,
  }),
  methods: {
    changeModel(value) {
      this.$emit('changeModel', value);
    },
  },
};
</script>
<style scoped>
.selecte-poke2vec-model {
  white-space: nowrap
}
</style>
