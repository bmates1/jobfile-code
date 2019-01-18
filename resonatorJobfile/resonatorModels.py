###################################################################################
#
# Resonator Models
#
# Stores multiple models for our microwave resonators and allows the calculation
# of resonances frequencies and the slider shifts required to obtain target
# resonance frequencies.
#

import numpy as np
import scipy.optimize as op

# Maximum allowed shift for the various models
MAXSHIFT = {'wigglemodel1':95,
            'wigglemodel1b':120}


def wigglemodel1(delta,e,w,s,Z1,Cc,Lc):
    """ Calculate the resonance frequency using a linear model

    This model predicts electrical length as a function of: excess length (e),
    number of wiggles (w), number of sliders (s), and slider shift (delta).

    It also adjusts the electrical length (in s) according the the coupling
    capacitance (Cc) and coupling inductance (Lc) relative to characteristic
    impedance (Z1).

    Note: this is the model based off the measurement of 16 wiggletest chips.
    """
    if delta<0.0 or delta>MAXSHIFT['wigglemodel1']:
        raise ValueError('Slider shift out of range.')

    # Coefficients taken from fit to resonance data from 16 chips:
    fitoffset = 7.4567232486167533e-11
    fitdlde = 3.4941888676681529e-14
    fitdldw = 7.1328613023022007e-12
    fitdldsdelta = -6.629475813451534e-14

    model_l = fitoffset + fitdlde*e + fitdldw*w + fitdldsdelta*s*delta
    model_f0 = 1 / (model_l + 4*Cc*Z1 + 4*Lc/Z1)

    return model_f0

def wigglemodel1b(delta,e,w,s,Z1,Cc,Lc):
    """ Calculate the resonance frequency using a linear model

    This model predicts electrical length as a function of: excess length (e),
    number of wiggles (w), number of sliders (s), and slider shift (delta).

    It also adjusts the electrical length (in s) according the the coupling
    capacitance (Cc) and coupling inductance (Lc) relative to characteristic
    impedance (Z1).

    Note: this is a modification of wigglemodel1 for slightly broader wiggles
    """
    if delta<0.0 or delta>MAXSHIFT['wigglemodel1b']:
        raise ValueError('Slider shift out of range.')

    # Coefficients modified from wigglemodel1: NOTE: I HAVENT CHANGED THESE VALUES YET!
    fitoffset = 7.4567232486167533e-11
    fitdlde = 3.4941888676681529e-14
    fitdldw = 7.1328613023022007e-12
    fitdldsdelta = -6.629475813451534e-14

    model_l = fitoffset + fitdlde*e + fitdldw*w + fitdldsdelta*s*delta
    model_f0 = 1 / (model_l + 4*Cc*Z1 + 4*Lc/Z1)

    return model_f0


######################################################################################
######################################################################################
#                            Model Selector & Solver                                 #
######################################################################################
######################################################################################

def getModel(modelname):
    """ Select a model function by name """
    if modelname == 'wigglemodel1':
        return wigglemodel1
    elif modelname == 'wigglemodel1b':
        return wigglemodel1b
    else:
        raise ValueError('Model not found.')

def calcDelta(modelname,designparams,f0):
    """ Calculate deltas for a target frequency

    Numerically solves the inverse model by bisection of a range. Note
    that this assumes the model is monotonic across the range and spans
    the target frequency.
    """
    model = getModel(modelname)
    tempfun = lambda delta : model(delta,**designparams) - f0
    delta = op.bisect(tempfun,0.0,MAXSHIFT[modelname])

    return delta

def calcDeltas(modelname,designparams,f0s):
    """ Calculate deltas for a list of target frequencies

    Numerically solves the inverse model by bisection of a range. Note
    that this assumes the model is monotonic across the range and spans
    the target frequency.
    """
    deltas = np.zeros_like(f0s)
    model = getModel(modelname)

    for n in range(len(f0s)):
        tempfun = lambda delta : model(delta,**designparams) - f0s[n]
        deltas[n] = op.bisect(tempfun,0.0,MAXSHIFT[modelname])

    return deltas