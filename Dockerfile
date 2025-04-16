FROM rockylinux:9

RUN dnf update -y && dnf install -y python3.12 python3.12-pip

COPY . /flask-todo-app/

WORKDIR /flask-todo-app

RUN pip3.12 install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]