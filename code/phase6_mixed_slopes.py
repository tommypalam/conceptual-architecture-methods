"""Crossed random intercepts PLUS a random slope of condition by item. Zero API calls.

**Why this exists.** `phase5_mixed_effects` fits random intercepts for agent and
item. Intercepts absorb different baseline tendencies; they do not absorb
different responses to the manipulation across items, which is the heterogeneity
the thesis's statistical section names as the real concern. A reviewer pointed
out that agreement between the intercept-only model and the sign tests therefore
does not establish that treatment-effect heterogeneity has been handled. This
module fits the model that does:

    logit P(good) = b0 + b1 * x + u_agent + v_item + w_item * x
    u ~ N(0, sa^2)   v ~ N(0, st^2)   w ~ N(0, sw^2)

Estimation is by Laplace approximation, exactly as in `phase5_mixed_effects`, with
the random-slope vector added to the joint mode. `validate()` recovers known
parameters from simulated data before any real fit is reported. With six to
eight items the slope variance is estimated from very few clusters and its
estimate is reported for what it is: weakly identified.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, sparse, stats
from scipy.sparse import linalg as splinalg


def _design(rows):
    agents = sorted({r["agent"] for r in rows})
    items = sorted({r["item"] for r in rows})
    ai = {a: i for i, a in enumerate(agents)}
    ti = {t: i for i, t in enumerate(items)}
    y = np.array([1.0 if r["y"] else 0.0 for r in rows])
    x = np.array([float(r["x"]) for r in rows])
    a = np.array([ai[r["agent"]] for r in rows])
    t = np.array([ti[r["item"]] for r in rows])
    return y, x, a, t, len(agents), len(items)


def _mode(y, x, a, t, na, nt, b0, b1, sa, st, sw, tol=1e-9, maxit=80):
    n = len(y)
    Zu = sparse.csr_matrix((np.ones(n), (np.arange(n), a)), shape=(n, na))
    Zv = sparse.csr_matrix((np.ones(n), (np.arange(n), t)), shape=(n, nt))
    Zw = sparse.csr_matrix((x, (np.arange(n), t)), shape=(n, nt))
    Z = sparse.hstack([Zu, Zv, Zw]).tocsc()
    prior = np.concatenate([np.full(na, 1.0 / sa ** 2), np.full(nt, 1.0 / st ** 2),
                            np.full(nt, 1.0 / sw ** 2)])
    P = sparse.diags(prior)
    theta = np.zeros(na + 2 * nt)
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


def _nll(params, y, x, a, t, na, nt):
    b0, b1, ls_a, ls_t, ls_w = params
    sa, st, sw = math.exp(ls_a), math.exp(ls_t), math.exp(ls_w)
    if not (1e-4 < sa < 50 and 1e-4 < st < 50 and 1e-4 < sw < 50):
        return 1e10
    out = _mode(y, x, a, t, na, nt, b0, b1, sa, st, sw)
    if out is None:
        return 1e10
    theta, H, eta = out
    u, v, wv = theta[:na], theta[na:na + nt], theta[na + nt:]
    ll = np.sum(y * eta - np.logaddexp(0.0, eta))
    ll -= np.sum(u ** 2) / (2 * sa ** 2) + na * math.log(sa)
    ll -= np.sum(v ** 2) / (2 * st ** 2) + nt * math.log(st)
    ll -= np.sum(wv ** 2) / (2 * sw ** 2) + nt * math.log(sw)
    lu = splinalg.splu(H.tocsc())
    diagU = np.abs(lu.U.diagonal())
    if np.any(diagU <= 0):
        return 1e10
    ll += 0.5 * (na + 2 * nt) * math.log(2 * math.pi) - 0.5 * np.sum(np.log(diagU))
    return -ll if np.isfinite(ll) else 1e10


def fit(rows, start=None):
    y, x, a, t, na, nt = _design(rows)
    p0 = start or [0.0, 0.0, math.log(0.5), math.log(0.8), math.log(0.4)]
    res = optimize.minimize(_nll, p0, args=(y, x, a, t, na, nt), method="Nelder-Mead",
                            options={"maxiter": 6000, "xatol": 1e-6, "fatol": 1e-6})
    b0, b1, ls_a, ls_t, ls_w = res.x
    sa, st, sw = math.exp(ls_a), math.exp(ls_t), math.exp(ls_w)

    def f2(bb):
        return _nll([bb[0], bb[1], ls_a, ls_t, ls_w], y, x, a, t, na, nt)

    h = 1e-4
    H2 = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            pp = [b0, b1]; pm = [b0, b1]; mp = [b0, b1]; mm = [b0, b1]
            pp[i] += h; pp[j] += h
            pm[i] += h; pm[j] -= h
            mp[i] -= h; mp[j] += h
            mm[i] -= h; mm[j] -= h
            H2[i, j] = (f2(pp) - f2(pm) - f2(mp) + f2(mm)) / (4 * h * h)
    try:
        se = math.sqrt(abs(np.linalg.inv(H2)[1, 1]))
    except Exception:
        se = float("nan")
    z = b1 / se if se and np.isfinite(se) and se > 0 else float("nan")
    p = 2 * (1 - stats.norm.cdf(abs(z))) if np.isfinite(z) else float("nan")
    return {"beta": b1, "se": se, "z": z, "p": p,
            "ci95": (b1 - 1.96 * se, b1 + 1.96 * se) if np.isfinite(se) else (None, None),
            "sd_agent": sa, "sd_item": st, "sd_slope": sw,
            "n_obs": len(y), "n_agents": na, "n_items": nt,
            "converged": bool(res.success), "neg_loglik": float(res.fun)}


def validate(seed=20260920, verbose=True):
    rng = np.random.default_rng(seed)
    out = {}
    na, nt = 40, 7
    true = dict(b1=0.80, sa=0.60, st=1.00, sw=0.50)
    u = rng.normal(0, true["sa"], na); v = rng.normal(0, true["st"], nt); w = rng.normal(0, true["sw"], nt)
    rows = []
    for ag in range(na):
        for it in range(nt):
            for cond in (0, 1):
                eta = -0.2 + true["b1"] * cond + u[ag] + v[it] + w[it] * cond
                rows.append({"agent": ag, "item": it, "x": cond, "y": rng.random() < 1 / (1 + math.exp(-eta))})
    f = fit(rows)
    out["recovery"] = {"true_beta": true["b1"], "est_beta": round(f["beta"], 4),
                       "est_sd_slope": round(f["sd_slope"], 4), "true_sd_slope": true["sw"],
                       "within_2se": abs(f["beta"] - true["b1"]) < 2 * f["se"]}
    rows2 = []
    u2 = rng.normal(0, 0.6, na); v2 = rng.normal(0, 1.0, nt); w2 = rng.normal(0, 0.5, nt)
    for ag in range(na):
        for it in range(nt):
            for cond in (0, 1):
                eta = -0.2 + 0.0 * cond + u2[ag] + v2[it] + w2[it] * cond
                rows2.append({"agent": ag, "item": it, "x": cond, "y": rng.random() < 1 / (1 + math.exp(-eta))})
    f2_ = fit(rows2)
    out["null"] = {"est_beta": round(f2_["beta"], 4), "p": round(f2_["p"], 4), "not_significant": f2_["p"] > 0.05}
    if verbose:
        print("validation (random slopes):")
        for k, v_ in out.items():
            print(f"  {k}: {v_}")
    return out


if __name__ == "__main__":
    validate()
