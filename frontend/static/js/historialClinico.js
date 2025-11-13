// historialClinico.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Inicializar la vista de Datos Personales
    // Nota: 'patientData' y 'prescriptions' se definen en el script de historialClinico.html
    renderPatientData(patientData);
    
    // 2. Inicializar la vista de Recetas
    renderPrescriptions(prescriptions);

    // 3. Configurar la navegación de pestañas
    setupTabs();
});


/**
 
 * @param {object} data - Datos del paciente.
 */
function renderPatientData(data) {
    
    const container = document.getElementById('tab-content-personal');
    if (!container) return;
    
    // 1. Campos de la cuadrícula (Peso, Altura, Grupo Sanguíneo)
    const fields = [
        { label: "Peso", value: data.weight || 'N/A' },
        { label: "Altura", value: data.height || 'N/A' },
        { label: "Grupo Sanguíneo", value: data.bloodType || 'N/A' },
    ];

    const gridHtml = fields.map(field => `
        <div class="card p-6 text-center">
            <div class="text-sm text-muted-foreground mb-2">${field.label}</div>
            <div class="text-3xl font-bold text-foreground">
                ${field.value}
            </div>
        </div>
    `).join('');

    // 2. Nuevo Bloque para Enfermedades Crónicas
    const chronicDiseasesHtml = `
        <div class="mt-6">
            <h4 class="font-semibold text-lg text-foreground mb-2">Enfermedades Crónicas</h4>
            <div class="card p-4">
                <p class="text-sm text-muted-foreground">
                    ${data.chronicDiseases && data.chronicDiseases.length > 0 ? data.chronicDiseases : 'Ninguna registrada.'}
                </p>
            </div>
        </div>
    `;

    // 3. Ensamblar y inyectar el HTML final, incluyendo el grid y el nuevo bloque
    container.innerHTML = `
        <div id="patient-data-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4"> 
            ${gridHtml}
        </div>
        ${chronicDiseasesHtml}
    `;
}


/**
 * Renderiza la lista de Recetas.
 * @param {Array<object>} prescriptions - Lista de recetas.
 */
function renderPrescriptions(prescriptions) {
    const listContainer = document.getElementById('prescriptions-list');
    if (!listContainer) return;
    listContainer.innerHTML = ''; // Limpiar

    prescriptions.forEach((prescription, index) => {
        const prescriptionCard = document.createElement('div');
        // Aseguramos que se vea bien el borde de la card
        prescriptionCard.className = 'card p-6 space-y-4 border rounded-xl shadow-sm bg-white'; 
        
        // 1. Encabezado de la Receta (Diagnóstico, Doctor, Fecha)
        const header = `
            <div class="flex items-start justify-between">
                <div>
                    <h3 class="font-semibold text-lg text-foreground">${prescription.diagnosis}</h3>
                    <p class="text-sm text-muted-foreground">
                        ${prescription.doctorName} • ${prescription.date}
                    </p>
                </div>
                <div class="icon-pill-link">
                    <i class="fas fa-prescription-bottle-alt icon-pill-link-icon text-lg"></i> 
                </div>
            </div>
            <hr class="separator my-4" />
            <h4 class="font-medium text-sm text-foreground">
                Medicamentos Recetados:
            </h4>
        `;

        // 2. Lista de Medicamentos
        const medicationsList = prescription.medications.map(med => `
            <div class="medication-card p-3 rounded-lg border border-gray-100 bg-gray-50 space-y-1">
                <div class="font-medium text-sm text-foreground">${med.name}</div>
                <div class="grid grid-cols-3 gap-2 text-xs text-muted-foreground">
                    <div>
                        <span class="font-medium text-gray-700">Dosis:</span> ${med.dosage}
                    </div>
                    <div>
                        <span class="font-medium text-gray-700">Frecuencia:</span> ${med.frequency}
                    </div>
                    <div>
                        <span class="font-medium text-gray-700">Duración:</span> ${med.duration}
                    </div>
                </div>
            </div>
        `).join('');

        prescriptionCard.innerHTML = header + `<div class="space-y-3">${medicationsList}</div>`;
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

/**
 * Función para cerrar la modal (simulada).
 */
function closeDialog() {
    const dialog = document.getElementById('medical-history-dialog');
    if (dialog) {
        dialog.classList.remove('active');
    }
}