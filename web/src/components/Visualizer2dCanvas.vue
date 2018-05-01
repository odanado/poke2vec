<template>
  <div
    id='canvas-wrapper'
    ref='canvasWrapper'>
    <canvas
      id='visualizer2d'
      ref='visualizer2d'
      @mousewheel='mouseWheel'
      v-hammer:pan="handlePan"
      v-hammer:panstart="handlePanStart" />
  </div>
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
    this.resize();

    this.last.x = this.wrapper.canvas.width / 2;
    this.last.y = this.wrapper.canvas.height / 2;

    this.miniIcons = new Image();
    this.miniIcons.src = '/static/smicons-sheet.png';
    this.miniIcons.onload = () => {
      this.draw();
    };
  },
  methods: {
    draw() {
      this.reset();

      const { xs, ys } = this.vectors;
      const { width, height } = this.icon;
      const factor = this.wrapper.getScaleFactor();
      this.names.forEach((name, i) => {
        const dx = (xs[i] * (this.wrapper.canvas.width - width));
        const dy = (ys[i] * (this.wrapper.canvas.height - height));

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

      this.wrapper.ctx.strokeStyle = 'rgb(00,00,255)';
      this.wrapper.ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
    },
    resize() {
      this.wrapper.canvas.width = this.$refs.canvasWrapper.clientWidth;
      this.wrapper.canvas.height = this.$refs.canvasWrapper.clientHeight;
    },
    mouseWheel(e) {
      this.$emit('handleZoom', { isZoomIn: e.wheelDelta < 0 });
    },
    handlePanStart(e) {
      this.last = this.wrapper.transformedPoint(e.deltaX, e.deltaY);
    },
    handlePan(e) {
      const point = this.wrapper.transformedPoint(e.deltaX, e.deltaY);
      const dx = point.x - this.last.x;
      const dy = point.y - this.last.y;

      this.wrapper.translate(dx, dy);

      this.draw();
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

<style scoped>
@media (min-width: 768px) {
  #canvas-wrapper {
    width: 750px;
    height: 375px;
  }
}
</style>
