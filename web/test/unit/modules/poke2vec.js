
import { dot } from '@/modules/poke2vec';

describe('poke2vec', () => {
  it('test dot function', () => {
    const a = new Float32Array([1, 2]);
    const b = new Float32Array([3, 4]);
    const act = dot(a, b);
    const exp = 11;
    expect(exp).to.equal(act);
  });
});
