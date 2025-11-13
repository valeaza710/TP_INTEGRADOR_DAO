// reportes.js

const API_BASE = "http://localhost:5000/api";

// Variable global para la instancia del gráfico
let asistenciaChartInstance = null;

// --- 1. FUNCIONES PARA CONSULTAR API ---

async function fetchMedicos() {
    const res = await fetch(`${API_BASE}/medico`);
    if (!res.ok) throw new Error("Error al obtener médicos");
    return res.json();
}

// ✅ 1️⃣ Turnos por médico
async function fetchTurnosPorMedico(idMedico, fechaInicio, fechaFin) {
    const url = `${API_BASE}/reportes/turnos-medico?id_medico=${idMedico}&fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Error al obtener turnos por médico");
    return res.json();
}

// ✅ 2️⃣ Turnos por especialidad
async function fetchTurnosPorEspecialidad(fechaInicio, fechaFin) {
    const url = `${API_BASE}/reportes/turnos-especialidad?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Error al obtener turnos por especialidad");
    return res.json();
}

// ✅ 3️⃣ Pacientes atendidos
async function fetchPacientesAtendidos(fechaInicio, fechaFin) {
    const url = `${API_BASE}/reportes/pacientes-atendidos?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Error al obtener pacientes atendidos");
    return res.json();
}

// ✅ 4️⃣ Asistencia vs inasistencia
async function fetchAsistencia(fechaInicio, fechaFin) {
    const url = `${API_BASE}/reportes/asistencia?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Error al obtener datos de asistencia");
    return res.json();
}

// --- 2. DESCARGA DE PDF ---

async function handlePdfClick(event) {
    const activeReportContainer = event.target.closest(".report-content");
    if (!activeReportContainer) {
        return alert("Error: No se encontró el contenedor del reporte.");
    }

    const idReporte = activeReportContainer.id.replace("tab-content-", "");
    let nombreArchivo = "Reporte";
    let endpoint = "";

    switch (idReporte) {
        case "turnos_medico":
            endpoint = `${API_BASE}/reportes/archivo-turnos_medico`;
            nombreArchivo = "Reporte_Turnos_por_Medico";
            break;
        case "turnos_especialidad":
            endpoint = `${API_BASE}/reportes/archivo-turnos_especialidad`;
            nombreArchivo = "Reporte_Turnos_por_Especialidad";
            break;
        case "pacientes_atendidos":
            endpoint = `${API_BASE}/reportes/archivo-pacientes_atendidos`;
            nombreArchivo = "Reporte_Pacientes_Atendidos";
            break;
        case "asistencia_grafico":
            endpoint = `${API_BASE}/reportes/archivo-asistencia_grafico`;
            nombreArchivo = "Reporte_Asistencia_Inasistencia";
            break;
        default:
            return alert("Tipo de reporte no reconocido");
    }

    try {
        const response = await fetch(endpoint, { method: "GET", headers: { Accept: "application/pdf" } });
        if (!response.ok) throw new Error("Error al obtener PDF");
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${nombreArchivo}_${new Date().toLocaleDateString()}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error("❌ Error al descargar PDF:", error);
        alert("No se pudo descargar el PDF.");
    }
}

function setupPdfListener(id) {
    const btn = document.getElementById(id);
    if (btn) {
        btn.removeEventListener("click", handlePdfClick);
        btn.addEventListener("click", handlePdfClick);
    }
}

// --- 3. RENDERIZADOS ---

// ✅ 1️⃣ Turnos por médico
async function renderTurnosPorMedico() {
    const container = document.getElementById("tab-content-turnos_medico");

    try {
        const medicos = await fetchMedicos();
        const medicoOptions = medicos.map(m => `<option value="${m.id}">${m.nombre} ${m.apellido}</option>`).join("");

        container.innerHTML = `
            <div class="card p-6 border rounded-lg shadow-sm space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4 bg-gray-50 rounded-lg">
                    <div class="space-y-2">
                        <label for="medico">Médico</label>
                        <select id="medico" class="w-full border p-2 rounded">${medicoOptions}</select>
                    </div>
                    <div class="space-y-2">
                        <label for="fecha-inicio">Fecha Inicio</label>
                        <input id="fecha-inicio" type="date" class="w-full border p-2 rounded" />
                    </div>
                    <div class="space-y-2">
                        <label for="fecha-fin">Fecha Fin</label>
                        <input id="fecha-fin" type="date" class="w-full border p-2 rounded" />
                    </div>
                </div>
                <div class="flex justify-between items-center">
                    <button id="btn-generar-medico" class="btn-primary">Generar Reporte</button>
                    <button id="btn-pdf-turnos_medico" class="btn-primary-pdf">
                        <i class="fas fa-file-pdf"></i> Generar PDF
                    </button>
                </div>
                <div id="tabla-turnos" class="border rounded-lg overflow-x-auto"></div>
            </div>
        `;

        document.getElementById("btn-generar-medico").addEventListener("click", async () => {
            const idMedico = document.getElementById("medico").value;
            const fechaInicio = document.getElementById("fecha-inicio").value;
            const fechaFin = document.getElementById("fecha-fin").value;

            const data = await fetchTurnosPorMedico(idMedico, fechaInicio, fechaFin);
            const turnos = data.turnos || [];

            const rows = turnos.map(t => `
                <tr>
                    <td>${t.fecha}</td>
                    <td>${t.hora}</td>
                    <td>${t.paciente}</td>
                    <td>${t.especialidad}</td>
                    <td>${t.estado}</td>
                </tr>`).join("");

            document.getElementById("tabla-turnos").innerHTML = `
                <table class="w-full table-auto text-left">
                    <thead class="bg-gray-100">
                        <tr>
                            <th>Fecha</th><th>Hora</th><th>Paciente</th><th>Especialidad</th><th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>`;
        });

        setupPdfListener("btn-pdf-turnos_medico");
    } catch (e) {
        console.error(e);
        container.innerHTML = `<p class="text-red-600">Error al cargar médicos.</p>`;
    }
}

// ✅ 2️⃣ Turnos por especialidad
async function renderTurnosPorEspecialidad() {
    const container = document.getElementById("tab-content-turnos_especialidad");
    try {
        const data = await fetchTurnosPorEspecialidad();
        const especialidades = data.especialidades || [];
        const total = especialidades.reduce((sum, i) => sum + i.cantidad, 0);

        const rows = especialidades.map(i => `
            <tr>
                <td>${i.especialidad}</td>
                <td class="text-right">${i.cantidad}</td>
                <td class="text-right">${i.porcentaje}%</td>
            </tr>`).join("");

        container.innerHTML = `
            <div class="card p-6 border rounded-lg space-y-6">
                <h3 class="text-xl font-semibold mb-2">Turnos por Especialidad</h3>
                <p>Total: <b>${total}</b></p>
                <div class="flex justify-end">
                    <button id="btn-pdf-turnos_especialidad" class="btn-primary-pdf"><i class="fas fa-file-pdf"></i> PDF</button>
                </div>
                <table class="w-full table-auto">
                    <thead><tr><th>Especialidad</th><th>Cantidad</th><th>Porcentaje</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>`;
        setupPdfListener("btn-pdf-turnos_especialidad");
    } catch (err) {
        console.error(err);
        container.innerHTML = `<p class="text-red-600">Error al cargar reporte.</p>`;
    }
}

// ✅ 3️⃣ Pacientes atendidos
async function renderPacientesAtendidos() {
    const container = document.getElementById("tab-content-pacientes_atendidos");
    container.innerHTML = `
        <div class="card p-6 border rounded-lg shadow-sm space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                <div><label>Fecha Inicio</label><input id="fecha-inicio-pacientes" type="date" class="border p-2 rounded w-full"></div>
                <div><label>Fecha Fin</label><input id="fecha-fin-pacientes" type="date" class="border p-2 rounded w-full"></div>
            </div>
            <div class="flex justify-between items-center">
                <button id="btn-generar-pacientes" class="btn-primary">Generar Reporte</button>
                <button id="btn-pdf-pacientes_atendidos" class="btn-primary-pdf"><i class="fas fa-file-pdf"></i> PDF</button>
            </div>
            <div id="tabla-pacientes"></div>
        </div>`;

    document.getElementById("btn-generar-pacientes").addEventListener("click", async () => {
        const inicio = document.getElementById("fecha-inicio-pacientes").value;
        const fin = document.getElementById("fecha-fin-pacientes").value;
        const data = await fetchPacientesAtendidos(inicio, fin);
        const pacientes = data.pacientes || [];

        const rows = pacientes.map(p => `
            <tr>
                <td>${p.paciente}</td><td>${p.dni}</td><td>${p.fecha_atencion}</td>
                <td>${p.medico}</td><td>${p.especialidad}</td>
            </tr>`).join("");

        document.getElementById("tabla-pacientes").innerHTML = `
            <table class="w-full table-auto">
                <thead><tr><th>Paciente</th><th>DNI</th><th>Fecha</th><th>Médico</th><th>Especialidad</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>`;
    });

    setupPdfListener("btn-pdf-pacientes_atendidos");
}

// ✅ 4️⃣ Gráfico de asistencia
async function renderAsistenciaChart() {
    const container = document.getElementById("tab-content-asistencia_grafico");
    const data = await fetchAsistencia();
    const asistencia = data.asistencia || [];

    const ctxId = "graficoAsistencia";
    container.innerHTML = `
        <div class="card p-6 border rounded-lg space-y-6">
            <h3 class="text-xl font-semibold">Gráfico de Asistencia</h3>
            <div class="flex justify-end">
                <button id="btn-pdf-asistencia" class="btn-primary-pdf"><i class="fas fa-file-pdf"></i> PDF</button>
            </div>
            <canvas id="${ctxId}"></canvas>
        </div>`;

    const ctx = document.getElementById(ctxId).getContext("2d");
    if (asistenciaChartInstance) asistenciaChartInstance.destroy();

    asistenciaChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: asistencia.map(d => d.name),
            datasets: [{ data: asistencia.map(d => d.value), backgroundColor: asistencia.map(d => d.color) }]
        },
        options: { responsive: true }
    });

    setupPdfListener("btn-pdf-asistencia");
}

// --- 4. SETUP DE TABS ---

function setupReportTabs() {
    const triggers = document.querySelectorAll(".tab-trigger");
    const contents = document.querySelectorAll(".report-content");

    const renderMap = {
        "turnos_medico": renderTurnosPorMedico,
        "turnos_especialidad": renderTurnosPorEspecialidad,
        "pacientes_atendidos": renderPacientesAtendidos,
        "asistencia_grafico": renderAsistenciaChart
    };

    const initialTab = document.querySelector(".tab-trigger.active");
    if (initialTab) renderMap[initialTab.dataset.tab]?.();

    triggers.forEach(trigger => {
        trigger.addEventListener("click", () => {
            triggers.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.add("hidden"));
            trigger.classList.add("active");

            const tab = trigger.dataset.tab;
            const content = document.getElementById(`tab-content-${tab}`);
            if (content) {
                content.classList.remove("hidden");
                renderMap[tab]?.();
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", setupReportTabs);
