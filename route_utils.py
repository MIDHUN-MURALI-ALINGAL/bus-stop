from database import db

cursor = db.cursor


def search_route(source, destination):

    cursor.execute("""

    SELECT

    buses.bus_name,

    buses.bus_number,

    routes.source,

    routes.destination,

    routes.fare,

    routes.travel_time

    FROM buses

    JOIN routes

    ON buses.id=routes.bus_id

    WHERE

    routes.source=?

    AND

    routes.destination=?

    """,(source,destination))

    return cursor.fetchall()