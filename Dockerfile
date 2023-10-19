FROM python:3.11.5
COPY . /
RUN pip install poetry
RUN cd content_service
RUN poetry update
RUN poetry install
EXPOSE 9000

CMD ["./wait-for-it.sh", "content-db:5432", "--", "poetry", "run", "uvicorn", "content_service.server:app", "--host", "0.0.0.0", "--port", "9000"]
