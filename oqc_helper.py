import numpy as np

X = np.matrix([[0, 1], [1, 0]])
Y = np.matrix([[0, -1j], [1j, 0]])
Z = np.matrix([[1, 0], [0, -1]])
I = np.matrix([[1, 0], [0, 1]])


def Rx(th):
    th = th * np.pi / 180
    return np.cos(th / 2) * I - 1j * np.sin(th / 2) * X


def Ry(th):
    th = th * np.pi / 180
    return np.cos(th / 2) * I - 1j * np.sin(th / 2) * Y


def Rz(th):
    th = th * np.pi / 180
    return np.cos(th / 2) * I - 1j * np.sin(th / 2) * Z


def seq_to_matrix(g_s, a_s):
    mat = np.matrix(np.eye(2), dtype=complex)
    for gate, angle in zip(g_s, a_s):
        if gate == "X":
            mat *= Rx(angle)
        elif gate == "Y":
            mat *= Ry(angle)
        elif gate == "Z":
            mat *= Rz(angle)
    
    if np.abs(mat[0, 0]) > 0.1:
        mat *= np.exp(-1j * np.angle(mat[0, 0]))  # fixing the phase of first entry to zero
    else:
        mat *= np.exp(-1j * np.angle(mat[0, 1]))  # fixing the phase of first entry to zero
    mat = np.around(mat, decimals=7)  # for cleaner results

    return mat
