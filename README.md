# PruebaTecnicaTS

# Video de presentacion

https://youtu.be/7RxvAmy7dAw

# Instalacion del backend

cd backend

# Ejecucion del backend (User Service)

cd backend
cd user_service
python -m venv venv  
.\venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Ejecucion del backend (Auth Service)

cd backend
cd auth_service
python -m venv venv  
.\venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload

# Instalacion del frontend

cd frontend

# Instala dependencias

npm install

# Ejecuta el frontend

npm run dev

# Ejecuta el api gateway

cd api_gateway
python -m venv venv  
.\venv\Scripts\Activate
uvicorn main:app --host 127.0.0.1 --port 8001 --reload

# Ejecuta el websocket service

cd websocket_service
go run main.go
