import * as THREE from 'three';

class Axis extends THREE.Line {
  constructor(axis, length, color) {
    const material = new THREE.LineBasicMaterial({
      color,
    });

    const geometry = new THREE.Geometry();
    geometry.vertices.push(
      new THREE.Vector3(0, 0, 0),
    );
    if (axis === 'x') {
      geometry.vertices.push(
        new THREE.Vector3(length, 0, 0),
      );
    } else if (axis === 'y') {
      geometry.vertices.push(
        new THREE.Vector3(0, length, 0),
      );
    } else if (axis === 'z') {
      geometry.vertices.push(
        new THREE.Vector3(0, 0, length),
      );
    } else {
      throw new Error('axis error');
    }
    super(geometry, material);
  }
}

export default Axis;
