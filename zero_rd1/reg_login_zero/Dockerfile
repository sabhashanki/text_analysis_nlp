FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "reg_login_zero:app", "--host=0.0.0.0", "--port=8001", "--reload"]
