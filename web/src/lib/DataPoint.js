import * as THREE from 'three';

class DataPoint extends THREE.Sprite {
  constructor(scale, x, y, z, image) {
    const material = new THREE.SpriteMaterial({
      map: new THREE.TextureLoader().load(image),
    });
    super(material);
    this.position.set(x, y, z);
    this.scale.set(scale, scale, scale);
  }
}
export default DataPoint;
