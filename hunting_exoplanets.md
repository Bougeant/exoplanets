---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Hunting exoplanets

```python
%load_ext autoreload
%autoreload 2
```

```python
import logging
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from astropy.table import Table
from astroquery.mast import Observations
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from lightkurve import search_lightcurvefile

from exoplanets import astro_data
```

```python
pd.set_option("display.max_rows", 2000)
pd.set_option("display.max_columns", 1000)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
```

## Exploring Kepler targets with light curves


### Reading Kepler stellar data with available light curves

```python
df = astro_data.read_kepler_data(table="q1_q17_dr25_stellar", filename="./data/kepler_stellar_data.csv")
```

### Displaying distribution of Kepler target stars as a function of magnitude and mass.

```python
plt.figure(figsize=(16, 8))
sns.kdeplot(df["Kepler-band Magnitude Value [mag]"], df["Stellar Mass Value [Solar mass]"], n_levels=10, shade=True, shade_lowest=False, bw=0.05, label="Stars with Kepler light curves", alpha=0.8)
sns.kdeplot(df[df["Number of Associated Confirmed Planets"] >0]["Kepler-band Magnitude Value [mag]"], df[df["Number of Associated Confirmed Planets"] >0]["Stellar Mass Value [Solar mass]"], n_levels=10, shade=True, shade_lowest=False, bw=0.2, alpha=0.5, label="Confirmed planets")
plt.xlim(10, 18)
plt.ylim(.3, 1.5)
leg = plt.legend()
for lh in leg.legendHandles: 
    lh.set_alpha(0.5)
sns.despine()
```

```python
grid = sns.jointplot(data=df, x="Kepler-band Magnitude Value [mag]", y="Stellar Mass Value [Solar mass]", kind="kde", n_levels=20, joint_kws={'bw':0.1, "shade_lowest": False}, marginal_kws={'bw':0.05}, height=8, xlim=(10, 18), ylim=(0, 1.8), cmap="Blues")
sns.scatterplot(data=df, x="Kepler-band Magnitude Value [mag]", y="Stellar Mass Value [Solar mass]", s=2, ax=grid.ax_joint, linewidth=0, alpha=0.3, label="Stars with available light curves")
grid.fig.set_figwidth(16)
sns.despine()
```

### Distribution of number of objects per star

```python
fig = plt.figure(figsize=(16, 8))
plt.hist(
    x= [df["Number of Associated TCEs"], df["Number of Associated KOIs"], df["Number of Associated Confirmed Planets"]], 
    label=["Threshold Crossing Events", "Kepler Objects of Interest", "Confirmed Planets", ],
    log=True,
    alpha=0.7
)
plt.xlabel("Number of objects per star")
plt.ylabel("Number of stars")
plt.xticks([i+0.5 for i in range(11)], [i for i in range(10)])
plt.legend(frameon=False)
sns.despine()
plt.show()
```

## Exploring Kepler Objects of Interest


### Reading Kepler Objects of Interest (KOI) data

```python
df_koi = astro_data.read_kepler_data(table="cumulative", filename="./data/kepler_objects_of_interest.csv")
```

```python
df_koi.sample(5)
```

### Distribution of KOIs as a function of orbital period

```python
plt.figure(figsize=(16, 8))
sns.distplot(df_koi[df_koi["Orbital Period (days)"]<700]["Orbital Period (days)"], kde=False)
plt.yscale("log")
plt.ylabel("Number of KOIs (log scale)")
sns.despine()
```

### Distribution of KOIs per category

```python
df_koi["Outcome"] = df_koi["Exoplanet Archive Disposition"].str.title()
df_koi.loc[df_koi["Contamination Flag"] == 1, "Outcome"] = "Contamination"
df_koi.loc[df_koi["Nearby Star Flag"] == 1, "Outcome"] = "Nearby Star"
df_koi.loc[df_koi["Stellar Eclipse Flag"] == 1, "Outcome"] = "Stellar Eclipse"
df_koi.loc[df_koi["Not Transit-Like Flag"] == 1, "Outcome"] = "Not Transit-Like"
df_koi.loc[df_koi["Outcome"] == "False Positive", "Outcome"] = "Other False Positive"
```

```python
plt.figure(figsize=(16, 8))
sns.countplot(df_koi["Outcome"], order=["Candidate", "Stellar Eclipse", "Not Transit-Like", "Nearby Star", "Contamination", "Other False Positive"])
plt.ylabel("Number of KOI")
sns.despine()
```

## Exploring light curves: example of exoplanet Kepler-167e (KIC 3239945)


### Reading light curve for Kepler-167e's host star

```python
lc_all = search_lightcurvefile(target="KIC3239945", mission="Kepler").download_all(download_dir="./data/")
lc = lc_all.PDCSAP_FLUX.stitch()
lc = lc.to_pandas()
```

```python
os.mkdir()
```

### Light curve for Kepler-167e's host star (first 90 days of data)

```python
fig = plt.figure(figsize=(16, 8))
sns.scatterplot(lc_all[0].SAP_FLUX.to_pandas()["time"], lc_all[0].SAP_FLUX.to_pandas()["flux"], s=20, linewidth=0, label="Raw flux (SAP)")
sns.scatterplot(lc_all[0].PDCSAP_FLUX.to_pandas()["time"], lc_all[0].PDCSAP_FLUX.to_pandas()["flux"], s=20, linewidth=0, label="Pre-conditioned flux (PDCSAP)")
sns.despine()
plt.legend(frameon=False)
plt.xlabel("Time (days)")
plt.ylabel("Flux (e-/s)")
plt.show()
```

### Light curve for Kepler-167e transit

```python
fig = plt.figure(figsize=(16, 8))
sns.scatterplot(lc["time"], lc["flux"], s=50, linewidth=0, label="Pre-conditioned flux (PDCSAP)")
plt.ylim(0.975, 1.005)
plt.xlim(419, 421.5)
plt.xlabel("Time (days)")
plt.ylabel("Normalized flux")
plt.legend()
sns.despine()
```

```python

```
