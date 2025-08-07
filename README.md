# PruebaTecnicaTS

# Video de presentacion

https://youtu.be/7RxvAmy7dAw

# Instalacion del backend

cd backend

# Crea un entorno virtual

python -m venv env
env\Scripts\activate

# Instala dependencias

pip install fastapi uvicorn

# Ejecucion del backend

uvicorn app.main:app --reload

# Instalacion del frontend

cd frontend

# Instala dependencias

npm install

# Ejecuta el frontend

npm run dev
