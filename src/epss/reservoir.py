
"""Monthly reservoir mass balance (sheet eqs. 10-13).

Units: volumes hm³, levels m, areas km², evaporation mm/month.
1 hm³/m = 1 km², so dV/dh from the h-V table is directly an area in km².
"""

import numpy as np
import pandas as pd


class Reservoir:
    def __init__(self, hv, hmax, hmin=0.0, area=None):
        """hv: DataFrame with columns h_m, v_hm3 (increasing).
        area: fixed surface area A0 (km²), or None to use A(h) = dV/dh.
        """
        self.hv = hv.sort_values("h_m").reset_index(drop=True)
        self.area0 = area
        self.hmax, self.hmin = hmax, hmin
        self.vmax = float(self.volume(hmax))
        self.vmin = float(self.volume(hmin))

    def volume(self, h):
        """Volume (hm³) at level h (m)."""
        return np.interp(h, self.hv.h_m, self.hv.v_hm3)

    def level(self, v):
        """Level (m) at volume v (hm³)."""
        return np.interp(v, self.hv.v_hm3, self.hv.h_m)

    def area(self, v):
        """Surface area (km²) at volume v: fixed A0, or dV/dh."""
        if self.area0 is not None:
            return self.area0

        dVdh = np.gradient(self.hv.v_hm3, self.hv.h_m)

        return np.interp(self.level(v), self.hv.h_m, dVdh)

    def simulate(self, inflow, evap_mm, demand, eflow, v0=None):
        """Month-by-month simulation.

        All inputs are pd.Series on the same monthly index.
        Order: inflow -> e-flow -> evaporation -> supply -> spill.
        """

        # Initial reservoir volume
        V = self.vmax if v0 is None else v0
        results = []

        for date in inflow.index:

            # Volume at the beginning of the month
            V_start = V

            Qin = inflow.loc[date]
            D = demand.loc[date]
            E = evap_mm.loc[date]
            target = eflow.loc[date]

            # 1. Add inflow
            V = V + Qin

            # 2. Environmental flow
            eco = min(target, Qin)
            V = V - eco

            # 3. Evaporation
            evaporation = E * self.area(V_start) / 1000
            evaporation = min(evaporation, max(0, V - self.vmin))
            V = V - evaporation

            # 4. Water supply
            supply = min(D, max(0, V - self.vmin))
            deficit = D - supply
            V = V - supply

            # 5. Spill
            spill = max(0, V - self.vmax)
            V = V - spill

            results.append({
                "inflow": Qin,
                "eflow": eco,
                "evaporation": evaporation,
                "supply": supply,
                "deficit": deficit,
                "spill": spill,
                "volume": V,
                "level": self.level(V)
            })

        return pd.DataFrame(results, index=inflow.index)
