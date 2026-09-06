"""Offline analysis of the Phase 1.5 sweep; no model calls or file writes."""
from __future__ import annotations

import math
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, xlogy
from scipy.stats import beta, chi2, norm

VALUES = (0.1, 0.3, 0.5, 0.7, 0.9)
# Thesis 6.1.1, expressed against each problem's FIRST decision label.
# Absence means no pre-specified simple-problem direction, not a null hypothesis.
DIRECTIONS = {("RE", "S1"): 1, ("TfA", "S1"): 1, ("PD", "S1"): 1,
              ("ID", "S2"): 1, ("TfA", "S2"): -1, ("MS", "S2"): 1,
              ("RT", "S3"): 1, ("MoR", "S3"): 1, ("RE", "S3"): -1}


def wilson(k, n):
    if not n:
        return None
    z = float(norm.ppf(.975))
    p = k / n
    den = 1 + z*z/n
    mid = (p + z*z/(2*n))/den
    width = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return [max(0., mid-width), min(1., mid+width)]


def logistic(cells):
    """Grouped binomial MLE, LR slope test and Wald CI; flag separation explicitly."""
    used = [c for c in cells if c['n_valid']]
    if len(used) < 2:
        return {'status': 'insufficient_data'}
    x = np.array([c['value'] for c in used])
    n = np.array([c['n_valid'] for c in used])
    k = np.array([c['opt0_count'] for c in used])
    if k.sum() in (0, n.sum()):
        return {'status': 'pinned', 'slope': None, 'p_value': None, 'ci95': None}
    # With a single continuous predictor, these conditions exactly detect
    # complete and quasi separation (including overlap at one boundary point).
    yes, no = x[k > 0], x[k < n]
    if yes.min() >= no.max() or no.min() >= yes.max():
        return {'status': 'separation', 'slope': None, 'p_value': None, 'ci95': None}
    design = np.column_stack([np.ones(len(x)), x])

    def loss(b):
        eta = design @ b
        return float(np.sum(n*np.logaddexp(0, eta)-k*eta))

    def gradient(b):
        return design.T @ (n*expit(design @ b)-k)

    p0 = k.sum()/n.sum()
    fit = minimize(loss, [math.log(p0/(1-p0)), 0.], jac=gradient,
                   method='BFGS', options={'gtol': 1e-7})
    if not np.isfinite(fit.fun) or np.max(np.abs(gradient(fit.x))) > 1e-5:
        return {'status': 'fit_failed'}
    p = expit(design @ fit.x)
    information = design.T @ ((n*p*(1-p))[:, None]*design)
    try:
        covariance = np.linalg.inv(information)
    except np.linalg.LinAlgError:
        return {'status': 'singular_information'}
    se = math.sqrt(float(covariance[1, 1]))
    slope = float(fit.x[1])
    null_loss = -float(np.sum(xlogy(k, p0)+xlogy(n-k, 1-p0)))
    lr = max(0., 2*(null_loss-fit.fun))
    return {'status': 'ok', 'slope': slope, 'se': se,
            'ci95': [slope-1.95996398454*se, slope+1.95996398454*se],
            'p_value': float(chi2.sf(lr, 1)), 'test': 'likelihood_ratio_1df',
            'lr_statistic': lr}


def analyze(records, *, params, problems, arms, n):
    """Account for every planned cell; incomplete/failed cells cannot pass."""
    grouped = {}
    seen = set()
    for r in records:
        key = (r['arm'], r['swept_parameter'], r['problem_id'],
               r['sweep_value'], r['call_index'])
        if key in seen:
            raise ValueError(f'Duplicate observation: {key}')
        seen.add(key)
        if (key[0] not in arms or key[1] not in params or key[2] not in problems
                or key[3] not in VALUES or not 1 <= key[4] <= n):
            raise ValueError(f'Observation outside frozen design: {key}')
        grouped.setdefault(key[:4], []).append(r)
    rows = []
    for arm in arms:
        for param in params:
            for problem in problems:
                cells = []
                for value in VALUES:
                    data = grouped.get((arm, param, problem, value), [])
                    valid = [r for r in data if r['parse_status'] == 'ok'
                             and r['parsed_decision'] in r['labels']]
                    k = sum(r['parsed_decision'] == r['labels'][0] for r in valid)
                    cells.append({'value': value, 'n_expected': n, 'n_recorded': len(data),
                                  'n_valid': len(valid), 'n_missing': n-len(data),
                                  'n_invalid': len(data)-len(valid), 'opt0_count': k,
                                  'rate': k/len(valid) if valid else None,
                                  'ci95': wilson(k, len(valid))})
                fit = logistic(cells)
                rates = [c['rate'] for c in cells]
                complete = all(c['n_recorded'] == n for c in cells)
                quality = all(c['n_valid']/n >= .98 for c in cells)
                direction = DIRECTIONS.get((param, problem))
                available = all(p is not None for p in rates)
                monotonic = (available and (all(a <= b for a, b in zip(rates, rates[1:]))
                                           or all(a >= b for a, b in zip(rates, rates[1:]))))
                h = (abs(2*math.asin(math.sqrt(rates[-1])) -
                         2*math.asin(math.sqrt(rates[0]))) if available else None)
                match = (direction*fit['slope'] > 0 if direction and fit['status'] == 'ok'
                         else None)
                passed = bool(complete and quality and fit['status'] == 'ok'
                              and fit['p_value'] < .05 and h >= .20 and monotonic and match)
                rows.append({'arm': arm, 'parameter': param, 'problem': problem,
                             'cells': cells, 'fit': fit, 'complete': complete,
                             'parse_quality_98pct': quality, 'cohens_h_extremes': h,
                             'monotonic': bool(monotonic), 'predicted_direction': direction,
                             'direction_matches': match, 'criterion_met': passed})
    # Independent-call difference in endpoint rate changes. Same requested seed
    # does not make the stochastic model outputs statistically paired.
    contrasts = []
    if len(arms) == 2:
        for param in params:
            for problem in problems:
                pair = [next(r for r in rows if r['arm'] == a and
                             r['parameter'] == param and r['problem'] == problem) for a in arms]
                endpoints = [r['cells'][i] for r in pair for i in (0, -1)]
                if not all(c['n_valid'] for c in endpoints):
                    continue
                p = [c['rate'] for c in endpoints]
                delta = (p[3]-p[2])-(p[1]-p[0])
                # Four exact binomial intervals with Bonferroni coverage give
                # a conservative 95% interval for the linear contrast, including
                # all-zero/all-one cells where a Wald SE is misleadingly zero.
                bounds = []
                for c in endpoints:
                    k, count = c['opt0_count'], c['n_valid']
                    tail = .05/8
                    lo = float(beta.ppf(tail, k, count-k+1)) if k else 0.
                    hi = float(beta.ppf(1-tail, k+1, count-k)) if k<count else 1.
                    bounds.append((lo,hi))
                lower = bounds[0][0]-bounds[1][1]-bounds[2][1]+bounds[3][0]
                upper = bounds[0][1]-bounds[1][0]-bounds[2][0]+bounds[3][1]
                contrasts.append({'parameter': param, 'problem': problem,
                                  'contrast': f'{arms[1]} endpoint change minus {arms[0]} endpoint change',
                                  'estimate': delta,
                                  'ci95_conservative': [lower, upper],
                                  'inference': 'Bonferroni-combined Clopper-Pearson endpoint intervals; independent binomial-call assumption'})
    return {'schema_version': '1.0', 'n_records': len(records),
            'n_expected': len(arms)*len(params)*len(problems)*len(VALUES)*n,
            'sweeps': rows, 'delivery_contrasts': contrasts,
            'battery_status': 'NOT CLOSED: coherence, paraphrase and numeric/verbal tests also required',
            'inference_note': 'Unadjusted p<0.05 follows spec 4.1; no new directional hypotheses inferred.'}


def markdown(report):
    lines = ['# Phase 1.5 delivery comparison', '', report['battery_status'], '',
             f"Records: {report['n_records']} / {report['n_expected']}. Missing and invalid calls are retained in the JSON accounting.", '',
             '| Delivery | Parameter | Problem | Rates (.1/.3/.5/.7/.9) | Slope p | h | Monotonic | Direction | Sweep criterion |',
             '|---|---|---|---|---|---|---|---|---|---|']
    for r in report['sweeps']:
        rates = ' / '.join('NA' if c['rate'] is None else f"{c['rate']:.2f}" for c in r['cells'])
        p = r['fit'].get('p_value')
        ptext = f'{p:.4g}' if p is not None else r['fit']['status']
        h = r['cohens_h_extremes']
        htext = f'{h:.3f}' if h is not None else 'NA'
        direction = 'not pre-specified' if r['predicted_direction'] is None else str(r['direction_matches'])
        verdict = ('incomplete' if not r['complete'] else 'not assessable (no predicted sign)'
                   if r['predicted_direction'] is None else 'met' if r['criterion_met'] else 'not met')
        lines.append(f"| {r['arm']} | {r['parameter']} | {r['problem']} | {rates} | {ptext} | {htext} | {r['monotonic']} | {direction} | {verdict} |")
    lines += ['', report['inference_note'], '',
              'The alternative delivery retains the profile and scaffold. Headroom is measured, not assumed. The two arms jointly vary message role and requested response format; this is a delivery-package contrast, not attribution to either component alone.', '']
    return '\n'.join(lines)
