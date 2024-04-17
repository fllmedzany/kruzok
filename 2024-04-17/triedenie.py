import random

z = []

for i in range(20):
    z.append( random.randint(1,100) )
print(z)


nc = -1

for i in range(len(z)):
    if z[i] > nc:
        print (' zatial javacsie:' + str(z[i]) + ' na pozicii '+str(i))
        nc = z[i]
