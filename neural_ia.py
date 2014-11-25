import numpy as np
import math
import neurolab as nl
import fuzzy_ia

"""
Creates the network with 6 neurons on hidden layer and 2 on output layer
"""
net = nl.net.newff([[-180,180],[-180,180]],[6,2])


"""
Creates the input data that will be used to train the network
"""
data = np.array([fuzzy_ia.angle_dmn, fuzzy_ia.angle_dmn]).reshape(360,2)


"""
Set the target function to the fuzzy function plus some random gaussian noise
"""
target_function = lambda x: fuzzy_ia.next_action(int(d[0]+0.2*np.random.randn()),
                                                 int(d[1]+0.2*np.random.randn()),
                                                 None)


"""
Creates the desired output
"""
target = [ target_function(d) for d in data  ]


"""
Trains the network using gd with a learning rate of 0.01, for 500 epochs or 0.01 MSE
ref: https://pythonhosted.org/neurolab/lib.html#neurolab.train.train_gd
"""
net.train(data, target, show=15)


"""
Creates the function that will feed foward the learnt weights
"""
def next_action(t, b, s):
      data = np.array([t,b]).reshape(1,2)
      return net.sim(data)[0]

