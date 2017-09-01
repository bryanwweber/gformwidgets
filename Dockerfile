FROM jupyter/base-notebook

USER root

RUN conda config --add channels bryanwweber \
    && conda install -yq \
        thermostate \
        numpy \
        matplotlib \
        ipywidgets \
        pandas \
        gspread \
        oauth2client \
        bqplot \
        segno \
        && conda clean -tipsy

RUN cd /tmp \
    && mkdir -p expand-cell-fullscreen \
    && wget --quiet -O expand-cell-fullscreen/main.js https://raw.githubusercontent.com/scottlittle/expand-cell-fullscreen/master/main.js \
    && jupyter nbextension install expand-cell-fullscreen \
    && jupyter nbextension enable expand-cell-fullscreen/main


USER $NB_USER
