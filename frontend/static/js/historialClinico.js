// historialClinico.js
document.addEventListener('DOMContentLoaded', async () => {
    try {

        // 1. Traer datos del paciente
        // -------------------------------
        const pacienteRes = await fetch(`/api/pacientes/historial/${paciente_id}`);
        const pacienteJson = await pacienteRes.json();

        if (!pacienteJson.success || !pacienteJson.data) {
            console.error("No se pudieron cargar los datos del paciente.");
        } else {
            const pacienteData = pacienteJson.data;
            renderPatientData(pacienteData);
        }

        // -------------------------------
        // 2. Traer recetas del paciente
        // -------------------------------
        const recetasRes = await fetch(`/api/recetas/paciente/${paciente_id}`);
        const recetasJson = await recetasRes.json();

        if (!recetasJson.success || !recetasJson.data) {
            console.error("No se pudieron cargar las recetas del paciente.");
        } else {
            const prescriptions = recetasJson.data;

            renderPrescriptions(prescriptions);
        }

        // -------------------------------
        // 3. Configurar navegación de pestañas
        // -------------------------------
        setupTabs();

        // -------------------------------
        // 4. Configurar botón de cerrar
        // -------------------------------
        setupCloseButtonRedirect();

    } catch (error) {
        console.error("Error cargando datos del historial clínico:", error);
        alert("❌ Error al cargar los datos del paciente.");
    }
});


/**
 * Renderiza los datos del paciente.
 * @param {object} data - Datos del paciente
 */
function renderPatientData(data) {
    const container = document.getElementById('tab-content-personal');
    if (!container) return;

    const fields = [
        { label: "Nombre", value: `${data.nombre || ''} ${data.apellido || ''}`.trim() },
        { label: "DNI", value: data.dni || 'N/A' },
        { label: "Edad", value: data.edad || 'N/A' },
        { label: "Teléfono", value: data.telefono || 'N/A' },
        { label: "Email", value: data.mail || 'N/A' },
        { label: "Dirección", value: data.direccion || 'N/A' },
    ];

    const gridHtml = fields.map(field => `
        <div class="card p-6 text-center">
            <div class="text-sm text-muted-foreground mb-2">${field.label}</div>
            <div class="text-3xl font-bold text-foreground">
                ${field.value}
            </div>
        </div>
    `).join('');

    container.innerHTML = `
        <div id="patient-data-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4"> 
            ${gridHtml}
        </div>
    `;
}


/**
 * Renderiza la lista de recetas.
 * @param {Array<object>} prescriptions - Lista de recetas
 */
function renderPrescriptions(prescriptions) {
    const listContainer = document.getElementById('prescriptions-list');
    if (!listContainer) return;
    listContainer.innerHTML = ''; // Limpiar

    prescriptions.forEach((prescription) => {
        const prescriptionCard = document.createElement('div');
        prescriptionCard.className = 'card p-6 space-y-4 border rounded-xl shadow-sm bg-white'; 
        
        const header = `
            <div class="flex items-start justify-between">
                <div>
                    <h3 class="font-semibold text-lg text-foreground">${prescription.enfermedad.nombre}</h3>
                    <p class="text-sm text-muted-foreground">
                       Dr. ${prescription.visita.medico_apellido || '-'} ${prescription.visita.medico_nombre || '-'} • ${prescription.fecha_emision || '-'}
                    </p>
                </div>
                <div class="icon-pill-link">
                    <i class="fas fa-prescription-bottle-alt icon-pill-link-icon text-lg"></i> 
                </div>
            </div>
        `;

        const medicationsHtml = `
                <div class="medication-card p-3 rounded-lg border border-gray-100 bg-gray-50 space-y-1">
                    <div class="font-medium text-sm text-foreground">${prescription.descripcion}</div>

                </div>
            `

        prescriptionCard.innerHTML = header + `<hr class="separator my-4" /><h4 class="font-medium text-sm text-foreground">Medicamentos Recetados:</h4>` + medicationsHtml;
        listContainer.appendChild(prescriptionCard);
    });
}

/**
 * Maneja el cambio de pestañas.
 */
function setupTabs() {
    const triggers = document.querySelectorAll('.tab-trigger');
    const contents = document.querySelectorAll('.tab-content');

    const initialContent = document.getElementById('tab-content-personal');
    if (initialContent) {
        initialContent.classList.remove('hidden');
    }
    
    const initialTrigger = document.querySelector('.tab-trigger[data-tab="personal"]');
    if (initialTrigger) {
        initialTrigger.classList.add('active');
    }

    triggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const targetTab = trigger.getAttribute('data-tab');

            // 1. Desactivar todos los triggers (botones)
            triggers.forEach(t => t.classList.remove('active'));

            // 2. Ocultar todos los contenidos de las pestañas
            contents.forEach(c => c.classList.add('hidden'));
            
            // 3. Activar el trigger (botón) seleccionado
            trigger.classList.add('active');
            
            // 4. Mostrar el contenido objetivo
            const targetContent = document.getElementById(`tab-content-${targetTab}`);
            if (targetContent) {
                targetContent.classList.remove('hidden');
            }
        });
    });
}

function setupCloseButtonRedirect() {
    // 🚨 Debes usar el selector de la cruz de tu HTML de Historial Clínico.
    // Usamos el selector de la imagen subida (image_a26c40.png) que suele ser:
    const closeButton = document.querySelector('.close-dialog-button') || document.querySelector('.close-btn') || document.querySelector('.modal-close');

    if (closeButton) {
        closeButton.addEventListener('click', async function(event) {
            event.preventDefault();

            try {
                const response = await fetch(`/api/pacientes/historial/${paciente_id}`);
                const pacienteData = await response.json();

                if (!pacienteData.success || !pacienteData.data) {
                    // Si no hay datos, redirigir a home genérico
                    window.location.href = '/home';
                } else {
                    // Redirigir usando el ID real del paciente
                    const paciente = pacienteData.data;
                    window.location.href = `/home/${paciente.usuario.id}`; 
                }

            } catch (error) {
                console.error("Error al obtener paciente para cerrar:", error);
                window.location.href = '/home'; // fallback
            }
        });
    }
}
/**
 * Función para cerrar la modal (simulada).
 */
function closeDialog() {
    const dialog = document.getElementById('medical-history-dialog');
    if (dialog) {
        dialog.classList.remove('active');
    }
}