from flask import Flask, jsonify, request
import zoneinfo
import shapely
from .utils import get_tree_and_geoms

app = Flask(__name__)


tree_without_oceans, geoms_without_oceans = get_tree_and_geoms(
    "../tz-without-oceans/world/tz_world_mp.shp"
)
tree_with_oceans, geoms_with_oceans = get_tree_and_geoms(
    "../tz-with-oceans/combined-shapefile-with-oceans-now.shp"
)


def find_timezone(obj):
    lat = float(obj["lat"])
    lon = float(obj["lon"])

    point = shapely.Point(lon, lat)

    indices = tree_without_oceans.query(point, predicate="within")

    if len(indices):
        pair = geoms_without_oceans[indices[0]]
        shape_record = pair[1]

        return jsonify({"tzid": shape_record.record.TZID})
    else:
        indices = tree_with_oceans.query(point, predicate="within")

        if len(indices):
            pair = geoms_with_oceans[indices[0]]
            shape_record = pair[1]

            return jsonify({"tzid": shape_record.record.tzid})
        else:
            return jsonify({"tzid": None, "error": True})


@app.route("/timezones")
def timezones():

    if "lat" in request.args and "lon" in request.args:
        return find_timezone(request.args)

    exclude_tz = ["build/etc/localtime", "localtime"]

    zones = sorted(
        [zone for zone in zoneinfo.available_timezones() if zone not in exclude_tz]
    )

    return jsonify(zones)
