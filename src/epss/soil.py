
"""Monthly Thornthwaite-Mather soil water balance (sheet eqs. 3-7)."""

import numpy as np
import pandas as pd


def thornthwaite_mather(p, pet, smax, s0=0.0):
    """Monthly soil water balance. All values in mm (per month).

    p, pet: pd.Series (same index)
    smax: soil water capacity
    s0: initial soil water

    Returns a DataFrame with columns:
    p, pet, deficit, aet, soil, runoff.

    P = H + AET + dS closes every month.
    """

    # Initial conditions
    S = float(s0)
    L = 0.0
    results = []

    for P, PET in zip(p, pet):

        if P >= PET:
            # Wet month
            aet = PET

            water = S + P - PET

            S_new = min(smax, water)
            runoff = max(0.0, water - smax)

            L = 0.0

        else:
            # Dry month
            deficit = PET - P
            L = L - deficit

            # Soil water storage
            S_new = S * np.exp(L / smax)

            # Actual evapotranspiration
            aet = min(PET, P + S - S_new)

            # Remaining water goes to runoff
            runoff = max(0.0, P + S - S_new - aet)

        results.append({
            "p": P,
            "pet": PET,
            "deficit": L,
            "aet": aet,
            "soil": S_new,
            "runoff": runoff
        })

        S = S_new

    return pd.DataFrame(results, index=p.index)


