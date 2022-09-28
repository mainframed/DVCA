#!/usr/bin/env python3

# This script builds the KSDS VSAM 'databases' JCL used by DVCA. 
# Syntax: python3 generate_vsam.py
# If this script isn't being used as part of a larger JCL script
# You can run it as a one off with:
#   python3 generate_vsam.py J
#
# License GPL3
# Author Philip Young
#

import random
import sys
import datetime


JOBCARD = '''//VSMFILES JOB (BAL),
//             'MELS CARGO VSAM',
//             CLASS=A,
//             MSGCLASS=A,
//             TIME=1440,
//             MSGLEVEL=(1,1),
//             USER=IBMUSER,PASSWORD=SYS1'''

JCL = '''//*
//* The KICKS programs STKCARD is used to make the data for ADDRESS
//* It is a C program, the first argument is the number of cards i.e. 
//* Lines. The second argument is the length of each line, default 80. 
//* 
//ADDRESS  EXEC PGM=STKCARDS,PARM='6'
//STEPLIB  DD DSN=KICKS.KICKSSYS.V1R5M0.SKIKLOAD,DISP=SHR
//SYSTERM  DD SYSOUT=*,DCB=BLKSIZE=120
//SYSPRINT DD DSN=&REPROIN,DISP=(,PASS),UNIT=SYSDA,
//         SPACE=(CYL,(1,1)),DCB=(RECFM=FB,LRECL=268,BLKSIZE=2000)
//SYSIN    DD *,DCB=BLKSIZE=80
0001Philip Young                                100 Adelaide St W               
            Toronto                                     Ontario                 
                    M5H 0B3                                     Canada          

/*
//MCCAMS EXEC PGM=IDCAMS
//SYSPRINT DD   SYSOUT=*
//PRODUCTS  DD *
{office_supplies}
99999 N 0000000000000000000000000000000000 999999.99 999999.99 Control Record
/*
//HISTORY  DD *
{history_office_supplies}
99999 99/99/99 0000000000000000000000000000000000 $999,999.99 $999,999.99
/*
//ADDRESS DD DSN=&REPROIN,DISP=(OLD,DELETE)
//SYSIN    DD *
 DELETE KICKS.DVCA.PRODUCTS.VSAM CLUSTER PURGE
 DELETE KICKS.DVCA.HISTORY.VSAM CLUSTER PURGE
 DELETE KICKS.DVCA.ADDRESS.VSAM CLUSTER PURGE
 /* IF THERE WAS NO DATASET TO DELETE, RESET CC           */
 IF LASTCC = 8 THEN
   DO
       SET LASTCC = 0
       SET MAXCC = 0
   END
 /* Create PRODUCTS VSAM Key based */
 DEFINE CLUSTER (                        -
        NAME( KICKS.DVCA.PRODUCTS.VSAM ) -
        VOLUME( KICKS0 )                 -
        INDEXED                          -
        KEYS( 5,0 )                      -
        RECORDSIZE ( 80,80 )             -
        RECORDS( 500 )                   -
        UNIQUE                           -
        )                                -
        DATA ( NAME(KICKS.DVCA.PRODUCTS.VSAM.DATA)) -
        INDEX ( NAME(KICKS.DVCA.PRODUCTS.VSAM.INDEX))

 /* Create HISTORY VSAM Key based */
 DEFINE CLUSTER (                        -
        NAME( KICKS.DVCA.HISTORY.VSAM )  -
        VOLUME( KICKS0 )                 -
        INDEXED                          -
        KEYS( 5,0 )                      -
        RECORDSIZE ( 80,80 )             -
        RECORDS( 500 )                   -
        UNIQUE                           -
        )                                -
        DATA ( NAME(KICKS.DVCA.HISTORY.VSAM.DATA)) -
        INDEX ( NAME(KICKS.DVCA.HISTORY.VSAM.INDEX))

 /* Create ADDRESS VSAM Key based */
 DEFINE CLUSTER (                        -
        NAME( KICKS.DVCA.ADDRESS.VSAM ) -
        VOLUME( KICKS0 )                 -
        INDEXED                          -
        KEYS( 4,0 )                      -
        RECORDSIZE ( 268,268 )           -
        RECORDS( 2 )                     -
        UNIQUE                           -
        )                                -
        DATA ( NAME(KICKS.DVCA.ADDRESS.VSAM.DATA)) -
        INDEX ( NAME(KICKS.DVCA.ADDRESS.VSAM.INDEX))

 /* PUT THE DATA IN THE FILE */
 IF LASTCC=0 THEN                    -
     REPRO INFILE(PRODUCTS)           -
     OUTDATASET(KICKS.DVCA.PRODUCTS.VSAM)
 IF LASTCC=0 THEN                    -
     REPRO INFILE(HISTORY)           -
     OUTDATASET(KICKS.DVCA.HISTORY.VSAM)
 IF LASTCC=0 THEN                    -
     REPRO INFILE(ADDRESS)           -
     OUTDATASET(KICKS.DVCA.ADDRESS.VSAM)
 IF LASTCC=0 THEN                    -
     LISTCAT ALL ENTRY(KICKS.DVCA.PRODUCTS.VSAM)
 IF LASTCC=0 THEN                    -
     LISTCAT ALL ENTRY(KICKS.DVCA.HISTORY.VSAM)
 IF LASTCC=0 THEN                    -
     LISTCAT ALL ENTRY(KICKS.DVCA.ADDRESS.VSAM)
/*
'''


stuff = '''Printer paper
Three-hole punched paper
Dom Perignon Rose 1959
24K Gold Macbook Pro
Tracing paper
Carbon paper
Color card stock
Heavy-duty card stock
Wrapping paper
Greeting cards and envelopes
Business cards
Letterhead
Poster board
Legal envelopes
Manila mailing envelopes
Padded legal envelope mailers
Mailing labels
Return address labels
Postage scale
Postage stamps
Envelope sealer
Packaging bubble
Cardboard boxes (small, medium, large)
Composition notebooks
Spiral-bound notebooks
Legal pads
Steno pads
Notepads
Planners
Binders
Binder tabs
Binder pockets
Binder dividers
Binder labels
Binder sheet reinforcements
Clear binder document holders
Hole puncher
Three-hole puncher
Tape gun
Duct tape
Twine
Sticky notes (small, medium, large)
Bookmark sticky flags (small, medium, large)
Bookmarks
White glue
Rubber cement
Tacky wall mount gum
Hanging hooks
Magnifying glass
Ink pads
Correction fluid
Wall calendar
Desk calendar
Dry/Wet erase board
Dry/Wet erase markers
Dry/Wet erase spray
Bookends
Paperweight
Magazine holders
Bulletin board
Pushpins
Letter opener
Pen holder
Printer
Toner or print cartridges
Telephone
Speakerphone
Headset
Calculator
Postage meter
Projection device
Photocopier
Digital camera
Lamps
Lightbulbs
Label maker
Laminating machine
Scanner
Fax machine'''

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2022, 10, 15)
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days


if len(sys.argv) > 1 and sys.argv[1] == "J":
    print(JOBCARD)

office_supplies = []
key = 1
record = "{key:05d} Y {name:<34.34} {price:>09.2f} {shipping:>09.2f}"
for supply in stuff.split('\n'):
    office_supplies.append(
        record.format(
            key=key,
            name=supply,
            price=random.uniform(100, 999),
            shipping=random.uniform(000000.00, 99.99),
            )
        )
    key += 1
    #print(office_supplies[-1])

office_supplies[2] = "00003 N Dom Perignon Rose 1959             084700.00 000250.00 DO NOT BUY"
office_supplies[3] = "00004 Y 24K Gold Macbook Pro               022178.01 000165.48 OVER BUDGET"
office_supplies[4] = "00005 N Ancient Golden Idol                000568.01 000246.96 HAUNTED"


x = 1
history = []
for i in random.choices(office_supplies,k=5):
   p = "${:>10,.2f}".format(float(i[43:52].lstrip("0")))
   s = "${:>10,.2f}".format(float(i[53:62].lstrip("0")))

   random_number_of_days = random.randrange(days_between_dates)
   random_date = start_date + datetime.timedelta(days=random_number_of_days)
   history.append("{key:05d} {rand_date}{therest}{p} {s}".format(rand_date=random_date.strftime('%m/%d/%y'),key=x,therest=i[7:43],p=p,s=s))
   x += 1

print(JCL.format(
        office_supplies='\n'.join(office_supplies),
        history_office_supplies = '\n'.join(history)
        )
    )