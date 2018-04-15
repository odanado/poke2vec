<template>
  <v-list-tile>
    <v-list-tile-action>
      <v-icon
        color="white"
        class="polarity-icon"
        :style="{ 'background-color': iconColor}">
        {{ icon }}
      </v-icon>
    </v-list-tile-action>
    <v-list-tile-content>
      <v-list-tile-title>
        {{ item.text }}
      </v-list-tile-title>
    </v-list-tile-content>
    <v-list-tile-action>
      <v-btn
        icon
        ripple>
        <v-icon color="grey lighten-1">delete</v-icon>
      </v-btn>
    </v-list-tile-action>
  </v-list-tile>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  computed: {
    icon() {
      return this.item.polarity === '+' ? 'add' : 'remove';
    },
    iconColor() {
      return this.item.polarity === '+' ? 'deeppink' : 'blue';
    },
  },
};
</script>


<style scoped>
.polarity-icon {
  border-radius: 50%;
}
</style>
