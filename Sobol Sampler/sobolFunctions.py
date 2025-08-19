'''
@author: Mason Fox
date: 11 OCT 2023

Define functions and values to be used for sampling.
'''

from dataclasses import dataclass
from enum import Enum

class uncertaintyType(Enum):
    """Restrict uncertainty type to percent or abs value in uncertain_parameter class"""
    pct = 1
    absv = 2
    std_dev = 3

@dataclass(kw_only=True)
class property():
    """Defines information for problem specification. Permits generating uncertain_value or function object based on parameter."""
    name:             str
    type:             uncertaintyType
    dist:             str
    mean_boundLow:    float
    stddev_boundHigh: float
    unit:             str

def defineParams() -> dict:
    nb_mult     = property(name='nb_multiplier',     type=uncertaintyType.absv, dist='unif',  mean_boundLow=0.8,   stddev_boundHigh=1.2,  unit='-')
    chf_mult    = property(name='chf_multiplier',    type=uncertaintyType.absv, dist='unif',  mean_boundLow=1.0,   stddev_boundHigh=3.0, unit='-') #https://doi.org/10.1016/j.nucengdes.2023.112509
    trans_mult  = property(name='trans_multiplier',  type=uncertaintyType.absv, dist='unif',  mean_boundLow=0.8,   stddev_boundHigh=1.2, unit='-')
    fb_mult     = property(name='fb_multiplier',     type=uncertaintyType.absv, dist='unif',  mean_boundLow=0.8,   stddev_boundHigh=1.2,  unit='-')
    k_clad      = property(name='clad_cond_scale',   type=uncertaintyType.absv, dist='norm',  mean_boundLow=1.0,   stddev_boundHigh=0.0675,  unit='-') #MATPRO @473K
    cp_clad     = property(name='clad_cp_scale',     type=uncertaintyType.absv, dist='norm',  mean_boundLow=1.0,   stddev_boundHigh=0.07, unit='-') #MATPRO @1248K
    k_fuel      = property(name='fuel_cond_scale',   type=uncertaintyType.absv, dist='norm',  mean_boundLow=1.0,   stddev_boundHigh=0.055, unit='-') #https://doi.org/10.1016/j.nucengdes.2023.112304
    cp_fuel     = property(name='fuel_cp_scale',     type=uncertaintyType.absv, dist='norm',  mean_boundLow=1.0,   stddev_boundHigh=0.03,  unit='-') #https://doi.org/10.13182/NT72-6
#    energyDep   = property(name='energyDep_val',     type=uncertaintyType.absv, dist='unif',  mean_boundLow=150.0, stddev_boundHigh=190.0,  unit='cal/g') #PWR relevant
    pulse_width = property(name='pulse_width',       type=uncertaintyType.absv, dist='unif',  mean_boundLow=20E-3,  stddev_boundHigh=100E-3,  unit='s') #PWR relevant
    k_gas       = property(name='gas_cond_scale',    type=uncertaintyType.absv, dist='norm',  mean_boundLow=1.0,   stddev_boundHigh=0.271, unit='-') #https://doi.org/10.1016/j.nucengdes.2019.110289

 #   paramList = [k_fuel, cp_fuel, k_clad, cp_clad, pulse_width, energyDep, nb_mult, chf_mult, trans_mult, fb_mult, k_gas]
    paramList = [k_fuel, cp_fuel, k_clad, cp_clad, pulse_width, nb_mult, chf_mult, trans_mult, fb_mult, k_gas]

    problem = {
        'num_vars': len(paramList),
        'names':    [param.name for param in paramList],
        'dists':    [param.dist for param in paramList],
        'bounds':   [[param.mean_boundLow, param.stddev_boundHigh] for param in paramList]
    }

    return problem
