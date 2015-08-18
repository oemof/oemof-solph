from sqlalchemy import (create_engine, Column, MetaData, Numeric, String,
                        Table)
from sqlalchemy.orm import mapper, sessionmaker
import keyring
from . import config as cfg
from .network.entities import components


def connection():
    engine = create_engine(
        "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}".format(
            user=cfg.get("postGIS", "username"),
            passwd=keyring.get_password(
                cfg.get("postGIS", "database"),
                cfg.get("postGIS", "username")),
            host=cfg.get("postGIS", "host"),
            db=cfg.get("postGIS", "database"),
            port=int(cfg.get("postGIS", "port"))))
    return engine.connect()


if __name__ == "__main__":
    print(connection())
#    coal = components.Bus(uid="Coal", type="coal")
#    power = components.Bus(uid="Power", type="electricity")

    # And example of how to connect to a PostgreSQL database
    engine = create_engine(
        "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}".format(
            user=cfg.get("postGIS", "username"),
            passwd=keyring.get_password(
                cfg.get("postGIS", "database"),
                cfg.get("postGIS", "username")),
            host=cfg.get("postGIS", "host"),
            db=cfg.get("postGIS", "database"),
            port=int(cfg.get("postGIS", "port"))))
    Session = sessionmaker(bind=engine)
    session = Session()

    # This example is for a spefic table from the "auswertung" database
    cpps = Table(
        "geo_power_plant_bnetza_2014", MetaData(schema="vn"),
        Column("bnetza_id", String(), primary_key=True),
        Column("inbetriebnahme", String()),
        Column("energietraeger", String()),
        Column("el_nennleistung",  Numeric(10, 1)))
    print(cpps)

    mapper(components.Transformer, cpps, properties={
        "uid": cpps.c.bnetza_id,
        "year": cpps.c.inbetriebnahme,
        "type": cpps.c.energietraeger,
        "eta_el": cpps.c.el_nennleistung
        })

    old_coal_plants = session.query(
        components.Transformer
        ).filter(
            components.Transformer.year < "1950"
            ).filter(
                components.Transformer.type.like("%kohle%")
                ).all()

    for ocp in old_coal_plants:
        print("Transformer => id: {0}, built: {1}, type: {2} Nel: {3}".format(
            ocp.uid, ocp.year, ocp.type, ocp.eta_el))

#    for ocp in old_coal_plants:
#        ocp.inputs = [coal]
#        ocp.outputs = [power]
