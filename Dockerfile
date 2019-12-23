# Dockerfile

# A python runtime base image
FROM python:3.7.5-buster

# pip
RUN pip install --upgrade pip

# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY requirements.txt /app/

# Specific COPY
COPY src/ /app/

# Port
EXPOSE 8050

# Create mountpoint
VOLUME /app/images

# ENTRYPOINT
ENTRYPOINT ["python"]

# CMD sets default arguments to executable which may be overwritten when using docker run
CMD ["/app/src/main.py"]