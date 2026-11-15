"""Tests for the Thornthwaite-Mather soil water balance."""

import numpy as np
import pandas as pd

from epss.soil import thornthwaite_mather


def series(values):
    return pd.Series(
        values,
        index=pd.date_range(
            "2001-01-01",
            periods=len(values),
            freq="MS"
        )
    )


def test_hand_checked_months():
    p = series([120.0, 0.0, 50.0])
    pet = series([20.0, 40.0, 20.0])

    tm = thornthwaite_mather(p, pet, smax=80)

    # First month: soil fills and excess becomes runoff
    assert np.isclose(tm["soil"].iloc[0], 80.0)
    assert np.isclose(tm["aet"].iloc[0], 20.0)
    assert np.isclose(tm["runoff"].iloc[0], 20.0)

    # Second month: soil loses water
    expected_soil = 80 * np.exp(-40 / 80)

    assert np.isclose(tm["soil"].iloc[1], expected_soil)
    assert np.isclose(
        tm["aet"].iloc[1],
        80 - expected_soil
    )
    assert np.isclose(tm["runoff"].iloc[1], 0.0)

    # Third month: soil storage increases again
    assert np.isclose(
        tm["soil"].iloc[2],
        expected_soil + 30
    )
    assert np.isclose(tm["aet"].iloc[2], 20.0)


def test_balance_closes_every_month():
    rng = np.random.default_rng(1)

    p = series(rng.gamma(1.0, 50, 120))
    pet = series(rng.uniform(10, 180, 120))

    tm = thornthwaite_mather(p, pet, smax=80)

    # Change in soil storage (S0 = 0)
    dS = tm["soil"].diff().fillna(
        tm["soil"].iloc[0]
    )

    # Monthly water balance
    assert np.allclose(
        p,
        tm["runoff"] + tm["aet"] + dS
    )

    # Physical limits
    assert (tm["soil"] >= -1e-9).all()
    assert (tm["soil"] <= 80 + 1e-9).all()
    assert (tm["runoff"] >= -1e-9).all()
    assert (tm["aet"] <= pet + 1e-9).all()

