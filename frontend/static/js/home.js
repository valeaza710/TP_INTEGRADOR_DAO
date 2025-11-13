document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("appointments-container");

    // 🔹 Muestra un spinner inicial
    container.innerHTML = `<div class="loader"></div>`;

    // ✅ 1. Cargar citas desde el backend
    async function cargarCitas() {
        try {
            const res = await fetch("http://localhost:5000/api/turnos");
            if (!res.ok) throw new Error("Error de red o servidor caído");

            const data = await res.json();

            if (!data.success || !Array.isArray(data.data)) {
                container.innerHTML = `<p class="error-text">⚠️ Error al cargar las citas.</p>`;
                return;
            }

            if (data.data.length === 0) {
                container.innerHTML = `<p class="no-citas">No tienes citas programadas 🩵</p>`;
                return;
            }

            renderizarCitas(data.data);

        } catch (error) {
            console.error("Error conectando al backend:", error);
            container.innerHTML = `<p class="error-text">❌ No se pudieron cargar las citas. Intenta nuevamente más tarde.</p>`;
        }
    }

    // ✅ 2. Renderizar tarjetas de citas
    function renderizarCitas(citas) {
        container.innerHTML = "";

        citas.forEach(cita => {
            const card = document.createElement("div");
            card.classList.add("appointment-card");
            card.setAttribute("data-appointment-id", cita.id);

            card.innerHTML = `
                <div class="card-header">
                    <h3 class="doctor-name">${cita.doctor}</h3>
                    <span class="status-tag">Próxima</span>
                </div>
                <p class="specialty">${cita.especialidad}</p>
                
                <div class="details">
                    <p class="detail-item"><span class="icon">📅</span> ${cita.fecha}</p>
                    <p class="detail-item"><span class="icon">🕒</span> ${cita.hora}</p>
                    <p class="detail-item"><span class="icon">📍</span> ${cita.lugar}</p>
                </div>

                <button class="cancel-btn">Cancelar Cita</button>
            `;

            // Agregar animación al renderizar
            card.style.opacity = "0";
            setTimeout(() => {
                card.style.transition = "opacity 0.5s ease-in";
                card.style.opacity = "1";
            }, 50);

            // Agregar evento al botón
            card.querySelector(".cancel-btn").addEventListener("click", () => cancelarCita(cita.id, card));

            container.appendChild(card);
        });
    }

    // ✅ 3. Función para cancelar cita
    async function cancelarCita(id, cardElement) {
        const confirmar = confirm("¿Seguro que desea cancelar esta cita?");
        if (!confirmar) return;

        try {
            const res = await fetch(`http://localhost:5000/api/turnos/${id}`, {
                method: "DELETE"
            });
            const data = await res.json();

            if (data.success) {
                // Transición suave al eliminar
                cardElement.style.transition = "opacity 0.4s ease-out";
                cardElement.style.opacity = "0";
                setTimeout(() => cardElement.remove(), 400);
            } else {
                alert("⚠️ No se pudo cancelar la cita");
            }

        } catch (error) {
            console.error("Error al cancelar cita:", error);
            alert("❌ Error al intentar cancelar la cita");
        }
    }

    // ✅ Cargar citas al entrar
    cargarCitas();
});
