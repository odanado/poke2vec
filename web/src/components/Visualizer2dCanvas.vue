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

    this.last.x = this.canvas.width / 2;
    this.last.y = this.canvas.height / 2;

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
        const dx = (xs[i] * this.canvas.width);
        const dy = (ys[i] * this.canvas.height);

        const { top, left } = calcPos(this.poke2num.get(name));
        this.ctx.drawImage(this.miniIcons, left, top, width, height, dx, dy, width / this.xform.a, height / this.xform.d);
      });
    },
    reset() {
      const p1 = this.transformedPoint(0, 0);
      const p2 = this.transformedPoint(this.canvas.width, this.canvas.height);
      this.ctx.clearRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
    },
    zoom(isZoomUp) {
      const point = this.transformedPoint(this.last.x, this.last.y);

      this.xform = this.xform.translate(point.x, point.y);
      this.ctx.translate(point.x, point.y);

      const baseFactor = 1.1;
      const factor = isZoomUp ? 1 / baseFactor : baseFactor;

      console.log(factor, this.xform);
      this.xform = this.xform.scaleNonUniform(factor, factor);
      console.log(factor, this.xform);
      this.ctx.scale(factor, factor);

      this.xform = this.xform.translate(-point.x, -point.y);
      this.ctx.translate(-point.x, -point.y);

      this.draw();
    },
    mouseWheel(e) {
      this.zoom(e.wheelDelta > 0);
    },
    mouseDown(e) {
      this.last.x = e.offsetX || (e.pageX - this.canvas.offsetLeft);
      this.last.y = e.offsetY || (e.pageY - this.canvas.offsetTop);
      this.startDragPos = this.transformedPoint(this.last.x, this.last.y);
    },
    mouseMove(e) {
      if (this.dragging) {
        this.last.x = e.offsetX || (e.pageX - this.canvas.offsetLeft);
        this.last.y = e.offsetY || (e.pageY - this.canvas.offsetTop);
        const point = this.transformedPoint(this.last.x, this.last.y);

        const dx = point.x - this.startDragPos.x;
        const dy = point.y - this.startDragPos.y;
        this.xform = this.xform.translate(dx, dy);
        this.ctx.translate(dx, dy);

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
