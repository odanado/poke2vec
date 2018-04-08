import os
import json
import random

import click
import numpy as np
from pathlib import Path
from collections import Counter
from logzero import logger
from easydict import EasyDict

import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
import chainer.optimizers as O
from chainer import training
from chainer import reporter
from chainer.training import extensions
from chainer.datasets import TupleDataset


class ContinuousBoW(chainer.Chain):
    """Definition of Continuous Bag of Words Model"""

    def __init__(self, n_vocab, n_units, loss_func):
        super(ContinuousBoW, self).__init__()

        with self.init_scope():
            self.embed = L.EmbedID(
                n_vocab, n_units, initialW=I.Uniform(1. / n_units))
            self.loss_func = loss_func

    def __call__(self, contexts, x):
        e = self.embed(contexts)
        h = F.sum(e, axis=1) * (1. / contexts.shape[1])
        loss = self.loss_func(h, x)
        reporter.report({'loss': loss}, self)
        return loss


class SoftmaxCrossEntropyLoss(chainer.Chain):
    """Softmax cross entropy loss function preceded by linear transformation.
    """

    def __init__(self, n_in, n_out):
        super(SoftmaxCrossEntropyLoss, self).__init__()
        with self.init_scope():
            self.out = L.Linear(n_in, n_out, initialW=0)

    def __call__(self, x, t):
        return F.softmax_cross_entropy(self.out(x), t)


def convert(pokes):
    X, y = [], []
    for poke in pokes:
        for i in range(6):
            center = poke[i]
            contexts = [poke[j] for j in range(6) if i != j]

            X.append(contexts)
            y.append(center)

    return np.array(X, dtype='int32'), np.array(y, dtype='int32')


def vectorize(pokes, vocab):
    return [[vocab[x] if x in vocab else vocab['<unk>']
             for x in poke] for poke in pokes]


def set_seed(seed):
    os.environ['CHAINER_SEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)


@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('save_dir', type=str)
@click.argument('parsed_battle_logs_file', type=str)
def preprocess(save_dir, parsed_battle_logs_file):
    set_seed(42)
    save_dir = Path(save_dir)
    parsed_battle_logs_file = Path(parsed_battle_logs_file)

    data = json.loads(parsed_battle_logs_file.read_text())
    ladder = data['ladder']

    save_file = save_dir / '{}_dataset.json'.format(ladder)

    pokes = []
    for poke in data['pokes']:
        if not poke:
            continue
        if len(poke['p1']) == 6:
            pokes.append(tuple(sorted(poke['p1'])))
        if len(poke['p2']) == 6:
            pokes.append(tuple(sorted(poke['p2'])))

    uniq_pokes = list(set(pokes))

    logger.info('reduce {} -> {} ({:.03f} %)'
                .format(len(pokes), len(uniq_pokes),
                        100 * len(uniq_pokes) / len(pokes)))

    np.random.shuffle(uniq_pokes)
    N = len(uniq_pokes)

    train = uniq_pokes[N // 10:]
    valid = uniq_pokes[:N // 10]

    save_file.write_text(json.dumps({
        'ladder': ladder,
        'train': train,
        'valid': valid
    }))


@cmd.command()
@click.argument('dataset_file', type=str)
@click.argument('n_units', type=int)
@click.option('--topk', type=int, default=100)
@click.option('--negative_size', type=int, default=5)
@click.option('--loss_func',
              type=click.Choice(['softmax', 'ns']), default='ns')
def train(**args):
    set_seed(42)
    args = EasyDict(args)
    logger.info(args)
    dataset_file = Path(args.dataset_file)

    data = json.loads(dataset_file.read_text())
    ladder = data['ladder']
    train_data, valid_data = data['train'], data['valid']

    counter = Counter()
    pokes = train_data + valid_data
    for poke in pokes:
        counter.update(poke)

    counts = [0] * (args.topk + 1)
    index2poke = ['<unk>']
    for i, (name, freq) in enumerate(counter.most_common()):
        if i < args.topk:
            counts[i + 1] = freq
            index2poke.append(name)
        else:
            counts[0] += freq
    vocab = {x: i for i, x in enumerate(index2poke)}
    n_vocab = len(vocab)
    logger.info('n_vocab = {}'.format(n_vocab))

    train_data = vectorize(train_data, vocab)
    valid_data = vectorize(valid_data, vocab)

    X_valid, y_valid = convert(valid_data)
    X_train, y_train = convert(train_data)

    train = TupleDataset(X_train, y_train)
    valid = TupleDataset(X_valid, y_valid)

    logger.info('train size = {}'.format(len(train)))
    logger.info('valid size = {}'.format(len(valid)))

    train_iter = chainer.iterators.SerialIterator(train, 32)
    valid_iter = chainer.iterators.SerialIterator(valid, 32,
                                                  repeat=False, shuffle=False)
    if args.loss_func == 'softmax':
        loss_func = SoftmaxCrossEntropyLoss(args.n_units, n_vocab)
    elif args.loss_func == 'ns':
        loss_func = L.NegativeSampling(
            args.n_units, counts, args.negative_size)
        loss_func.W.data[...] = 0
    else:
        raise ValueError('invalid loss_func: {}'.format(args.loss_func))

    prefix = '{}_{}_{}'.format(ladder, args.loss_func, args.n_units)

    model = ContinuousBoW(n_vocab, args.n_units, loss_func)
    optimizer = O.Adam()
    optimizer.setup(model)

    updater = training.updater.StandardUpdater(train_iter, optimizer)
    trainer = training.Trainer(updater, (10, 'epoch'), out='results')
    trainer.extend(extensions.Evaluator(valid_iter, model))
    trainer.extend(extensions.LogReport(log_name='{}_log'.format(prefix)))
    trainer.extend(extensions.PrintReport(
        ['epoch', 'main/loss', 'validation/main/loss']))
    trainer.extend(extensions.ProgressBar())

    trainer.run()

    # Save the word2vec model
    Path('results').mkdir(exist_ok=True)
    poke2vec_file = 'results/{}_poke2vec.model'.format(prefix)
    with open(poke2vec_file, 'w') as f:
        f.write('%d %d\n' % (n_vocab, args.n_units))
        w = model.embed.W.data
        for i, wi in enumerate(w):
            v = ' '.join(map(str, wi))
            f.write('%s %s\n' % (index2poke[i], v))


if __name__ == '__main__':
    cmd()
