from dataclasses import dataclass, field
from typing import Optional
import geopandas as gpd
import pandas as pd


@dataclass
class ColumnProfile:
    name: str
    dtype_category: str 
    n_null: int
    min_value: Optional[float] = None   
    max_value: Optional[float] = None
    mean_value: Optional[float] = None
    n_unique: Optional[int] = None      


@dataclass
class DataProfile:
    geometry_type: str        
    n_rows: int
    columns: list[ColumnProfile] 
    crs_epsg: Optional[int] = None


def profile(gdf: gpd.GeoDataFrame) -> DataProfile:
    # step 1: get geometry type from gdf.geom_type
    # step 2: get CRS epsg from gdf.crs
    # step 3: loop through columns, build a ColumnProfile for each
    # step 4: return a DataProfile
    unique_types = gdf.geom_type.unique()
    geometry_type = unique_types[0] if len(unique_types) == 1 else "Mixed"
    crs_epsg = gdf.crs.to_epsg() if gdf.crs else None
    columns = []

    for col in gdf.columns:
        if col == gdf.geometry.name:
            continue
        dtype = gdf[col].dtype
        
        if dtype.kind in 'iuf':
            dtype_category = 'numeric'
        elif dtype.kind == 'M':
            dtype_category = 'datetime'
        elif dtype.kind == 'b':
            dtype_category = 'boolean'
        else:
            dtype_category = 'categorical'
        n_null = gdf[col].isnull().sum()
        n_unique = gdf[col].nunique() if dtype_category == 'categorical' else None
        min_value = gdf[col].min() if pd.api.types.is_numeric_dtype(gdf[col]) else None
        max_value = gdf[col].max() if pd.api.types.is_numeric_dtype(gdf[col]) else None
        mean_value = gdf[col].mean() if pd.api.types.is_numeric_dtype(gdf[col]) else None

        column_profile = ColumnProfile(
            name=col,
            dtype_category=dtype_category,
            n_null=n_null,
            min_value=min_value,
            max_value=max_value,
            mean_value=mean_value,
            n_unique=n_unique
        )
        columns.append(column_profile)
    # step 4: return a DataProfile
    return DataProfile(
        geometry_type=geometry_type,
        n_rows=len(gdf),
        columns=columns,
        crs_epsg=crs_epsg
    )