FROM python:3.10

# Oracle instant client
RUN apt-get update \

    && apt-get install -y unzip libaio1 libaio-dev wget git \
    && rm -rf /var/lib/apt/lists/*
RUN wget https://download.oracle.com/otn_software/linux/instantclient/218000/instantclient-basiclite-linux.x64-21.8.0.0.0dbru.zip \

    && mkdir /opt/oracle \
    && unzip instantclient-basiclite-linux.x64-21.8.0.0.0dbru.zip -d /opt/oracle \
    && rm instantclient-basiclite-linux.x64-21.8.0.0.0dbru.zip

ENV PATH="$PATH:/opt/oracle/instantclient_21_8"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/oracle/instantclient_21_8"

WORKDIR /app
COPY requirements.txt ./
# Install dependencies
RUN pip install -r requirements.txt

ENV HOME="/app"
RUN mkdir /app/.streamlit
RUN chgrp -R 0 /app/.streamlit && \

    chmod -R g=u /app/.streamlit 




# Copy the current directory contents into the container at /app
RUN ls -l
COPY pages images custom_funct.py Home_Page.py startup.sh ./
RUN ls -l /app


#Nasos
#WORKDIR /app
# COPY . /app
# EXPOSE 8501
# CMD ["streamlit", "run", "home_page.py"]


EXPOSE 8501
ENTRYPOINT ["sh", "startup.sh"]
