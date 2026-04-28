"""
MRDE EXP001 -- Phase 2E: Terrain Elevation Extraction
Stage 2 Phase 2E

Supports:
1. Local Raster Mode: Samples elevation from a local DEM GeoTIFF.
2. Online Point-Query Mode: Queries the official USGS 3DEP EPQS.

FORBIDDEN: no downloads, no residuals, no ASOS alignment.
"""
import os
import urllib.request
import urllib.error
import json
from typing import Union


def query_elevation_online(lat: float, lon: float) -> dict:
    """
    Query the USGS 3DEP Elevation Point Query Service (EPQS).
    """
    url = f"https://epqs.nationalmap.gov/v1/json?x={lon}&y={lat}&units=Meters"
    req = urllib.request.Request(url, headers={"User-Agent": "MRDE-Phase2E-Agent"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            
        # The EPQS returns a 'value' string, or empty/error if outside US.
        if "value" in data and data["value"] is not None:
            elev_val = float(data["value"])
            # Nodata in EPQS is often returned as a very large negative or positive, 
            # but usually it's just missing. Let's assume typical nodata > -20000
            if elev_val < -20000:
                is_nodata = True
                elev_val = None
            else:
                is_nodata = False
                elev_val = round(elev_val, 2)
            
            return {
                "elevation_m": elev_val,
                "nodata": is_nodata,
                "error": "nodata from service" if is_nodata else None,
                "raster_crs": "EPSG:4326 (EPQS)",
                "input_lat": lat,
                "input_lon": lon,
            }
        else:
            return {
                "elevation_m": None,
                "nodata": True,
                "error": "EPQS returned no value",
                "raster_crs": "EPSG:4326",
                "input_lat": lat,
                "input_lon": lon,
            }
            
    except Exception as exc:
        return {
            "elevation_m": None,
            "nodata": False,
            "error": f"EPQS query error: {exc}",
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }


def sample_elevation(
    lat: float,
    lon: float,
    raster_path: str = None,
    online: bool = False,
) -> dict:
    """
    Sample elevation at a single WGS84 point.
    Dispatches to online API or local raster.
    """
    if online:
        return query_elevation_online(lat, lon)
        
    if not raster_path:
        return {
            "elevation_m": None,
            "nodata": False,
            "error": "Neither online=True nor raster_path provided.",
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }

    try:
        import rasterio
        from rasterio.crs import CRS
        from pyproj import Transformer
    except ImportError as exc:
        return {
            "elevation_m": None,
            "nodata": False,
            "error": f"Missing dependency: {exc}. Install rasterio and pyproj.",
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }

    if not os.path.exists(raster_path):
        return {
            "elevation_m": None,
            "nodata": False,
            "error": (
                f"Elevation raster not found: {raster_path}\n"
                "Provide a local raster path or use --online."
            ),
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }

    try:
        with rasterio.open(raster_path) as src:
            raster_crs = src.crs.to_string()
            nodata_val = src.nodata

            # Reproject WGS84 -> raster CRS if needed
            wgs84 = CRS.from_epsg(4326)
            if src.crs.to_epsg() != 4326:
                transformer = Transformer.from_crs(wgs84, src.crs, always_xy=True)
                x, y = transformer.transform(lon, lat)
            else:
                x, y = lon, lat

            # Sample at the transformed point
            row, col = src.index(x, y)
            if row < 0 or row >= src.height or col < 0 or col >= src.width:
                return {
                    "elevation_m": None,
                    "nodata": True,
                    "error": (
                        f"Point ({lat}, {lon}) maps outside raster extent "
                        f"(row={row}, col={col}, height={src.height}, width={src.width})."
                    ),
                    "raster_crs": raster_crs,
                    "input_lat": lat,
                    "input_lon": lon,
                }

            window = rasterio.windows.Window(col, row, 1, 1)
            data = src.read(1, window=window)
            pixel_val = float(data[0, 0])

            is_nodata = (nodata_val is not None) and (pixel_val == nodata_val)

            return {
                "elevation_m": None if is_nodata else round(pixel_val, 2),
                "nodata": is_nodata,
                "error": "nodata pixel" if is_nodata else None,
                "raster_crs": raster_crs,
                "input_lat": lat,
                "input_lon": lon,
            }

    except Exception as exc:
        return {
            "elevation_m": None,
            "nodata": False,
            "error": f"Rasterio read error: {exc}",
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }
