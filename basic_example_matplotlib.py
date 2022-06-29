from matplotlib import pyplot as plt
import numpy as np

# create arrays from normal distribution
x =  np.random.normal(loc=5,scale=1,size=20)
y =  np.random.normal(loc=2,scale=.1,size=20)

# create plot
plt.scatter(x,y)

# show plot
plt.show()
