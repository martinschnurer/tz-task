FROM dokken/ubuntu-22.04
RUN apt update
RUN apt install unzip
RUN apt install -y python3.10 python3-pip

WORKDIR /task/src

# download data sources
RUN mkdir -p /task/tz-with-oceans && mkdir -p /task/tz-without-oceans 
RUN wget -P /task/tz-without-oceans http://efele.net/maps/tz/world/tz_world_mp.zip && cd /task/tz-without-oceans && unzip tz_world_mp.zip
RUN wget -P /task/tz-with-oceans https://github.com/evansiroky/timezone-boundary-builder/releases/download/2024a/timezones-with-oceans-now.shapefile.zip && cd /task/tz-with-oceans && unzip timezones-with-oceans-now.shapefile.zip


# Install python requirements
COPY requirements.txt /task/
RUN pip install -r /task/requirements.txt

# Copy app files & utils
COPY src/* /task/src/

EXPOSE 5000
CMD flask -A app run --host=0.0.0.0