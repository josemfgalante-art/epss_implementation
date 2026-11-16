# EPSS 2026/27 · Part 1 · Water balance and long-term simulation of a reservoir

## Group

| Name | Student number |
| José Galante | 1120342 |
| Sebastião Minau | 1111133 |
| Dinis Barata | 1109759 |
| Nolan Rosa | 1110781 |

## How to run

```
conda env create -f environment.yml      # once
conda activate epss
python -m ipykernel install --user --name epss --display-name "Python (epss)"   # once
pytest                                   # tests
```

The parts you must write are marked `# TODO` and raise `NotImplementedError` with a description of the
task; the comments below each `TODO` say what goes in and what comes out. The notebooks keep the outputs of
a complete solution, so you can see what is intended: your results should look alike.

`pytest` (also run by GitHub Actions on every push) fails until the TODOs are done. One test is itself a
TODO: write the checks of `test_balance_closes_every_month` in `tests/test_soil.py`.

Open the notebooks in `notebooks/` in order (01 → 06) with the **epss** kernel and run them top to bottom.
Notebook 01 downloads ERA5-Land data (needs a CDS account and `~/.cdsapirc`); if
`data/raw/era5land_monthly.nc` already exists, the download is skipped.

| Folder | Content |
|---|---|
| `src/epss/` | `climate`, `pet`, `soil`, `eflows`, `reservoir`, `metrics` |
| `notebooks/` | 01 download · 02 climate · 03 PET · 04 Thornthwaite–Mather · 05 reservoir · 06 design |
| `tests/` | `pytest` tests, incl. a reference case in `data/reference/` |
| `data/` | `case.json`, `catchment.kml`, `hv_curve.csv`, `raw/` ERA5-Land files |

## Data

`data/raw/` holds ERA5-Land monthly averaged data (Muñoz Sabater, 2019, C3S Climate Data Store,
[doi:10.24381/cds.68d2bb30](https://doi.org/10.24381/cds.68d2bb30)), cropped to 36.9–39.7° N, 9.2–6.2° W,
1981–2020: `era5land_monthly.nc` (2 m temperature, total precipitation) and `tmax_tmin.nc` (monthly maximum
and minimum of the mean diurnal cycle of 2 m temperature). Licence: CC-BY 4.0. Generated using Copernicus
Climate Change Service information 2026. Neither the European Commission nor ECMWF is responsible for any
use that may be made of the Copernicus information or data it contains.

`data/reference/` is a synthetic case (made-up climate) with known results, used by `tests/test_reference.py`.

## Answers (section 3.7)

## Reservoir design

The objective was to determine the maximum reservoir water level required to achieve a target time reliability of 90%.

For the present climate conditions, the calculated maximum water level was approximately **6.76 m**, corresponding to a maximum storage volume of approximately **0.537 hm³**.

Under a scenario with a temperature increase of 2 °C, the required maximum water level increased to approximately **7.48 m**.

The results indicate that higher temperatures increase potential evapotranspiration and reduce the water available for reservoir inflow. Consequently, a larger reservoir capacity is required to maintain the same supply reliability.

### Results figure

[Reservoir reliability](reliability.png)

The simulation evaluates reservoir reliability for different maximum water levels (hmax).

The results show that increasing the maximum water level improves both time-based (Rt) and volumetric (Rv) reliability. Under present climate conditions, a maximum water level of approximately **6.76 m** is required to achieve the target time reliability of 90%.

The sensitivity analysis also shows that reducing irrigation demand by 25% decreases the required height to approximately 6.34 m, while increasing demand by 25% raises it to approximately 7.14 m.

Under the +2 °C scenario, the required maximum water level increases to approximately **7.48 m**, highlighting the impact of higher temperatures on reservoir storage requirements.

## AI declaration
ChatGPT was used to help understand programming concepts, explain error messages, troubleshoot Python code, and review parts of the notebook implementation.
It was also used to support the interpretation of the hydrological calculations and to improve the clarity of the project documentation.
The results and code were checked by the group before submission.
