FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0.tar.gz --no-deps
# RUN python3 -c 'import nltk; nltk.download("punkt"); nltk.download("stopwords")'
EXPOSE 8001
CMD ["uvicorn", "keyword_fastapi:app", "--host=0.0.0.0", "--port=8001", "--reload"]