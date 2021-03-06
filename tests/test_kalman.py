from pymht.utils import kalman
import numpy as np
from pymht.models import pv
from pymht.models import polar
from pymht.models import ais

dT = 1.0
x_0 = np.zeros(4)
p = np.power(1.0, 2)
P_0 = np.diag([p, p, p, p])
A = np.array([[1.0,  0.,   dT,  0.],
              [0.,   1.0,  0.,  dT],
              [0.,   0.,  1.0,  0.],
              [0.,   0.,   0., 1.0]])
C = np.array([[1.0,  0.,  0., 0.],
              [0.,   1.0, 0., 0.]])
sigmaQ = 1.0
Q = pv.Q(dT)
sigmaR = 1.0
R = np.eye(2) * np.power(sigmaR, 2)
n = 10
x_0_list = np.array([x_0, ] * n)
P_0_list = np.array([P_0, ] * n)
x_bar_list = np.copy(x_0_list)
P_bar_list = np.copy(P_0_list)

def test_KalmanFilter_class():
    kf = kalman.KalmanFilter(x_0, P_0, A, C, Q, R)
    y = np.ones(2)
    kf.filter(y=y)
    kf2 = kf.filterAndCopy()
    y_tilde = y
    kf3 = kf.filterAndCopy(y_tilde)


def test_predict():
    x_bar_list, P_bar_list = kalman.predict(A, Q, x_0_list, P_0_list)

def test_numpyPredict():
    z_hat_list, S_list, S_inv_list, K_list, P_hat_list = kalman.precalc(
        C, R, x_bar_list, P_bar_list)

    gated_z_tilde_list = np.random.random((n, 5, 2))
    gated_x_hat_list = [kalman.numpyFilter(x_bar_list[i],
                                           K_list[i],
                                           gated_z_tilde_list[i])
                        for i in range(n)]
