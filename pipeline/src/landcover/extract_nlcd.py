"""
MRDE EXP001 — Phase 2E: NLCD 2021 Land Cover Extraction
Stage 2 Phase 2E

Samples NLCD 2021 class codes from a local NLCD GeoTIFF at one or more
WGS84 lat/lon points using rasterio.

NLCD caveat (static year): Data represents 2021 land cover and may not
reflect conditions present during the EXP001 window (2024-06-01 — 2024-08-30).

FORBIDDEN: no downloads, no residuals, no ASOS alignment.
"""
import os


# ---------------------------------------------------------------------------
# NLCD 2021 class code → label mapping (Anderson Level II)
# Source: https://www.mrlc.gov/data/legends/national-land-cover-database-class-legend-and-description
# ---------------------------------------------------------------------------
NLCD_2021_CLASSES: dict[int, str] = {
    11: "Open Water",
    12: "Perennial Ice/Snow",
    21: "Developed, Open Space",
    22: "Developed, Low Intensity",
    23: "Developed, Medium Intensity",
    24: "Developed, High Intensity",
    31: "Barren Land (Rock/Sand/Clay)",
    41: "Deciduous Forest",
    42: "Evergreen Forest",
    43: "Mixed Forest",
    51: "Dwarf Scrub",
    52: "Shrub/Scrub",
    71: "Grassland/Herbaceous",
    72: "Sedge/Herbaceous",
    73: "Lichens",
    74: "Moss",
    81: "Pasture/Hay",
    82: "Cultivated Crops",
    90: "Woody Wetlands",
    95: "Emergent Herbaceous Wetlands",
}

NLCD_STATIC_YEAR_CAVEAT = (
    "NLCD 2021 is a static dataset. It may not reflect land cover conditions "
    "during the EXP001 analysis window (2024-06-01 to 2024-08-30)."
)


def sample_nlcd_class(
    lat: float,
    lon: float,
    raster_path: str,
) -> dict:
    """
    Sample the NLCD 2021 class code at a single WGS84 point from a local
    NLCD GeoTIFF.

    Parameters
    ----------
    lat : float       WGS84 latitude (decimal degrees)
    lon : float       WGS84 longitude (decimal degrees)
    raster_path : str Path to the local NLCD 2021 GeoTIFF.

    Returns
    -------
    dict with keys:
        class_code  : int | None   — NLCD class code (e.g. 42 = Evergreen Forest)
        class_label : str | None   — human-readable class name
        nodata      : bool
        error       : str | None
        raster_crs  : str | None
        caveat      : str          — static-year caveat always included
        input_lat   : float
        input_lon   : float
    """
    try:
        import rasterio
        from rasterio.crs import CRS
        from pyproj import Transformer
    except ImportError as exc:
        return {
            "class_code": None,
            "class_label": None,
            "nodata": False,
            "error": f"Missing dependency: {exc}. Install rasterio and pyproj.",
            "raster_crs": None,
            "caveat": NLCD_STATIC_YEAR_CAVEAT,
            "input_lat": lat,
            "input_lon": lon,
        }

    if not os.path.exists(raster_path):
        return {
            "class_code": None,
            "class_label": None,
            "nodata": False,
            "error": (
                f"NLCD raster not found: {raster_path}\n"
                "Download NLCD 2021 from https://www.mrlc.gov/data "
                "and supply its path with --nlcd-raster."
            ),
            "raster_crs": None,
            "caveat": NLCD_STATIC_YEAR_CAVEAT,
            "input_lat": lat,
            "input_lon": lon,
        }

    try:
        with rasterio.open(raster_path) as src:
            raster_crs = src.crs.to_string()
            nodata_val = src.nodata

            # Reproject WGS84 → raster CRS (NLCD uses Albers Equal Area)
            wgs84 = CRS.from_epsg(4326)
            if src.crs.to_epsg() != 4326:
                transformer = Transformer.from_crs(wgs84, src.crs, always_xy=True)
                x, y = transformer.transform(lon, lat)
            else:
                x, y = lon, lat

            row, col = src.index(x, y)

            if row < 0 or row >= src.height or col < 0 or col >= src.width:
                return {
                    "class_code": None,
                    "class_label": None,
                    "nodata": True,
                    "error": (
                        f"Point ({lat}, {lon}) maps outside NLCD raster extent "
                        f"(row={row}, col={col}, height={src.height}, width={src.width})."
                    ),
                    "raster_crs": raster_crs,
                    "caveat": NLCD_STATIC_YEAR_CAVEAT,
                    "input_lat": lat,
                    "input_lon": lon,
                }

            window = rasterio.windows.Window(col, row, 1, 1)
            data = src.read(1, window=window)
            raw_val = int(data[0, 0])

            is_nodata = (nodata_val is not None) and (raw_val == int(nodata_val))

            if is_nodata:
                return {
                    "class_code": None,
                    "class_label": None,
                    "nodata": True,
                    "error": f"nodata pixel at ({lat}, {lon})",
                    "raster_crs": raster_crs,
                    "caveat": NLCD_STATIC_YEAR_CAVEAT,
                    "input_lat": lat,
                    "input_lon": lon,
                }

            label = NLCD_2021_CLASSES.get(raw_val, f"Unknown code {raw_val}")
            return {
                "class_code": raw_val,
                "class_label": label,
                "nodata": False,
                "error": None,
                "raster_crs": raster_crs,
                "caveat": NLCD_STATIC_YEAR_CAVEAT,
                "input_lat": lat,
                "input_lon": lon,
            }

    except Exception as exc:
        return {
            "class_code": None,
            "class_label": None,
            "nodata": False,
            "error": f"Rasterio read error: {exc}",
            "raster_crs": None,
            "caveat": NLCD_STATIC_YEAR_CAVEAT,
            "input_lat": lat,
            "input_lon": lon,
        }


def sample_nlcd_batch(
    points: list[dict],
    raster_path: str,
) -> list[dict]:
    """
    Sample NLCD class for a list of {'label': str, 'lat': float, 'lon': float} dicts.
    Returns the input dicts extended with NLCD result fields.
    """
    results = []
    for pt in points:
        result = sample_nlcd_class(pt["lat"], pt["lon"], raster_path)
        results.append({**pt, **result})
    return results
