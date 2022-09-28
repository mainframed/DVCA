# This file automates the install for use with Docker

from pathlib import Path
import sys
from automvs import automation
import logging
import argparse
import os

cwd = os.getcwd()

USERJOB = ('''//TSO JOB (1),'ADD TSO USERS',CLASS=S,MSGLEVEL=(1,1),
//             MSGCLASS=A,
//             USER=IBMUSER,PASSWORD=SYS1
//RAKFCL  EXEC MVP,ACTION='UPDATE'
//RAKFCL  EXEC MVP,INSTALL='RAKFCL -D'
//TSOUSER EXEC TSONUSER,ID=DVCA,
//      PW='DVCA',
//      PR='IKJACCNT',
//      OP='NOOPER',
//      AC='NOACCT',
//      JC='JCL',
//      MT='NOMOUNT'
''')

RAKF_COMMANDS = ('''//RAKF JOB (1),'ADD TSO USERS',CLASS=S,MSGLEVEL=(1,1),
//             MSGCLASS=A,
//             USER=IBMUSER,PASSWORD=SYS1
//RAKFUPDT EXEC PGM=IKJEFT01,                  
//       REGION=8192K                                         
//TSOLIB   DD   DSN=BREXX.CURRENT.RXLIB,DISP=SHR                             
//RXLIB    DD   DSN=BREXX.CURRENT.RXLIB,DISP=SHR                             
//SYSEXEC  DD   DSN=SYS2.EXEC,DISP=SHR                         
//SYSPRINT DD   SYSOUT=*                                      
//SYSTSPRT DD   SYSOUT=*                                      
//SYSTSIN  DD   *
 RX ADDSD 'KICKS.* UACC(READ)'
 RX PERMIT 'KICKS.* ID(USER) ACCESS(UPDATE)'
 RX ADDUSER 'DVCA PASSWORD(DVCA) DFLTGRP(USER)'
//STDOUT   DD   SYSOUT=*,DCB=(RECFM=FB,LRECL=140,BLKSIZE=5600)
//STDERR   DD   SYSOUT=*,DCB=(RECFM=FB,LRECL=140,BLKSIZE=5600)
//STDIN    DD   DUMMY  
//EDITSTEP EXEC PGM=IKJEFT01,REGION=1024K,DYNAMNBR=50
//SYSPRINT DD  SYSOUT=*
//SYSTSPRT DD  SYSOUT=*
//SYSTERM  DD  SYSOUT=*
//SYSTSIN  DD  *
 EDIT 'SYS1.CMDPROC(STDLOGON)' CNTL OLD
 LIST
 INSERT IF &SYSUID EQ &STR(DVCA) THEN DO
 INSERT  EXEC 'SYS1.CMDPROC(DVCA)'        
 INSERT END    
 LIST
 SAVE
 END
/*
''')

desc = 'Automated DVCA Installer'
arg_parser = argparse.ArgumentParser(description=desc)
arg_parser.add_argument('-d', '--debug', help="Print debugging statements", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING)
arg_parser.add_argument('-m', '--mvsce', help="MVS/CE folder location", default="MVSCE")
args = arg_parser.parse_args()

builder = automation(mvsce=args.mvsce,loglevel=args.loglevel)
try:
    builder.ipl(clpa=False)
    builder.submit_and_check(USERJOB)
    builder.submit_and_check(RAKF_COMMANDS)
    with open("{}/release.jcl".format(cwd), "r") as injcl:
        builder.submit_and_check(injcl.read())

# except:
    # with open("/MVSCE/printers/prt00e.txt", "r") as prt:
    #    print(prt.read()) 
finally:
    builder.quit_hercules()
                            