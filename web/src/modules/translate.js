
const pokeDict = require('@/data/poke_dict.json');

export default function (id, lang) {
  return pokeDict[id][lang];
}
