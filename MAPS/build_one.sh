# This script will build one MAP file on MVS3.8j KICKS
# syntax: bash build_one.sh <mapfile.bms> | ncat localhost 3505

cat << 'END'
//BUILDMAP JOB (JOB),
//             'BUILD A MAP',
//             CLASS=A,
//             MSGCLASS=A,
//             MSGLEVEL=(1,1),
//             USER=IBMUSER,
//             PASSWORD=SYS1,
//             REGION=7000K
//JOBPROC  DD DSN=KICKS.KICKSSYS.V1R5M0.PROCLIB,DISP=SHR 
END

m=${1%.*}
mapname=${m##*/}

cat << END
//* Adding $mapname
//$mapname EXEC KIKMAPS,MAPNAME=$mapname
//*$mapname EXEC KIKMAPS,MAPNAME=$mapname,PARM.ASM='DECK,LIST,OBJECT'
//COPY.SYSUT1 DD DATA,DLM=@@
END
    cat "$1"
    echo ""
    echo "@@"