import theano
import theano.tensor as T
import numpy as np
import cPickle
import random
import matplotlib.pyplot as plt

class RNN(object):

	def __init__(self, nin, n_hidden, nout):
		rng = np.random.RandomState(1234)
		W_uh = np.asarray(
			rng.normal(size=(nin, n_hidden), scale= .01, loc = .0), dtype = theano.config.floatX)
		W_hh = np.asarray(
			rng.normal(size=(n_hidden, n_hidden), scale=.01, loc = .0), dtype = theano.config.floatX)
		W_hy = np.asarray(
			rng.normal(size=(n_hidden, nout), scale =.01, loc=0.0), dtype = theano.config.floatX)
		b_hh = np.zeros((n_hidden,), dtype=theano.config.floatX)
		b_hy = np.zeros((nout,), dtype=theano.config.floatX)
		self.activ = T.nnet.sigmoid
		lr = T.scalar()
		u = T.matrix()
		t = T.vector()

		W_uh = theano.shared(W_uh, 'W_uh')
		W_hh = theano.shared(W_hh, 'W_hh')
		W_hy = theano.shared(W_hy, 'W_hy')
		b_hh = theano.shared(b_hh, 'b_hh')
		b_hy = theano.shared(b_hy, 'b_hy')

		h0_tm1 = theano.shared(np.zeros(n_hidden, dtype=theano.config.floatX))

		h, _ = theano.scan(self.recurrent_fn, sequences = u,
					   outputs_info = [h0_tm1],
					   non_sequences = [W_hh, W_uh, W_hy, b_hh])

		y = T.dot(h[-1], W_hy) + b_hy
		cost = ((t - y)**2).mean(axis=0).sum()

		gW_hh, gW_uh, gW_hy,\
		   gb_hh, gb_hy = T.grad(
			   cost, [W_hh, W_uh, W_hy, b_hh, b_hy])

		self.train_step = theano.function([u, t, lr], cost,
							on_unused_input='warn',
							updates=[(W_hh, W_hh - lr*gW_hh),
									 (W_uh, W_uh - lr*gW_uh),
									 (W_hy, W_hy - lr*gW_hy),
									 (b_hh, b_hh - lr*gb_hh),
									 (b_hy, b_hy - lr*gb_hy)],
							allow_input_downcast=True)

	def recurrent_fn(self, u_t, h_tm1, W_hh, W_uh, W_hy, b_hh):
		h_t = self.activ(T.dot(h_tm1, W_hh) + T.dot(u_t, W_uh) + b_hh)
		return h_t

if __name__ == '__main__':
	rnn = RNN(2, 20, 1)
	lr = 0.01
	e = 1
	vals = []
	for i in xrange(int(5e5)):
		u = np.random.rand(10,2)
		t = np.dot(u[:,0], u[:,1])
		c = rnn.train_step(u, t, lr)
		print "iteration {0}: {1}".format(i, np.sqrt(c))
		e = 0.1*np.sqrt(c) + 0.9*e
		if i % 1000 == 0:
			vals.append(e)
	plt.plot(vals)
	plt.savefig('plots/error.png')
