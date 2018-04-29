import { storiesOf } from '@storybook/vue';

import Footer from '@/components/Footer';

storiesOf('Footer', module)
  .add('simple', () => ({
    components: { Footer },
    template: '<Footer/>',
  }));
