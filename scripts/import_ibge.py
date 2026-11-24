"""Import official IBGE census sectors GeoPackage or GeoJSON. Requires geopandas and shapely.
Usage: python scripts/import_ibge.py /path/to/official.gpkg --population-column v0001 --households-column v0002
The variable names are examples ONLY. Confirm against the IBGE data dictionary.
"""
import argparse,json,pathlib
import geopandas as gpd
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--population-column',required=True);p.add_argument('--households-column',required=True);p.add_argument('--municipality-prefix',default='');p.add_argument('--code-column',default='CD_SETOR');args=p.parse_args()
gdf=gpd.read_file(args.source)
for c in (args.population_column,args.households_column):
 if c not in gdf.columns:raise ValueError(f'Column {c} missing. Available: {list(gdf.columns)}')
if args.municipality_prefix:
 if args.code_column not in gdf.columns:raise ValueError('Missing sector code column')
 gdf=gdf[gdf[args.code_column].astype(str).str.startswith(tuple(args.municipality_prefix.split(',')))]
gdf=gdf.to_crs('EPSG:4326');gdf=gdf[gdf.geometry.notna()];gdf['population']=gdf[args.population_column].apply(lambda x:float(x) if str(x).replace('.','',1).isdigit() else None);gdf['households']=gdf[args.households_column].apply(lambda x:float(x) if str(x).replace('.','',1).isdigit() else None)
gdf=gdf[['population','households','geometry']];out=pathlib.Path(__file__).resolve().parents[1]/'data'/'sectors.geojson';out.write_text(gdf.to_json(),encoding='utf-8');print(f'{len(gdf)} sectors saved to {out}')
