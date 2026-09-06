"""Constrained-score TOST for independent binomial decision rates (spec 4.3)."""
import math
from scipy.optimize import minimize_scalar
from scipy.special import xlogy
from scipy.stats import norm


def _score(k1,n1,k2,n2,delta):
    # Null p1-p2=delta; maximise the joint binomial likelihood over p2.
    lower=max(0.,-delta)
    upper=min(1.,1-delta)
    def loss(q):
        p=q+delta
        return -float(xlogy(k1,p)+xlogy(n1-k1,1-p)+xlogy(k2,q)+xlogy(n2-k2,1-q))
    fit=minimize_scalar(loss,bounds=(lower,upper),method='bounded',
                        options={'xatol':1e-14})
    q=min([lower,upper,float(fit.x)],key=loss)
    p=q+delta
    variance=(p*(1-p)/n1+q*(1-q)/n2)*(n1+n2)/(n1+n2-1)
    difference=k1/n1-k2/n2-delta
    if variance<=0:
        return math.copysign(math.inf,difference) if difference else 0.
    return difference/math.sqrt(variance)


def tost(k1,n1,k2,n2,margin=.10,alpha=.05):
    if not (n1>0 and n2>0 and 0<=k1<=n1 and 0<=k2<=n2):
        raise ValueError('Invalid binomial counts')
    if not 0<margin<1 or not 0<alpha<.5:
        raise ValueError('Invalid equivalence settings')
    lower_p=float(norm.sf(_score(k1,n1,k2,n2,-margin)))
    upper_p=float(norm.cdf(_score(k1,n1,k2,n2,margin)))
    p=max(lower_p,upper_p)
    return {'difference':k1/n1-k2/n2,'margin':margin,'alpha':alpha,
            'p_lower':lower_p,'p_upper':upper_p,'p_value':p,'equivalent':p<alpha,
            'method':'constrained-binomial score TOST with Miettinen-Nurminen variance correction',
            'interpretation':'equivalent' if p<alpha else 'equivalence_not_established'}
