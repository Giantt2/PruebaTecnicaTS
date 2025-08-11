import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// Definicion del tipo de datos de usuario
type UserData = {
  id: number;
  name: string;
  email: string;
};

// Componente para la gestion de usuarios
function Users() {
  const [users, setUsers] = useState<UserData[]>([]);
  const navigate = useNavigate();

  // Se verifica si el usuario esta autenticado
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    getUsers();

    // Conexion al WebSocket
    const socket = new WebSocket("ws://127.0.0.1:8001/ws");
    socket.onmessage = (event) => {
      alert(`Mensaje del backend: ${event.data}`);
      getUsers();
    };
    return () => socket.close();
  }, []);

  // Función para obtener usuarios
  const getUsers = async () => {
    const token = localStorage.getItem("token");

    const res = await fetch("http://127.0.0.1:8001/users", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Si el token es invalido, se redirige al usuario al login
    if (res.status === 401) {
      navigate("/login");
      return;
    }

    const data = await res.json();
    setUsers(data.users);
  };

  // Función para crear un usuario
  const createUser = () => {
    const name = prompt("Nombre:");
    const email = prompt("Email:");
    const password = prompt("Contraseña:");

    if (!name || !email || !password) return;

    fetch("http://127.0.0.1:8001/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    }).then(() => getUsers());
  };

  // Función para editar un usuario
  const editUser = (user: UserData) => {
    const name = prompt("Nuevo nombre:", user.name);
    const email = prompt("Nuevo email:", user.email);
    const password = prompt("Nueva contraseña:", "");

    if (!name || !email || !password) return;

    // Se consigue el token para la autenticacion persistente
    const token = localStorage.getItem("token");
    // Se envia la peticion de edicion
    fetch(`http://127.0.0.1:8001/users/${user.id}`, {
      method: "PUT",
      // Se verifica el token antes de enviar la peticion
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name, email, password }),
    }).then(() => getUsers());
  };

  // Función para eliminar un usuario
  const deleteUser = async (id: number) => {
    // Se consigue el token para la autenticacion persistente
    const token = localStorage.getItem("token");
    // Se envia la peticion de eliminacion
    await fetch(`http://127.0.0.1:8001/users/${id}`, {
      method: "DELETE",
      headers: {
        // Se verifica el token antes de enviar la peticion
        Authorization: `Bearer ${token}`,
      },
    });
    getUsers();
  };

  // Función para cerrar sesion
  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="flex flex-col items-center p-4">
      <header className="flex justify-between items-center m-4">
        <h1 className="font-bold text-3xl">Lista de Usuarios</h1>
      </header>
      <button
        onClick={logout}
        className="bg-red-500 text-white px-4 py-2 rounded"
      >
        Cerrar sesión
      </button>
      <button
        className="m-2 bg-green-500 text-white px-3 py-1 rounded"
        onClick={createUser}
      >
        Añadir Usuario
      </button>
      <table className="table-auto w-full border">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id} className="text-center">
              <td className="border px-4 py-2">{user.id}</td>
              <td className="border px-4 py-2">{user.name}</td>
              <td className="border px-4 py-2">{user.email}</td>
              <td className="border px-4 py-2">
                <button
                  className="mr-2 bg-yellow-500 text-white px-2 py-1 rounded"
                  onClick={() => editUser(user)}
                >
                  Editar
                </button>
                <button
                  className="ml-2 bg-red-500 text-white px-2 py-1 rounded"
                  onClick={() => deleteUser(user.id)}
                >
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

export default Users;
