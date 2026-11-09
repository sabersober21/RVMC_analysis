# Regional Vaccine Manufacturing Analyses

Independent analyses of the barriers to regional vaccine manufacturing, one region per folder. Each one asks a single question that the Regionalized Vaccine Manufacturing Collaborative (RVMC) has raised but not yet answered, and answers it with public data.

**Author:** Neilay Bhalerao, MSc Control of Infectious Diseases (LSHTM)
**Contact:** neilay21@gmail.com

This is unsolicited work based on public data. It is not affiliated with or endorsed by RVMC, CEPI, CHAI, PAHO, UNICEF or Gavi.

## Analyses

| Region | Folder | Question | Angle | Report | Date |
|---|---|---|---|---|---|
| Africa | [`Africa/`](Africa/) | What would a time-limited price premium for African-made vaccines cost? | Market and financing | [PDF](Africa/RVMC_analysis.pdf) | Nov 2026 |
| Latin America and the Caribbean | [`LAC/`](LAC/) | How far can a vaccine approved by a Latin American regulator travel? | Regulatory and political | [PDF](LAC/RVMC-LAC-regulatory-analysis-Neilay-Bhalerao.pdf) | Nov 2026 |
| ASEAN | `ASEAN/` | Planned | | | |

```text
.
├── README.md          this file
├── Africa/            The Price of Predictable Demand
├── LAC/               Who Trusts a Latin American Approval?
└── ASEAN/             planned
```

Each folder holds its own report PDF, a web version (`report.html`) and an `analysis/` folder with the data and code needed to reproduce every number.

---

## Africa: The Price of Predictable Demand

📁 [`Africa/`](Africa/) · 📄 [Report](Africa/RVMC_analysis.pdf) · 📘 [Folder README](Africa/README.md)

RVMC's Vision asks what time-limited price premium is acceptable for locally made vaccines. This analysis estimates what that premium would cost in Africa, vaccine by vaccine, and tests whether price is the main barrier to committed demand.

| Finding | Result |
|---|---|
| Annual cost at a 41% premium and a 30% African share | About US$95M (uncertainty range US$48–267M) |
| Compared with announced African manufacturing investment | About 18% of US$530M a year |
| Demand reached if African firms won all eight pipeline vaccines | About 45%, against a 60% goal |
| Pipeline doses with only fill-finish planned in Africa | 61% |
| Dakar yellow fever premium over the lowest other UNICEF award, 2014–2025 | Median 35% |

**Method:** annual premium cost = 2030 African demand × reference price × premium × African share. The inputs are CHAI's 2026 demand estimates, 2026 UNICEF prices and RVMC Indicator 5.1. The sensitivity analysis uses one-way ranges and 200,000 probabilistic draws.

## LAC: Who Trusts a Latin American Approval?

📁 [`LAC/`](LAC/) · 📄 [Report](LAC/RVMC-LAC-regulatory-analysis-Neilay-Bhalerao.pdf)

Prepared for the Regional Vaccine Production session at the 10th Global Health Conference of the Americas (Panama, 12 November 2026). RVMC and CHAI's 2026 strategy for the region names limited market access as a structural risk. This analysis measures how far national reliance laws let one regulator's approval travel across the region.

| Finding | Result |
|---|---|
| Births reachable by reliance after an FDA or EMA approval | 86% (27 countries) |
| After an ANVISA (Brazil) approval | 52%, up from 22% before Mexico's 2026 pathway |
| After a COFEPRIS, ANMAT or CECMED approval | 20%, 17% and 16% |
| Births in countries whose reliance laws name only regulators outside the region | 70% |
| Reach of each Latin American regulator if those lists added PAHO reference regulators | 80–87% |

**Method:** reach is the share of 2023 births (World Bank, 9.31M across 33 countries) outside the approving regulator's home country where national law allows reliance on its approval. The baseline is Durán et al. (2021), which covers 20 regulators and 34 countries. It is updated for Brazil (IN 289/2024), Argentina (Decree 892/2025) and Mexico (2026 ANVISA pathway).

---

## Run it yourself

You need Python 3. The Africa model also needs NumPy and pandas. The LAC model uses only the standard library.

```bash
pip install numpy pandas
```

**Africa** (run from inside the folder):

```bash
cd Africa
python analysis/model.py
python analysis/build_report.py . report.html analysis/report_template.html
cd ..
```

**LAC** (run from the repository root):

```bash
python LAC/analysis/reach.py
python LAC/analysis/build_report.py LAC/analysis/report_template.html LAC/report.html LAC/analysis/report.css
```

Each model rewrites its results file (`results.json` or `reach_results.json`), and each build script rebuilds `report.html` from those results.

## Folder contents

### `Africa/`

| File | Purpose |
|---|---|
| `RVMC_analysis.pdf` | Full report |
| `RVMC-analysis-Neilay-Bhalerao.pdf` | Alternative print layout of the report |
| `report.html` | Web version |
| `analysis/inputs.csv` | Demand, reference prices, ranges and sources |
| `analysis/yf_prices.csv` | Yellow fever price series from UNICEF |
| `analysis/model.py` | Model and sensitivity analysis |
| `analysis/results.json` | Model outputs |
| `analysis/build_report.py`, `analysis/report_template.html` | Report builder and text |

### `LAC/`

| File | Purpose |
|---|---|
| `RVMC-LAC-regulatory-analysis-Neilay-Bhalerao.pdf` | Full report |
| `report.html` | Web version |
| `analysis/reliance.csv` | Reliance status for each country, with sources and notes |
| `analysis/births_2023_worldbank.json` | Births by country, 2023 |
| `analysis/reach.py` | Reach model |
| `analysis/reach_results.json` | Model outputs |
| `analysis/build_report.py`, `analysis/report_template.html`, `analysis/report.css` | Report builder, text and styles |

## Limitations

**Africa**
- African production costs at realistic volumes are not public, so observed price premiums stand in for the true cost gap.
- The model sizes the total cost but does not decide who pays it.
- Prices are held at 2026 levels. Freight, financing and regulatory costs are excluded.

**LAC**
- The legal baseline is from 2019–20. Only Brazil, Argentina and Mexico were updated, and the Argentine and Mexican details come from secondary sources.
- The source study covers new medicines. Vaccine-specific rules, and exemptions for vaccines bought through PAHO or UNICEF, may differ.
- A legal pathway does not guarantee fast approval, and births are only a proxy for routine vaccine demand.

These are estimates to support discussion, not forecasts. Each report lists the gaps I would work on next.

## Adding a new region

Each new analysis gets its own folder (for example `ASEAN/`) with the same layout:

```text
REGION/
├── <report>.pdf
├── report.html
└── analysis/
    ├── <input data>.csv
    ├── <model>.py
    ├── <results>.json
    ├── build_report.py
    └── report_template.html
```

Then add a row to the **Analyses** table, a summary section, and its run commands above.

## Key sources

- [RVMC Insights Hub](https://rvmc.net/vaccine-insights)
- [RVMC First Status Report, November 2025](https://static.rvmc.net/downloads/2025-11/RVMC%20Status%20Report%20November%202025.pdf)
- [RVMC Vision, April 2025](https://static.rvmc.net/downloads/2025-04/RVMC_Vision%20Document_April%202025.pdf)
- [CHAI African Vaccine Manufacturing 2026 Supply Landscape](https://static.rvmc.net/downloads/2026-09/African-Vaccine-Manufacturing-2026-Supply-Landscape%20(2).pdf)
- [RVMC and CHAI market-shaping strategy for Latin America and the Caribbean, May 2026](https://static.rvmc.net/downloads/2026-05/RVMC%20CHAI%20Market-shaping%20strategy%20for%20a%20sustainable%20vaccine%20manufacturing%20footprint%20in%20Latin%20America%20and%20the%20Caribbean.pdf)
- [Durán et al. 2021, Rev Panam Salud Publica 45:e10](https://pmc.ncbi.nlm.nih.gov/articles/PMC8040933/)
- [UNICEF vaccine pricing data](https://www.unicef.org/supply/vaccines-pricing-data)

Each report has its full source list.

## AI assistance

Prepared with AI assistance (Claude) for document review and drafting.
