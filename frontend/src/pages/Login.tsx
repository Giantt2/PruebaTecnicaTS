import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

// Componente para el inicio de sesion
function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Al cargar la pagina de login se elimina cualquier token antiguo
  useEffect(() => {
    localStorage.removeItem("token");
  }, []);

  // Funcion para manejar el inicio de sesion
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Se crea un FormData para enviar los datos del formulario
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    // Se realiza la peticion al backend
    try {
      const res = await fetch("http://127.0.0.1:8001/token", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        setError("Credenciales incorrectas");
        return;
      }

      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      navigate("/");
    } catch {
      setError("Error de conexion");
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen flex items-center justify-center">
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded shadow-md w-80"
      >
        <h2 className="text-2xl mb-4 text-center font-bold">Iniciar sesión</h2>
        {error && (
          <div className="bg-red-100 text-red-700 p-2 mb-3 rounded text-sm">
            {error}
          </div>
        )}
        <input
          type="email"
          placeholder="Correo"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Entrar
        </button>
      </form>
    </div>
  );
}

export default Login;
