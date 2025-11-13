document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Obtener datos del formulario
        const formData = {
            username: document.getElementById("username").value.trim(),
            password: document.getElementById("password").value.trim(),
            nombre: document.getElementById("name").value.trim(),
            apellido: document.getElementById("lastname").value.trim(),
            dni: document.getElementById("dni").value.trim(),
            edad: parseInt(document.getElementById("age").value),
            fecha_nacimiento: document.getElementById("dob").value,
            email: document.getElementById("email").value.trim()

        };

        // Validaciones básicas
        if (!formData.username || !formData.password || !formData.email || !formData.nombre || !formData.apellido || !formData.dni) {
            alertMessage("Complete todos los campos obligatorios", "error");
            return;
        }

        if (formData.password.length < 8) {
            alertMessage("La contraseña debe tener al menos 8 caracteres", "warning");
            return;
        }

        try {
            // 🎯 PEGA A: /api/usuarios/registro
            const response = await fetch("http://localhost:5000/api/usuarios/registro", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            console.log("Respuesta del backend:", data);

            if (!data.success) {
                alertMessage(data.message || "Error al registrar usuario", "error");
                return;
            }

            // Registro exitoso
            alertMessage("¡Registro exitoso! Redirigiendo al login...", "success");
            
            setTimeout(() => {
                window.location.href = "/login";
            }, 2000);

        } catch (error) {
            console.error("Error:", error);
            alertMessage("No se pudo conectar con el servidor", "error");
        }
    });
});

// Función de alertas (reutiliza la que ya tienes en el HTML)
function alertMessage(message, type = 'info') {
    const containerId = 'custom-alert-container';
    let container = document.getElementById(containerId);
    
    if (!container) {
        container = document.createElement('div');
        container.id = containerId;
        container.className = 'fixed top-4 right-4 z-50 space-y-2 pointer-events-none';
        document.body.appendChild(container);
    }

    let bgColor = 'bg-blue-500';
    let icon = 'ℹ️';
    if (type === 'success') { bgColor = 'bg-green-500'; icon = '✅'; } 
    else if (type === 'error') { bgColor = 'bg-red-500'; icon = '❌'; } 
    else if (type === 'warning') { bgColor = 'bg-yellow-500'; icon = '⚠️'; }

    const alertElement = document.createElement('div');
    alertElement.className = `${bgColor} text-white px-4 py-3 rounded-xl shadow-lg flex items-center transform transition-all duration-300 ease-out translate-x-full opacity-0`;
    alertElement.innerHTML = `<span class="mr-2">${icon}</span><span>${message}</span>`;
    
    container.appendChild(alertElement);

    setTimeout(() => {
        alertElement.classList.remove('translate-x-full', 'opacity-0');
        alertElement.classList.add('translate-x-0', 'opacity-100');
    }, 10);

    setTimeout(() => {
        alertElement.classList.remove('translate-x-0', 'opacity-0');
        alertElement.classList.add('translate-x-full', 'opacity-0');
        alertElement.addEventListener('transitionend', () => alertElement.remove());
    }, 3000);
}