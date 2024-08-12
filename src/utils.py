import shapefile
import shapely


def get_tree_and_geoms(shapefile_path):
    shapereader = shapefile.Reader(shapefile_path)
    geoms = []

    for shape_record in shapereader.shapeRecords():
        shape_type = shape_record.__geo_interface__["geometry"]["type"]

        if shape_type == "Polygon":
            polygon = shapely.Polygon(
                shape_record.__geo_interface__["geometry"]["coordinates"][0]
            )

            geoms.append((polygon, shape_record))

        elif shape_type == "MultiPolygon":
            polygons = [
                shapely.Polygon(shape[0])
                for shape in shape_record.__geo_interface__["geometry"]["coordinates"]
            ]

            multipolygon = shapely.MultiPolygon(
                polygons,
            )

            geoms.append((multipolygon, shape_record))

    tree = shapely.STRtree([pair[0] for pair in geoms])

    return tree, geoms
