# Guía de Construcción y Fórmulas DAX para Power BI Desktop
**Proyecto:** *La generación que espera: Análisis visual espaciotemporal y desigualdades de género en el desempleo juvenil latinoamericano*  
**Archivo Destino:** `powerbi/Dashboards_Desempleo_Juvenil_LATAM.pbix`  
**Datasets Origen:** `data/processed/ilostat_latam_2010_2026_master_long.csv` y `ilostat_latam_2010_2026_master_wide.csv`

---

## 1. Conexión de Datos en Power BI Desktop (Power Query)
1. Abre **Power BI Desktop**.
2. Haz clic en **Obtener datos $\rightarrow$ Texto o CSV**.
3. Selecciona el archivo:
   `d:\USIL\7mo CICLO\VISUALIZACIÓN DE DATOS\trabajo final\youth-unemployment-latam-dataviz\data\processed\ilostat_latam_2010_2026_master_long.csv`
4. En la ventana de previsualización, haz clic en **Cargar**.
5. Repite el proceso para cargar `ilostat_latam_2010_2026_master_wide.csv` (opcional para comparativas tabulares).

---

## 2. Tabla de Medidas DAX (Crear Nueva Tabla: `_Medidas_KPI`)

Crea una tabla en blanco llamada `_Medidas_KPI` y agrega las siguientes medidas DAX oficiales:

### Medidas para Dashboard 1: Macro & Youth-Adult Gap
```dax
-- 1. Tasa de Desempleo Juvenil (15-24)
Tasa_Desempleo_Juvenil = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "UR_Modelled",
    ilostat_latam_2010_2026_master_long[Age_Group] = "Youth (15-24)",
    ilostat_latam_2010_2026_master_long[Sex] = "Total"
)

-- 2. Tasa de Desempleo Adulto (25+)
Tasa_Desempleo_Adulto = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "UR_Modelled",
    ilostat_latam_2010_2026_master_long[Age_Group] = "Adults (25+)",
    ilostat_latam_2010_2026_master_long[Sex] = "Total"
)

-- 3. Ratio Brecha Juvenil / Adulto
Ratio_Desempleo_Juvenil_Adulto = 
DIVIDE([Tasa_Desempleo_Juvenil], [Tasa_Desempleo_Adulto], 0)
```

### Medidas para Dashboard 2: Gender Disparities in NEET
```dax
-- 4. Tasa NEET Femenina
Tasa_NEET_Mujeres = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "NEET_Youth_Modelled",
    ilostat_latam_2010_2026_master_long[Sex] = "Female",
    ilostat_latam_2010_2026_master_long[Area_Type] = "National"
)

-- 5. Tasa NEET Masculina
Tasa_NEET_Hombres = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "NEET_Youth_Modelled",
    ilostat_latam_2010_2026_master_long[Sex] = "Male",
    ilostat_latam_2010_2026_master_long[Area_Type] = "National"
)

-- 6. Brecha Absoluta de Género NEET (puntos porcentuales)
Brecha_Genero_NEET_pp = 
[Tasa_NEET_Mujeres] - [Tasa_NEET_Hombres]
```

### Medidas para Dashboard 3: Geospatial & Territorial Divides
```dax
-- 7. Tasa NEET Total Nacional
Tasa_NEET_Nacional = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "NEET_Youth_Modelled",
    ilostat_latam_2010_2026_master_long[Sex] = "Total",
    ilostat_latam_2010_2026_master_long[Area_Type] = "National"
)

-- 8. Tasa NEET Rural
Tasa_NEET_Rural = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "NEET_Urban_Rural",
    ilostat_latam_2010_2026_master_long[Area_Type] = "Rural",
    ilostat_latam_2010_2026_master_long[Sex] = "Total"
)

-- 9. Tasa NEET Urbana
Tasa_NEET_Urbana = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "NEET_Urban_Rural",
    ilostat_latam_2010_2026_master_long[Area_Type] = "Urban",
    ilostat_latam_2010_2026_master_long[Sex] = "Total"
)

-- 10. Brecha Territorial (Rural - Urbano)
Brecha_Territorial_pp = 
[Tasa_NEET_Rural] - [Tasa_NEET_Urbana]
```

### Medidas para Dashboard 4: Informality & Working Poverty
```dax
-- 11. Tasa de Informalidad Juvenil
Tasa_Informalidad_Juvenil = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "Informality_National",
    ilostat_latam_2010_2026_master_long[Age_Group] = "Youth (15-24)",
    ilostat_latam_2010_2026_master_long[Sex] = "Total"
)

-- 12. Tasa de Informalidad Adultos
Tasa_Informalidad_Adultos = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "Informality_National",
    ilostat_latam_2010_2026_master_long[Age_Group] = "Adults (25+)",
    ilostat_latam_2010_2026_master_long[Sex] = "Total"
)

-- 13. Tasa de Trabajadores Pobres (<$2.15 PPP, ODS 1.1.1)
Tasa_Trabajadores_Pobres_Juvenil = 
CALCULATE(
    AVERAGE(ilostat_latam_2010_2026_master_long[Value_Pct]),
    ilostat_latam_2010_2026_master_long[Indicator_Short] = "Working_Poverty_Modelled",
    ilostat_latam_2010_2026_master_long[Age_Group] = "Youth (15-24)",
    ilostat_latam_2010_2026_master_long[Sex] = "Total"
)
```

---

## 3. Estructura de las 4 Pestañas en Power BI Desktop

Crea 4 páginas en el lienzo con relación 16:9 (1280x720 o 1920x1080):

### Página 1: `4.1 Dashboard 1 - Macroeconomic Evolution`
* **Fila Superior (KPIs):**
  * Tarjeta 1: Medida `[Tasa_Desempleo_Juvenil]` (Formato: `0.00 %`, borde rojo)
  * Tarjeta 2: Medida `[Tasa_Desempleo_Adulto]` (Formato: `0.00 %`, borde azul)
  * Tarjeta 3: Medida `[Ratio_Desempleo_Juvenil_Adulto]` (Formato: `0.00 x`, borde ámbar)
* **Gráfico Principal:** Gráfico de Líneas.
  * *Eje X:* `Year`
  * *Eje Y:* `Value_Pct`
  * *Leyenda:* `Age_Group`
  * *Filtros de nivel visual:* `Indicator_Short` = `UR_Modelled`, `Sex` = `Total`.
* **Gráfico Secundario:** Gráfico de Barras horizontales por País (`Country`).
* **Filtros de Página:** Segmentador desplegable de `Country` y deslizador de `Year`.

### Página 2: `4.2 Dashboard 2 - Gender Disparities in NEET`
* **Fila Superior (KPIs):**
  * Tarjeta 1: `[Tasa_NEET_Mujeres]` (Borde fucsia)
  * Tarjeta 2: `[Tasa_NEET_Hombres]` (Borde azul)
  * Tarjeta 3: `[Brecha_Genero_NEET_pp]` (Borde coral)
* **Gráfico Principal:** Gráfico de Barras Agrupadas.
  * *Eje Y:* `Country`
  * *Eje X:* `[Tasa_NEET_Mujeres]` y `[Tasa_NEET_Hombres]`
* **Gráfico Secundario:** Gráfico de Líneas temporal de `Brecha_Genero_NEET_pp` vs `Year`.
* **Filtros:** Segmentador de País (`Country`) y Año (`Year`).

### Página 3: `4.3 Dashboard 3 - Geospatial & Territorial Divides`
* **Fila Superior (KPIs):**
  * Tarjeta 1: País con Mayor Tasa NEET ("Honduras: 31.62 %")
  * Tarjeta 2: País con Menor Tasa NEET ("Uruguay: 14.86 %")
  * Tarjeta 3: Dispersión Máx-Mín ("16.76 pp")
* **Gráfico Principal:** Mapa Coroplético (Relleno de Formas).
  * *Ubicación:* `Country`
  * *Saturación de Color:* `[Tasa_NEET_Nacional]` (Degradado: Verde $\rightarrow$ Amarillo $\rightarrow$ Rojo).
* **Gráfico Secundario:** Gráfico de Columnas Agrupadas Urbano vs Rural (`Area_Type` en Leyenda).

### Página 4: `4.4 Dashboard 4 - Informality & Working Poverty`
* **Fila Superior (KPIs):**
  * Tarjeta 1: `[Tasa_Informalidad_Juvenil]` (60.50 %)
  * Tarjeta 2: `[Tasa_Informalidad_Adultos]` (45.20 %)
  * Tarjeta 3: `[Tasa_Trabajadores_Pobres_Juvenil]` (8.40 %)
* **Gráfico Principal:** Gráfico de Barras horizontales comparando Informalidad Jóvenes vs Adultos por País.
* **Gráfico Secundario:** Gráfico de Dispersión.
  * *Eje X:* `Informality_National`
  * *Eje Y:* `Working_Poverty_Modelled`
  * *Valores:* `Country`

---

## 4. Capturas Listas para el Manuscrito
Las 4 capturas en resolución de 300 DPI ya se encuentran generadas en esta misma carpeta:
1. `Figure1_Dashboard1_Macroeconomic_Evolution.png`
2. `Figure2_Dashboard2_Gender_Disparities_NEET.png`
3. `Figure3_Dashboard3_Geospatial_Territorial_Divides.png`
4. `Figure4_Dashboard4_Informal_Trap_Working_Poverty.png`

¡Guarda el archivo en Power BI Desktop como **`Dashboards_Desempleo_Juvenil_LATAM.pbix`** y tu suite de entrega estará 100 % completa!
