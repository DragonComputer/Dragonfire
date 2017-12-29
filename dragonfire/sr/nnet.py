from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import theano
import theano.tensor as T

try:
    xrange  # Python 2
except NameError:
    xrange = range  # Python 3


class RNN():
    def __init__(self, nin, n_hidden, nout):
        rng = np.random.RandomState(1234)
        self.W_uh = np.asarray(
            rng.normal(size=(nin, n_hidden), scale=.01, loc=.0),
            dtype=theano.config.floatX)
        self.W_hh = np.asarray(
            rng.normal(size=(n_hidden, n_hidden), scale=.01, loc=.0),
            dtype=theano.config.floatX)
        self.W_hy = np.asarray(
            rng.normal(size=(n_hidden, nout), scale=.01, loc=0.0),
            dtype=theano.config.floatX)
        self.b_hh = np.zeros((n_hidden, ), dtype=theano.config.floatX)
        self.b_hy = np.zeros((nout, ), dtype=theano.config.floatX)
        self.activ = T.nnet.sigmoid
        lr = T.scalar()
        u = T.matrix()
        t = T.vector()

        self.W_uh = theano.shared(self.W_uh, 'W_uh')
        self.W_hh = theano.shared(self.W_hh, 'W_hh')
        self.W_hy = theano.shared(self.W_hy, 'W_hy')
        self.b_hh = theano.shared(self.b_hh, 'b_hh')
        self.b_hy = theano.shared(self.b_hy, 'b_hy')

        self.h0_tm1 = theano.shared(
            np.zeros(n_hidden, dtype=theano.config.floatX))

        h, _ = theano.scan(
            self.recurrent_fn,
            sequences=u,
            outputs_info=[self.h0_tm1],
            non_sequences=[self.W_hh, self.W_uh, self.W_hy, self.b_hh])

        y = T.dot(h[-1], self.W_hy) + self.b_hy
        cost = ((t - y)**2).mean(axis=0).sum()

        gW_hh, gW_uh, gW_hy,\
            gb_hh, gb_hy = T.grad(
                cost, [self.W_hh, self.W_uh, self.W_hy, self.b_hh, self.b_hy])

        self.train_step = theano.function(
            [u, t, lr],
            cost,
            on_unused_input='warn',
            updates=[(self.W_hh, self.W_hh - lr * gW_hh),
                     (self.W_uh,
                      self.W_uh - lr * gW_uh), (self.W_hy,
                                                self.W_hy - lr * gW_hy),
                     (self.b_hh,
                      self.b_hh - lr * gb_hh), (self.b_hy,
                                                self.b_hy - lr * gb_hy)],
            allow_input_downcast=True)

        self.run = theano.function([u], y)

    def recurrent_fn(self, u_t, h_tm1, W_hh, W_uh, W_hy, b_hh):
        h_t = self.activ(T.dot(h_tm1, W_hh) + T.dot(u_t, W_uh) + b_hh)
        return h_t

    def dump(self, path, filename='model.npz'):
        with open(path + filename, "wb") as thefile:
            np.savez(
                thefile,
                W_uh=self.W_uh.get_value(),
                W_hh=self.W_hh.get_value(),
                W_hy=self.W_hy.get_value(),
                b_hh=self.b_hh.get_value(),
                b_hy=self.b_hy.get_value(),
                h0_tm1=self.h0_tm1.get_value())

    def importdump(self, path_to_file):
        with open(path_to_file, "rb") as thefile:
            npzfile = np.load(thefile)
            self.W_uh.set_value(npzfile['W_uh'])
            self.W_hh.set_value(npzfile['W_hh'])
            self.W_hy.set_value(npzfile['W_hy'])
            self.b_hh.set_value(npzfile['b_hh'])
            self.b_hy.set_value(npzfile['b_hy'])
            self.h0_tm1.set_value(npzfile['h0_tm1'])


if __name__ == '__main__':
    rnn = RNN(2, 20, 1)
    lr = 0.01
    e = 1
    vals = []
    for i in xrange(int(5e5)):
        u = np.random.rand(10, 2)
        t = np.dot(u[:, 0], u[:, 1])
        c = rnn.train_step(u, t, lr)
        print("iteration {0}: {1}".format(i, np.sqrt(c)))
        e = 0.1 * np.sqrt(c) + 0.9 * e
        if i % 1000 == 0:
            vals.append(e)
    plt.plot(vals)
    plt.savefig('plots/error.png')
