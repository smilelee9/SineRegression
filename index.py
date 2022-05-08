import random
import math
import sympy
import matplotlib.pyplot as plt

def regression(dataset):
  """
  Curve fitting of form y=a*sin(x+b), where a is positive and b is in [0, 2*pi).
  It uses angle addition formula and bilinear least-square method.
  """
  # Let A = a cos(b), B = a sin(b), Si = sin(xi) and Ci = cos(xi)
  # y = a sin(x+b) = a cos(b)sin(x) +  sin(b)cos(x) = A*Si + B*Ci.
  # Here, the bilinear model y = f(S,C) = AS + BC can be obtained.
  A, B = sympy.symbols('A B')
  squareError = 0
  # Adding square error (yi - Asin(xi) - Bcos(xi))**2
  for i in range(len(dataset[0])):
    xi, yi = dataset[0][i], dataset[1][i]
    squareError += (yi - A*math.sin(xi) - B*math.cos(xi))**2
  # Partially differentiate w.r.t. A and B.
  partial_A = sympy.diff(squareError, A)
  partial_B = sympy.diff(squareError, B)
  # Error is minimized when the values of all partial derivatives are 0
  sol = sympy.solve((partial_A, partial_B), dict=True)
  print("A : ", sol[0][A], "  B : ", sol[0][B])
  # a**2 = A**2 + B**2 and b = atan(B/A) by definition.
  a = math.sqrt(sol[0][A]**2 + sol[0][B]**2)
  b = math.atan(sol[0][B]/sol[0][A])
  # Sign of a can be determined by square error.
  err_po, err_neg = 0, 0
  for i in range(len(dataset[0])):
    xi, yi = dataset[0][i], dataset[1][i]
    err_po += (yi - a*math.sin(xi+b))**2
    err_neg += (yi + a*math.sin(xi+b))**2
  # Inverse the sign of a if err_po > err_neg
  a = a if err_po <= err_neg else -a
  return a, b

def make_data(n, a, b):
  """
  Generates data (x, y) from random x values and y=a*sin(x+b)+noise.
  Noise is uniformly distributed in range [-0.1, 0.1].
  """
  xs = []
  # Generates n random numbers uniformly distributed in [0, 2*pi).
  for i in range(n):
    xs.append(random.random() * 2 * math.pi)
  xs.sort()
  # Generates noises uniformly distributed in [-0.1, 0.1).
  ys = list(map(lambda x: a*math.sin(x+b) + (random.random() * 2 - 1) * 0.1, xs))
  return xs, ys

data = make_data(5, -5, 2.5)  # Generates test data
print("x : ", data[0], "\ny : ", data[1])
plt.scatter(data[0], data[1])  # Marks test data as a point
a, b = regression(data)  # Apply least-square method to get coefficients
print("a : ", a, "  b : ", b)
x = list(map(lambda x: x/100, range(628)))
y = list(map(lambda x: a*math.sin(x+b), x))
plt.plot(x, y)  # Plot y=a sin(x+b) on the scatter plot, where a,b are the result of regression()
