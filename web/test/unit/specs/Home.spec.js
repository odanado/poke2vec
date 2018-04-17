import Vue from 'vue';
import Home from '@/pages/Home';

describe('Home.vue', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(Home);
    const vm = new Constructor().$mount();
    expect(vm.$el.querySelector('div.home').textContent)
      .to.equal('This is Home.');
  });
});
