# KICKS Tables

This folder contains the tables needed to be able to run the programs.
Unlike CICS, KICKS uses hard coded tables. 

`KIKFCT1$` is the File Control Table. It lists the names of allocated datasets
(allocated in the DVCA CLIST) and makes them available to the COBOL programs.

`KIKPCT1$` is the Program Control Table. It tells KICKS which transaction 
ID (i.e. MCGM) should be mapped to which COBOL program.

`KIKPPT1$` is the Processing Program Table. This defines the programs
and their CICS maps.

To see the changes/additions made by DVCA go to the bottom of the file
until you see 

```
*        M""""""'YMM M""MMMMM""M MM'""""'YMM MMP"""""""MM 
*        M  mmmm. `M M  MMMMM  M M' .mmm. `M M' .mmmm  MM 
*        M  MMMMM  M M  MMMMP  M M  MMMMMooM M         `M 
*        M  MMMMM  M M  MMMM' .M M  MMMMMMMM M  MMMMM  MM 
*        M  MMMM' .M M  MMP' .MM M. `MMM' .M M  MMMMM  MM 
*        M       .MM M     .dMMM MM.     .dM M  MMMMM  MM 
*        MMMMMMMMMMM MMMMMMMMMMM MMMMMMMMMMM MMMMMMMMMMMM 
```

