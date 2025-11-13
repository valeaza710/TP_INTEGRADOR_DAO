// reportes.js

// --- 1. MOCK DATA (Datos de ejemplo) ---
const mockData = {
    medicos: [
        { id: "1", nombre: "Dr. Juan Pérez" },
        { id: "2", nombre: "Dra. María García" },
        { id: "3", nombre: "Dr. Carlos López" },
    ],
    turnosPorMedico: [
        { id: 1, fecha: "2024-01-15", hora: "09:00", paciente: "Ana Martínez", especialidad: "Cardiología", estado: "Confirmado" },
        { id: 2, fecha: "2024-01-15", hora: "10:00", paciente: "Pedro González", especialidad: "Cardiología", estado: "Completado" },
        { id: 3, fecha: "2024-01-16", hora: "11:00", paciente: "Laura Rodríguez", especialidad: "Cardiología", estado: "Confirmado" },
    ],
    turnosPorEspecialidad: [
        { especialidad: "Cardiología", cantidad: 45, porcentaje: 30 },
        { especialidad: "Pediatría", cantidad: 38, porcentaje: 25 },
        { especialidad: "Traumatología", cantidad: 32, porcentaje: 21 },
        { especialidad: "Dermatología", cantidad: 23, porcentaje: 15 },
        { especialidad: "Neurología", cantidad: 12, porcentaje: 9 },
    ],
    pacientesAtendidos: [
        { id: 1, nombre: "Ana Martínez", dni: "12345678", fecha: "2024-01-15", medico: "Dr. Juan Pérez", especialidad: "Cardiología" },
        { id: 2, nombre: "Pedro González", dni: "23456789", fecha: "2024-01-15", medico: "Dra. María García", especialidad: "Pediatría" },
        { id: 3, nombre: "Laura Rodríguez", dni: "34567890", fecha: "2024-01-16", medico: "Dr. Carlos López", especialidad: "Traumatología" },
        { id: 4, nombre: "Carlos Fernández", dni: "45678901", fecha: "2024-01-16", medico: "Dr. Juan Pérez", especialidad: "Cardiología" },
        { id: 5, nombre: "Sofía López", dni: "56789012", fecha: "2024-01-17", medico: "Dra. María García", especialidad: "Pediatría" },
    ],
    asistencia: [
        { name: "Asistencias", value: 142, color: "hsl(142 76% 36%)" },
        { name: "Inasistencias", value: 28, color: "hsl(0 84.2% 60.2%)" },
    ]
};

// Variable global para almacenar la instancia del gráfico (Chart.js)
let asistenciaChartInstance = null; 

// --- 2. LÓGICA DE PDF (CORRECCIÓN) ---

/**
 * Lógica central para generar el PDF.
 */
function handlePdfClick(event) {
    // 1. Busca el contenedor del reporte (el ancestro más cercano con la clase 'report-content')
    const activeReportContainer = event.target.closest('.report-content');
    
    if (!activeReportContainer) {
        return alert("Error: No se encontró el contenedor del reporte para exportar.");
    }

    // 2. Definir el nombre del archivo (basado en el ID del contenedor)
    const idReporte = activeReportContainer.id.replace('tab-content-', '');
    let nombreArchivo = "Reporte_Estadistico";
    switch (idReporte) {
        case 'turnos_medico':
            nombreArchivo = 'Reporte_Turnos_por_Medico';
            break;
        case 'turnos_especialidad':
            nombreArchivo = 'Reporte_Turnos_por_Especialidad';
            break;
        case 'pacientes_atendidos':
            nombreArchivo = 'Reporte_Pacientes_Atendidos';
            break;
        case 'asistencia_grafico':
            nombreArchivo = 'Reporte_Asistencia_Inasistencia';
            break;
    }

    // 3. Opciones de html2pdf
    const opt = {
        margin:        [0.5, 0.5, 0.5, 0.5],
        filename:      `${nombreArchivo}_${new Date().toLocaleDateString()}.pdf`,
        image:         { type: 'jpeg', quality: 0.98 },
        html2canvas:   { scale: 2 },
        jsPDF:         { unit: 'in', format: 'a4', orientation: 'portrait' }
    }
    

    // 4. Generar y descargar el PDF del contenedor del reporte
    // Esto funciona porque el botón de PDF solo existe y es visible en el reporte activo
    html2pdf().from(activeReportContainer).set(opt).save();
}

/**
 * Adjunta el Event Listener de PDF al botón recién creado en el DOM.
 * @param {string} buttonId - El ID del botón PDF a escuchar.
 */
function setupPdfListener(buttonId) {
    const button = document.getElementById(buttonId);
    
    if (button) {
        // Remover cualquier listener anterior para evitar duplicados al re-renderizar
        button.removeEventListener('click', handlePdfClick);
        button.addEventListener('click', handlePdfClick);
    }
}


// --- 3. FUNCIONES DE RENDERIZADO DE REPORTES ---

function renderTurnosPorMedico() {
    const container = document.getElementById('tab-content-turnos_medico');
    const { medicos, turnosPorMedico: turnos } = mockData;
    
    const medicoOptions = medicos.map(medico => 
        `<option value="${medico.id}">${medico.nombre}</option>`
    ).join('');

    const turnosRows = turnos.map(turno => `
        <tr>
            <td>${turno.fecha}</td>
            <td>${turno.hora}</td>
            <td>${turno.paciente}</td>
            <td>${turno.especialidad}</td>
            <td>${turno.estado}</td>
        </tr>
    `).join('');

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
                <button id="btn-generar-medico" class="btn-primary">
                    Generar Reporte
                </button>
                <button id="btn-pdf-turnos_medico" class="btn-primary-pdf">
                    <i class="fas fa-file-pdf"></i> Generar PDF
                </button>
            </div>


            <div class="border rounded-lg overflow-x-auto">
                <table class="w-full table-auto text-left whitespace-nowrap">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-3 font-medium">Fecha</th>
                            <th class="p-3 font-medium">Hora</th>
                            <th class="p-3 font-medium">Paciente</th>
                            <th class="p-3 font-medium">Especialidad</th>
                            <th class="p-3 font-medium">Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${turnosRows}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    // Agregar el listener al botón de generar reporte (simulación)
    document.getElementById('btn-generar-medico').addEventListener('click', () => {
        const medico = document.getElementById('medico').value;
        const inicio = document.getElementById('fecha-inicio').value;
        const fin = document.getElementById('fecha-fin').value;
        console.log("Generando reporte de Médico:", { medico, inicio, fin });
    });
    
    // 🚨 Inicializa el listener del PDF
    setupPdfListener('btn-pdf-turnos_medico');
}


function renderTurnosPorEspecialidad() {
    const container = document.getElementById('tab-content-turnos_especialidad');
    const datos = mockData.turnosPorEspecialidad;
    const total = datos.reduce((sum, item) => sum + item.cantidad, 0);

    const rowsHtml = datos.map((item) => `
        <tr>
            <td class="font-medium p-3">${item.especialidad}</td>
            <td class="text-right p-3">${item.cantidad}</td>
            <td class="text-right p-3">
                <div class="flex items-center justify-end gap-2">
                    <div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div class="h-full bg-blue-500 rounded-full" style="width: ${item.porcentaje}%;"></div>
                    </div>
                    <span>${item.porcentaje}%</span>
                </div>
            </td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card p-6 border rounded-lg shadow-sm space-y-6">
            <h3 class="text-xl font-semibold mb-2 flex items-center gap-2"><i class="fas fa-chart-bar"></i> Cantidad de Turnos por Especialidad</h3>
            <p class="text-sm text-muted-foreground">Distribución total de turnos agendados por especialidad médica</p>

            <div class="p-4 bg-gray-50 rounded-lg">
                <p class="text-sm text-muted-foreground">Total de Turnos</p>
                <p class="text-3xl font-bold text-blue-600">${total}</p>
            </div>
            
            <div class="flex justify-end">
                <button id="btn-pdf-turnos_especialidad" class="btn-primary-pdf">
                    <i class="fas fa-file-pdf"></i> Generar PDF
                </button>
            </div>

            <div class="border rounded-lg overflow-x-auto">
                <table class="w-full table-auto text-left">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-3 font-medium">Especialidad</th>
                            <th class="text-right p-3 font-medium">Cantidad</th>
                            <th class="text-right p-3 font-medium">Porcentaje</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rowsHtml}
                    </tbody>
                </table>
            </div>
        </div>
    `;

    // 🚨 Inicializa el listener del PDF
    setupPdfListener('btn-pdf-turnos_especialidad');
}


function renderPacientesAtendidos() {
    const container = document.getElementById('tab-content-pacientes_atendidos');
    const pacientes = mockData.pacientesAtendidos;

    const rowsHtml = pacientes.map(paciente => `
        <tr>
            <td class="font-medium p-3">${paciente.nombre}</td>
            <td class="p-3">${paciente.dni}</td>
            <td class="p-3">${paciente.fecha}</td>
            <td class="p-3">${paciente.medico}</td>
            <td class="p-3">${paciente.especialidad}</td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="card p-6 border rounded-lg shadow-sm space-y-6">
            <h3 class="text-xl font-semibold mb-2 flex items-center gap-2"><i class="fas fa-users"></i> Pacientes Atendidos</h3>
            <p class="text-sm text-muted-foreground">Listado de pacientes atendidos en un rango de fechas específico</p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                <div class="space-y-2">
                    <label for="fecha-inicio-pacientes">Fecha Inicio</label>
                    <input id="fecha-inicio-pacientes" type="date" class="w-full border p-2 rounded" />
                </div>
                <div class="space-y-2">
                    <label for="fecha-fin-pacientes">Fecha Fin</label>
                    <input id="fecha-fin-pacientes" type="date" class="w-full border p-2 rounded" />
                </div>
            </div>

            <div class="flex justify-between items-center">
                <button id="btn-generar-pacientes" class="btn-primary">
                    Generar Reporte
                </button>
                <button id="btn-pdf-pacientes_atendidos" class="btn-primary-pdf">
                    <i class="fas fa-file-pdf"></i> Generar PDF
                </button>
            </div>

            <div class="border rounded-lg overflow-x-auto">
                <table class="w-full table-auto text-left">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-3 font-medium">Paciente</th>
                            <th class="p-3 font-medium">DNI</th>
                            <th class="p-3 font-medium">Fecha</th>
                            <th class="p-3 font-medium">Médico</th>
                            <th class="p-3 font-medium">Especialidad</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rowsHtml}
                    </tbody>
                </table>
            </div>
            
            <div class="p-4 bg-gray-50 rounded-lg">
                <p class="text-sm text-muted-foreground">Total de Pacientes Atendidos</p>
                <p class="text-3xl font-bold text-blue-600">${pacientes.length}</p>
            </div>
        </div>
    `;

    // Agregar el listener al botón de generar reporte (simulación)
    document.getElementById('btn-generar-pacientes').addEventListener('click', () => {
        const inicio = document.getElementById('fecha-inicio-pacientes').value;
        const fin = document.getElementById('fecha-fin-pacientes').value;
        console.log("Generando reporte de Pacientes Atendidos:", { inicio, fin });
    });
    
    // 🚨 Inicializa el listener del PDF
    setupPdfListener('btn-pdf-pacientes_atendidos');
}


function renderAsistenciaChart() {
    const container = document.getElementById('tab-content-asistencia_grafico');
    const data = mockData.asistencia;
    const total = data.reduce((sum, item) => sum + item.value, 0);
    const porcentajeAsistencia = ((data[0].value / total) * 100).toFixed(1);
    const porcentajeInasistencia = ((data[1].value / total) * 100).toFixed(1);

    container.innerHTML = `
        <div class="card p-6 border rounded-lg shadow-sm space-y-6">
            <h3 class="text-xl font-semibold mb-2 flex items-center gap-2"><i class="fas fa-chart-pie"></i> Gráfico Estadístico de Asistencia</h3>
            <p class="text-sm text-muted-foreground">Comparación entre asistencias e inasistencias de pacientes</p>
            
            <div class="flex justify-end">
                <button id="btn-pdf-asistencia" class="btn-primary-pdf">
                    <i class="fas fa-file-pdf"></i> Generar PDF
                </button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="card-indicator p-4 bg-gray-100 rounded-lg">
                    <p class="text-sm text-muted-foreground">Total de Turnos</p>
                    <p class="text-3xl font-bold text-gray-800">${total}</p>
                </div>
                
                <div class="card-indicator p-4 bg-success-light border border-success-border rounded-lg">
                    <p class="text-sm text-muted-foreground">Asistencias</p>
                    <p class="text-3xl font-bold text-success">${data[0].value}</p>
                    <p class="text-sm text-muted-foreground">${porcentajeAsistencia}%</p>
                </div>
                
                <div class="card-indicator p-4 bg-destructive-light border border-destructive-border rounded-lg">
                    <p class="text-sm text-muted-foreground">Inasistencias</p>
                    <p class="text-3xl font-bold text-destructive">${data[1].value}</p>
                    <p class="text-sm text-muted-foreground">${porcentajeInasistencia}%</p>
                </div>
            </div>

            <div class="w-full h-[350px] flex items-center justify-center">
                <canvas id="graficoAsistencia"></canvas>
            </div>
        </div>
    `;

    // 🚨 Inicializar Chart.js 🚨
    const ctx = document.getElementById('graficoAsistencia').getContext('2d');

    // Destruye la instancia anterior si existe
    if (asistenciaChartInstance) {
        asistenciaChartInstance.destroy();
    }
    
    asistenciaChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.name),
            datasets: [{
                label: 'Distribución de Asistencia',
                data: data.map(item => item.value),
                backgroundColor: ['hsl(142, 76%, 36%)', 'hsl(0, 84%, 60%)'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += context.parsed + ' (' + ((context.parsed / total) * 100).toFixed(1) + '%)';
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });

    // 🚨 Inicializa el listener del PDF
    setupPdfListener('btn-pdf-asistencia');
}


// --- 4. LÓGICA DE NAVEGACIÓN DE PESTAÑAS (SETUP) ---

/**
 * Maneja el cambio de pestañas y llama a la función de renderizado del reporte correspondiente.
 */
function setupReportTabs() {
    const triggers = document.querySelectorAll('.tab-trigger');
    const contents = document.querySelectorAll('.report-content');
    
    const renderMap = {
        'turnos_medico': renderTurnosPorMedico,
        'turnos_especialidad': renderTurnosPorEspecialidad,
        'pacientes_atendidos': renderPacientesAtendidos,
        'asistencia_grafico': renderAsistenciaChart
    };

    // 1. Inicializa el reporte activo (el primero en el HTML)
    const initialTab = document.querySelector('.tab-trigger.active');
    if (initialTab) {
        const initialReport = initialTab.getAttribute('data-tab');
        if (renderMap[initialReport]) {
            renderMap[initialReport]();
        }
    }

    triggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const targetTab = trigger.getAttribute('data-tab');

            // 1. Desactivar y Ocultar
            triggers.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.add('hidden'));
            
            // 2. Activar y Mostrar
            trigger.classList.add('active');
            const targetContent = document.getElementById(`tab-content-${targetTab}`);
            if (targetContent) {
                targetContent.classList.remove('hidden');
                
                // 3. Renderizar el reporte seleccionado
                // Esto es crucial: renderiza el HTML y activa el botón PDF en el mismo paso.
                if (renderMap[targetTab]) {
                    renderMap[targetTab]();
                }
            }
        });
    });
}


// --- 5. INICIALIZACIÓN DE LA APLICACIÓN ---

document.addEventListener('DOMContentLoaded', () => {
    // Inicializa la navegación de pestañas (esto llama al primer renderizado)
    setupReportTabs();
});