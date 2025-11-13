document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("appointments-container");
    const globalLoader = document.getElementById("global-loader");

    console.log("paciente_id:", paciente_id); // Verificar que paciente_id esté definido

    // Función auxiliar de log visual
    function log(msg, type = "info") {
        console[type === "error" ? "error" : "log"](`📘 [MediCare]: ${msg}`);
    }

    // Mostrar u ocultar loader global
    function toggleLoader(show) {
        if (!globalLoader) return;
        globalLoader.classList.toggle("hidden", !show);
    }

    // ✅ 1. Cargar citas desde el backend
    async function cargarCitas() {
        toggleLoader(true);

        try {
            const res = await fetch("http://localhost:5000/api/turnos");
            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const data = await res.json();
            log("Datos recibidos del backend.");

            if (!data.success || !Array.isArray(data.data)) {
                log("Respuesta inesperada del servidor.", "error");
                container.innerHTML = `<p class="error-text">⚠️ Error al cargar las citas.</p>`;
                return;
            }

            if (data.data.length === 0) {
                container.innerHTML = `<p class="no-citas">No tienes citas programadas 🩵</p>`;
                return;
            }

            renderizarCitas(data.data);

        } catch (error) {
            log("Error conectando al backend: " + error.message, "error");
            container.innerHTML = `<p class="error-text">❌ No se pudieron cargar las citas. Intenta nuevamente más tarde.</p>`;
        } finally {
            toggleLoader(false);
        }
    }

    // ✅ 2. Renderizar tarjetas
    function renderizarCitas(citas) {
        container.innerHTML = "";

        citas.forEach(cita => {
            const card = document.createElement("div");
            card.classList.add("appointment-card");
            card.setAttribute("data-appointment-id", cita.id);

            card.innerHTML = `
                <div class="card-header">
                    <h3 class="doctor-name">${cita.doctor}</h3>
                    <span class="status-tag">${cita.estado || "Próxima"}</span>
                </div>
                <p class="specialty">${cita.especialidad}</p>
                
                <div class="details">
                    <p class="detail-item"><span class="icon">📅</span> ${cita.fecha}</p>
                    <p class="detail-item"><span class="icon">🕒</span> ${cita.hora}</p>
                    <p class="detail-item"><span class="icon">📍</span> ${cita.lugar}</p>
                </div>

                <button class="cancel-btn">Cancelar Cita</button>
            `;

            // Animación de aparición
            card.style.opacity = "0";
            setTimeout(() => {
                card.style.transition = "opacity 0.5s ease-in";
                card.style.opacity = "1";
            }, 50);

            card.querySelector(".cancel-btn").addEventListener("click", () => cancelarCita(cita.id, card));
            container.appendChild(card);
        });
    }

    // ✅ 3. Cancelar cita
    async function cancelarCita(id, cardElement) {
        const confirmar = confirm("¿Seguro que desea cancelar esta cita?");
        if (!confirmar) return;

        try {
            const res = await fetch(`http://localhost:5000/api/turnos/${id}`, { method: "DELETE" });
            const data = await res.json();

            if (data.success) {
                log(`Cita ${id} cancelada correctamente.`);
                cardElement.style.transition = "opacity 0.4s ease-out";
                cardElement.style.opacity = "0";
                setTimeout(() => cardElement.remove(), 400);
            } else {
                alert("⚠️ No se pudo cancelar la cita.");
            }

        } catch (error) {
            log("Error al cancelar cita: " + error.message, "error");
            alert("❌ Error al intentar cancelar la cita.");
        }
    }

    // 🚀 Iniciar carga
    cargarCitas();
});
