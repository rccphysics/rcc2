def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def crad_to_varian_coords(vert, long, lat):
    vvert = round(-1*vert/10,1)
    vlong = round(long/10,1)
    if lat < 0:
        vlat = round((10000+lat)/10,1)
    else:
        vlat = round(lat/10,1)

    return (vvert, vlong, vlat)
