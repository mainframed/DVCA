# Damn Vulnerable CICS Application (DVCA)

Welcome to the Damn Vulnerable CICS application. This is a z/OS CICS (and
MVS 3.8j KICKS) application that is just loaded with vulnerabilities. 

This repo contains the source code for running DVCA on MVS/CE KICKS.

## Running DVCA

A Docker container of the most recent release is available at https://hub.docker.com/r/mainframed767/dvca.

Once you've deployed the container, logon with the user `DVCA` and a password
of `DVCA`. This will automatically launch KICKS and DVCA for you. If you're not
using the container and installed manually run the command `DVCA` after logon.

![CSGM](screenshots/CSGM.png?raw=true "CSGM")

At the CSGM screen press `F3` or `CLEAR` to clear the screen and enter `MCGM`
to access the vulnerable application. 

![MCGM](screenshots/MCGM.png?raw=true "MCGM")

Be sure to be using a tool like BIRP to be able to find the vulnerabilities. Strongly recommend you watch this talk: 
https://www.youtube.com/watch?v=Qakj82DoKME

## Building From Source

1) Download and build MVS/CE:
2) Follow the instructions to install KICKS: https://www.jaymoseley.com/hercules/kicks/index.htm
3) Run the `release.sh` script and send the results to the MVS/CE card reader:
`bash release.sh|ncat localhost 3505`
