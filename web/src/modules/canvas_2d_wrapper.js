export default class Canvas2DWrapper {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.xform = this.svg.createSVGMatrix();
    this.point = this.svg.createSVGPoint();
  }
  transformedPoint(x, y) {
    this.point.x = x;
    this.point.y = y;
    return this.point.matrixTransform(this.xform.inverse());
  }
  translate(x, y) {
    this.xform = this.xform.translate(x, y);
    this.ctx.translate(x, y);
  }
  transform(angle, dx, dy) {
    const rad = (angle * Math.PI) / 180;
    const mtx = this.svg.createSVGMatrix();
    mtx.a = Math.cos(rad);
    mtx.b = Math.sin(rad);
    mtx.c = -Math.sin(rad);
    mtx.d = Math.cos(rad);
    mtx.e = dx;
    mtx.f = dy;
    this.xform = this.xform.multiply(mtx);
    this.ctx.setTransform(Math.cos(rad), Math.sin(rad), -Math.sin(rad), Math.cos(rad), dx, dy);
  }
  scale(factor) {
    this.xform = this.xform.scaleNonUniform(factor, factor);
    this.ctx.scale(factor, factor);
  }
  zoom(centor, factor) {
    this.translate(centor.x, centor.y);

    this.scale(factor);

    this.translate(-centor.x, -centor.y);
  }
  getScaleFactor() {
    return { x: this.xform.a, y: this.xform.d };
  }
}
