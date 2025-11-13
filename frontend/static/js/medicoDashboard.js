/*
 * Archivo: app.js
 * Ubicación recomendada en Flask: static/js/
 */

document.addEventListener("DOMContentLoaded", () => {

    // ------------------- PESTAÑAS -------------------
    const tabs = document.querySelectorAll(".tab");
    const tabContents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const target = tab.getAttribute("data-tab");
            tabContents.forEach(c => c.classList.remove("active"));
            document.getElementById(target).classList.add("active");
        });
    });

    // ------------------- MODAL CANCELAR -------------------
    const cancelDialog = document.getElementById("cancel-dialog");
    const closeDialogBtn = document.getElementById("close-dialog");
    const confirmCancelBtn = document.getElementById("confirm-cancel");
    let selectedId = null;

    // Delegación de eventos: funciona para tarjetas dinámicas
    document.getElementById("agenda").addEventListener("click", (e) => {
        if(e.target.closest(".btn-cancel")) {
            selectedId = e.target.closest(".card").dataset.id;
            cancelDialog.style.display = "flex";
        }
    });

    closeDialogBtn.addEventListener("click", () => {
        cancelDialog.style.display = "none";
        selectedId = null;
    });

    confirmCancelBtn.addEventListener("click", async () => {
        if(selectedId) {
            try {
                const response = await fetch("/cancel", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ id: selectedId })
                });

                if(response.ok){
                    const elementToRemove = document.querySelector(`[data-id="${selectedId}"]`);
                    if(elementToRemove) elementToRemove.remove();
                } else {
                    console.error("Error al cancelar el turno:", response.statusText);
                }

            } catch(error){
                console.error("Error de red al cancelar:", error);
            } finally {
                cancelDialog.style.display = "none";
                selectedId = null;
            }
        }
    });

    // ------------------- TURNOS DE HOY -------------------
    const user = JSON.parse(localStorage.getItem("user"));
    console.log("ID del médico logueado:", user?.id);
    if(user && user.rol && user.rol.toUpperCase() === "MEDICO") {

        (async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/agenda/medico/${user.id}/hoy`);
                const data = await response.json();

                if(data.success){
                    const turnos = data.data;
                    console.log("📅 Turnos de hoy:", turnos);

                    // Contenedor de turnos
                    const agendaContainer = document.getElementById("agenda").querySelector(".space-y-6");
                    agendaContainer.innerHTML = ""; // Limpiamos tarjetas actuales

                    // Actualizamos contadores
                    const turnosCount = document.getElementById("turnos-count");
                    const turnosCountText = document.getElementById("turnos-count-text");
                    if(turnosCount) turnosCount.textContent = turnos.length;
                    if(turnosCountText) turnosCountText.textContent = turnos.length;

                    // Creamos tarjetas por turno
                    turnos.forEach(turno => {
                        const card = document.createElement("div");
                        card.className = "card bg-white p-6 rounded-xl shadow-lg border border-gray-200 transition duration-300 hover:shadow-xl";
                        card.dataset.id = `turno-${turno.id}`;
                        card.dataset.patientName = turno.paciente_nombre;
                        card.dataset.patientDni = turno.paciente_dni;

                        card.innerHTML = `
                            <div class="flex justify-between items-start mb-4">
                                <div class="flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                    </svg>
                                    <div>
                                        <h4 class="text-lg font-semibold text-gray-900">${turno.paciente_nombre}</h4>
                                        <p class="text-sm text-gray-500">DNI: ${turno.paciente_dni}</p>
                                    </div>
                                </div>
                                <span class="text-lg font-bold text-gray-700">${turno.hora}</span>
                            </div>

                            <div class="bg-gray-50 p-3 rounded-lg border border-gray-100 mb-4">
                                <p class="text-sm font-medium text-gray-600">Motivo: ${turno.motivo}</p>
                                <p class="text-xs text-gray-400 mt-1">${turno.fecha}</p>
                            </div>

                            <div class="flex space-x-3">
                                <button data-appointment-id="appointment-${turno.id}" class="btn-atendido bg-emerald-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-emerald-700 transition duration-150 flex items-center shadow-md">
                                    <i class="ph ph-check-circle-light text-xl mr-2"></i>
                                    Turno Atendido
                                </button>
                                <button class="btn-recipe btn-action bg-cyan-500 text-white hover:bg-cyan-600 flex-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    Generar Receta
                                </button>
                                <button class="btn-cancel btn-action bg-red-500 text-white hover:bg-red-600 flex-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    Cancelar Turno
                                </button>
                            </div>
                        `;
                        agendaContainer.appendChild(card);
                    });

                } else {
                    console.error("❌ Error al obtener turnos de hoy:", data.message);
                }

            } catch(error){
                console.error("Error al conectar con el backend:", error);
            }
        })();
    }

});
