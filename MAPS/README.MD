# CICS MAPS

This folder contains the CICS Basic Mapping Support (BMS) maps. Some were
auto generated from ANSI2BMS and others were made by hand to mirror the
ANSI art. As it stands now the CSGM transaction is set to display a DVCA
ascii art logo. To change it to the more authentic CICS logo move `CSGMMAP.bms`
to `CSGMMAP.DVCA` and move `CSGMMAP.CICS` to `CSGMMAP.bms` and rebuild the
CSGM map with `bash build_one.sh CSGMMAP.bms|ncat localhost 3505`.

## `build_one.sh`

This script will build one BMS file on MVS3.8J KICKS. 