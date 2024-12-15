import mitt from 'mitt';

type Events = {
  'formulas-update': void;
};

export const eventBus = mitt<Events>(); 