# Usa una imagen ligera y estable
FROM python:3.12-slim  

# Establece el directorio de trabajo
WORKDIR /app  

# Copia solo los archivos necesarios
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# Copia el resto del código
COPY . .  

# Expone el puerto donde corre FastAPI
EXPOSE 8000  

# Usa Uvicorn para ejecutar FastAPI correctamente
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
