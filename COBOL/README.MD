# COBOL

This folder contains all the COBOL programs which drives the logic
behind DVCA. Each program itself has a comment in the top which describes
what the program does and what vulnerbilities (if any) it has. 

To compile/link any of these on MVS3.8J you can use the following
script:

```bash
# This script will build one COBOL file on MVS3.8j KICKS
# syntax: bash cobol_one.sh <mapfile.bms> | ncat localhost 3505

cat << 'END'
//COMPCOB JOB (JOB),
//             'COMPILE COBOL',
//             CLASS=A,
//             MSGCLASS=A,
//             MSGLEVEL=(1,1),
//             USER=IBMUSER,
//             PASSWORD=SYS1,
//             REGION=7000K
//JOBPROC  DD DSN=KICKS.KICKSSYS.V1R5M0.PROCLIB,DISP=SHR 
END

m=${1%.*}
progname=${m##*/}

cat << END   
//* Compiling $progname                                         
//$progname EXEC K2KCOBCL                                  
//COPY.SYSUT1 DD DATA,DLM=@@
END

cat $1

cat << END
@@
//COB1.STEPLIB  DD DSN=SYSC.LINKLIB,DISP=SHR
//COB2.STEPLIB  DD DSN=SYSC.LINKLIB,DISP=SHR   
//LKED.SYSLIB   DD DISP=SHR,DSN=SYSC.COBLIB
//LKED.SYSIN DD *
 INCLUDE SKIKLOAD(KIKCOBGL)
 ENTRY $progname
 NAME  $progname(R)
/*
END
```