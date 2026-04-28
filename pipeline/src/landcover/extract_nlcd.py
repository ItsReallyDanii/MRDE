"""
MRDE EXP001 -- Phase 2E: NLCD Land Cover Extraction
Stage 2 Phase 2E

Supports:
1. Local Raster Mode: Samples NLCD 2021 class from a local GeoTIFF.
2. Online Mode: Blocked. Returns BLOCKED_FOR_NLCD_DOWNLOAD.

FORBIDDEN: no residuals, no ASOS alignment.
"""
import os

NLCD_STATIC_YEAR_CAVEAT = (
    "NLCD 2021 is a static dataset. It may not reflect land cover "
    "conditions during the EXP001 analysis window (2024-06-01 to 2024-08-30)."
)

NLCD_CLASSES = {
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


def query_nlcd_online(lat: float, lon: float) -> dict:
    """
    Returns blocked status as MRLC point APIs are restricted/unreliable.
    """
    return {
        "class_code": None,
        "class_label": None,
        "nodata": True,
        "error": "BLOCKED_FOR_NLCD_DOWNLOAD",
        "raster_crs": "Online endpoint unavailable",
        "input_lat": lat,
        "input_lon": lon,
    }


def sample_nlcd_class(
    lat: float,
    lon: float,
    raster_path: str = None,
    online: bool = False,
) -> dict:
    """
    Sample NLCD 2021 class at a WGS84 point.
    """
    if online:
        return query_nlcd_online(lat, lon)
        
    if not raster_path:
        return {
            "class_code": None,
            "class_label": None,
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
            "class_code": None,
            "class_label": None,
            "nodata": False,
            "error": f"Missing dependency: {exc}",
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }

    if not os.path.exists(raster_path):
        return {
            "class_code": None,
            "class_label": None,
            "nodata": False,
            "error": "NLCD raster not found. Provide path or use --online.",
            "raster_crs": None,
            "input_lat": lat,
            "input_lon": lon,
        }

    try:
        with rasterio.open(raster_path) as src:
            raster_crs = src.crs.to_string()
            nodata_val = src.nodata

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
                    "error": "Point outside NLCD raster extent.",
                    "raster_crs": raster_crs,
                    "input_lat": lat,
                    "input_lon": lon,
                }

            window = rasterio.windows.Window(col, row, 1, 1)
            data = src.read(1, window=window)
            pixel_val = int(data[0, 0])

            is_nodata = (nodata_val is not None and pixel_val == int(nodata_val)) or pixel_val == 0

            if is_nodata:
                return {
                    "class_code": None,
                    "class_label": None,
                    "nodata": True,
                    "error": "nodata pixel (or 0)",
                    "raster_crs": raster_crs,
                    "input_lat": lat,
                    "input_lon": lon,
                }

            label = NLCD_CLASSES.get(pixel_val, "Unknown Class")
            return {
                "class_code": pixel_val,
                "class_label": label,
                "nodata": False,
                "error": None,
                "raster_crs": raster_crs,
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
            "input_lat": lat,
            "input_lon": lon,
        }
