"""Week 11 — anomaly detectors under one interface.

Five detectors, all fitted on the SAME clean warm-up split and scored on the SAME test split
(the plan requires >=4 models compared on identical splits):

  1. Isolation Forest   (PyOD IForest)      — tree-based isolation of sparse regions
  2. One-Class SVM      (PyOD OCSVM)        — kernel boundary around the normal region
  3. LOF                (PyOD LOF)          — local density deviation
  4. AutoEncoder        (PyOD AutoEncoder)  — small NN; reconstruction error as score
  5. Control chart      (this module)       — EWMA + k-sigma statistical baseline

Every detector exposes: fit(X_train) -> self, and score(X_test) -> np.ndarray of anomaly scores
where HIGHER = more anomalous. Scores (not hard labels) are returned so the evaluation layer can
sweep thresholds for the PR curve and pick an operating point from a stated operational rule.

Determinism: all randomised models take random_state=42; the run is reproducible.
"""
from __future__ import annotations
import warnings
import numpy as np
warnings.filterwarnings("ignore")

from pyod.models.iforest import IForest
from pyod.models.ocsvm import OCSVM
from pyod.models.lof import LOF
from pyod.models.auto_encoder import AutoEncoder
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


class _PyODWrapper:
    """Adapts a PyOD detector to the shared fit/score interface, with scaling."""

    def __init__(self, name: str, make_model):
        self.name = name
        self._make = make_model
        self.scaler = StandardScaler()
        self.model = None

    def fit(self, X):
        Xs = self.scaler.fit_transform(np.asarray(X, float))
        self.model = self._make()
        self.model.fit(Xs)
        return self

    def score(self, X):
        Xs = self.scaler.transform(np.asarray(X, float))
        return np.asarray(self.model.decision_function(Xs), float)


class ControlChart:
    """EWMA control-chart baseline (classic SPC).

    Calibrates an EWMA centre line and residual sigma on the clean warm-up window, then scores
    each test point by how many sigmas its EWMA residual sits from the centre. This is the
    'what a plant engineer would already do' benchmark that the ML models must beat to justify
    their added complexity.

    Multivariate input is reduced to the max per-channel sigma deviation, so a spike in ANY
    channel raises the score (a deliberately conservative choice for safety monitoring).
    """

    name = "Control chart (EWMA)"

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.center_ = None
        self.sigma_ = None

    @staticmethod
    def _ewma(x: np.ndarray, alpha: float) -> np.ndarray:
        out = np.empty_like(x, dtype=float)
        out[0] = x[0]
        for i in range(1, len(x)):
            out[i] = alpha * x[i] + (1 - alpha) * out[i - 1]
        return out

    def fit(self, X):
        X = np.asarray(X, float)
        self.center_ = np.nanmean(X, axis=0)
        resid = X - self._apply_ewma(X)
        self.sigma_ = np.nanstd(resid, axis=0)
        self.sigma_[self.sigma_ == 0] = 1e-9
        return self

    def _apply_ewma(self, X):
        return np.column_stack([self._ewma(X[:, j], self.alpha) for j in range(X.shape[1])])

    def score(self, X):
        X = np.asarray(X, float)
        sm = self._apply_ewma(X)
        dev = np.abs(X - sm) / self.sigma_
        return np.nanmax(dev, axis=1)


def build_models(n_features: int, contamination: float = 0.05):
    """The five detectors. Sized sensibly for the data at hand."""
    hidden = [max(4, n_features), max(2, n_features // 2)]
    return [
        _PyODWrapper("Isolation Forest",
                     lambda: IForest(n_estimators=200, contamination=contamination,
                                     random_state=RANDOM_STATE)),
        _PyODWrapper("One-Class SVM",
                     lambda: OCSVM(kernel="rbf", nu=contamination, gamma="scale")),
        _PyODWrapper("LOF",
                     lambda: LOF(n_neighbors=20, contamination=contamination, novelty=True)),
        _PyODWrapper("AutoEncoder",
                     lambda: AutoEncoder(hidden_neuron_list=hidden, epoch_num=30, batch_size=64,
                                         contamination=contamination, random_state=RANDOM_STATE,
                                         verbose=0)),
        ControlChart(alpha=0.05),
    ]
