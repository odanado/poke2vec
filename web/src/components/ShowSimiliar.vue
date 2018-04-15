<template>
  <v-flex xs12>
    <v-data-table
      v-if="items.length"
      :headers="headers"
      :items="items"
      hide-actions
      class="elevation-1"
    >
      <template
        slot="items"
        slot-scope="props">
        <td>{{ props.item.text }}</td>
        <td class="text-xs-right">{{ props.item.similarity }}</td>
      </template>
    </v-data-table>
  </v-flex>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      headers: [
        {
          text: 'ポケモン名',
          align: 'left',
          sortable: false,
          value: 'text',
        },
        {
          text: '類似度',
          sortable: false,
          value: 'similarity',
        },
      ],
    };
  },
};
</script>
