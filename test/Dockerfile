FROM python:3.12

# install chrome for headless testing
RUN apt-get update && apt install -yqq \
                unzip \
                chromium \
                chromium-driver \
                dnsutils

ENV DISPLAY=:99
ENV chromedriver_path=/usr/bin/chromedriver

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "/usr/src/app/testapp.sh" ]
