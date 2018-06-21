FROM python:3.6-slim

RUN apt-get update \
    && apt-get install -y bc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && pip install pipenv

ADD Pipfile* run_qwant.sh conftest.py /

WORKDIR /

RUN pipenv install --system --deploy

# the sources are copied as late as possible since they are likely to change often
ADD geocoder_tester/ /geocoder_tester/

ENV BRAGI_URL "http://bragi:4000/autocomplete"

CMD ["sh", "-c", "/run_qwant.sh /results ${BRAGI_URL}"]
