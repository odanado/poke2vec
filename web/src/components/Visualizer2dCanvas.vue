<template>
  <canvas
    width="800"
    height="400"
    id='visualizer2d'
    ref='visualizer2d'
    @mousewheel='mouseWheel'
    @mousedown='mouseDown'
    @mousemove='mouseMove'
    @mouseup='mouseUp' />
</template>

<script>

import Vue from 'vue';

const poke2numOriginal = require('@/data/poke2num');

const calcPos = num => ({
  top: Math.floor(num / 12) * 30,
  left: (num % 12) * 40,
});


const normalize = (vec) => {
  const min = Math.min(...vec);
  const max = Math.max(...vec);
  return vec.map(v => (v - min) / (max - min));
};

export default {
  props: {
    poke2vec: {
      type: Array,
      required: true,
    },
  },
  mounted() {
    const poke2num = new Map();
    poke2numOriginal.forEach((x) => {
      poke2num.set(x[0], x[1]);
    });
    this.canvas = this.$refs.visualizer2d;
    this.ctx = this.canvas.getContext('2d');

    this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.xform = this.svg.createSVGMatrix();
    this.point = this.svg.createSVGPoint();

    this.miniIcons = new Image();
    this.miniIcons.src = '/static/smicons-sheet.png';
    this.miniIcons.onload = () => {
      this.draw();
    };
  },
  methods: {
    transformedPoint(x, y) {
      this.point.x = x;
      this.point.y = y;
      return this.point.matrixTransform(this.xform.inverse());
    },
    draw() {
      this.reset();

      const { xs, ys } = this.vectors;
      const { width, height } = this.icon;
      this.names.forEach((name, i) => {
        const dx = ((xs[i] * this.canvas.width) + this.offset.x) * this.zoomRatio;
        const dy = ((ys[i] * this.canvas.height) + this.offset.y) * this.zoomRatio;

        const { top, left } = calcPos(this.poke2num.get(name));
        this.ctx.drawImage(this.miniIcons, left, top, width, height, dx, dy, width, height);
      });
    },
    reset() {
      this.ctx.fillStyle = 'white';
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

      // 枠線
      this.ctx.strokeStyle = 'rgb(00,00,255)';
      this.ctx.strokeRect(0, 0, this.canvas.width, this.canvas.height);
    },
    mouseWheel(e) {
      this.zoomRatio += e.wheelDelta * 0.0001;
      this.draw();
    },
    mouseDown(e) {
      this.startDragPos = {
        x: e.offsetX,
        y: e.offsetY,
      };
    },
    mouseMove(e) {
      if (this.dragging) {
        const x = (e.offsetX - this.startDragPos.x);
        const y = (e.offsetY - this.startDragPos.y);
        Vue.set(this.offset, 'x', x);
        Vue.set(this.offset, 'y', y);

        this.draw();
      }
    },
    mouseUp() {
      this.startDragPos = null;
    },
  },
  data: () => ({
    startDragPos: null,
    zoomRatio: 1,
    offset: {
      x: 0,
      y: 0,
    },
    icon: {
      width: 40,
      height: 30,
    },
  }),
  computed: {
    dragging() {
      return this.startDragPos !== null;
    },
    poke2num() {
      const poke2num = new Map();
      poke2numOriginal.forEach((x) => {
        poke2num.set(x[0], x[1]);
      });
      return poke2num;
    },
    names() {
      return this.poke2vec.map(x => x.name);
    },
    vectors() {
      const vectors = this.poke2vec.map(x => x.vector);
      return {
        xs: normalize(vectors.map(v => v[0])),
        ys: normalize(vectors.map(v => v[1])),
      };
    },
  },
};
</script>
