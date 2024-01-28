FROM python:3.9

RUN pip install pandas
RUN mkdir data

WORKDIR /app

COPY pipeline.py  pipeline.py

ENTRYPOINT ["bash"]