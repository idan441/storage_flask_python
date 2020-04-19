FROM alpine

RUN apk update
RUN apk add python3 
RUN apk add py3-setuptools

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

RUN adduser --disabled-password storage_user && addgroup storage
RUN chown -R storage_user:storage /app
RUN chown -R storage_user:storage * 
USER storage_user

#Install the application, put here the admin user details: python3 setup.py <username> <display_name> <password>
RUN python3 setup.py admin MyName 1234
EXPOSE 5000 

ENTRYPOINT ["python3"]
CMD ["main.py"]