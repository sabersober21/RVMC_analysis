# The Price of Predictable Demand

An independent analysis of what it would cost to buy African-made vaccines at a time-limited price premium.

**Author:** Neilay Bhalerao, MSc Control of Infectious Diseases (LSHTM) (Graduated)
**Date:** November 2026
**Report:** [Read the PDF](RVMC_analysis.pdf)

This is unsolicited work based on public data. It was written for the Regionalized Vaccine Manufacturing Collaborative (RVMC) Secretariat, but it is not affiliated with or endorsed by RVMC, CEPI, CHAI, UNICEF or Gavi.

## The question

RVMC's Vision asks: "What is the acceptable time-limited price premium for locally manufactured vaccines?" This project estimates what such a premium would cost in Africa, vaccine by vaccine, and tests whether the premium is the main barrier to committed demand.

## Key findings

| Finding | Result |
|---|---|
| Annual cost at a 41% premium and a 30% African share | About US$95M (uncertainty range US$48–267M) |
| Compared with announced African manufacturing investment | About 18% of US$530M a year |
| Demand reached if African firms won all eight pipeline vaccines | About 45%, against a 60% goal |
| Pipeline doses with only fill-finish planned in Africa | 61% |
| Dakar yellow fever premium over the lowest other UNICEF award, 2014–2025 | Median 35% |

The premium looks affordable at these levels unless true African production costs are much higher than current evidence suggests. The current pipeline's coverage limit and its reliance on imported drug substance may matter more.

## Method

For each of the eight vaccines:

```text
annual premium cost = 2030 African demand × reference price × premium × African share
```

The base case uses:

- **Demand:** CHAI's 2026 Supply Landscape, using Linksbridge GVMM
- **Prices:** 2026 UNICEF awarded prices at the Gavi tier
- **Premium:** 41%, from RVMC Indicator 5.1
- **African share:** 30%, the level African Union heads of state asked Gavi to source from Africa

The sensitivity analysis includes one-way ranges and a 200,000-draw probabilistic analysis with a fixed random seed. The ranges for premium (15–100%), share (15–50%) and demand (±20%) are my assumptions.

## Run it yourself

You need Python 3 with NumPy and pandas.

```bash
pip install numpy pandas
python analysis/model.py
```

This prints the results and updates `analysis/results.json`.

To rebuild the HTML report from those results:

```bash
python analysis/build_report.py . report.html analysis/report_template.html
```

## Repository contents

| File | Purpose |
|---|---|
| `RVMC_analysis.pdf` | Full report |
| `report.html` | Web version of the report |
| `analysis/inputs.csv` | Demand, reference prices, price ranges and source files |
| `analysis/yf_prices.csv` | Yellow fever price series from UNICEF |
| `analysis/model.py` | Model and sensitivity analysis |
| `analysis/results.json` | Model outputs |
| `analysis/build_report.py` | Builds the report and its charts |
| `analysis/report_template.html` | Report text and layout |

## Limitations

- African production costs at realistic volumes are not public, so observed price premiums stand in for the true cost gap.
- The model sizes the total cost but does not decide who pays it.
- Global prices are held fixed, and 2026 prices are applied to 2030 demand.
- Freight, financing, regulatory and supply-reliability costs are excluded, as is any value from outbreak readiness.
- The 45% coverage limit compares 2030 pipeline demand with a 2035 demand projection, so it is indicative.

These are estimates to support discussion, not forecasts.

## Sources

- [RVMC Insights Hub](https://rvmc.net/vaccine-insights)
- [RVMC First Status Report](https://static.rvmc.net/downloads/2025-11/RVMC%20Status%20Report%20November%202025.pdf)
- [RVMC Vision](https://static.rvmc.net/downloads/2025-04/RVMC_Vision%20Document_April%202025.pdf)
- [CHAI African Vaccine Manufacturing 2026 Supply Landscape](https://static.rvmc.net/downloads/2026-09/African-Vaccine-Manufacturing-2026-Supply-Landscape%20(2).pdf)
- [UNICEF vaccine pricing data](https://www.unicef.org/supply/vaccines-pricing-data)
- [Gavi AVMA+ proposal, May 2026](https://www.gavi.org/news/media-room/gavi-propose-new-incentives-aimed-advancing-vaccine-manufacturing-africa)

The report has the full source list.

## AI assistance

Prepared with AI assistance (Claude) for document review and formatting.

## Contact

Neilay Bhalerao: neilay21@gmail.com
