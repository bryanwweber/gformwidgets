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
        ipympl \
        && conda clean -tipsy

USER $NB_USER
