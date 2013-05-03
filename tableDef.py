#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ruzickao
#
# Created:     30.04.2013
# Copyright:   (c) ruzickao 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

tabledef={
    "obce":{
        "field":{
            "obi_kod":{"dbtype":"integer","notNull":"yes","pkey":"yes"},
            "obi_nazev":{"dbtype":"text"},
            "obi_status_kod":{"dbtype":"integer"},
            "oki_kod":{"dbtype":"integer"},
            "pui_kod":{"dbtype":"integer"},
            "obi_plati_od":{"dbtype":"date"},
            "obi_plati_do":{"dbtype":"date"},
            "obi_id_transakce":{"dbtype:bigint"},
            "obi_globalni_id_navrhu_zmeny":{"dbtype":"bigint"},
            "obi_vlajka_text":{"dbtype":"text"},
            "obi_znak_text":{"dbtype":"text"},
            "obi_nuts_lau":{"dbtype":"text"},
            "obi_definicni_bod":{"dbtype":"text"},
            "obi_originalni_hranice":{"dbtype":"text"}
            },
        "index":{"obi_nazev":{"idxtype":"btree","cluster":"yes"}}
        }
    }
print (tabledef)