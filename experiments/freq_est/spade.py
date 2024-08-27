from .common import *

# SPADE's time domain estmator is extremely simple.
def estimator(data):
    data = read(data)
    time_domain = {}
    for k in data.keys():
        time_domain[k] = data[k][:, 1] - data[k][:, 0]
    return time_domain


def gen(s_list, photons, noise=0):

    def p1(s):
        return (s+2*sigma)**2*np.exp(-s**2/(4*sigma**2))/(8*sigma**2)
    def p2(s):
        return (s-2*sigma)**2*np.exp(-s**2/(4*sigma**2))/(8*sigma**2)

    data = [np.histogram(np.random.uniform(0, 1, photons), 
            bins=[0, p1(s), p1(s)+p2(s)])[0] for s in s_list]

    return (np.array(data) + np.random.poisson(noise, 2)).astype(float)

