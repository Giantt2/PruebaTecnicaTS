import { useEffect, useState } from "react";
import "./App.css";

// Se crea UserData para definir la estructura de los usuarios
type UserData = {
  id: number;
  name: string;
  email: string;
};

function App() {
  // Se crea el arreglo de usuarios
  const [users, setUsers] = useState<UserData[]>([]);

  // Se hace la peticion para obtener los usuarios al cargar la aplicacion
  useEffect(() => {
    getUsers();
  }, []);

  // Se conecta al websocket
  useEffect(() => {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws");

    socket.onmessage = (event) => {
      const message = event.data;
      console.log("Mensaje del backend: ", message);
      alert(`Mensaje del backend: ${message}`);
      getUsers();
    };

    return () => {
      socket.close();
    };
  }, []);

  // Se hace la peticion para obtener los usuarios de la base de datos
  const getUsers = async () => {
    const response = await fetch("http://127.0.0.1:8000/users");
    const results = await response.json();
    setUsers(results.users);
  };

  // Peticion para crear un usuario en la base de datos
  const createUser = () => {
    const name = prompt("Nombre:");
    const email = prompt("Email:");
    const password = prompt("Contraseña:");

    if (!name || !email || !password) return;

    fetch("http://127.0.0.1:8000/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    }).then(() => getUsers());
  };

  // Peticion para eliminar un usuario de la base de datos
  const deleteUser = async (id: number) => {
    await fetch(`http://127.0.0.1:8000/users/${id}`, {
      method: "DELETE",
    });
    getUsers();
  };

  // Peticion para editar un usuario en la base de datos
  const editUser = (user: UserData) => {
    const name = prompt("Nuevo nombre:", user.name);
    const email = prompt("Nuevo email:", user.email);
    const password = prompt("Nueva contraseña:", "");

    if (!name || !email || !password) return;

    // Se hace la peticion para actualizar el usuario
    fetch(`http://127.0.0.1:8000/users/${user.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    }).then(() => getUsers());
  };

  // Se renderiza la tabla y botones
  return (
    <div>
      <header className="font-bold text-5xl m-2">Lista de Usuarios</header>
      <button className="m-2" onClick={createUser}>
        Añadir Usuario
      </button>

      <table className="table-auto w-full">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td className="border px-4 py-2">{user.id}</td>
              <td className="border px-4 py-2">{user.name}</td>
              <td className="border px-4 py-2">{user.email}</td>
              <td className="border px-4 py-2">
                <button className="mr-2" onClick={() => editUser(user)}>
                  Editar
                </button>
                <button className="ml-2" onClick={() => deleteUser(user.id)}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
