# Pulling from base docker image
FROM continuumio/anaconda3:2021.11

# Install apt packages
RUN apt-get update \
    && apt-get install -y \
    unzip \
    vim 

# Setting up filesystem
RUN mkdir -p /lab \
    && mkdir -p /lab/input \
    && mkdir -p /lab/output \
    && mkdir -p /lab/database \
    && mkdir -p /lab/build \
    && mkdir -p /lab/bin

# Building environments and inputting script
COPY ./lab.txt /lab/build
RUN conda create --name lab --file /lab/build/lab.txt \
    && conda init bash
RUN echo "conda activate" >> ~/.bashrc

# Adding scripts
COPY ./docker_lib/* /lab/bin/
RUN echo 'export PATH="/lab/bin:$PATH"' >> ~/.bashrc

# Setting up PHROGs database
WORKDIR /lab/build
COPY ./database/all_phrogs.hmm.gz /lab/build/ 
RUN gunzip all_phrogs.hmm.gz \
    && mv all_phrogs.hmm /opt/conda/envs/lab/db/hmm \
    && rm /opt/conda/envs/lab/db/hmm/*hmm.h*

#RUN wget http://warwick.s3.climb.ac.uk/ADM_share/all_phrogs.hmm.gz \
#    && gunzip all_phrogs.hmm.gz \
#    && mv all_phrogs.hmm /opt/conda/envs/lab/db/hmm \
#    && rm /opt/conda/envs/lab/db/hmm/*hmm.h*

# Copying index over
COPY ./database/PHROG_index.csv /lab/database/

# Setting entry
WORKDIR /lab
CMD [ "echo worklab" ]
