from numpy.random import normal, seed

seed(1)
data = normal(loc=0, scale=1, size=1000)
ra = max(data) - min(data)
scaled_data = sorted([(x+ra) / (2*ra) for x in data])
