<template>
  <div>
    <v-layout
      justify-center
      text-xs-center
      row
      wrap
    >
      <v-flex xs12>
        <SelectPoke2vecModel
          :poke2vec-models="poke2vecModels"
          @changeModel="changePoke2vecModel"
        />
      </v-flex>
      <v-flex>
        <div
          ref="stage"/>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import * as THREE from 'three';
import DataPoint from '@/lib/DataPoint';
import Axis from '@/lib/Axis';
import SelectPoke2vecModel from '@/components/SelectPoke2vecModel';

const OrbitControls = require('three-orbit-controls')(THREE);

const calcMean = xs => xs.reduce((x, y) => x + y, 0) / xs.length;
const calcStdev = (xs, mean) => xs.reduce((x, y) => x + ((y - mean) ** 2), 0) / xs.length;

const normalize = (vec) => {
  let ret = vec;

  const mean = calcMean(ret);
  const stdev = calcStdev(ret, mean);

  // データの平均と分散がそれぞれ0と1になるように標準化
  ret = ret.map(x => (x - mean) / stdev);

  const min = Math.min(...ret);
  const max = Math.max(...ret);

  // ベクトルの取る値が[0, 1]になるようにする
  ret = ret.map(v => (v - min) / (max - min));
  // ベクトルの取る値が[-1, 1]になるようにする
  ret = ret.map(x => (2 * x) - 1);

  // データの重心を計算
  const centroid = calcMean(ret);
  // データの重心を原点に移動する
  return ret.map(x => (x - centroid));
};


const calcPos = num => ({
  top: Math.floor(num / 12) * 30,
  left: (num % 12) * 40,
});

/* eslint-disable global-require */
const poke2vecs = new Map(Object.entries({
  pca_3d_gen7battlespotsingles_ns_64: require('@/data/pca_3d_gen7battlespotsingles_ns_64_poke2vec.json'),
  pca_3d_gen7vgc2018_ns_64: require('@/data/pca_3d_gen7vgc2018_ns_64_poke2vec.json'),
}));

const poke2numOriginal = require('@/data/poke2num');
/* eslint-enable global-require */
export default {
  created() {
    this.selectedPoke2vecModel = this.poke2vecModels[0];
  },
  components: {
    SelectPoke2vecModel,
  },
  data() {
    const width = 540;
    const height = 540;

    // Scene = 3次元空間
    const scene = new THREE.Scene();

    // WebGLのレンダラー
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);
    renderer.setClearColor(0xF9F9F9, 1.0);

    // カメラ = 3次元空間を切り取る2次元平面の位置
    const camera = new THREE.PerspectiveCamera(45, width / height);
    camera.position.set(80, 80, 80);

    // マウスでカメラ移動が可能になる
    const controls = new OrbitControls(camera, renderer.domElement);

    return {
      scene,
      renderer,
      camera,
      controls,
      selectedPoke2vecModel: null,
      poke2vecModels: [
        // { text: 'VGC2018 3次元', value: 'pca_3d_gen7vgc2018_ns_64' },
        { text: 'シングルバトル 3次元', value: 'pca_3d_gen7battlespotsingles_ns_64' },
      ],
    };
  },
  computed: {
    poke2vec() {
      const { value } = this.selectedPoke2vecModel;
      if (poke2vecs.has(value)) {
        return poke2vecs.get(value);
      }
      return [];
    },
    poke2num() {
      const poke2num = new Map();
      poke2numOriginal.forEach((x) => {
        poke2num.set(x[0], x[1]);
      });
      return poke2num;
    },
  },
  mounted() {
    // 軸の設定
    const axisLength = 50;
    this.scene.add(new Axis('x', axisLength, 0x0000ff));
    this.scene.add(new Axis('y', axisLength, 0x00ff00));
    this.scene.add(new Axis('z', axisLength, 0xff0000));

    // 各点を取得
    const vectors = this.poke2vec.map(x => x.vector);
    const xs = normalize(vectors.map(v => v[0]));
    const ys = normalize(vectors.map(v => v[1]));
    const zs = normalize(vectors.map(v => v[2]));

    const canvas = document.createElementNS('http://www.w3.org/1999/xhtml', 'canvas');
    // キャンバスを32x32にするのは、縦横の長さが2のべき乗にしないといけないため
    canvas.width = 32;
    canvas.height = 32;
    const context = canvas.getContext('2d');

    this.miniIcons = new Image();
    this.miniIcons.src = '/static/smicons-sheet.png';
    this.miniIcons.onload = () => {
      this.poke2vec.forEach((x, i) => {
        // xs, ys, zsは[-1, 1]の間の座標なので拡大してやる
        const dx = xs[i] * axisLength;
        const dy = ys[i] * axisLength;
        const dz = zs[i] * axisLength;

        const { top, left } = calcPos(this.poke2num.get(x.name));
        const width = 40;
        const height = 30;

        context.clearRect(0, 0, canvas.width, canvas.height);

        // いい感じに切り出して、32x32にリサイズする
        context.drawImage(this.miniIcons,
          left, top, width, height,
          0, 0, canvas.width, canvas.height);

        this.scene.add(new DataPoint(5, dx, dy, dz, canvas.toDataURL()));
      });
      this.$refs.stage.appendChild(this.renderer.domElement);

      // アニメーションの開始
      this.animate();
    };
  },

  methods: {
    animate() {
      // 実際に描画を行っている関数
      requestAnimationFrame(this.animate);
      this.renderer.render(this.scene, this.camera);
    },
    changePoke2vecModel(model) {
      this.selectedPoke2vecModel = model;
    },

  },
};

</script>
<style scoped>
@media (min-width: 768px) {
  #stage {
    width: 750px;
    height: 70vh;
  }
}
@media (max-width: 768px) {
  #stage {
    height: 50vh;
  }
}
</style>
