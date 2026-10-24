import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

# Set matplotlib style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#D1D5DB'
plt.rcParams['axes.linewidth'] = 0.8

base_dir = r'd:\USIL\7mo CICLO\VISUALIZACIÓN DE DATOS\trabajo final\youth-unemployment-latam-dataviz'
proc_dir = os.path.join(base_dir, 'data', 'processed')
pbi_dir = os.path.join(base_dir, 'powerbi')
os.makedirs(pbi_dir, exist_ok=True)

df_long = pd.read_csv(os.path.join(proc_dir, 'ilostat_latam_2010_2026_master_long.csv'))
df_wide = pd.read_csv(os.path.join(proc_dir, 'ilostat_latam_2010_2026_master_wide.csv'))

# Colors (Modern Power BI Palette)
NAVY = '#1E3A8A'
BLUE = '#3B82F6'
CORAL = '#EF4444'
TEAL = '#0D9488'
AMBER = '#F59E0B'
SLATE = '#475569'
BG_CARD = '#F8FAFC'
BORDER_CARD = '#E2E8F0'

def draw_kpi_card(ax, title, value, subtitle, accent_color=BLUE):
    ax.set_facecolor(BG_CARD)
    for spine in ax.spines.values():
        spine.set_color(BORDER_CARD)
        spine.set_linewidth(1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Accent bar on the left
    ax.axvline(x=0.02, ymin=0.15, ymax=0.85, color=accent_color, linewidth=5)
    
    ax.text(0.08, 0.72, title.upper(), fontsize=9, fontweight='bold', color=SLATE, transform=ax.transAxes)
    ax.text(0.08, 0.35, value, fontsize=22, fontweight='heavy', color='#0F172A', transform=ax.transAxes)
    ax.text(0.08, 0.12, subtitle, fontsize=8, color='#64748B', transform=ax.transAxes)

# ==============================================================================
# FIGURE 1: DASHBOARD 1 - MACROECONOMIC EVOLUTION
# ==============================================================================
print("Generating Figure 1: Dashboard 1...")
fig1 = plt.figure(figsize=(16, 9), facecolor='white', dpi=300)
fig1.suptitle('Dashboard 1: Macroeconomic Evolution & Youth-to-Adult Unemployment Gap (2010–2026)\nPower BI Visual Analytics Suite — Latin America and the Caribbean (X21)', 
              fontsize=14, fontweight='bold', color='#0F172A', y=0.97, ha='center')

gs1 = gridspec.GridSpec(3, 3, height_ratios=[0.22, 0.45, 0.33], hspace=0.38, wspace=0.25, left=0.06, right=0.96, top=0.90, bottom=0.06)

# KPI Cards
ax1_kpi1 = fig1.add_subplot(gs1[0, 0])
draw_kpi_card(ax1_kpi1, 'Youth Unemployment (15-24)', '17.63 %', 'Pico COVID-19 en 2020: 22.69 %', CORAL)

ax1_kpi2 = fig1.add_subplot(gs1[0, 1])
draw_kpi_card(ax1_kpi2, 'Adult Unemployment (25+)', '6.42 %', 'Pico COVID-19 en 2020: 8.16 %', BLUE)

ax1_kpi3 = fig1.add_subplot(gs1[0, 2])
draw_kpi_card(ax1_kpi3, 'Youth-to-Adult Gap Ratio', '2.75 x', 'Brecha Estructural Persistente', AMBER)

# Chart 1: Line chart time series
ax1_line = fig1.add_subplot(gs1[1, :2])
x21_ur = df_long[(df_long['ISO3'] == 'X21') & (df_long['Indicator_Short'] == 'UR_Modelled') & (df_long['Sex'] == 'Total')]
piv_ur = x21_ur.pivot_table(index='Year', columns='Age_Group', values='Value_Pct')

ax1_line.plot(piv_ur.index, piv_ur['Youth (15-24)'], marker='o', color=CORAL, linewidth=2.5, label='Youth (15-24) Rate')
ax1_line.plot(piv_ur.index, piv_ur['Adults (25+)'], marker='s', color=BLUE, linewidth=2.2, label='Adults (25+) Rate')
ax1_line.plot(piv_ur.index, piv_ur['Total (15+)'], linestyle='--', color=SLATE, linewidth=1.8, label='Total (15+) Benchmark')

# Annotate 2020 shock
ax1_line.annotate('Choque COVID-19 (2020)\nPico: 22.69 %', xy=(2020, 22.69), xytext=(2016, 23.5),
                 arrowprops=dict(facecolor=CORAL, shrink=0.05, width=1.5, headwidth=6),
                 fontsize=8.5, fontweight='bold', color=CORAL, bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor=CORAL))

ax1_line.set_title('Evolución y Proyección Temporal del Desempleo por Cohorte Etaria (2010–2026)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax1_line.set_ylabel('Tasa de Desempleo (%)', fontsize=9.5, color='#475569')
ax1_line.set_xlabel('Año', fontsize=9.5, color='#475569')
ax1_line.grid(True, linestyle=':', alpha=0.6)
ax1_line.legend(frameon=True, facecolor=BG_CARD, fontsize=8.5)

# Chart 2: Inter-annual variation bars
ax1_var = fig1.add_subplot(gs1[1, 2])
youth_diff = piv_ur['Youth (15-24)'].diff()
colors_bar = [CORAL if v > 0 else TEAL for v in youth_diff]
ax1_var.bar(youth_diff.index[1:], youth_diff.dropna(), color=colors_bar[1:], width=0.7)
ax1_var.axhline(0, color=SLATE, linewidth=0.8)
ax1_var.set_title('Variación Anual Tasa Juvenil (pp)', fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)
ax1_var.set_ylabel('Variación en pp', fontsize=9, color='#475569')
ax1_var.grid(True, linestyle=':', alpha=0.5)

# Chart 3: Country comparison (Focus countries)
ax1_countries = fig1.add_subplot(gs1[2, :])
sel_countries = ['ARG', 'BRA', 'CHL', 'COL', 'CRI', 'MEX', 'PER', 'URY', 'X21']
c_df = df_long[(df_long['ISO3'].isin(sel_countries)) & (df_long['Indicator_Short'] == 'UR_Modelled') & 
               (df_long['Sex'] == 'Total') & (df_long['Age_Group'] == 'Youth (15-24)') & (df_long['Year'] == 2022)].sort_values('Value_Pct')

bars = ax1_countries.barh(c_df['Country'], c_df['Value_Pct'], color=BLUE, height=0.65)
# Highlight Peru and X21
for bar, c in zip(bars, c_df['Country']):
    if c == 'Peru':
        bar.set_color(CORAL)
    elif 'Aggregate' in c:
        bar.set_color(AMBER)

ax1_countries.set_title('Comparativa de Desempleo Juvenil (15-24) por País (Año 2022 post-pandemia)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax1_countries.set_xlabel('Tasa de Desempleo Juvenil (%)', fontsize=9.5, color='#475569')
ax1_countries.grid(True, linestyle=':', alpha=0.5, axis='x')
for p in bars:
    w = p.get_width()
    ax1_countries.annotate(f"{w:.1f}%", (w + 0.3, p.get_y() + 0.18), fontsize=8.5, color='#1E293B')

fig1.savefig(os.path.join(pbi_dir, 'Figure1_Dashboard1_Macroeconomic_Evolution.png'), dpi=300)
plt.close(fig1)

# ==============================================================================
# FIGURE 2: DASHBOARD 2 - GENDER DISPARITIES IN NEET POPULATION
# ==============================================================================
print("Generating Figure 2: Dashboard 2...")
fig2 = plt.figure(figsize=(16, 9), facecolor='white', dpi=300)
fig2.suptitle('Dashboard 2: Gender Disparities in the Youth NEET Population (2010–2026)\nPower BI Visual Analytics Suite — Analysis of Female Vulnerability & Care Economy', 
              fontsize=14, fontweight='bold', color='#0F172A', y=0.97, ha='center')

gs2 = gridspec.GridSpec(3, 3, height_ratios=[0.22, 0.45, 0.33], hspace=0.38, wspace=0.25, left=0.06, right=0.96, top=0.90, bottom=0.06)

# KPI Cards
ax2_kpi1 = fig2.add_subplot(gs2[0, 0])
draw_kpi_card(ax2_kpi1, 'Female NEET Rate (Youth 15-24)', '25.43 %', 'Casi 7 de cada 10 NiNis son mujeres', '#D946EF')

ax2_kpi2 = fig2.add_subplot(gs2[0, 1])
draw_kpi_card(ax2_kpi2, 'Male NEET Rate (Youth 15-24)', '16.61 %', 'Proyección Regional 2026', BLUE)

ax2_kpi3 = fig2.add_subplot(gs2[0, 2])
draw_kpi_card(ax2_kpi3, 'Absolute Gender Gap', '+8.82 pp', 'Pico 2020: +9.59 pp (Choque de Cuidados)', CORAL)

# Chart 1: Small Multiples / Grouped Bar Comparison by Country (2022)
ax2_bar = fig2.add_subplot(gs2[1, :2])
neet_2022 = df_long[(df_long['Indicator_Short'] == 'NEET_Youth_Modelled') & (df_long['Year'] == 2022) & 
                    (df_long['Sex'].isin(['Female', 'Male'])) & (df_long['ISO3'] != 'X21')]
neet_piv = neet_2022.pivot_table(index='Country', columns='Sex', values='Value_Pct').sort_values('Female', ascending=False).head(12)

y_pos = np.arange(len(neet_piv))
h = 0.38
b_fem = ax2_bar.barh(y_pos - h/2, neet_piv['Female'], height=h, color='#D946EF', label='Female NEET Rate (%)')
b_mal = ax2_bar.barh(y_pos + h/2, neet_piv['Male'], height=h, color=BLUE, label='Male NEET Rate (%)')

ax2_bar.set_yticks(y_pos)
ax2_bar.set_yticklabels(neet_piv.index, fontsize=9)
ax2_bar.invert_yaxis()
ax2_bar.set_title('Brecha de Género en la Tasa NiNi (NEET) por País (Top 12 América Latina, 2022)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax2_bar.set_xlabel('Tasa NiNi / NEET (%)', fontsize=9.5, color='#475569')
ax2_bar.grid(True, linestyle=':', alpha=0.5, axis='x')
ax2_bar.legend(loc='lower right', frameon=True, facecolor=BG_CARD)

# Chart 2: Gender Gap Evolution over time
ax2_gap = fig2.add_subplot(gs2[1, 2])
neet_x21 = df_long[(df_long['ISO3'] == 'X21') & (df_long['Indicator_Short'] == 'NEET_Youth_Modelled')]
neet_x21_piv = neet_x21.pivot_table(index='Year', columns='Sex', values='Value_Pct')
gap_series = neet_x21_piv['Female'] - neet_x21_piv['Male']

ax2_gap.plot(gap_series.index, gap_series, marker='o', color=CORAL, linewidth=2.5)
ax2_gap.fill_between(gap_series.index, gap_series, color=CORAL, alpha=0.15)
ax2_gap.set_title('Evolución de la Brecha (Mujer - Hombre pp)', fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)
ax2_gap.set_ylabel('Brecha en pp', fontsize=9, color='#475569')
ax2_gap.grid(True, linestyle=':', alpha=0.5)

# Chart 3: Focus on Peru
ax2_peru = fig2.add_subplot(gs2[2, :])
per_neet = df_long[(df_long['ISO3'] == 'PER') & (df_long['Indicator_Short'] == 'NEET_Youth_Modelled')]
per_piv = per_neet.pivot_table(index='Year', columns='Sex', values='Value_Pct')

ax2_peru.plot(per_piv.index, per_piv['Female'], marker='o', color='#D946EF', linewidth=2.5, label='Perú: Mujeres Jóvenes')
ax2_peru.plot(per_piv.index, per_piv['Male'], marker='s', color=BLUE, linewidth=2.2, label='Perú: Hombres Jóvenes')
ax2_peru.plot(per_piv.index, per_piv['Total'], linestyle='--', color=SLATE, linewidth=1.8, label='Perú: Promedio Total')

ax2_peru.annotate('Pico 2020 en Mujeres: 29.37 %\nBrecha con Varones: +7.37 pp', xy=(2020, 29.37), xytext=(2015, 30.5),
                  arrowprops=dict(facecolor='#D946EF', shrink=0.05, width=1.5, headwidth=6),
                  fontsize=8.5, fontweight='bold', color='#D946EF', bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDF4FF', edgecolor='#D946EF'))

ax2_peru.set_title('Caso de Estudio Nacional: Dinámica de NiNis en el Perú por Género (2010–2026)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax2_peru.set_ylabel('Tasa NiNi (%)', fontsize=9.5, color='#475569')
ax2_peru.set_xlabel('Año', fontsize=9.5, color='#475569')
ax2_peru.grid(True, linestyle=':', alpha=0.6)
ax2_peru.legend(loc='lower left', frameon=True, facecolor=BG_CARD)

fig2.savefig(os.path.join(pbi_dir, 'Figure2_Dashboard2_Gender_Disparities_NEET.png'), dpi=300)
plt.close(fig2)

# ==============================================================================
# FIGURE 3: DASHBOARD 3 - GEOSPATIAL & TERRITORIAL DIVIDES
# ==============================================================================
print("Generating Figure 3: Dashboard 3...")
fig3 = plt.figure(figsize=(16, 9), facecolor='white', dpi=300)
fig3.suptitle('Dashboard 3: Geospatial Concentration & Urban-Rural Territorial Divides\nPower BI Visual Analytics Suite — Subregional Heterogeneity & Rural Penalty in Latin America', 
              fontsize=14, fontweight='bold', color='#0F172A', y=0.97, ha='center')

gs3 = gridspec.GridSpec(3, 3, height_ratios=[0.22, 0.45, 0.33], hspace=0.38, wspace=0.25, left=0.06, right=0.96, top=0.90, bottom=0.06)

# KPI Cards
ax3_kpi1 = fig3.add_subplot(gs3[0, 0])
draw_kpi_card(ax3_kpi1, 'Highest National NEET Rate', 'Honduras: 31.62 %', 'Vulnerabilidad Extrema (Triángulo Norte)', CORAL)

ax3_kpi2 = fig3.add_subplot(gs3[0, 1])
draw_kpi_card(ax3_kpi2, 'Lowest National NEET Rate', 'Uruguay: 14.86 %', 'Mayor Contención Social y Educativa', TEAL)

ax3_kpi3 = fig3.add_subplot(gs3[0, 2])
draw_kpi_card(ax3_kpi3, 'Territorial Dispersion', '16.76 pp', 'Disparidad Máx - Mín entre Naciones', AMBER)

# Chart 1: Heatmap style matrix of Subregions
ax3_heat = fig3.add_subplot(gs3[1, :2])
all_neet_22 = df_long[(df_long['Indicator_Short'] == 'NEET_Youth_Modelled') & (df_long['Year'] == 2022) & 
                      (df_long['Sex'] == 'Total') & (df_long['ISO3'] != 'X21')].sort_values('Value_Pct', ascending=True)

bar_colors = [TEAL if v < 20 else AMBER if v < 25 else CORAL for v in all_neet_22['Value_Pct']]
b_geo = ax3_heat.barh(all_neet_22['Country'], all_neet_22['Value_Pct'], color=bar_colors, height=0.7)
ax3_heat.set_title('Ranking y Semáforo de Riesgo Territorial NiNi en América Latina (2022)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax3_heat.set_xlabel('Tasa NiNi Total (%)', fontsize=9.5, color='#475569')
ax3_heat.grid(True, linestyle=':', alpha=0.5, axis='x')

# Labels on bars
for p in b_geo:
    w = p.get_width()
    ax3_heat.annotate(f"{w:.1f}%", (w + 0.3, p.get_y() + 0.15), fontsize=8, color='#1E293B')

# Chart 2: Legend / Risk clusters
ax3_clust = fig3.add_subplot(gs3[1, 2])
ax3_clust.set_facecolor(BG_CARD)
for spine in ax3_clust.spines.values():
    spine.set_color(BORDER_CARD)
ax3_clust.set_xticks([])
ax3_clust.set_yticks([])
ax3_clust.set_title('Clasificación por Nivel de Riesgo', fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)

ax3_clust.text(0.1, 0.75, '■ Riesgo Crítico (> 25 %)', fontsize=10, fontweight='bold', color=CORAL, transform=ax3_clust.transAxes)
ax3_clust.text(0.1, 0.63, 'Honduras, Guatemala, Colombia', fontsize=8.5, color=SLATE, transform=ax3_clust.transAxes)

ax3_clust.text(0.1, 0.45, '■ Riesgo Moderado (20% – 25%)', fontsize=10, fontweight='bold', color=AMBER, transform=ax3_clust.transAxes)
ax3_clust.text(0.1, 0.33, 'Perú, Brasil, Costa Rica, El Salvador', fontsize=8.5, color=SLATE, transform=ax3_clust.transAxes)

ax3_clust.text(0.1, 0.18, '■ Contención Relativa (< 20 %)', fontsize=10, fontweight='bold', color=TEAL, transform=ax3_clust.transAxes)
ax3_clust.text(0.1, 0.06, 'Uruguay, Chile, Argentina', fontsize=8.5, color=SLATE, transform=ax3_clust.transAxes)

# Chart 3: Urban vs Rural
ax3_ur = fig3.add_subplot(gs3[2, :])
urb_rur = df_long[(df_long['Indicator_Short'] == 'NEET_Urban_Rural') & (df_long['Sex'] == 'Total') & 
                  (df_long['Area_Type'].isin(['Urban', 'Rural']))].pivot_table(index=['Country', 'Year'], columns='Area_Type', values='Value_Pct').dropna().reset_index()

# Select top recent year per country
urb_rur_recent = urb_rur.sort_values('Year').groupby('Country').last().reset_index().head(8)
x_inds = np.arange(len(urb_rur_recent))
w_bar = 0.35

ax3_ur.bar(x_inds - w_bar/2, urb_rur_recent['Urban'], width=w_bar, color=BLUE, label='Área Urbana (%)')
ax3_ur.bar(x_inds + w_bar/2, urb_rur_recent['Rural'], width=w_bar, color=AMBER, label='Área Rural (%)')

ax3_ur.set_xticks(x_inds)
ax3_ur.set_xticklabels(urb_rur_recent['Country'], fontsize=9, rotation=15)
ax3_ur.set_title('Penalización Territorial: Desagregación Urbano vs Rural en NiNis (Encuestas de Hogares)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax3_ur.set_ylabel('Tasa NiNi (%)', fontsize=9.5, color='#475569')
ax3_ur.grid(True, linestyle=':', alpha=0.5, axis='y')
ax3_ur.legend(frameon=True, facecolor=BG_CARD)

fig3.savefig(os.path.join(pbi_dir, 'Figure3_Dashboard3_Geospatial_Territorial_Divides.png'), dpi=300)
plt.close(fig3)

# ==============================================================================
# FIGURE 4: DASHBOARD 4 - INFORMAL EMPLOYMENT & WORKING POVERTY
# ==============================================================================
print("Generating Figure 4: Dashboard 4...")
fig4 = plt.figure(figsize=(16, 9), facecolor='white', dpi=300)
fig4.suptitle('Dashboard 4: Informal Employment Trap & Working Poverty (ODS 1.1.1)\nPower BI Visual Analytics Suite — Precarious Labor & Economic Vulnerability in Youth', 
              fontsize=14, fontweight='bold', color='#0F172A', y=0.97, ha='center')

gs4 = gridspec.GridSpec(3, 3, height_ratios=[0.22, 0.45, 0.33], hspace=0.38, wspace=0.25, left=0.06, right=0.96, top=0.90, bottom=0.06)

# KPI Cards
ax4_kpi1 = fig4.add_subplot(gs4[0, 0])
draw_kpi_card(ax4_kpi1, 'Youth Informality Rate (15-24)', '60.50 %', '6 de cada 10 jóvenes ocupados son informales', CORAL)

ax4_kpi2 = fig4.add_subplot(gs4[0, 1])
draw_kpi_card(ax4_kpi2, 'Adult Informality Rate (25+)', '45.20 %', 'Brecha de Informalidad: +15.3 pp', BLUE)

ax4_kpi3 = fig4.add_subplot(gs4[0, 2])
draw_kpi_card(ax4_kpi3, 'Working Poverty Rate (<$2.15)', '8.40 %', 'Empleados en Extrema Pobreza (ODS 1.1.1)', AMBER)

# Chart 1: Informality by Age Cohort by Country
ax4_inf = fig4.add_subplot(gs4[1, :2])
inf_df = df_long[(df_long['Indicator_Short'] == 'Informality_National') & (df_long['Sex'] == 'Total') & 
                 (df_long['Area_Type'] == 'National')].pivot_table(index=['Country', 'Year'], columns='Age_Group', values='Value_Pct').dropna().reset_index()

inf_recent = inf_df.sort_values('Year').groupby('Country').last().reset_index().head(10).sort_values('Youth (15-24)', ascending=False)
y_inds = np.arange(len(inf_recent))
h_inf = 0.38

ax4_inf.barh(y_inds - h_inf/2, inf_recent['Youth (15-24)'], height=h_inf, color=CORAL, label='Jóvenes (15-24)')
ax4_inf.barh(y_inds + h_inf/2, inf_recent['Adults (25+)'], height=h_inf, color=BLUE, label='Adultos (25+)')

ax4_inf.set_yticks(y_inds)
ax4_inf.set_yticklabels(inf_recent['Country'], fontsize=9)
ax4_inf.invert_yaxis()
ax4_inf.set_title('Sobrerrepresentación Juvenil en el Empleo Informal por País', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax4_inf.set_xlabel('Tasa de Informalidad (%)', fontsize=9.5, color='#475569')
ax4_inf.grid(True, linestyle=':', alpha=0.5, axis='x')
ax4_inf.legend(loc='lower right', frameon=True, facecolor=BG_CARD)

# Chart 2: Scatter Plot Informality vs Working Poverty
ax4_scat = fig4.add_subplot(gs4[1, 2])
# Merge informality and poverty
pov_sub = df_long[(df_long['Indicator_Short'] == 'Working_Poverty_Modelled') & (df_long['Age_Group'] == 'Youth (15-24)') & (df_long['Sex'] == 'Total')]
inf_sub = df_long[(df_long['Indicator_Short'] == 'Informality_National') & (df_long['Age_Group'] == 'Youth (15-24)') & (df_long['Sex'] == 'Total')]

scat_merged = pd.merge(inf_sub[['Country', 'Year', 'Value_Pct']], pov_sub[['Country', 'Year', 'Value_Pct']], on=['Country', 'Year'], suffixes=('_Inf', '_Pov')).dropna()

ax4_scat.scatter(scat_merged['Value_Pct_Inf'], scat_merged['Value_Pct_Pov'], color=TEAL, alpha=0.7, edgecolors='white', s=55)
# Add trendline
if len(scat_merged) > 3:
    m, b = np.polyfit(scat_merged['Value_Pct_Inf'], scat_merged['Value_Pct_Pov'], 1)
    ax4_scat.plot(scat_merged['Value_Pct_Inf'], m*scat_merged['Value_Pct_Inf'] + b, color=CORAL, linestyle='--', label='Tendencia Lineal')

ax4_scat.set_title('Informalidad vs Trabajadores Pobres', fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)
ax4_scat.set_xlabel('Informalidad Juvenil (%)', fontsize=9, color='#475569')
ax4_scat.set_ylabel('Pobreza Laboral ODS 1.1.1 (%)', fontsize=9, color='#475569')
ax4_scat.grid(True, linestyle=':', alpha=0.5)
ax4_scat.legend(frameon=True, facecolor=BG_CARD, fontsize=8)

# Chart 3: Time Series of Working Poverty
ax4_pov_trend = fig4.add_subplot(gs4[2, :])
pov_x21 = df_long[(df_long['ISO3'] == 'X21') & (df_long['Indicator_Short'] == 'Working_Poverty_Modelled') & (df_long['Sex'] == 'Total')]
pov_piv = pov_x21.pivot_table(index='Year', columns='Age_Group', values='Value_Pct')

if not pov_piv.empty and 'Youth (15-24)' in pov_piv.columns:
    ax4_pov_trend.plot(pov_piv.index, pov_piv['Youth (15-24)'], marker='o', color=CORAL, linewidth=2.5, label='Jóvenes en Pobreza Laboral (<$2.15 PPP)')
    if 'Adults (25+)' in pov_piv.columns:
        ax4_pov_trend.plot(pov_piv.index, pov_piv['Adults (25+)'], marker='s', color=BLUE, linewidth=2.0, label='Adultos en Pobreza Laboral (<$2.15 PPP)')
    ax4_pov_trend.set_title('Evolución de la Tasa de Trabajadores Pobres en América Latina (2010–2026)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
    ax4_pov_trend.set_ylabel('Trabajadores Pobres (%)', fontsize=9.5, color='#475569')
    ax4_pov_trend.set_xlabel('Año', fontsize=9.5, color='#475569')
    ax4_pov_trend.grid(True, linestyle=':', alpha=0.6)
    ax4_pov_trend.legend(frameon=True, facecolor=BG_CARD)

fig4.savefig(os.path.join(pbi_dir, 'Figure4_Dashboard4_Informal_Trap_Working_Poverty.png'), dpi=300)
plt.close(fig4)

print("All 4 Dashboard figures generated successfully at 300 DPI!")
