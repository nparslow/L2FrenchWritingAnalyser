__author__ = 'nparslow'

import theano.tensor as T

# gradients
from theano import pp
from theano import function

x = T.dscalar("x")
y = x ** 2
gy = T.grad(y, x)
print pp(gy) # pretty print dy/dx (fill(a,b) means make a matrix of shape a and fill it with bs)
# shows that the derivative is derived (i.e. power is 2-1), the optimiser simplifies this

f = function([x], gy)
print pp(f.maker.fgraph.outputs[0]) # simplified form by compiler
print f(4)
print f(94.2)


# compute and plot the gradient of the logistic function
x = T.dmatrix('x')
s = T.sum(1/(1+T.exp(-x)))

gs = T.grad(s,x) # use grad to get partial derivative vector
dlogistic = function([x], gs)
print dlogistic([[0,1], [-1,-2]])

# to compute the jacobian:
# theano.gradient.jacobian()
# to do it manually you can use scan:
x = T.dvector('x')
y = x**2
import theano
# T.arange creates a sequence of ints from 0 to y.shape[0]
# loop over and compute gradient at each x
J, updates = theano.scan(lambda i, y, x: T.grad(y[i], x), sequences=T.arange(y.shape[0]), non_sequences=[y,x])
f = function([x], J, updates=updates)
print f([4, 4])

# to compute the hessian
# theano.gradient.hessian()
# to do it manually:
cost = y.sum()
gy = T.grad(cost,x)
H, updates = theano.scan(lambda i, gy, x: T.grad(gy[i], x), sequences=T.arange(gy.shape[0]), non_sequences=[gy, x])

# there are ways to avoid calculating a Jacobian but to get its product with a vector
W = T.dmatrix('W')
V = T.dmatrix('V')
x = T.dvector('x')
y = T.dot(x, W)
JV = T.Rop(y, W, V) # product of J times V
f = theano.function([W, V, x], JV)
print f([[1,1], [1,1]], [[2,2], [2,2]], [0,1])

# similar for v times J:
v = T.dvector('v')
VJ = T.Lop(y, W, v)
f = theano.function([v,x], VJ)
print f([2,2], [0,1])

# same idea but with Hessian times vector
x = T.dvector('x')
v = T.dvector('v')
y = T.sum(x ** 2)
gy = T.grad(y,x)
vH = T.grad(T.sum(gy * v), x)
f = theano.function([x,v], vH)
print f([4,4], [2,2])

# same but with an alternative method (faster one will depend on actual system)
x = T.dvector('x')
v = T.dvector('v')
y = T.sum(x ** 2)
gy = T.grad(y, x)
Hv = T.Rop(gy, x, v)
f = theano.function([x, v], Hv)
print f([4,4], [2,2])