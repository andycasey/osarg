

import numpy as np

def design_matrix(time, L, order):
    """
    Build a design matrix for fitting a number of sines and cosine functions.

    :param time:
        The times (x-axis) of each measurement.

    :param L:
        The length-scale (in time) for the sine and cosine functions.

    :param order:
        The number of sines and cosines to use in the fit,
    """

    L, time = float(L), np.array(time)
    scale = 2 * (np.pi / L)
    return np.vstack([
        np.ones_like(time).reshape((1, -1)), 
        np.array([
            [np.cos(o * scale * time), np.sin(o * scale * time)] \
            for o in range(1, order + 1)]).reshape((2 * order, time.size))
        ])


def generate_data(time, L, amplitudes):
    O = amplitudes.size / 2
    return np.dot(amplitudes, design_matrix(time, L, O))



if __name__ == "__main__":

    # Generate some data.
    np.random.seed(42)

    O = 5
    scale = 3
    L = np.random.uniform(0, 10)

    x = np.sort(np.random.choice(1000, size=100, replace=False))

    amplitudes = np.random.uniform(-scale, scale, size=2*O + 1)


    # Generate data.
    y = generate_data(x, L, amplitudes)
    y += np.random.normal(0, 1, size=y.size) * np.random.normal(0, 0.1, size=y.size)
    yerr = 0.1 * np.ones_like(x)

    import matplotlib.pyplot as plt


    fig, ax = plt.subplots()
    ax.scatter(x, y, facecolor="k")

    xi = np.linspace(x.min(), x.max(), 1000)
    yi = generate_data(xi, L, amplitudes)

    ax.plot(xi, yi, zorder=-1, c="#cccccc", lw=0.5)



    scalar = 1e-6 # MAGIC SCALAR

    ivar = yerr**-2

    DM = design_matrix(x, L, O)

    MTM = np.dot(DM, ivar[:, None] * DM.T)
    MTy = np.dot(DM, (ivar * y).T)

    eigenvalues = np.linalg.eigvalsh(MTM)

    MTM[np.diag_indices(len(MTM))] += scalar * np.max(eigenvalues)
    eigenvalues = np.linalg.eigvalsh(MTM)
    condition_number = max(eigenvalues)/min(eigenvalues)

    inferred_amplitudes = np.linalg.solve(MTM, MTy)

    fig, ax = plt.subplots()
    ax.scatter(amplitudes, inferred_amplitudes)





