import httpx

# This is kind of hacky, but essentially the setting below is the default margin 
# we'll use to create bounding boxes around a lat/lon pair for USGS water data 
# queries.
USGS_BOUNDING_BOX_MARGIN = 0.2

# USGS NWIS web service parameter codes for water temperature and gage height.
USGS_PARAMETER_CODES = {
    "water_temperature": "00010"
}

# USGS NWIS web service site type for lakes.
USGS_SITE_TYPE_LAKE = "LK"

class USGSService:
    """Service to fetch water data from the USGS NWIS web service.

    Attributes:
        None
    
    Methods:
        create_bounding_box(lat: float, lon: float, margin: float = USGS_BOUNDING_BOX_MARGIN) -> str:
            Create a bounding box string for USGS NWIS web service queries.
        get_parameter_codes() -> str:
            Get the parameter codes for water data queries.
        get_usgs_data(lat: float, lon: float) -> dict:
            Fetch water data from the USGS NWIS web service for a given latitude and longitude.
    """

    def create_bounding_box(self, lat: float, lon: float, margin: float = USGS_BOUNDING_BOX_MARGIN) -> str:
        """Create a bounding box string for USGS NWIS web service queries."""
        
        # For now, this only supports lat/lon pairs in the US.
        west_bound = lon - margin
        south_bound = lat - margin
        east_bound = lon + margin
        north_bound = lat + margin

        return f"{west_bound:.7f},{south_bound:.7f},{east_bound:.7f},{north_bound:.7f}"
    
    def get_parameter_codes(self) -> dict:
        return ",".join(USGS_PARAMETER_CODES.values())            

    async def get_usgs_data(self, lat: float, lon: float) -> str:
        url = f"https://waterservices.usgs.gov/nwis/iv/"
        params = {
            "format": "json",
            "bBox": self.create_bounding_box(lat, lon),
            "parameterCd": self.get_parameter_codes(),
            "siteType": USGS_SITE_TYPE_LAKE,
            "siteStatus": "active",
        }
        headers = {
            "accept-encoding": "deflate, gzip"
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params=params, headers=headers)
                resp.raise_for_status()
                data = resp.json()
            except httpx.HTTPError as e:
                return {"error": str(e)}

            return data

try:
    usgs_service = USGSService()
except Exception:
    usgs_service = None
