FROM python:3.13.2
WORKDIR /myloginFastAPI
COPY ./requirements.txt /myloginFastAPI/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /myloginFastAPI/requirements.txt
COPY . /myloginFastAPI
CMD ["fastapi", "run", "./main.py", "--port", "80"]