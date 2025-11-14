// ====================
//   VARIABLES GLOBALES
// ====================
let appointments = [];
let newAppointmentData = {};
let allPacientes = [];
let allMedicos = [];
// ====================
//     UTILIDADES UI
// ====================
const showToast = (message, type = "success") => {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");

    const colors = {
        success: "bg-green-500",
        error: "bg-red-500",
        info: "bg-blue-500",
    };

    toast.className = `${colors[type] || colors.success} text-white px-4 py-3 rounded-lg shadow-xl mb-2 opacity-0 transition-opacity duration-300`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-4 opacity-70 hover:opacity-100">✖</button>
    `;

    container.appendChild(toast);
    setTimeout(() => toast.classList.remove("opacity-0"), 50);
    setTimeout(() => toast.classList.add("opacity-0"), 3500);
    setTimeout(() => toast.remove(), 3800);
};

// ====================
//  GET STATUS BADGE
// ====================
const getStatusBadgeHtml = (id_estado) => {
    if (id_estado === 1)
        return `<span class="px-2 py-1 text-xs bg-green-200 text-green-800 rounded-full">Agendado</span>`;
    return `<span class="px-2 py-1 text-xs bg-gray-200 text-gray-800 rounded-full">Otro</span>`;
};

// ====================
//   CARGAR TURNOS
// ====================
async function loadAppointments() {
    try {
        const res = await fetch("/api/agenda/detalles");
        const data = await res.json();

        appointments = data.map(a => ({
            id_turno: a.id_turno,
            dni_paciente: a.dni_paciente,
            paciente: a.paciente,
            medico: a.medico,
            fecha: a.fecha,
            hora_turno: a.hora_turno,
            estado: a.estado
        }));

        renderAppointments();
    } catch (e) {
        console.error("Error cargando turnos:", e);
        showToast("Error al cargar turnos", "error");
    }
}


// ====================
//   RENDER TURNOS
// ====================
function renderAppointments() {
    const searchTerm = document.getElementById("search-input").value.toLowerCase();
    const filtered = appointments
        .filter(a => a.paciente) // solo turnos con paciente
        .filter(a =>
        a.dni_paciente.toLowerCase().includes(searchTerm) ||
        a.paciente.toLowerCase().includes(searchTerm)
    );

    const tbody = document.getElementById("appointments-table-body");
    tbody.innerHTML = "";

    if (!filtered.length) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-6 text-gray-400">No se encontraron turnos.</td></tr>`;
        return;
    }

    filtered.forEach(a => {
        const row = document.createElement("tr");
        row.classList = "hover:bg-gray-50 transition";
        row.innerHTML = `
            <td class="px-4 py-3">${a.dni_paciente}</td>
            <td class="px-4 py-3">${a.paciente}</td>
            <td class="px-4 py-3">${a.medico}</td>
            <td class="px-4 py-3">${a.fecha}</td>
            <td class="px-4 py-3">${a.hora_turno}</td>
            <td class="px-4 py-3">${a.estado}</td>
            <td class="px-4 py-3 text-right flex justify-end gap-2">
                <button onclick="eliminarTurno(${a.id_turno})" class="px-2 py-1 bg-red-500 text-white rounded">Cancelar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}


// ====================
//   CANCELAR TURNO
// ====================
// ====================
//   CANCELAR TURNO (actualizado usando update)
// ====================
async function eliminarTurno(id) {
    if (!confirm(`¿Cancelar turno #${id}?`)) return;

    try {
        const res = await fetch(`/api/agenda/${id}`, {
            method: "PUT", // usa PUT porque tu backend tiene update
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id_estado_turno: 5,
                id_paciente: null
            }),
        });

        const data = await res.json();

        if (res.ok) {
            showToast("Turno cancelado correctamente.", "success");
            loadAppointments();
        } else {
            showToast(data.error || "Error al cancelar turno.", "error");
        }
    } catch (err) {
        console.error(err);
        showToast("Error al cancelar turno", "error");
    }
}

// ========================
//  MODAL NUEVO TURNO
// ========================
function openModal() {
    document.getElementById("new-appointment-modal").classList.remove("hidden");
}

function closeModal() {
    document.getElementById("new-appointment-modal").classList.add("hidden");
}

// ========================
//  REGISTRO TURNO NUEVO
// ========================
async function handleFinalSubmit(e) {
    e.preventDefault();

    const fecha = document.getElementById("fecha").value;
    const hora = document.getElementById("hora").value;
    const dniPaciente = document.getElementById("pacienteId").value;
    const horarioId = document.getElementById("horarioId").value;

    if (!fecha || !hora || !dniPaciente || !horarioId) {
        showToast("Complete todos los campos.", "error");
        return;
    }

    const data = {
        fecha,
        hora,
        dni_paciente: dniPaciente,
        id_estado_turno: 1,
        id_horario_medico: horarioId,
    };

    const res = await fetch("/api/agenda/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    if (res.status === 404) {
        showToast("❌ Paciente no encontrado.", "error");
        openPatientRegisterModal(dniPaciente);
        return;
    }

    if (!res.ok) {
        showToast("Error al crear turno.", "error");
        return;
    }

    showToast("✅ Turno creado correctamente.", "success");
    closeModal();
    loadAppointments();
}

// ========================
//  MODAL REGISTRO PACIENTE
// ========================
function openPatientRegisterModal(dni = "") {
    document
        .getElementById("patient-register-modal")
        .classList.remove("hidden");
    document.getElementById("regPacienteDni").value = dni;
}

function closePatientRegisterModal() {
    document.getElementById("patient-register-modal").classList.add("hidden");
}

async function submitPatientRegister() {
    const nombre = document.getElementById("regPacienteNombre").value;
    const dni = document.getElementById("regPacienteDni").value;
    const fecha_nacimiento = document.getElementById("regPacienteFN").value;

    if (!nombre || !dni || !fecha_nacimiento) {
        showToast("Complete todos los campos.", "error");
        return;
    }

    const res = await fetch("/api/pacientes/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, dni, fecha_nacimiento }),
    });

    if (!res.ok) {
        showToast("❌ Error al registrar paciente.", "error");
        return;
    }

    showToast("✅ Paciente registrado.", "success");
    closePatientRegisterModal();
}

// ========================
//   LISTAR PACIENTES
// ========================
async function loadPacientes() {
    const tbody = document.getElementById("patients-table-body");
    tbody.innerHTML = `
        <tr><td colspan="3" class="text-center py-6 text-gray-400">Cargando pacientes...</td></tr>
    `;

    try {
        const res = await fetch("/api/pacientes//basico");
        const data = await res.json();

        if (!data.success || !Array.isArray(data.data)) {
            throw new Error("Respuesta inválida del servidor.");
        }
        allPacientes = data.data; 

        renderPacientes(data.data);
    } catch (error) {
        console.error("Error al cargar pacientes:", error);
        tbody.innerHTML = `
            <tr><td colspan="3" class="text-center py-6 text-red-500">Error al cargar pacientes</td></tr>
        `;
    }
}

// ========================
//   RENDER PACIENTES
// ========================
function renderPacientes(pacientes) {
    const tbody = document.getElementById("patients-table-body");
    tbody.innerHTML = "";

    if (!pacientes.length) {
        tbody.innerHTML = `
            <tr><td colspan="3" class="text-center py-6 text-gray-400">No hay pacientes registrados.</td></tr>
        `;
        return;
    }

    pacientes.forEach((p) => {
        const row = document.createElement("tr");
        row.classList = "hover:bg-gray-50 transition";
        row.innerHTML = `
            <td class="px-4 py-3">${p.dni}</td>
            <td class="px-4 py-3">${p.nombre}</td>
            <td class="px-4 py-3">${p.apellido || "-"}</td>
        `;
        tbody.appendChild(row);
    });
}


// ========================
//   LISTAR MÉDICOS
// ========================
async function loadMedicos() {
    const tbody = document.getElementById("medicos-table-body");
    tbody.innerHTML = `
        <tr><td colspan="3" class="text-center py-6 text-gray-400">Cargando médicos...</td></tr>
    `;

    try {
        const res = await fetch("/api/medicos/basico"); // 👈 endpoint similar a /pacientes/basico
        const data = await res.json();

        if (!data.success || !Array.isArray(data.data)) {
            throw new Error("Respuesta inválida del servidor.");
        }
        allMedicos = data.data; // <-- guardamos los médicos en la variable global

        renderMedicos(data.data);
    } catch (error) {
        console.error("Error al cargar médicos:", error);
        tbody.innerHTML = `
            <tr><td colspan="3" class="text-center py-6 text-red-500">Error al cargar médicos</td></tr>
        `;
    }
}

// ========================
//   RENDER MÉDICOS
// ========================
function renderMedicos(medicos) {
    const tbody = document.getElementById("medicos-table-body");
    tbody.innerHTML = "";

    if (!medicos.length) {
        tbody.innerHTML = `
            <tr><td colspan="3" class="text-center py-6 text-gray-400">No hay médicos registrados.</td></tr>
        `;
        return;
    }

    medicos.forEach((m) => {
        const row = document.createElement("tr");
        row.classList = "hover:bg-gray-50 transition";
        // Convertimos el array de especialidades en un string separado por comas
        const espStr = (m.especialidades || []).map(e => e.nombre).join(", ");
        row.innerHTML = `
            <td class="px-4 py-3">${m.nombre}</td>
            <td class="px-4 py-3">${m.apellido}</td>
            <td class="px-4 py-3">${espStr || "-"}</td>
            <td class="px-4 py-3 text-right flex justify-end gap-2">
                <button class="px-4 py-1 bg-blue-500 text-white rounded">Generar horario</button>
            </td>
        `;

        // Conectar botón al modal
        const btn = row.querySelector("button");
        btn.addEventListener("click", () => openScheduleModal(m.id, `${m.nombre} ${m.apellido}`));

        tbody.appendChild(row);
    });
}


// ============================
// BÚSQUEDA DE PACIENTE POR DNI
// ============================
async function buscarPaciente() {
    const dni = document.getElementById("pacienteDniSearch").value;
    if (!dni) return;

    try {
        const res = await fetch(`/api/pacientes/buscar?dni=${dni}`);
        const data = await res.json();

        if (res.ok && data.success && data.count > 0) {
            const paciente = data.data[0]; // tomamos el primer resultado
            console.log("Paciente encontrado:", paciente);
            document.getElementById("pacienteId").value = paciente.id; // guardamos el ID
            // mostrar info en el modal
            const resultDiv = document.getElementById("patient-result");
            resultDiv.classList.remove("hidden");
            resultDiv.innerHTML = `<p>Paciente: ${paciente.nombre} ${paciente.apellido} - DNI: ${paciente.dni}</p>`;
            document.getElementById("confirm-patient-btn").disabled = false;
        } else {
            alert("No se encontró el paciente.");
        }
    } catch (err) {
        console.error("Error buscando paciente:", err);
        alert("Error al buscar paciente.");
    }
}

// ============================
// CONFIRMAR PACIENTE Y REDIRECCIÓN
// ============================
function goToStep2() {
    const pacienteId = document.getElementById("pacienteId").value;

    if (!pacienteId) {
        alert("Debe seleccionar un paciente antes de continuar.");
        return;
    }

    // Redirigimos a agendarCita.html con el id del paciente en query string
    window.location.href = `/agendar?pacienteId=${pacienteId}`;
}

// ============================
// ABRIR Y CERRAR MODAL
// ============================
function openModal() {
    document.getElementById("new-appointment-modal").classList.remove("hidden");
    // Limpiar modal cada vez que se abre
    document.getElementById("pacienteDniSearch").value = "";
    document.getElementById("patient-result").classList.add("hidden");
    document.getElementById("confirm-patient-btn").disabled = true;
    document.getElementById("pacienteId").value = "";
}

function closeModal() {
    document.getElementById("new-appointment-modal").classList.add("hidden");
}

// ============================
// EVENTO BOTÓN NUEVO TURNO
// ============================
document.getElementById("open-modal-btn").addEventListener("click", openModal);




// ========================
//   CAMBIO DE SECCIONES
// ========================
const turnosSection = document.querySelector(".card");
const pacientesSection = document.getElementById("pacientes-section");
const medicosSection = document.getElementById("medicos-section");

const tabTurnos = document.getElementById("tab-turnos");
const tabPacientes = document.getElementById("tab-pacientes");
const tabMedicos = document.getElementById("tab-medicos");

tabPacientes.addEventListener("click", async () => {
    turnosSection.classList.add("hidden");
    medicosSection.classList.add("hidden");
    pacientesSection.classList.remove("hidden");

    tabTurnos.classList.add("text-gray-500");
    tabTurnos.classList.remove("bg-gray-100", "text-primary", "shadow-inner");

    tabMedicos.classList.add("text-gray-500");
    tabMedicos.classList.remove("bg-gray-100", "text-primary", "shadow-inner");

    tabPacientes.classList.remove("text-gray-500");
    tabPacientes.classList.add("bg-gray-100", "text-primary", "shadow-inner");

    await loadPacientes();
    
});

tabMedicos.addEventListener("click", async () => {
    turnosSection.classList.add("hidden");
    pacientesSection.classList.add("hidden");
    medicosSection.classList.remove("hidden");

    tabTurnos.classList.add("text-gray-500");
    tabTurnos.classList.remove("bg-gray-100", "text-primary", "shadow-inner");

    tabPacientes.classList.add("text-gray-500");
    tabPacientes.classList.remove("bg-gray-100", "text-primary", "shadow-inner");

    tabMedicos.classList.remove("text-gray-500");
    tabMedicos.classList.add("bg-gray-100", "text-primary", "shadow-inner");

    await loadMedicos();
});

tabTurnos.addEventListener("click", () => {
    pacientesSection.classList.add("hidden");
    medicosSection.classList.add("hidden");
    turnosSection.classList.remove("hidden");

    tabPacientes.classList.add("text-gray-500");
    tabPacientes.classList.remove("bg-gray-100", "text-primary", "shadow-inner");

    tabMedicos.classList.add("text-gray-500");
    tabMedicos.classList.remove("bg-gray-100", "text-primary", "shadow-inner");

    tabTurnos.classList.remove("text-gray-500");
    tabTurnos.classList.add("bg-gray-100", "text-primary", "shadow-inner");
});


// ==========================
//   EVENTOS INICIALES
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    document
        .getElementById("open-modal-btn")
        .addEventListener("click", openModal);
    document
        .getElementById("search-input")
        .addEventListener("input", renderAppointments);
    document.getElementById("buscar-pacientes").addEventListener("input", filterPacientes);
    document.getElementById("buscar-medicos").addEventListener("input", filterMedicos);

    loadAppointments();
});


// ----------------------------------------------
//BARRA DE BUSQUEDA
// ----------------------------------------------

// Filtrar pacientes por DNI
function filterPacientes() {
    const searchTerm = document.getElementById("buscar-pacientes").value.toLowerCase();
    const filtered = allPacientes.filter(p => (p.dni + "").toLowerCase().includes(searchTerm));
    renderPacientes(filtered);
}

// Filtrar médicos por APELLIDO
function filterMedicos() {
    const searchTerm = document.getElementById("buscar-medicos").value.toLowerCase();
    const filtered = allMedicos.filter(m =>
        m.apellido.toLowerCase().includes(searchTerm)

    );
    renderMedicos(filtered);
}




// Abrir modal y rellenar datos
function openScheduleModal(medicoId, medicoNombre) {
    document.getElementById("scheduleModal").classList.remove("hidden");
    document.getElementById("id_medico").value = medicoId;
    document.getElementById("modalDoctorName").textContent = medicoNombre;
    document.getElementById("doctorIDDisplay").textContent = `ID Médico: ${medicoId}`;

    // Opciones de mes y año
    const mesSelect = document.getElementById("mes");
    const anioSelect = document.getElementById("anio");
    mesSelect.innerHTML = "";
    anioSelect.innerHTML = "";
    const meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
    meses.forEach((m, i) => mesSelect.innerHTML += `<option value="${i+1}">${m}</option>`);
    const currentYear = new Date().getFullYear();
    for (let y = currentYear; y <= currentYear + 2; y++) anioSelect.innerHTML += `<option value="${y}">${y}</option>`;
}



// Enviar formulario
document.getElementById("scheduleForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const data = {
        id_medico: document.getElementById("id_medico").value,
        mes: document.getElementById("mes").value,
        anio: document.getElementById("anio").value,
        dia_semana: document.getElementById("dia_semana").value,
        hora_inicio: document.getElementById("hora_inicio").value,
        duracion_turno_min: document.getElementById("duracion_turno_min").value,
        hora_fin: document.getElementById("hora_fin").value
    };

    try {
        const res = await fetch("/api/horarios_medico", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (res.ok) {
            document.getElementById("confirmationMessage").classList.remove("hidden");
            console.log("Horario generado:", result);
        } else {
            alert(result.error || "Error generando horario (horarios duplicados)");
        }
    } catch (err) {
        console.error(err);
        alert("Error generando horario");
    }
});

// Cerrar modal
function closeScheduleModal() {
    document.getElementById("scheduleModal").classList.add("hidden");
    document.getElementById("confirmationMessage").classList.add("hidden");
}
