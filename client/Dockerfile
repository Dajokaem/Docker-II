FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias necesarias
COPY ./app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo de configuración de Flask
COPY ./app .

# Expone el puerto de la aplicación Flask
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

