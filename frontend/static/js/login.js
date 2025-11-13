document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");

    if (!form) {
        console.error("No se encontró el formulario de login");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

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
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            console.log("Respuesta del backend:", data);

            if (!data.success) {
                alert(data.message || "Credenciales incorrectas");
                return;
            }

            // Guardar usuario en localStorage
            localStorage.setItem("user", JSON.stringify(data.user));

            // ✅ Redirección según rol
            const rol = data.user.rol?.toUpperCase() || "PACIENTE";
            if (rol === "ADMIN") {
                window.location.href = "/administrador";
            } else if (rol === "MEDICO") {
                window.location.href = "/panel-medico";
            } else {
                window.location.href = "/home"; // ✅ Esta es la correcta
            }
        } catch (error) {
            console.error("Error en login:", error);
            alert("No se pudo conectar con el servidor");
        }
    });
});
