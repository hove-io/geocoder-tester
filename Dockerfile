FROM python:3.6-slim

RUN pip install pipenv

ADD Pipfile* run_qwant.sh conftest.py /

WORKDIR /

RUN pipenv install --system --deploy

# the sources are copied as late as possible since they are likely to change often
ADD geocoder_tester/ /geocoder_tester/

CMD ["/run_qwant.sh", "/results", "http://bragi:4000/autocomplete"]
