document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("appointments-container");

    // ✅ 1. Cargar citas desde el backend
    async function cargarCitas() {
        try {
            const res = await fetch("http://localhost:5000/api/turnos");
            const data = await res.json();

            if (!data.success) {
                container.innerHTML = "<p>Error al cargar citas</p>";
                return;
            }

            renderizarCitas(data.data);

        } catch (error) {
            console.error("Error conectando al backend:", error);
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

            // ✅ Agregar evento al botón
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
                cardElement.remove();
            } else {
                alert("No se pudo cancelar la cita");
            }

        } catch (error) {
            console.error("Error al cancelar cita:", error);
        }
    }

    // ✅ Cargar citas al entrar
    cargarCitas();
});

