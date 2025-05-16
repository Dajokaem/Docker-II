#Imagen oficial de PostgreSql
FROM postgres:13

#Copiar el archivo SQL al contenedor
COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432