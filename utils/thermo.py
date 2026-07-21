import math

def gibbs_energy(dH, dS, temperature):

    T = temperature + 273.15

    dG = dH - (T * dS / 1000)

    return round(dG,2)

def spontaneity(dG):

    if dG < 0:
        return "Spontaneous"

    elif dG == 0:
        return "Equilibrium"

    return "Non-Spontaneous"
