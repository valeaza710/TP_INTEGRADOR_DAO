document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const errorMessageDiv = document.getElementById("error-message"); // Referencia al div del error

    // 🔹 Función para ocultar el mensaje de error (evita el ReferenceError)
    function hideError() {
        if (errorMessageDiv) {
            errorMessageDiv.classList.add("hidden"); // si usás Tailwind
            // o: errorMessageDiv.style.display = "none";
        }
    }

    if (!form) {
        console.error("No se encontró el formulario de login");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        hideError(); // Limpia cualquier error anterior

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!username || !password) {
            alert("Complete todos los campos");
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/usuarios/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            console.log("Respuesta del backend:", data);

            if (!data.success) {
                // Mostrar error en pantalla (opcional)
                if (errorMessageDiv) {
                    errorMessageDiv.textContent = data.message || "Credenciales incorrectas";
                    errorMessageDiv.classList.remove("hidden");
                } else {
                    alert(data.message || "Credenciales incorrectas");
                }
                return;
            }

            // Guardar usuario en localStorage
            localStorage.setItem("user", JSON.stringify(data.user));

            // ✅ Redirección según rol
            const rol = data.user.rol?.toUpperCase() || "PACIENTE";
            if (rol === "ADMINISTRADOR") {
                window.location.href = "/administrador";
            } else if (rol === "MEDICO") {
                window.location.href = `/panel-medico/${data.user.id}`;
            } else if (rol === "SECRETARIA") {
                window.location.href = "/secretaria";
            } else {
                window.location.href = `/home/${data.user.id}`;
            }

        } catch (error) {
            console.error("Error en login:", error);
            alert("No se pudo conectar con el servidor");
        }
    });
});
