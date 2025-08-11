package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

// --- Variables Globales ---

// Mapa para guardar las conexiones
var clients = make(map[*websocket.Conn]bool)

var mutex = &sync.Mutex{}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

// --- (Handlers) ---

// handleConnections se encarga de las nuevas conexiones de WebSocket.
func handleConnections(w http.ResponseWriter, r *http.Request) {
	// La conexion http se convierte a websocket
	connection, error := upgrader.Upgrade(w, r, nil)
	if error != nil {
		log.Printf("Error al actualizar conexión: %v", error)
		return
	}
	// Se cierra la conexion cuando se termina la funcion
	defer connection.Close()

	// Logica de registro
	mutex.Lock()
	clients[connection] = true
	mutex.Unlock()
	log.Println("Un nuevo cliente se ha conectado.")

	// Bucle infinito para mantener la conexión viva
	for {
		// Si se detecta la desconexion del cliente, se cierra la conexion
		if _, _, error := connection.ReadMessage(); error != nil {
			log.Printf("Cliente desconectado: %v", error)
			break
		}
	}

	// Logica para eliminar un cliente desconectado
	mutex.Lock()
	delete(clients, connection)
	mutex.Unlock()
	log.Println("Cliente eliminado del registro.")
}

// Funcion que recibe una petición http y envía el mensaje a todos los clientes
func handleBroadcast(w http.ResponseWriter, r *http.Request) {
	var msg struct {
		Message string `json:"message"`
	}

	// Se lee el json del body de la peticion
	if error := json.NewDecoder(r.Body).Decode(&msg); error != nil {
		http.Error(w, "Cuerpo del mensaje invalido", http.StatusBadRequest)
		return
	}

	log.Printf("Mensaje recibido para broadcast: %s", msg.Message)

	// Logica para enviar el mensaje a todos
	mutex.Lock()
	defer mutex.Unlock()

	// Se recorre cada cliente del mapa
	for client := range clients {
		// Se intenta enviar mensaje al cliente
		error := client.WriteMessage(websocket.TextMessage, []byte(msg.Message))
		if error != nil {
			log.Printf("Error al enviar mensaje a un cliente: %v", error)
			// Si hay un error, se cierra y elimina el cliente
			client.Close()
			delete(clients, client)
		}
	}

	w.Write([]byte("Mensaje enviado a los clientes."))
}

func main() {
	// Endpoint para que los clientes se conecten
	http.HandleFunc("/ws", handleConnections)

	// Endpoint para que el backend envie notificaciones
	http.HandleFunc("/broadcast", handleBroadcast)

	// Iniciamos el servidor.
	log.Println("Servidor de WebSocket (versión simple) iniciado en http://127.0.0.1:8081")
	if error := http.ListenAndServe(":8081", nil); error != nil {
		log.Fatalf("Error al iniciar servidor: %v", error)
	}
}
