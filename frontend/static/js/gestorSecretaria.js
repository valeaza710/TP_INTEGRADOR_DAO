// ====================
//   VARIABLES GLOBALES
// ====================
let appointments = [];
let newAppointmentData = {};

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
        const res = await fetch("/api/agenda/");
        const data = await res.json();

        appointments = data.map((a) => ({
            id: a.id,
            fecha: a.fecha,
            hora: a.hora,
            pacienteId: a.id_paciente,
            horarioId: a.id_horario_medico,
            estadoId: a.id_estado_turno,
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
    const searchTerm = document
        .getElementById("search-input")
        .value.toLowerCase();

    const filtered = appointments.filter((a) =>
        (a.pacienteId + "").toLowerCase().includes(searchTerm)
    );

    const tbody = document.getElementById("appointments-table-body");
    tbody.innerHTML = "";

    if (!filtered.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-6 text-gray-400">No se encontraron turnos.</td>
            </tr>`;
        return;
    }

    filtered.forEach((a) => {
        const row = document.createElement("tr");
        row.classList = "hover:bg-gray-50 transition";
        row.innerHTML = `
            <td class="px-4 py-3">${a.pacienteId}</td>
            <td class="px-4 py-3">${a.horarioId}</td>
            <td class="px-4 py-3">${new Date(a.fecha).toLocaleDateString("es-ES")}</td>
            <td class="px-4 py-3">${a.hora}</td>
            <td class="px-4 py-3">${getStatusBadgeHtml(a.estadoId)}</td>
            <td class="px-4 py-3 text-right">
                <button onclick="handleCancelAppointment(${a.id})"
                    class="text-red-600 border border-red-300 px-3 py-1 rounded-md text-xs hover:bg-red-50">
                    Cancelar
                </button>
            </td>`;
        tbody.appendChild(row);
    });
}

// ====================
//   CANCELAR TURNO
// ====================
async function handleCancelAppointment(id) {
    if (!confirm(`¿Cancelar turno #${id}?`)) return;

    const res = await fetch(`/api/agenda/${id}`, { method: "DELETE" });

    if (res.ok) {
        showToast("Turno cancelado correctamente.", "success");
        await loadAppointments();
    } else {
        showToast("Error al cancelar turno.", "error");
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
        row.innerHTML = `
            <td class="px-4 py-3">${m.nombre}</td>
            <td class="px-4 py-3">${m.apellido}</td>
            <td class="px-4 py-3">${m.especialidad || "-"}</td>
        `;
        tbody.appendChild(row);
    });
}



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

    loadAppointments();
});
