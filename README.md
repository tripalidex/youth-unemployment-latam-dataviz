# The Waiting Generation: Spatiotemporal Visual Analytics and Gender Disparities in Latin American Youth Unemployment

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Data Source: ILOSTAT](https://img.shields.io/badge/Data%20Source-ILOSTAT%20API-red.svg)](https://ilostat.ilo.org/)
[![Target Journal: Journal of Visualization](https://img.shields.io/badge/Target%20Journal-Scopus%20Q3%20(Springer)-green.svg)](https://link.springer.com/journal/12650)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Research Overview & Abstract
This repository contains the official dataset pipeline, data dictionary, automated Jupyter Notebooks, and Power BI visual analytics artifacts for the research paper:

> **Title:** *The Waiting Generation: Spatiotemporal Visual Analytics and Gender Disparities in Latin American Youth Unemployment*  
> **Course:** Data Visualization (*Visualización de Datos*), 2026-02  
> **Institution:** Universidad San Ignacio de Loyola (USIL), Lima, Peru  
> **Faculty:** Faculty of Engineering and Artificial Intelligence  
> **Authors:** Juan Antonio Coronado Palacios, Lucero Milagros Cubas Quispe, Carlos Martin Quispe Bartolo, Maria Sofia Solari Hipólito  
> **Advisor:** Dr. Alfredo Daza Vergaray  
> **Target Journal:** *Journal of Visualization* (Springer, Scopus Q3) / *IEEE Latin America Transactions*

Youth unemployment and economic exclusion in Latin America represent persistent structural challenges aggravated by macroeconomic shocks and deeply rooted gender roles. Relying on static, multi-page tabular reports from institutional repositories limits the ability of policymakers and researchers to intuitively detect multidimensional patterns across time, geography, and gender. 

To overcome these constraints, this project develops a **Visual Analytics framework** backed by automated data pipelines and an interactive 4-page Power BI dashboard suite, exploring official ILOSTAT modelled estimates and household surveys covering **20 Latin American countries plus regional aggregates** over the period **2010–2026**.

---

## Repository Architecture

```text
youth-unemployment-latam-dataviz/
├── data/
│   ├── raw/                        # Product 2a: Original raw datasets extracted via ILOSTAT API
│   │   ├── 01_tasa_participacion_modelada_EAP_2WAP_SEX_AGE_RT.csv
│   │   ├── 02_relacion_empleo_poblacion_modelada_EMP_2WAP_SEX_AGE_RT.csv
│   │   ├── 03_tasa_desempleo_modelada_UNE_2EAP_SEX_AGE_RT.csv
│   │   ├── 04_tasa_neet_jovenes_modelada_EIP_2EET_SEX_RT.csv
│   │   ├── 05a_tasa_informalidad_modelada_sexo_EMP_2IFL_SEX_RT.csv
│   │   ├── 05b_tasa_informalidad_nacional_edad_EMP_NIFL_SEX_AGE_RT.csv
│   │   ├── 06_tasa_trabajadores_pobres_modelada_SDG_0111_SEX_AGE_RT.csv
│   │   ├── 07_desempleo_urbano_rural_UNE_DEAP_SEX_AGE_GEO_RT.csv
│   │   └── 08_neet_urbano_rural_EIP_NEET_SEX_GEO_RT.csv
│   │
│   └── processed/                  # Product 2b: Standardized and unified master datasets
│       ├── ilostat_latam_2010_2026_master_long.csv   # Long format (Tidy Data for dynamic filters)
│       └── ilostat_latam_2010_2026_master_wide.csv   # Wide format (Pivoted metrics for direct DAX/KPIs)
│
├── docs/
│   └── diccionario_de_datos.xlsx      # Product 3: Multi-sheet formal Data Dictionary & DAX catalog
│
├── notebooks/
│   └── 01_ETL_Limpieza_Unificacion_y_EDA.ipynb  # Documented 5-stage Python pipeline with pre-computed outputs
│
├── powerbi/
│   └── Dashboards_Desempleo_Juvenil_LATAM.pbix  # Product 5: 4-page Interactive Power BI solution
│
└── README.md                          # Repository documentation for peer reviewers and auditors
```

---

## Data Pipeline: 5 Methodological Stages

The entire data workflow is programmatically implemented in [`notebooks/01_ETL_Limpieza_Unificacion_y_EDA.ipynb`](notebooks/01_ETL_Limpieza_Unificacion_y_EDA.ipynb):

1. **Stage 1 (Automated Ingestion):** Direct API retrieval from the official ILOSTAT endpoint (`rplumber.ilo.org`) for 20 Latin American countries (`ARG`, `BOL`, `BRA`, `CHL`, `COL`, `CRI`, `CUB`, `DOM`, `ECU`, `SLV`, `GTM`, `HTI`, `HND`, `MEX`, `NIC`, `PAN`, `PRY`, `PER`, `URY`, `VEN`) and regional benchmark `X21` (2010–2026).
2. **Stage 2 (Standardization & Cleaning):** Homogenization of ISO-3 codes to English country names, standard sex labels (`Total`, `Male`, `Female`), age cohorts (`Youth (15-24)`, `Adults (25+)`, `Total (15+)`), and geographic domains (`National`, `Urban`, `Rural`). Filtering out out-of-range records and uninformative metadata.
3. **Stage 3 (Master Dataset Unification):** Construction of dual data representations:
   - **`master_long.csv` (23,891 records):** Ideal for dimensional modeling and Power BI multi-slicing.
   - **`master_wide.csv` (7,518 records):** Pivoted table facilitating column-to-column ratio calculations.
4. **Stage 4 (DAX Validation & Verification):** Python validation of critical derived KPIs ($\Delta_{\text{NEET}} = \text{NEET}_{\text{Female}} - \text{NEET}_{\text{Male}}$, $\text{Ratio}_{\text{UR}} = \text{UR}_{\text{Youth}} / \text{UR}_{\text{Adults}}$) ensuring complete consistency between analytical scripts and DAX measures.
5. **Stage 5 (Exploratory Data Analysis & Empirical Findings):** Computation of descriptive statistics and 8 empirical findings supporting the 4 dashboards.

---

## Traceability Matrix: Problems vs. Dashboards

| # | Problem Statement (Introduction) | Research Question | Target Dashboard | Core Metrics & KPIs |
|---|---|---|---|---|
| **P1** | **Macroeconomic Shock & Age Asymmetry:** Disproportionate youth vulnerability during recessions. | *How did the 2020 pandemic shock widen the youth-to-adult unemployment gap and how does it project toward 2026?* | **Dashboard 1:** Macroeconomic Evolution & Youth-to-Adult Unemployment Gap | `UR_Modelled`, `LFPR_Modelled`<br>**KPI:** Youth/Adult Ratio ($2.8\times$) |
| **P2** | **Hidden Exclusion & Gender Penalization:** Extreme concentration of young women in the NEET (NiNi) population. | *To what extent do unpaid care and domestic responsibilities drive gender disparities in youth NEET rates?* | **Dashboard 2:** Gender Disparities in the Youth NEET Population | `NEET_Youth_Modelled`<br>**KPI:** Absolute Gender Gap ($\Delta > 9.5\text{ pp}$) |
| **P3** | **Geographic Heterogeneity & Territorial Divide:** Subregional divergence and urban vs. rural barriers. | *What spatial concentration patterns and urban-rural divides characterize youth exclusion across Latin America?* | **Dashboard 3:** Geospatial Concentration & Urban-Rural Divides | `NEET_Urban_Rural`, `UR_Urban_Rural`<br>**KPI:** Territorial Dispersion Range |
| **P4** | **Employment Quality & In-Work Poverty:** Precarious informal jobs that fail to lift youth out of poverty. | *Does securing employment guarantee economic security, or does informality trap youth in working poverty?* | **Dashboard 4:** Informal Employment Trap & Working Poverty | `Informality_National`, `Working_Poverty_Modelled`<br>**KPI:** Youth Informality Rate ($>60\%$) |

---

## Summary of Empirical Findings (For Peer-Reviewed Paper)

* **Finding 1 (COVID-19 Shock Impact):** At the regional level (X21), youth unemployment jumped from $17.84\%$ in 2019 to a peak of $22.69\%$ in 2020 ($+4.85\text{ pp}$ in 12 months).
* **Finding 2 (Persistent Generational Gap):** Youth unemployment is systematically **$2.78\times$ higher** than adult unemployment during crises (2020) and is projected at $17.63\%$ toward 2026 ($2.75\times$ adult rate).
* **Finding 3 (Severe Gender Asymmetry in NEETs):** In 2020, female youth NEET rates reached $27.98\%$ vs. $18.39\%$ in males, establishing a regional gender gap of **$9.59\text{ pp}$**.
* **Finding 4 (Inertia Toward 2026 & Peru Case):** In Peru, the 2020 pandemic drove female NEET to **$29.37\%$** (vs. $22.00\%$ male). Regional 2026 projections estimate a persistent gap of $8.82\text{ pp}$ ($25.43\%$ female vs. $16.61\%$ male), showing that nearly $70\%$ of all regional NEETs are young women.
* **Finding 5 (Cross-Country Spatial Dispersion):** A spatial divide exceeding $20\text{ pp}$ exists between countries: Honduras ($31.62\%$) and Guatemala ($28.37\%$) exhibit the highest NEET vulnerability, compared to Uruguay ($14.86\%$).
* **Finding 6 (Rural Disadvantage):** Across regional household surveys, rural youth NEET rates consistently exceed urban rates, exacerbated by digital isolation and scarce secondary/technical education.
* **Finding 7 (Youth Informality Trap):** Informal employment among youth averages **$60.5\%$**, far outpacing adult informality ($45.2\%$), proving that 6 in 10 working youth lack legal protections or social safety nets.
* **Finding 8 (In-Work Poverty - SDG 1.1.1):** Working youth face an average working poverty rate ($<\$2.15$ PPP a day) of **$8.4\%$**, confirming that job insertion alone does not guarantee escaping socioeconomic vulnerability.

---

## Instructions for Execution & Reproducibility

### 1. Requirements
* Python 3.10 or higher (or [uv](https://github.com/astral-sh/uv) package manager).
* Power BI Desktop (for interacting with `.pbix` dashboards).

### 2. Environment Setup & Execution via `uv`
```bash
# Clone the repository
git clone https://github.com/<your-username>/youth-unemployment-latam-dataviz.git
cd youth-unemployment-latam-dataviz

# Run the master notebook with all dependencies
uv run --with jupyter --with pandas --with openpyxl --with nbconvert jupyter notebook notebooks/01_ETL_Limpieza_Unificacion_y_EDA.ipynb
```

### 3. Loading Data into Power BI Desktop
1. Open **Power BI Desktop**.
2. Select **Get Data $\rightarrow$ Text/CSV** and browse to:
   - `data/processed/ilostat_latam_2010_2026_master_long.csv` (Main fact table for slicing)
   - `data/processed/ilostat_latam_2010_2026_master_wide.csv` (Matrix table for direct column KPIs)
3. Connect visual dimensions (`Country`, `Year`, `Sex`, `Age_Group`, `Area_Type`) to your report pages.

---

## Citation & Academic License
If you utilize this dataset, notebook, or dashboard methodology in academic research, please cite:

```bibtex
@article{coronado2026waiting,
  title={The Waiting Generation: Spatiotemporal Visual Analytics and Gender Disparities in Latin American Youth Unemployment},
  author={Coronado Palacios, Juan Antonio and Cubas Quispe, Lucero Milagros and Quispe Bartolo, Carlos Martin and Solari Hip{\'o}lito, Maria Sofia},
  journal={Journal of Visualization (Submitted)},
  year={2026},
  publisher={Springer}
}
```

Distributed under the MIT License. Data originated and licensed under official ILO Open Data Terms.
