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

import Canvas2DWrapper from '@/modules/canvas_2d_wrapper';

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
    scaleFactor: {
      type: Number,
      required: true,
    },
  },
  mounted() {
    this.wrapper = new Canvas2DWrapper(this.$refs.visualizer2d);

    this.last.x = this.wrapper.canvas.width / 2;
    this.last.y = this.wrapper.canvas.height / 2;

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
      const factor = this.wrapper.getScaleFactor();
      this.names.forEach((name, i) => {
        const dx = (xs[i] * this.wrapper.canvas.width);
        const dy = (ys[i] * this.wrapper.canvas.height);

        const { top, left } = calcPos(this.poke2num.get(name));
        this.wrapper.ctx.drawImage(this.miniIcons,
          left, top, width, height,
          dx, dy, width / factor.x, height / factor.y);
      });
    },
    reset() {
      const p1 = this.wrapper.transformedPoint(0, 0);
      const p2 = this.wrapper.transformedPoint(
        this.wrapper.canvas.width, this.wrapper.canvas.height);
      this.wrapper.ctx.clearRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
    },
    mouseWheel(e) {
      const factor = e.wheelDelta > 0 ? 1 / this.baseFactor : this.baseFactor;
      this.wrapper.zoom(this.last, factor);
      this.draw();
    },
    mouseDown(e) {
      this.last.x = e.offsetX || (e.pageX - this.canvas.offsetLeft);
      this.last.y = e.offsetY || (e.pageY - this.canvas.offsetTop);
      this.startDragPos = this.wrapper.transformedPoint(this.last.x, this.last.y);
    },
    mouseMove(e) {
      if (this.dragging) {
        this.last.x = e.offsetX || (e.pageX - this.canvas.offsetLeft);
        this.last.y = e.offsetY || (e.pageY - this.canvas.offsetTop);
        const point = this.wrapper.transformedPoint(this.last.x, this.last.y);

        const dx = point.x - this.startDragPos.x;
        const dy = point.y - this.startDragPos.y;
        this.wrapper.translate(dx, dy);

        this.draw();
      }
    },
    mouseUp() {
      this.startDragPos = null;
    },
  },
  watch: {
    scaleFactor(newVal, oldVal) {
      const factor = newVal / oldVal;
      this.wrapper.zoom(this.last, factor);
      this.draw();
    },
  },
  data: () => ({
    startDragPos: null,
    baseFactor: 1.1,
    last: {
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
