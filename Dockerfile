FROM ubuntu:18.04
ENV container docker
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y libgl1-mesa-glx libgl1-mesa-dri && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
    add-apt-repository -y ppa:oibaf/graphics-drivers


RUN export TZ=Europe/Berlin    # must be at beginning for unknown reasons,
RUN apt-get install tzdata     # must be at beginning for unknown reasons,


RUN apt-get install -y xauth
RUN apt-get install -y libgtk-3-dev pkg-config apt-utils
RUN apt-get install -y git curl unzip tar
RUN apt-get install -y wget git

RUN apt install -y python3-pip python3-dev
RUN pip3 install numpy
RUN pip3 install opencv-python
RUN pip3 install psutil

RUN ln -s /usr/bin/python3 /usr/bin/python
ENV TANGO_HOST=ictrlfs.ictrl.frm2:10000
ENV QT_X11_NO_MITSHM=1
RUN echo "deb [trusted=yes] https://forge.frm2.tum.de/repos bionic/" >>/etc/apt/sources.list.d/mlz.list
RUN apt-get update

RUN echo "tango-common tango-common/tango-host string ${TANGO_HOST}" |  debconf-set-selections
RUN echo 'tango-db tango-db/dbconfig-install boolean false' |  debconf-set-selections
RUN apt-get install -y python3-pytango

RUN adduser --quiet --disabled-password -u 1000 qtuser

# Install Python 3, PyQt5
RUN apt-get update \
    && apt-get install -y \
      python3 \
      python3-pyqt5

RUN git clone https://forge.frm2.tum.de/review/frm2/tango/apps/quango.git \
    && cd quango && python3 setup.py install

RUN mkdir quangoplus
COPY . /quangoplus/

CMD ["python3", "/quangoplus/bin/quango+.py"]
