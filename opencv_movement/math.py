import numpy as np
import math
x = 5
y = 4


pythagoaras = np.sqrt(x**2 +y**2)

print(pythagoaras)
rad = math.sin(y/pythagoaras)
print(rad)
degress = math.degrees(rad)

print(degress)