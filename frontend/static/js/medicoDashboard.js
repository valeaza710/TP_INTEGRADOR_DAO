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
            const targetEl = document.getElementById(target);
            if (targetEl) targetEl.classList.add("active");
        });
    });

    // ------------------- MODALES -------------------
    const cancelDialog = document.getElementById("cancel-dialog");
    const closeDialogBtn = document.getElementById("close-cancel-dialog");
    const confirmCancelBtn = document.getElementById("confirm-cancel");
    let selectedTurnoId = null;

    const recipeDialog = document.getElementById("recipe-dialog");
    const patientInfoElement = document.getElementById("patient-info");
    const medicationContainer = document.getElementById("medication-container");
    let medicationCounter = 1;

    // ------------------- TURNOS -------------------
    const turnosContainer = document.getElementById("turnos-container");
    const turnosCount = document.getElementById("turnos-count");
    const turnosCountText = document.getElementById("turnos-count-text");

    // ------------------- FUNCIONES AUXILIARES -------------------
    const actualizarContadores = () => {
        const cantidad = turnosContainer.querySelectorAll(".card").length;
        turnosCount.textContent = cantidad;
        turnosCountText.textContent = cantidad;
    };

    const actualizarEstadoTurno = async (turnoId, estadoId, card) => {
        try {
            const response = await fetch(`/api/agenda/${turnoId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id_estado_turno: estadoId })
            });
            if (response.ok) {
                card.remove();
                actualizarContadores();
            } else {
                console.error("Error al actualizar el turno:", response.statusText);
            }
        } catch (error) {
            console.error("Error de red al actualizar el turno:", error);
        }
    };

    // ------------------- DELEGACIÓN DE EVENTOS -------------------
    turnosContainer.addEventListener("click", async (e) => {
        const card = e.target.closest(".card");
        if (!card) return;
        const turnoId = card.dataset.id;

        // Atendido OJO ACA HAY QUE VER A QUE LE CORRESPONDE EL COMPLETADO!!!!!!!!!!!
        if (e.target.closest(".btn-attended")) {
            actualizarEstadoTurno(turnoId, 4, card); 
            return;
        }

        // Cancelar OJO ACA HAY QUE VER A QUE LE CORRESPONDE EL CANCELADO!!!!!!!!!!!
        if (e.target.closest(".btn-cancel")) {
            actualizarEstadoTurno(turnoId, 3, card); // 3 = Cancelado
            return;
        }

        // Receta
        if (e.target.closest(".btn-recipe")) {
            const turnoId = card.dataset.id;  // <--- ESTE ES EL ID DEL TURNO
            window.currentTurnoId = turnoId;  // lo guardamos globalmente o como prefieras
            const pacienteNombre = card.querySelector("p.font-semibold")?.textContent || "Paciente";
            const pacienteDni = card.querySelector("p.text-sm")?.textContent.split(": ")[1] || "-";

            patientInfoElement.textContent = `Paciente: ${pacienteNombre} - DNI: ${pacienteDni}`;

            medicationCounter = 1;
            const template = document.querySelector('.medication-block');
            medicationContainer.innerHTML = template ? template.outerHTML : `
                <div class="medication-block p-4 border rounded-lg bg-gray-50">
                    <h4 class="font-semibold text-gray-800 mb-3">Medicamento 1</h4>
                    <div class="space-y-3">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Medicamento</label>
                            <input type="text" class="w-full p-2 border border-gray-300 rounded-lg" placeholder="Ej: Amoxicilina 500mg">
                        </div>
                    </div>
                </div>
            `;
            recipeDialog.style.display = "flex";
        }
    });

    // ------------------- GUARDAR RECETA -------------------
    document.getElementById("generate-pdf-btn").addEventListener("click", async () => {

        // DNI desde la info del paciente
        const patientInfo = patientInfoElement.textContent.match(/DNI: (\d+)/);
        const dniPaciente = patientInfo ? patientInfo[1] : null;

        // Medicamentos (corregido)
        const medicamentos = Array.from(document.querySelectorAll('.medication-block')).map(block => ({
            nombre: block.querySelector('input').value
        }));

        // Observaciones (corregido)
        const observaciones = document.getElementById("obs-receta").value;

        // Enfermedad seleccionada
        const enfermedadId = document.getElementById("enfermedad-select").value;

        // JSON FINAL CORRECTO PARA EL BACKEND
        const payload = {
            visita: { id: window.currentVisitaId },
            paciente: { id: window.currentPacienteId },
            enfermedad: enfermedadId ? { id: enfermedadId } : null,
            medicamentos: medicamentos,
            observaciones: observaciones,
            fecha_emision: new Date().toISOString().split("T")[0],
            id_agenda_turno: window.currentTurnoId,
        };

        console.log("JSON ENVIADO AL BACKEND:", payload);

        try {
            const response = await fetch("/api/guardar_receta", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                alert("Receta médica registrada correctamente!");
                recipeDialog.style.display = "none";
            } else {
                const error = await response.json();
                alert("Error al guardar la receta: " + error.message);
            }

        } catch (err) {
            console.error(err);
        }
    });


    // ------------------- CERRAR MODAL CANCELAR -------------------
    closeDialogBtn.addEventListener("click", () => {
        cancelDialog.style.display = "none";
        selectedTurnoId = null;
    });

    // ------------------- FETCH TURNOS DE HOY -------------------
    const fetchTurnosHoy = async () => {
        try {
            const response = await fetch(`/api/agenda/medico/${window.MEDICO_ID}/hoy`);
            if (!response.ok) throw new Error("Error al obtener los turnos");

            const turnos = await response.json();
            turnosContainer.innerHTML = "";

            if (!turnos.data || turnos.data.length === 0) {
                turnosContainer.innerHTML = `<p class="text-gray-500">No hay turnos programados para hoy.</p>`;
                actualizarContadores();
                return;
            }

            turnos.data.forEach(turno => {
                const paciente = turno.paciente || {};
                const pacienteNombre = paciente.nombre || "Sin nombre";
                const pacienteApellido = paciente.apellido || "";
                const pacienteDni = paciente.dni || "-";

                const card = document.createElement("div");
                card.className = "bg-white p-6 rounded-xl shadow-lg border border-gray-200 flex justify-between items-center card";
                card.dataset.id = turno.id;

                card.innerHTML = `
                    <div>
                        <p class="font-semibold text-gray-900">${pacienteNombre} ${pacienteApellido}</p>
                        <p class="text-sm text-gray-500">DNI: ${pacienteDni}</p>
                        <p class="text-sm text-gray-500">Motivo: ${turno.motivo || 'Consulta'}</p>
                    </div>
                    <div class="flex flex-col items-end space-y-2">
                        <span class="text-gray-600 text-sm">${turno.hora}</span>
                        <div class="flex space-x-2">
                            <button class="btn-attended bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 text-sm flex items-center">
                                <i class="ph ph-check-circle mr-1"></i> Atendido
                            </button>
                            <button class="btn-recipe bg-cyan-600 text-white px-3 py-1 rounded hover:bg-cyan-700 text-sm flex items-center">
                                <i class="ph ph-note mr-1"></i> Receta
                            </button>
                            <button class="btn-cancel bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 text-sm flex items-center">
                                <i class="ph ph-x-circle mr-1"></i> Cancelar
                            </button>
                        </div>
                    </div>
                `;
                turnosContainer.appendChild(card);
            });

            actualizarContadores();

        } catch (error) {
            console.error(error);
            turnosContainer.innerHTML = `<p class="text-red-500">No se pudieron cargar los turnos.</p>`;
        }
    };

    // ------------------- FETCH ENFERMEDADES -------------------
    const fetchEnfermedades = async () => {
        const select = document.getElementById("enfermedad-select");
        if (!select) return;

        try {
            const response = await fetch("/api/enfermedades");
            if (!response.ok) throw new Error("Error al obtener enfermedades");

            const enfermedades = await response.json();

            // Validar que vengan enfermedades
            if (!enfermedades.success || !Array.isArray(enfermedades.data)) {
                select.innerHTML = `<option value="">No se pudieron cargar</option>`;
                return;
            }

            select.innerHTML = `<option value="">Seleccione una enfermedad</option>`;

            // Recorrer enfermedades.data
            enfermedades.data.forEach(e => {
                const opt = document.createElement("option");
                opt.value = e.id;
                opt.textContent = e.nombre;
                select.appendChild(opt);
            });


        } catch (error) {
            console.error("Error cargando enfermedades:", error);
            select.innerHTML = `<option value="">No se pudieron cargar</option>`;
        }
    };


    // ------------------- LLAMADA INICIAL -------------------
    console.log("DOM listo, container:", turnosContainer);
    fetchTurnosHoy();
    fetchEnfermedades();
});