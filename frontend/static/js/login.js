document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const username = form.username.value.trim();
        const password = form.password.value.trim();

        if (!username || !password) {
            alert("Por favor, complete todos los campos");
            return;
        }

        // Simulación de login (aquí se conectará con el backend Flask)
        alert(`Iniciando sesión como ${username}...`);

        // Ejemplo: Redirección tras login
        // window.location.href = "/dashboard";
    });
});
