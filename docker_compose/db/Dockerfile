FROM postgres:13.12 
WORKDIR /db
ADD . /db
RUN echo "hello world"
RUN psql --version
# RUN psql -h localhost -U app -d movies_database -f movies_database.ddl
ENTRYPOINT ["sh", "settle_db.sh"]
# CMD ["psql -h 127.0.0.1 -U app -d movies_database -f movies_database.ddl"]
# RUN psql -h 127.0.0.1 -U app -d movies_database -f movies_database.ddl
# RUN psql 
# CMD ["python3", "load_data.py"] 
