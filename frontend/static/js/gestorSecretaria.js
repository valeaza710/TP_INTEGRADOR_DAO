// gestorSecretaria.js
async function loadAppointments() {
    const res = await fetch("/api/turnos/");
    const data = await res.json();
    appointments = data; // ahora vienen del backend
    filterAppointments();
}

document.addEventListener("DOMContentLoaded", () => {
    loadAppointments();
});



let modalStep = 1;
let newAppointmentData = {};

// Data Mockup para la demo (usando la estética de las imágenes)
const MOCK_SPECIALTIES = [
    { id: 'MG', name: 'Medicina General', doctors: ['Dr. Pérez', 'Dra. Ana López'], availableCount: 3 },
    { id: 'CAR', name: 'Cardiología', doctors: ['Dr. Juan Pérez', 'Dr. Roberto Díaz'], availableCount: 2 },
    { id: 'DER', name: 'Dermatología', doctors: ['Dra. Ana López', 'Dr. Soto'], availableCount: 2 },
    { id: 'TRA', name: 'Traumatología', doctors: ['Dr. Hernández', 'Dra. Gómez'], availableCount: 2 },
    { id: 'PED', name: 'Pediatría', doctors: ['Dr. Roberto Díaz', 'Dra. Méndez'], availableCount: 2 },
    { id: 'ODO', name: 'Odontología', doctors: ['Dr. García', 'Dra. Fuentes'], availableCount: 2 },
];

// --- Funciones de Utilidad y UI ---

/**
 * Muestra una notificación Toast.
 * @param {string} message - Mensaje a mostrar.
 * @param {('success'|'error'|'info')} type - Tipo de mensaje.
 */
const showToast = (message, type = 'success') => {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    let bgColor = 'bg-green-500';
    if (type === 'error') bgColor = 'bg-red-500';
    if (type === 'info') bgColor = 'bg-blue-500';

    toast.className = `${bgColor} text-white px-4 py-3 rounded-lg shadow-xl mb-2 flex items-center justify-between opacity-0 transition-opacity duration-300`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-4 opacity-70 hover:opacity-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
    `;
    
    container.appendChild(toast);
    setTimeout(() => { toast.classList.remove('opacity-0'); }, 10); // Fade in
    setTimeout(() => { toast.classList.add('opacity-0'); }, 4000);
    setTimeout(() => { toast.remove(); }, 4300);
};

/**
 * Genera el HTML de la insignia de estado.
 */
const getStatusBadgeHtml = (status) => {
    let className = '';
    let label = '';
    switch (status) {
        case 'scheduled':
            className = 'bg-teal-100 text-teal-800 border-teal-300';
            label = 'Agendado';
            break;
        case 'completed':
            className = 'bg-gray-100 text-gray-600 border-gray-300';
            label = 'Completado';
            break;
        case 'cancelled':
            className = 'bg-red-100 text-red-700 border-red-300';
            label = 'Cancelado';
            break;
        default:
             className = 'bg-gray-100 text-gray-600 border-gray-300';
             label = status;
    }
    return `<span class="inline-flex items-center px-3 py-0.5 rounded-full text-xs font-medium border ${className}">${label}</span>`;
};

// --- Lógica de la Tabla (Turnos) ---

/**
 * Renderiza la tabla de turnos filtrados.
 */
const filterAppointments = () => {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();

    const filteredAppointments = appointments
        .filter(apt =>
            (apt.paciente?.nombre ?? "").toLowerCase().includes(searchTerm) ||
            (apt.horario_medico?.medico ?? "").toLowerCase().includes(searchTerm)
        )
        .sort((a, b) => new Date(a.fecha) - new Date(b.fecha));

    const tbody = document.getElementById('appointments-table-body');
    tbody.innerHTML = ""; // limpiar la tabla

    if (filteredAppointments.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-8 text-gray-500">
                    No se encontraron turnos.
                </td>
            </tr>
        `;
        return;
    }

    filteredAppointments.forEach(apt => {
        const row = tbody.insertRow();
        row.className = "hover:bg-gray-50 transition-colors";

        row.innerHTML = `
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                ${apt.paciente?.nombre ?? "Sin nombre"}
            </td>

            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                ${apt.horario_medico?.medico ?? "Sin médico"}
            </td>

            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                ${apt.horario_medico?.especialidad ?? "Sin especialidad"}
            </td>

            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                ${new Date(apt.fecha).toLocaleDateString("es-ES")}
            </td>

            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                ${apt.hora}
            </td>

            <td class="px-4 py-3 whitespace-nowrap text-sm">
                ${getStatusBadgeHtml(apt.estado_turno?.estado ?? "scheduled")}
            </td>

            <td class="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end gap-2">
                    <button onclick="handleEditAppointment('${apt.id}')"
                        class="text-indigo-600 hover:text-indigo-900 px-3 py-1 border border-indigo-200 rounded-md text-xs font-semibold hover:bg-indigo-50 transition-colors">
                        Editar
                    </button>

                    ${(apt.estado_turno?.estado === "scheduled") ? `
                        <button onclick="handleCancelAppointment('${apt.id}')"
                            class="text-red-600 hover:text-red-900 px-3 py-1 border border-red-200 rounded-md text-xs font-semibold hover:bg-red-50 transition-colors">
                            Cancelar
                        </button>
                    ` : ""}
                </div>
            </td>
        `;
    });
};

/**
 * Maneja la cancelación de un turno (actualización en el arreglo local).
 */
async function handleCancelAppointment(id) {
    try {
        const res = await fetch(`/api/turnos/${id}`, { method: "DELETE" });

        if (res.ok) {
            showToast(`Turno ${id} cancelado correctamente.`, "success");
            await loadAppointments();   // 📌 Recarga real desde el backend
        } else {
            showToast("Error al cancelar el turno.", "error");
        }

    } catch (error) {
        console.error(error);
        showToast("Error interno al cancelar el turno.", "error");
    }
}


// --- Lógica del Modal Multi-pasos ---

/**
 * Abre el modal y muestra el primer paso.
 */
const openModal = () => {
    modalStep = 1;
    newAppointmentData = {};
    const modal = document.getElementById('new-appointment-modal');
    modal.classList.remove('pointer-events-none', 'opacity-0');
    modal.querySelector('#modal-content-area').classList.remove('scale-95');
    renderModalStep();
};

/**
 * Cierra el modal.
 */
const closeModal = () => {
    const modal = document.getElementById('new-appointment-modal');
    modal.classList.add('opacity-0');
    modal.querySelector('#modal-content-area').classList.add('scale-95');
    setTimeout(() => {
        modal.classList.add('pointer-events-none');
    }, 300);
};

/**
 * Renderiza el contenido del modal según el paso actual.
 */
const renderModalStep = () => {
    const container = document.getElementById('modal-step-container');
    const subtitle = document.getElementById('modal-subtitle');
    container.innerHTML = '';
    
    switch (modalStep) {
        case 1:
            subtitle.textContent = 'Selecciona una especialidad médica';
            container.innerHTML = renderStep1SpecialtySelection();
            break;
        case 2:
            subtitle.textContent = `Selecciona un médico, fecha y hora para ${newAppointmentData.specialty || ''}`;
            container.innerHTML = renderStep2DoctorAndDate();
            break;
        case 3:
            subtitle.textContent = 'Ingresa datos del paciente y confirma';
            container.innerHTML = renderStep3PatientDetails();
            break;
    }
};

// PASO 1: Selección de Especialidad
const renderStep1SpecialtySelection = () => {
    const cardsHtml = MOCK_SPECIALTIES.map(spec => `
        <div 
            class="interactive-card p-4 flex flex-col justify-center ${newAppointmentData.specialty === spec.name ? 'selected' : ''}"
            onclick="selectSpecialty('${spec.name}')"
        >
            <h3 class="font-semibold text-lg text-gray-800">${spec.name}</h3>
            <p class="text-sm text-gray-500">${spec.availableCount} médicos disponibles</p>
        </div>
    `).join('');

    return `
        <div class="mb-4">
            <h3 class="font-semibold text-gray-700 mb-3">Especialidad</h3>
            <div class="grid grid-cols-2 gap-4">
                ${cardsHtml}
            </div>
        </div>
        <div class="flex justify-end pt-4 border-t mt-4">
            <button id="next-step-1" class="bg-primary text-white font-semibold py-2 px-6 rounded-md shadow-md transition-colors duration-150 ${newAppointmentData.specialty ? 'hover:bg-primary-dark' : 'opacity-50 cursor-not-allowed'}" ${newAppointmentData.specialty ? '' : 'disabled'}>
                Siguiente
            </button>
        </div>
    `;
};

window.selectSpecialty = (specialtyName) => {
    newAppointmentData.specialty = specialtyName;
    
    const container = document.getElementById('modal-step-container');
    container.innerHTML = renderStep1SpecialtySelection(); // Volver a renderizar para actualizar el estado visual
    
    const nextButton = document.getElementById('next-step-1');
    nextButton.disabled = false;
    nextButton.classList.remove('opacity-50', 'cursor-not-allowed');
    nextButton.classList.add('hover:bg-primary-dark');
    nextButton.onclick = () => { modalStep = 2; renderModalStep(); };
};

// PASO 2: Selección de Doctor, Fecha y Hora
const renderStep2DoctorAndDate = () => {
    const currentSpecialty = MOCK_SPECIALTIES.find(s => s.name === newAppointmentData.specialty);
    const doctorOptions = currentSpecialty.doctors.map(doc => `<option value="${doc}" ${newAppointmentData.doctorName === doc ? 'selected' : ''}>${doc}</option>`).join('');

    return `
        <div class="space-y-6">
            <div class="border-b pb-4">
                <label for="doctor-select" class="block text-sm font-medium text-gray-700 mb-2">Selecciona un Médico</label>
                <select id="doctor-select" onchange="selectDoctor(this.value)" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary transition-all">
                    <option value="">-- Seleccionar Médico --</option>
                    ${doctorOptions}
                </select>
            </div>

            <div class="border-b pb-4">
                <h3 class="text-sm font-medium text-gray-700 mb-3">Selecciona una Fecha</h3>
                <div id="calendar-container" class="bg-gray-50 p-4 rounded-lg">
                    ${renderCalendarMockup()}
                </div>
            </div>

            <div>
                <h3 class="text-sm font-medium text-gray-700 mb-3" id="available-slots-title">Turnos disponibles - ${newAppointmentData.date ? new Date(newAppointmentData.date).toLocaleDateString('es-ES') : 'Selecciona una fecha'}</h3>
                <div id="available-slots-container" class="grid grid-cols-3 gap-3">
                    ${renderAvailableSlots()}
                </div>
            </div>
        </div>

        <div class="flex justify-between pt-4 border-t mt-4">
            <button onclick="goBack()" class="text-gray-600 font-semibold py-2 px-6 rounded-md transition-colors duration-150 hover:bg-gray-100">
                &larr; Volver
            </button>
            <button id="next-step-2" class="bg-primary text-white font-semibold py-2 px-6 rounded-md shadow-md transition-colors duration-150 ${newAppointmentData.date && newAppointmentData.time && newAppointmentData.doctorName ? 'hover:bg-primary-dark' : 'opacity-50 cursor-not-allowed'}" ${newAppointmentData.date && newAppointmentData.time && newAppointmentData.doctorName ? '' : 'disabled'}>
                Siguiente
            </button>
        </div>
    `;
};

// MOCKUP de Calendario
const renderCalendarMockup = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    
    // Días fijos para demo (simula la segunda mitad del mes)
    const days = [];
    // Rellenar espacios vacíos (para que el día 1 empiece correctamente)
    for(let i = 0; i < 7; i++) { days.push(null); }
    // Días del 13 al 30 (ejemplo)
    for(let i = 13; i <= 30; i++) { days.push(i); }
    
    return `
        <div class="flex justify-between items-center mb-4">
            <button class="p-2 text-gray-500 hover:bg-gray-200 rounded-full">&lt;</button>
            <span class="font-semibold">${monthNames[month]} ${year}</span>
            <button class="p-2 text-gray-500 hover:bg-gray-200 rounded-full">&gt;</button>
        </div>
        <div class="grid grid-cols-7 text-center text-xs font-medium text-gray-500 mb-2">
            <span>Lu</span><span>Ma</span><span>Mi</span><span>Ju</span><span>Vi</span><span>Sá</span><span>Do</span>
        </div>
        <div class="grid grid-cols-7 text-center gap-1">
            ${days.map((day, index) => {
                if (day === null) return '<div></div>';
                
                // Usamos la fecha actual para el mes y año
                const dayDateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                const isAvailable = day % 3 !== 0; // Ejemplo: días 3, 6, 9, etc. no disponibles
                const isSelected = newAppointmentData.date === dayDateStr;
                
                let dayClasses = `p-2 rounded-full text-sm cursor-pointer transition-colors`;
                if (isAvailable) {
                    dayClasses += ' hover:bg-blue-100 text-gray-800';
                } else {
                    dayClasses += ' text-gray-400 cursor-not-allowed line-through';
                }

                if (isSelected) {
                    dayClasses = 'p-2 rounded-full text-sm bg-primary text-white shadow-md font-bold';
                }
                
                return `
                    <div 
                        class="${dayClasses}"
                        onclick="${isAvailable ? `selectDate(${year}, ${month + 1}, ${day})` : ''}"
                    >
                        ${day}
                    </div>
                `;
            }).join('')}
        </div>
    `;
};

window.selectDate = (year, month, day) => {
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    newAppointmentData.date = dateStr;
    
    document.getElementById('available-slots-title').textContent = `Turnos disponibles - ${new Date(dateStr).toLocaleDateString('es-ES')}`;
    document.getElementById('calendar-container').innerHTML = renderCalendarMockup(); // Vuelve a renderizar para marcar la selección
    document.getElementById('available-slots-container').innerHTML = renderAvailableSlots();
    checkStep2Completion();
};

window.selectDoctor = (doctorName) => {
    newAppointmentData.doctorName = doctorName;
    checkStep2Completion();
};

// MOCKUP de Turnos Disponibles (Horarios)
const renderAvailableSlots = () => {
    if (!newAppointmentData.date) return '<p class="col-span-3 text-gray-500 text-center py-4">Selecciona una fecha.</p>';
    
    // Slots fijos para demo
    const slots = ['09:00', '10:30', '11:00', '14:00', '15:30', '17:00'];

    return slots.map(time => `
        <button 
            type="button"
            class="p-2 border rounded-lg text-sm font-medium interactive-card text-gray-700 ${newAppointmentData.time === time ? 'selected' : ''}"
            onclick="selectSlot('${time}')"
        >
            ${time}
        </button>
    `).join('');
};

window.selectSlot = (time) => {
    newAppointmentData.time = time;

    // Quitar selección previa y añadir la nueva
    document.querySelectorAll('#available-slots-container .selected').forEach(el => el.classList.remove('selected'));
    const newCard = Array.from(document.querySelectorAll('#available-slots-container .interactive-card')).find(c => c.innerHTML.includes(time));
    if (newCard) newCard.classList.add('selected');

    checkStep2Completion();
};

const checkStep2Completion = () => {
    const nextButton = document.getElementById('next-step-2');
    const requiredFields = newAppointmentData.date && newAppointmentData.time && newAppointmentData.doctorName;
    
    if (requiredFields) {
        nextButton.disabled = false;
        nextButton.classList.remove('opacity-50', 'cursor-not-allowed');
        nextButton.classList.add('hover:bg-primary-dark');
        nextButton.onclick = () => { modalStep = 3; renderModalStep(); }; 
    } else {
        nextButton.disabled = true;
        nextButton.classList.add('opacity-50', 'cursor-not-allowed');
        nextButton.classList.remove('hover:bg-primary-dark');
    }
};

// PASO 3: Detalles del Paciente y Confirmación
const renderStep3PatientDetails = () => {
      return `
        <form id="appointment-form">
            <div class="space-y-4">
                <div class="space-y-2">
                    <label for="patientName" class="block text-sm font-medium text-gray-700">Nombre del Paciente</label>
                    <input id="patientName" name="patientName" placeholder="Nombre completo del paciente" required class="w-full p-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary">
                </div>
                <div class="space-y-2">
                    <label for="patientId" class="block text-sm font-medium text-gray-700">ID / Cédula</label>
                    <input id="patientId" name="patientId" placeholder="Documento de identidad" required class="w-full p-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary">
                </div>
                
                <div class="p-4 bg-gray-100 rounded-lg border border-gray-200">
                    <h4 class="font-semibold text-gray-800 mb-2">Resumen del Turno</h4>
                    <p class="text-sm text-gray-600">
                        <span class="font-medium">Especialidad:</span> ${newAppointmentData.specialty}<br>
                        <span class="font-medium">Médico:</span> ${newAppointmentData.doctorName}<br>
                        <span class="font-medium">Fecha:</span> ${new Date(newAppointmentData.date).toLocaleDateString('es-ES')}<br>
                        <span class="font-medium">Hora:</span> ${newAppointmentData.time}
                    </p>
                </div>
            </div>
            
            <div class="flex justify-between pt-4 border-t mt-6">
                <button type="button" onclick="goBack()" class="text-gray-600 font-semibold py-2 px-6 rounded-md transition-colors duration-150 hover:bg-gray-100">
                    &larr; Volver
                </button>
                <button type="submit" onclick="handleFinalSubmit(event)" class="bg-green-500 text-white font-semibold py-2 px-6 rounded-md shadow-md hover:bg-green-600 transition-colors duration-150">
                    Confirmar y Agendar
                </button>
            </div>
        </form>
    `;
}

/**
 * Maneja el envío final del formulario y guarda en el arreglo local.
 */
window.handleFinalSubmit = async (e) => {
    e.preventDefault();

    const patientName = document.getElementById("patientName").value;
    const patientId = document.getElementById("patientId").value;

    if (!patientName || !patientId) {
        showToast("Por favor, complete todos los datos del paciente.", 'error');
        return;
    }

    const appointmentData = {
        fecha: newAppointmentData.date,
        hora: newAppointmentData.time,
        paciente_id: patientId,
        medico: newAppointmentData.doctorName,
        especialidad: newAppointmentData.specialty,
        estado_turno_id: 1   // estado inicial: "agendado" o el que corresponda
    };

    try {
        const res = await fetch("/api/turnos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(appointmentData)
        });

        if (!res.ok) {
            showToast("Error al agendar el turno en el servidor.", "error");
            return;
        }

        showToast("✅ Turno agendado correctamente.", "success");
        closeModal();

        // Recargar la tabla desde el backend
        await loadAppointments();

    } catch (error) {
        console.error("Error al enviar turno:", error);
        showToast("Error interno al registrar el turno.", "error");
    }
};


// Lógica de navegación del modal
window.goBack = () => {
    if (modalStep > 1) {
        modalStep--;
        renderModalStep();
    }
};


// Placeholder para la edición (expuesto porque se llama en onclick del HTML)
window.handleEditAppointment = (id) => {
    const apt = appointments.find(a => a.id === id);
    if (apt) {
        showToast(`Función de edición para ${apt.patientName} (ID: ${id}) no implementada.`, 'info');
    }
};


// --- Event Listeners Iniciales (al cargar el DOM) ---
const setupEventListeners = () => {
    // Estas funciones ya están definidas y expuestas en el ámbito global o son listeners.
    document.getElementById('open-modal-btn').addEventListener('click', openModal);
    document.getElementById('close-modal-btn').addEventListener('click', closeModal);
    document.getElementById('search-input').addEventListener('input', filterAppointments); 
    
    // Cierre del modal al hacer click fuera
    document.getElementById('new-appointment-modal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('new-appointment-modal')) {
            closeModal();
        }
    });

    // Renderizar la tabla inicial al cargar
    filterAppointments();
};

// Exposición de funciones globales (ya están en el código anterior, pero las confirmo aquí)
window.openModal = openModal;
window.closeModal = closeModal;
window.handleCancelAppointment = handleCancelAppointment;
window.handleFinalSubmit = handleFinalSubmit;
window.handleEditAppointment = handleEditAppointment;
window.goBack = goBack;
window.selectDate = selectDate;
window.selectDoctor = selectDoctor;
window.selectSlot = selectSlot;
window.selectSpecialty = selectSpecialty;

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', setupEventListeners);