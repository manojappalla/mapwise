import pandas as pd
import geopandas as gpd
from pathlib import Path
from mapwise.profiler import profile

DATA_PATH = Path(__file__).parent / "data" / "meteosat_fire_detections.csv"
df = pd.read_csv(DATA_PATH)

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE']),
    crs="EPSG:4326"
)

result = profile(gdf)

print("Geometry type:", result.geometry_type)
print("CRS EPSG:", result.crs_epsg)
print("Rows:", result.n_rows)
print("\nColumns:")
for col in result.columns:
    print(f"  {col.name} — {col.dtype_category} — nulls: {col.n_null}")

print("\nACQTIME sample:")
print(df['ACQTIME'].head())