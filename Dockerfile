FROM jfloff/alpine-python:2.7
RUN pip install requests
ADD ./slurp.py /slurp.py
CMD python /slurp.py

