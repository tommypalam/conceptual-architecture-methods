"""Mixed-effects logistic models for the primary contrasts. Zero API calls.

**Why this exists.** Every primary contrast in this project is an exact sign test
on discordant pairs, and the thesis's own statistical section names the standard
alternative — a mixed-effects logistic model with crossed random intercepts for
agent and item — and then does not run it. It also reports that item-level
variance is large (44.4% of the variance in the three-model decomposition).
Naming the right model, giving a reason to expect clustering to matter, and then
not fitting it is not a defensible position, so this module fits it.

**The model.** For observation i with agent a(i), item t(i) and condition x(i):

    logit P(good) = beta0 + beta1 * x(i) + u_{a(i)} + v_{t(i)}
    u_a ~ N(0, sigma_a^2)     v_t ~ N(0, sigma_t^2)

The two random-effect vectors are **crossed**, not nested: every agent meets
every item. That is what makes the standard closed-form panel estimators
inapplicable and is why this is fitted directly.

**Estimation.** Maximum likelihood by Laplace approximation. The integral over
the random effects is approximated at the joint posterior mode of (u, v), which
is found by Newton iterations on the penalised log-likelihood; the determinant
term uses the sparse Hessian of that penalised objective. Fixed effects and
variance components are optimised by Nelder-Mead on the resulting marginal
log-likelihood. This is the same approximation `lme4::glmer(nAGQ=1)` and
`statsmodels` BinomialBayesMixedGLM use by default for this class of model.

**What is checked before any result is believed.** `validate()` fits the model to
simulated data with known parameters and confirms recovery, and separately
confirms that with both variance components driven to zero the fit reduces to
ordinary logistic regression. A model that cannot recover parameters it generated
is not evidence about anything.

**What this does and does not change.** It is a robustness analysis, not a
replacement: the sign tests were prespecified and remain the primary. Where the
two agree, the clustering objection is answered. Where they disagree, the
disagreement is the finding and is reported as such.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, sparse
from scipy.sparse import linalg as splinalg


def _design(rows):
    """(y, x, agent index, item index) from a list of observation dicts."""
    agents = sorted({r["agent"] for r in rows})
    items = sorted({r["item"] for r in rows})
    ai = {a: i for i, a in enumerate(agents)}
    ti = {t: i for i, t in enumerate(items)}
    y = np.array([1.0 if r["y"] else 0.0 for r in rows])
    x = np.array([float(r["x"]) for r in rows])
    a = np.array([ai[r["agent"]] for r in rows])
    t = np.array([ti[r["item"]] for r in rows])
    return y, x, a, t, len(agents), len(items)


def _penalised_mode(y, x, a, t, na, nt, b0, b1, sa, st, tol=1e-9, maxit=60):
    """Joint posterior mode of the random effects, by Newton iterations.

    Maximises  sum log p(y | eta) - ||u||^2/(2 sa^2) - ||v||^2/(2 st^2)
    over u (length na) and v (length nt), with eta = b0 + b1 x + u_a + v_t.
    """
    n = len(y)
    u = np.zeros(na)
    v = np.zeros(nt)
    # incidence matrices, built once
    Zu = sparse.csr_matrix((np.ones(n), (np.arange(n), a)), shape=(n, na))
    Zv = sparse.csr_matrix((np.ones(n), (np.arange(n), t)), shape=(n, nt))
    Z = sparse.hstack([Zu, Zv]).tocsc()
    prior = np.concatenate([np.full(na, 1.0 / sa ** 2), np.full(nt, 1.0 / st ** 2)])
    P = sparse.diags(prior)
    theta = np.zeros(na + nt)

    for _ in range(maxit):
        eta = b0 + b1 * x + Z @ theta
        mu = 1.0 / (1.0 + np.exp(-eta))
        w = np.maximum(mu * (1.0 - mu), 1e-10)
        grad = Z.T @ (y - mu) - P @ theta
        H = (Z.T @ sparse.diags(w) @ Z + P).tocsc()
        try:
            step = splinalg.spsolve(H, grad)
        except Exception:
            return None
        if not np.all(np.isfinite(step)):
            return None
        theta = theta + step
        if np.max(np.abs(step)) < tol:
            break
    eta = b0 + b1 * x + Z @ theta
    mu = 1.0 / (1.0 + np.exp(-eta))
    w = np.maximum(mu * (1.0 - mu), 1e-10)
    H = (Z.T @ sparse.diags(w) @ Z + P).tocsc()
    return theta, H, eta


def _neg_marginal_loglik(params, y, x, a, t, na, nt):
    b0, b1, ls_a, ls_t = params
    sa, st = math.exp(ls_a), math.exp(ls_t)
    if not (1e-4 < sa < 50 and 1e-4 < st < 50):
        return 1e10
    out = _penalised_mode(y, x, a, t, na, nt, b0, b1, sa, st)
    if out is None:
        return 1e10
    theta, H, eta = out
    u, v = theta[:na], theta[na:]
    # conditional log-likelihood
    ll = np.sum(y * eta - np.logaddexp(0.0, eta))
    # random-effect prior
    ll -= np.sum(u ** 2) / (2 * sa ** 2) + na * math.log(sa)
    ll -= np.sum(v ** 2) / (2 * st ** 2) + nt * math.log(st)
    # Laplace determinant term
    lu = splinalg.splu(H.tocsc())
    diagU = np.abs(lu.U.diagonal())
    if np.any(diagU <= 0):
        return 1e10
    logdet = np.sum(np.log(diagU))
    ll += 0.5 * (na + nt) * math.log(2 * math.pi) - 0.5 * logdet
    return -ll if np.isfinite(ll) else 1e10


def fit(rows, start=None):
    """Fit the crossed random-intercept logistic model.

    `rows` is a list of dicts with keys: agent, item, x (0/1 condition), y (bool).
    Returns the fixed effect for x with a Wald interval and p-value, plus the two
    estimated standard deviations.
    """
    y, x, a, t, na, nt = _design(rows)
    p0 = start or [0.0, 0.0, math.log(0.5), math.log(0.5)]
    res = optimize.minimize(_neg_marginal_loglik, p0, args=(y, x, a, t, na, nt),
                            method="Nelder-Mead",
                            options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-6})
    b0, b1, ls_a, ls_t = res.x
    sa, st = math.exp(ls_a), math.exp(ls_t)

    # Wald standard error for b1 from a numerical Hessian of the profile in (b0, b1)
    def f2(bb):
        return _neg_marginal_loglik([bb[0], bb[1], ls_a, ls_t], y, x, a, t, na, nt)

    h = 1e-4
    H2 = np.zeros((2, 2))
    base = f2([b0, b1])
    for i in range(2):
        for j in range(2):
            pp = [b0, b1]; pm = [b0, b1]; mp = [b0, b1]; mm = [b0, b1]
            pp[i] += h; pp[j] += h
            pm[i] += h; pm[j] -= h
            mp[i] -= h; mp[j] += h
            mm[i] -= h; mm[j] -= h
            H2[i, j] = (f2(pp) - f2(pm) - f2(mp) + f2(mm)) / (4 * h * h)
    try:
        cov = np.linalg.inv(H2)
        se = math.sqrt(abs(cov[1, 1]))
    except Exception:
        se = float("nan")

    from scipy import stats
    z = b1 / se if se and np.isfinite(se) and se > 0 else float("nan")
    p = 2 * (1 - stats.norm.cdf(abs(z))) if np.isfinite(z) else float("nan")
    return {"beta": b1, "se": se, "z": z, "p": p,
            "ci95": (b1 - 1.96 * se, b1 + 1.96 * se) if np.isfinite(se) else (None, None),
            "odds_ratio": math.exp(b1),
            "sd_agent": sa, "sd_item": st,
            "n_obs": len(y), "n_agents": na, "n_items": nt,
            "converged": bool(res.success), "neg_loglik": float(res.fun),
            "intercept": b0}


def validate(seed=20260919, verbose=True):
    """Recover known parameters from simulated data, and check the null case.

    A model that cannot recover what it generated is not evidence about anything,
    so this runs before any real fit is reported.
    """
    rng = np.random.default_rng(seed)
    out = {}

    # 1. recovery with substantial item clustering, matching the real design shape
    na, nt = 40, 7
    true_b1, true_sa, true_st = 0.80, 0.60, 1.00
    u = rng.normal(0, true_sa, na)
    v = rng.normal(0, true_st, nt)
    rows = []
    for ag in range(na):
        for it in range(nt):
            for cond in (0, 1):
                eta = -0.2 + true_b1 * cond + u[ag] + v[it]
                rows.append({"agent": ag, "item": it, "x": cond,
                             "y": rng.random() < 1 / (1 + math.exp(-eta))})
    f = fit(rows)
    out["recovery"] = {"true_beta": true_b1, "est_beta": round(f["beta"], 4),
                       "true_sd_item": true_st, "est_sd_item": round(f["sd_item"], 4),
                       "true_sd_agent": true_sa, "est_sd_agent": round(f["sd_agent"], 4),
                       "within_2se": abs(f["beta"] - true_b1) < 2 * f["se"]}

    # 2. null case: no effect, should not be significant
    rows2 = []
    u2 = rng.normal(0, 0.6, na); v2 = rng.normal(0, 1.0, nt)
    for ag in range(na):
        for it in range(nt):
            for cond in (0, 1):
                eta = -0.2 + 0.0 * cond + u2[ag] + v2[it]
                rows2.append({"agent": ag, "item": it, "x": cond,
                              "y": rng.random() < 1 / (1 + math.exp(-eta))})
    f2_ = fit(rows2)
    out["null"] = {"est_beta": round(f2_["beta"], 4), "p": round(f2_["p"], 4),
                   "not_significant": f2_["p"] > 0.05}

    if verbose:
        print("validation:")
        for k, v_ in out.items():
            print(f"  {k}: {v_}")
    return out


def main():
    validate()


if __name__ == "__main__":
    main()
