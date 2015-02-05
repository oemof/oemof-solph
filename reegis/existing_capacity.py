#!/usr/bin/python
# -*- coding: utf-8

import psycopg2

conn = psycopg2.connect(
    "host=192.168.10.105 dbname=reiners_db user=wittenberg password=luTHer")
cur = conn.cursor()
cur.execute('''
    ALTER TABLE wittenberg.ortsbezogene_daten drop COLUMN if exists pv_p_nenn;
    ALTER TABLE wittenberg.ortsbezogene_daten ADD COLUMN pv_p_nenn real;

    ALTER TABLE wittenberg.ortsbezogene_daten drop COLUMN if exists wea_p_nenn;
    ALTER TABLE wittenberg.ortsbezogene_daten ADD COLUMN wea_p_nenn real;

    ALTER TABLE wittenberg.ortsbezogene_daten drop COLUMN if exists was_p_nenn;
    ALTER TABLE wittenberg.ortsbezogene_daten ADD COLUMN was_p_nenn real;

    ALTER TABLE wittenberg.ortsbezogene_daten drop COLUMN if exists bio_p_nenn;
    ALTER TABLE wittenberg.ortsbezogene_daten ADD COLUMN bio_p_nenn real;

    ALTER TABLE wittenberg.ortsbezogene_daten drop COLUMN if exists all_p_nenn;
    ALTER TABLE wittenberg.ortsbezogene_daten ADD COLUMN all_p_nenn real;

    select stadtname from wittenberg.ortsbezogene_daten
''')
ortsnamen = ((cur.fetchall()))
for ort in ortsnamen:
    print ((ort[0]))
    # Determine existing pv power capacity
    cur.execute('''
    update wittenberg.ortsbezogene_daten set pv_p_nenn =
    (select sum(p_nenn_kwp)
        from deutschland.eeg_03_2013 as e, wittenberg.gemeinden as g
            where st_contains (g.the_geom , e.geom)
                and g.stadtname = %(name)s
                and e.anlagentyp = 'Solarstrom')
    where stadtname = %(name)s;
    ''', {'name': ort})

    # Determine existing wind power capacity
    cur.execute('''
    update wittenberg.ortsbezogene_daten set wea_p_nenn =
    (select sum(p_nenn_kwp)
        from deutschland.eeg_03_2013 as e, wittenberg.gemeinden as g
            where st_contains (g.the_geom , e.geom)
                and g.stadtname = %(name)s
                and e.anlagentyp = 'Windkraft')
    where stadtname = %(name)s;
    ''', {'name': ort})

    # Determine existing water power capacity
    cur.execute('''
    update wittenberg.ortsbezogene_daten set was_p_nenn =
    (select sum(p_nenn_kwp)
        from deutschland.eeg_03_2013 as e, wittenberg.gemeinden as g
            where st_contains (g.the_geom , e.geom)
                and g.stadtname = %(name)s
                and e.anlagentyp = 'Wasserkraft')
    where stadtname = %(name)s;
    ''', {'name': ort})

    # Determine existing bio power capacity
    cur.execute('''
    update wittenberg.ortsbezogene_daten set bio_p_nenn =
    (select sum(p_nenn_kwp)
        from deutschland.eeg_03_2013 as e, wittenberg.gemeinden as g
            where st_contains (g.the_geom , e.geom)
                and g.stadtname = %(name)s
                and (e.anlagentyp = 'Biomasse'
                    or e.anlagentyp = 'Gas'))
    where stadtname = %(name)s;
    ''', {'name': ort})

    # Determine existing capacity of all eeg-plants (control column)
    cur.execute('''
    update wittenberg.ortsbezogene_daten set all_p_nenn =
    (select sum(p_nenn_kwp)
        from deutschland.eeg_03_2013 as e, wittenberg.gemeinden as g
            where st_contains (g.the_geom , e.geom)
                and g.stadtname = %(name)s)
    where stadtname = %(name)s;
    ''', {'name': ort})

conn.commit()
cur.close()
conn.close()
