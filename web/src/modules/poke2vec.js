const dot = (xs, ys) => {
  // assert xs.length == ys.length
  let sum = 0;
  for (let i = 0; i < xs.length; i += 1) {
    sum += xs[i] * ys[i];
  }
  return sum;
};
const l2norm = xs => Math.sqrt(dot(xs, xs));

const cosSim = (xs, ys) => dot(xs, ys) / (l2norm(xs) * l2norm(ys));

const toUnitVec = (xs) => {
  const norm = l2norm(xs);
  const ret = new Float32Array(xs.length);

  for (let i = 0; i < xs.length; i += 1) {
    ret[i] = xs[i] / norm;
  }
  return ret;
};


export const mostSimilar = (unitVec, vocab, positive, negative, topN) => {
  const used = new Set([...positive, ...negative]);

  // (num, dim)
  const vecs = [];
  positive.forEach(x => vecs.push(unitVec[vocab.get(x)]));
  negative.forEach(x => vecs.push(unitVec[vocab.get(x)].map(e => -e)));

  // (dim, num)
  const vecsT = new Array(vecs[0].length);
  for (let i = 0; i < vecsT.length; i += 1) {
    vecsT[i] = new Float32Array(vecs.length);
    vecsT[i].forEach((__, j) => {
      vecsT[i][j] = vecs[j][i];
    });
  }

  const mean = new Array(vecsT.length);
  for (let i = 0; i < mean.length; i += 1) {
    mean[i] = vecsT[i].reduce((x, y) => x + y) / vecsT[i].length;
  }

  const unitMean = toUnitVec(mean);

  const results = [];
  vocab.forEach((v, k) => {
    if (!used.has(k) && v < topN) {
      results.push({ id: k, similarity: cosSim(unitMean, unitVec[v]) });
    }
  });
  results.sort((x, y) => {
    if (x.similarity < y.similarity) return 1;
    if (x.similarity > y.similarity) return -1;
    return 0;
  });
  return results;
};

export const convertPoke2vec = (data) => {
  const unitVec = new Array(data.length);
  const vocab = new Map();

  data.forEach((x, i) => {
    unitVec[i] = toUnitVec(new Float32Array(x.vector));
    vocab.set(x.name, i);
  });
  return { vocab, unitVec };
};

if (process.env.NODE_ENV === 'testing') {
  module.exports.dot = dot;
  module.exports.l2norm = l2norm;
  module.exports.cosSim = cosSim;
  module.exports.toUnitVec = toUnitVec;
}
