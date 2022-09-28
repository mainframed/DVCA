FROM mainframed767/kicks:1.5.0 as builder
RUN unset LD_LIBRARY_PATH && apt-get update && apt-get install -yq git python3-pip
RUN pip3 install ebcdic requests
COPY ./ /workdir/
WORKDIR /workdir
RUN bash release.sh > PYTHON/release.jcl
WORKDIR /workdir/PYTHON
RUN git clone https://github.com/MVS-sysgen/automvs.git
RUN python3 -u docker.py -d -m /MVSCE

FROM mainframed767/kicks:1.5.0
COPY --from=builder /MVSCE /MVSCE
