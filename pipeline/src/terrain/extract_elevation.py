"""
MRDE EXP001 — Phase 2E: Terrain Elevation Extraction
Stage 2 Phase 2E

Samples elevation (meters, AMSL) from a local GeoTIFF DEM (e.g. SRTM 1-arc-sec
or USGS 3DEP) at one or more WGS84 lat/lon points using rasterio.

Coordinate reprojection: WGS84 → raster native CRS performed automatically.

FORBIDDEN: no downloads, no residuals, no ASOS alignment.
"""
import os
from typing import Union

import numpy as np


def sample_elevation(
    lat: float,
    lon: float,
    raster_path: str,
) -> dict:
    """
    Sample elevation at a single WGS84 point from a local DEM GeoTIFF.

    Parameters
    ----------
    lat : float       WGS84 latitude (decimal degrees, positive = north)
    lon : float       WGS84 longitude (decimal degrees, negative = west)
    raster_path : str Absolute or relative path to the local DEM GeoTIFF.

    Returns
    -------
    dict with keys:
        elevation_m    : float | None  — sampled elevation in metres
        nodata         : bool          — True if the pixel is nodata
        error          : str | None    — error message if sampling failed
        raster_crs     : str           — EPSG string of the raster CRS
        input_lat      : float
        input_lon      : float
    """
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
                "Download a DEM (e.g. SRTM 1-arc-sec from https://earthexplorer.usgs.gov/ "
                "or USGS 3DEP via https://apps.nationalmap.gov/downloader/) "
                "and supply its path with --elevation-raster."
            ),
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }

    try:
        with rasterio.open(raster_path) as src:
            raster_crs = src.crs.to_string()
            nodata_val = src.nodata

            # Reproject WGS84 → raster CRS if needed
            wgs84 = CRS.from_epsg(4326)
            if src.crs.to_epsg() != 4326:
                transformer = Transformer.from_crs(wgs84, src.crs, always_xy=True)
                x, y = transformer.transform(lon, lat)
            else:
                x, y = lon, lat

            # Sample at the transformed point
            row, col = src.index(x, y)
            # Bounds check
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


def sample_elevations_batch(
    points: list[dict],
    raster_path: str,
) -> list[dict]:
    """
    Sample elevation for a list of {'label': str, 'lat': float, 'lon': float} dicts.
    Returns the input dicts extended with elevation result fields.
    """
    results = []
    for pt in points:
        result = sample_elevation(pt["lat"], pt["lon"], raster_path)
        results.append({**pt, **result})
    return results
