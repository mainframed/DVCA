#!/bin/bash

# Generates the JCL needed to build DVCA

cat << 'END'
//DVCA JOB (JOB),
//             'INSTALL DVCA',
//             CLASS=A,
//             MSGCLASS=A,
//             MSGLEVEL=(1,1),
//             USER=IBMUSER,
//             PASSWORD=SYS1,
//             REGION=7000K
//JOBPROC  DD DSN=KICKS.KICKSSYS.V1R5M0.PROCLIB,DISP=SHR 
END

for i in MAPS/*.bms; do
    m=${i%.*}
    mapname=${m##*/}

cat << END
//* Adding $mapname
//$mapname EXEC PGM=IEFBR14  
//$mapname EXEC KIKMAPS,MAPNAME=$mapname
//COPY.SYSUT1 DD DATA,DLM=@@
END
    cat "$i"
    echo ""
    echo "@@"
done



for i in COBOL/*; do
    m=${i%.*}
    progname=${m##*/}

cat << END   
//* Compiling $progname 
//* To show what step we're on
//$progname EXEC PGM=IEFBR14                                        
//*
//$progname EXEC K2KCOBCL                                     
//COPY.SYSUT1 DD DATA,DLM=@@
END

cat $i

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
done


for i in TABLES/*; do
    m=${i%.*}
    tablename=${m##*/}

# cat << END
# //* Adding $tablename
# //$tablename EXEC ASMFCL,MAC='SYS1.MACLIB',
# //      MAC1='KICKS.KICKSSYS.V1R5M0.MACLIB',
# //      PARM.ASM='DECK,NOLIST',PARM.LKED='XREF,MAP,LET,NCAL'
# //ASM.SYSIN DD DATA,DLM=@@
# END
cat << END
//$tablename EXEC PGM=IFOX00,
//            PARM='DECK,NOLIST'
//SYSLIB   DD DSN=SYS1.MACLIB,DISP=SHR
//         DD DSN=KICKS.KICKSSYS.V1R5M0.MACLIB,DISP=SHR
//SYSUT1   DD UNIT=SYSDA,SPACE=(CYL,(2,1))
//SYSUT2   DD UNIT=SYSDA,SPACE=(CYL,(2,1))
//SYSUT3   DD UNIT=SYSDA,SPACE=(CYL,(2,1))
//SYSPRINT DD SYSOUT=*
//SYSLIN   DD DUMMY
//SYSPUNCH DD DSN=&&OBJSET,
//         UNIT=SYSDA,SPACE=(80,(200,200)),
//         DISP=(,PASS)
//SYSIN    DD DATA,DLM=@@
END
    cat "$i"
    echo ""
    echo "@@"

cat << END
//LKED     EXEC PGM=IEWL,PARM='XREF,MAP,LET,NCAL',
//         COND=(0,NE,$tablename)
//SYSLIN   DD DSN=&&OBJSET,DISP=(OLD,DELETE)
//SYSIN    DD DUMMY
//SYSLMOD  DD DSN=KICKS.KICKSSYS.V1R5M0.SKIKLOAD($tablename),DISP=SHR
//SYSUT1   DD UNIT=SYSDA,SPACE=(CYL,(2,1))
//SYSPRINT DD SYSOUT=*
END
    # echo "//LKED.SYSLMOD DD DISP=SHR,"
    # echo "//    DSN=KICKS.KICKSSYS.V1R5M0.SKIKLOAD($tablename)"
done

cat << 'END'
//CLIST  EXEC PGM=PDSLOAD
//STEPLIB  DD  DSN=SYSC.LINKLIB,DISP=SHR
//SYSPRINT DD  SYSOUT=*
//SYSUT2   DD  DISP=SHR,DSN=SYS1.CMDPROC
//SYSUT1   DD DATA,DLM=@@
./ ADD NAME=DVCA
END

cat CLIST/DVCA

echo "@@"
# This generates the VSAM file for PRODUCTS
python3 PYTHON/generate_vsam.py

