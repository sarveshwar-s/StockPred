from python:3.5-slim
WORKDIR /code
ADD . /code
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
ENV NAME STOCKS
CMD ["python","test.py"]
