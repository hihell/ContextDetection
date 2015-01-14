
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

a = np.array([[1,2],[3,3],[4,4],[5,2]])
plt.plot(a[:,0], a[:,1], 'ro-')

plt.axis([0, 10, 0, 10])

plt.show()