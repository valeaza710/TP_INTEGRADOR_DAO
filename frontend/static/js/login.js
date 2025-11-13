document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const errorMessageDiv = document.getElementById("error-message"); // Referencia al nuevo div

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
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();
            console.log("Respuesta del backend:", data);

            if (!data.success) {
                alert("Credenciales incorrectas");
                return;
            }

            // Guardar usuario en localStorage
            localStorage.setItem("user", JSON.stringify(data.user));

            // Redirección según rol
            if (data.user.rol === "ADMIN") {
                window.location.href = "/administrador";
            } else if (data.user.rol === "MEDICO") {
                window.location.href = "/panel-medico";
            } else {
                window.location.href = "/home";
            }

        } catch (error) {
            console.error("Error:", error);
            alert("No se pudo conectar con el servidor");
        }
    });
});
