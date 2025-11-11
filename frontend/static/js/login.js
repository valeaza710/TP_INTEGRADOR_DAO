document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const errorMessageDiv = document.getElementById("error-message"); // Referencia al nuevo div

    // Función para mostrar/ocultar errores
    const displayError = (message) => {
        errorMessageDiv.textContent = message;
        errorMessageDiv.classList.remove("hidden");
        // Puedes agregar una clase de animación o color aquí (ej: 'visible')
    };

    const hideError = () => {
        errorMessageDiv.classList.add("hidden");
        errorMessageDiv.textContent = "";
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        hideError(); // Limpia cualquier error anterior

        const username = form.username.value.trim();
        const password = form.password.value.trim();

        if (!username || !password) {
            // Este caso ya lo manejabas, lo cambiamos a usar el nuevo div de error
            displayError("Por favor, complete todos los campos.");
            return;
        }

        // --- LÓGICA DE CONEXIÓN CON EL BACKEND  ---

        try {
            const response = await fetch("/", { // Asumiendo que Flask usa la ruta /login
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) { // Código 200-299 (Éxito)
                // Éxito en el login
                alert("Inicio de sesión exitoso. Redirigiendo...");
                
            } else if (response.status === 401) { // Código 401 (Contraseña incorrecta, No autorizado)
                // Fallo: Credenciales incorrectas
                const errorData = await response.json(); 
                // Asume que el backend envía un JSON como: {"error": "Contraseña incorrecta."}
                displayError(errorData.error || "Credenciales incorrectas. Intente nuevamente.");

            } else {
                // Otros errores del servidor (500, etc.)
                displayError("Error de servidor. Intente más tarde.");
            }
        } catch (error) {
            console.error("Error al conectar con el servidor:", error);
            displayError("No se pudo conectar con el servicio de login.");
        }
    });
});
