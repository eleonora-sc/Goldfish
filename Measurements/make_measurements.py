from ripe.atlas.cousteau import AtlasSource
# from ripe.atlas.sagan import SslResult

# Traceroute Measurements
source = AtlasSource(
    type="area",
    value="WW",
    requested=5,
    tags={"include":["system-ipv4-works"]}
)
source1 = AtlasSource(
    type="country",
    value="NL",
    requested=50,
    tags={"exclude": ["system-anchor"]}
)
