FROM python:3.8
RUN mkdir -p /test1/
WORKDIR /test1/
COPY . /test1/
CMD ["python","myfile.py"]

