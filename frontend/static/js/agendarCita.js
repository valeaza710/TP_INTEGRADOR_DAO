let currentCalendarDate = new Date();
let selectedDate = null;
let selectedSlot = null;
let selectedSpecialty = null;
let selectedDoctor = null;

// --- 🎯 LÓGICA DE ID DEL PACIENTE (SOLUCIÓN) 🎯 ---
let pacienteId = null; 

// 1. Obtener ID de la URL (si viene de /agendar?pacienteId=4)
const urlParams = new URLSearchParams(window.location.search);
const pacienteIdFromUrl = urlParams.get('pacienteId');

// 2. Intentar usar la URL, sino la variable global de Jinja (GLOBAL_PACIENTE_ID)
if (pacienteIdFromUrl) {
    pacienteId = parseInt(pacienteIdFromUrl, 10); 
} else if (typeof GLOBAL_PACIENTE_ID_FROM_SESSION !== 'undefined' && GLOBAL_PACIENTE_ID_FROM_SESSION !== '') {
    // 🚨 NOTA: Se usa 'GLOBAL_PACIENTE_ID_FROM_SESSION' según tu HTML.
    pacienteId = parseInt(GLOBAL_PACIENTE_ID_FROM_SESSION, 10);
}
// ---------------------------------------------------

// --- 🔹 Referencias a elementos UI ---
const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");
const backButton = document.getElementById("back-button");
const dialogDescription = document.getElementById("dialog-description");
const selectedSpecialtyName = document.getElementById("selected-specialty-name");
const doctorSelect = document.getElementById("doctor-select");
const dateInput = document.getElementById("date-input");
const slotsContainer = document.getElementById("slots");
const slotsDateDisplay = document.getElementById("slots-date-display");

const descriptions = {
    "step1": "Selecciona una especialidad médica",
    "step2": "Filtra por médico (opcional)",
    "step3": "Selecciona fecha y turno disponible"
};

// --- FUNCIÓN DE UTILIDAD: Mostrar mensaje modal o error en consola ---
function showMessage(message, isError = false) {
    if (isError) {
        console.error("Mensaje de Error:", message);
    } else {
        console.log("Mensaje:", message);
    }
}


// --- 🔹 Mostrar paso ---
function showStep(stepId) {
    [step1, step2, step3].forEach(step => step?.classList.add("hidden"));
    const targetStep = document.getElementById(stepId);
    if (targetStep) targetStep.classList.remove("hidden");

    const stepNumber = parseInt(stepId.replace("step", ""));
    dialogDescription.textContent = descriptions[stepId];

    if (stepNumber > 1) {
        backButton.classList.remove("hidden");
        backButton.setAttribute("onclick", `goBack(${stepNumber - 1})`);
    } else {
        backButton.classList.add("hidden");
    }
}

// --- 🔹 PASO 1: Cargar Especialidades ---
async function loadSpecialties() {
    const specialtiesContainer = document.getElementById("specialty-list");
    // Se elimina la verificación 'children.length === 0' para forzar la carga si es necesario
    if (specialtiesContainer) { 
        specialtiesContainer.innerHTML = "<p>Cargando especialidades...</p>";

        try {
            const res = await fetch("/api/especialidades/");
            const data = await res.json();
            
            // Asume que la respuesta tiene la estructura: { data: [...] }
            const especialidades = data.data || data; 

            if (!especialidades || especialidades.length === 0) throw new Error(data.error || "Error al obtener especialidades");

            specialtiesContainer.innerHTML = "";

            especialidades.forEach(especialidad => {
                const card = document.createElement("button");
                card.className = "specialty-card p-4 border border-border rounded-lg text-left group";
                // Asume que la especialidad tiene 'nombre' y 'id' (si usas ID para la API)
                card.setAttribute('data-specialty', especialidad.nombre); 
                card.innerHTML = `<p class="font-medium text-foreground">${especialidad.nombre}</p>`;
                
                // Si la API de médicos espera el ID, es mejor pasarlo como primer argumento.
                // Si la API de médicos espera el nombre, mantenemos 'especialidad.nombre'.
                // Mantenemos 'especialidad.nombre' como en tu original:
                card.onclick = () => selectSpecialty(especialidad.nombre, card);
                specialtiesContainer.appendChild(card);
            });
        } catch (err) {
            console.error("❌ Error cargando especialidades:", err);
            specialtiesContainer.innerHTML = "<p class='text-red-500'>Error al cargar especialidades.</p>";
        }
    }
}


// --- 🔹 PASO 1: Seleccionar especialidad ---
function selectSpecialty(specialty, element) {
    selectedSpecialty = specialty;
    document.querySelectorAll(".specialty-card").forEach(card => card.classList.remove("selected"));
    element.classList.add("selected");
    selectedSpecialtyName.textContent = specialty;

    // Cargar doctores
    // La API usa el nombre (o el ID si 'specialty' es el ID)
    fetch(`/api/medicos/por_especialidad/${encodeURIComponent(specialty)}`)
        .then(res => res.json())
        .then(response => {
            // Se asume que la respuesta del backend tiene la forma { data: [...] }
            const doctors = response.data || [];
            const doctorSelect = document.getElementById("doctor-select");
            doctorSelect.innerHTML = '<option value="all">Todos los médicos de la especialidad</option>';

            doctors.forEach(d => {
                // Se asume que el objeto doctor tiene 'id', 'nombre' y 'apellido'
                doctorSelect.innerHTML += `<option value="${d.id}">${d.nombre} ${d.apellido}</option>`;
            });

            showStep("step2");
        })
        .catch(error => console.error("Error al cargar doctores:", error));
}

// --- 🔹 PASO 2: Ir al calendario ---
function goToCalendar() {
    selectedDoctor = doctorSelect.value;
    showStep("step3");
    generateCalendarUI(currentCalendarDate); 
}

// --- 🔹 Volver atrás ---
function goBack(targetStepNumber) {
    showStep(`step${targetStepNumber}`);
    if (targetStepNumber === 1) {
        selectedDoctor = "all";
        selectedSpecialty = null;
    } else if (targetStepNumber === 2) {
        selectedDate = null;
        slotsContainer.innerHTML = '<div class="info-message">Por favor, selecciona una fecha.</div>';
        document.getElementById("confirm-btn")?.remove();
    }
}

// --- 🔹 Generar calendario (sin cambios) ---
function generateCalendarUI(date) {
    const monthLabel = document.getElementById("month-label");
    const datesGrid = document.getElementById("calendar-dates-grid");
    datesGrid.innerHTML = "";

    const year = date.getFullYear();
    const month = date.getMonth();
    const locale = 'es-ES';
    monthLabel.textContent = date.toLocaleDateString(locale, { month: 'long', year: 'numeric' });

    const firstDayOfMonth = new Date(year, month, 1);
    let startingDayOfWeek = firstDayOfMonth.getDay();
    startingDayOfWeek = (startingDayOfWeek === 0) ? 6 : startingDayOfWeek - 1;
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < startingDayOfWeek; i++) {
        const div = document.createElement("div");
        div.className = "date-item date-padding";
        datesGrid.appendChild(div);
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    for (let day = 1; day <= daysInMonth; day++) {
        const div = document.createElement("div");
        const dayDate = new Date(year, month, day);
        const dayDateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`; 
        div.textContent = day;
        div.className = "date-item";
        div.setAttribute('data-date', dayDateString);

        const isPastDay = dayDate < today;
        const isSelected = selectedDate && dayDateString === selectedDate;

        if (isPastDay) {
            div.classList.add("past-day");
        } else {
            div.onclick = () => selectDay(dayDateString, div);
            if (isSelected) div.classList.add("selected");
        }

        datesGrid.appendChild(div);
    }
}

function selectDay(dateString, element) {
    if (element.classList.contains("past-day")) return;
    document.querySelectorAll(".date-item").forEach(d => d.classList.remove("selected"));
    element.classList.add("selected");
    selectedDate = dateString;
    document.getElementById("date-input").value = dateString;
    slotsDateDisplay.textContent = new Date(dateString).toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    loadSlots();
}

function prevMonth() {
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const newDate = new Date(currentCalendarDate);
    newDate.setMonth(newDate.getMonth() - 1);

    if (newDate.getMonth() < currentMonth && newDate.getFullYear() <= currentYear) {
        return;
    }

    currentCalendarDate = newDate;
    generateCalendarUI(currentCalendarDate);
}

function nextMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
    generateCalendarUI(currentCalendarDate);
}

// --- 🔹 Consultar turnos disponibles (slots) ---
async function loadSlots() {
    if (!selectedDate || !selectedSpecialty) return;

    try {
        selectedSlot = null;
        document.getElementById("confirm-btn")?.remove();
        slotsContainer.innerHTML = '<div class="info-message">Cargando turnos...</div>';

        const response = await fetch("/api/turnos/slots", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                specialty: selectedSpecialty,
                doctor: selectedDoctor === "all" ? null : selectedDoctor,
                date: selectedDate
            })
        });

        if (!response.ok) throw new Error("Error al consultar turnos disponibles");

        const slots = await response.json();
        slotsContainer.innerHTML = "";

        if (!slots || slots.length === 0) {
            slotsContainer.innerHTML = `<p class="text-sm text-muted-foreground">No hay turnos disponibles para esta fecha.</p>`;
            return;
        }

        slots.forEach(slot => {
            const btn = document.createElement("button");
            // 🚨 Cambiado a slot-card para que coincida con tu CSS
            btn.className = "slot-btn"; 
            
            // 🚨 Estructura interna para usar los detalles del CSS (slot-details, icon-placeholder)
            btn.innerHTML = `
                <div class="icon-placeholder"><i class="fas fa-clock"></i></div>
                <div class="slot-details">
                    <strong>${slot.time}</strong>
                    <span class="doctor-name">${slot.doctor}</span>
                </div>
            `;
            
            btn.onclick = () => selectSlot(slot, btn);
            slotsContainer.appendChild(btn);
        });
    } catch (error) {
        console.error("Error al cargar turnos:", error);
        slotsContainer.innerHTML = `<p class="text-sm text-red-500">Error al cargar turnos. Intente de nuevo.</p>`;
    }
}

// --- 🔹 Seleccionar slot (AGREGADA UX: MARCAR CON CLASE 'active') ---
function selectSlot(slot, button) {
    selectedSlot = slot;
    console.log(selectedSlot);
    // 🚨 Agregado para marcar visualmente el slot seleccionado
    document.querySelectorAll(".slot-btn").forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    let confirmBtn = document.getElementById("confirm-btn");
    if (!confirmBtn) {
        confirmBtn = document.createElement("button");
        confirmBtn.id = "confirm-btn";
        confirmBtn.textContent = "Confirmar Turno";
        confirmBtn.className = "btn-primary w-full mt-4";
        confirmBtn.onclick = registerTurno;
        document.getElementById("slots-container").appendChild(confirmBtn);
    }
}
// --- 🔹 Función de redirección simple (NECESARIO PARA EL BOTÓN DEL MODAL) ---
function redirectToHome() {
    // Redirige al home del paciente 
    window.location.href = `/home/${pacienteId}`; 
}

// --- 🔹 Mostrar Modal de Confirmación (NECESARIO PARA UX) ---
function showConfirmationModal(isSuccess, title, message) {
    const modal = document.getElementById("confirmation-modal");
    if (!modal) {
        showMessage("Error: No se encontró el elemento 'confirmation-modal'. Asegúrate de agregarlo al HTML.", true);
        redirectToHome();
        return;
    }
    
    const modalTitle = document.getElementById("modal-title");
    const modalMessage = document.getElementById("modal-message");

    modalTitle.textContent = title;
    modalMessage.textContent = message;

    if (isSuccess) {
        modalTitle.classList.remove("text-red-600");
        modalTitle.classList.add("text-green-600");
        document.getElementById("modal-close-btn").textContent = "Volver a la Agenda";
    } else {
        modalTitle.classList.remove("text-green-600");
        modalTitle.classList.add("text-red-600");
        document.getElementById("modal-close-btn").textContent = "Cerrar";
    }

    modal.classList.remove("hidden");
    
    // Ocultar el contenido principal para enfocar en el modal
    document.getElementById("slots-container")?.classList.add("hidden"); 
}


// --- 🔹 Registrar turno real (CORREGIDA LÓGICA DE ÉXITO Y MODAL) ---
async function registerTurno() {
    if (!selectedSlot || !selectedDate) {
        showMessage("Por favor selecciona un horario.", true);
        return;
    }

    // ✅ La variable global 'pacienteId' se usa aquí.
    const pacienteIdFinal = pacienteId; 

    if (isNaN(pacienteIdFinal) || pacienteIdFinal === null || pacienteIdFinal <= 0) {
        showMessage("Error: No se detecta un paciente logueado o el ID no es válido. Redirigiendo a home...", true);
        window.location.href = "/home";
        return;
    }
    
    // Deshabilitar el botón mientras se procesa
    const confirmBtn = document.getElementById("confirm-btn");
    confirmBtn.disabled = true;
    confirmBtn.textContent = "Procesando...";

    try {
        const response = await fetch("/api/turnos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id_paciente: pacienteIdFinal, 
                id_turno: selectedSlot.id_turno,
                doctor_id: selectedSlot.doctor_id || 1, 
                fecha: selectedDate,
                hora: selectedSlot.time
            })
        });

        console.log("Datos a enviar:", {
                id_paciente: pacienteIdFinal, 
                id_turno: selectedSlot.id_turno, 
                doctor_id: selectedSlot.doctor_id, 
                fecha: selectedDate,
                hora: selectedSlot.time
            });

        const data = await response.json();
        
        // 🚨 CORRECCIÓN CLAVE: Verificar el código de estado HTTP 201
        if (response.status === 201) { 
            // 1. Mostrar el modal de éxito 
            showConfirmationModal(true, "Turno Registrado Exitosamente", "Tu cita ha sido confirmada. Revisa tu agenda.");
            
            // 2. No redirigimos aquí. El botón en el modal lo hace.
            confirmBtn.textContent = "¡Listo!";
            return; 

        } else if (response.status === 400) {
            // Error 400 (Bad Request): "Turno no disponible" u otros errores de validación
            showMessage("❌ Error al registrar el turno: " + (data.error || "El turno ya no está disponible."), true);
        } else {
            // Manejar otros errores (404, 500, etc.)
            showMessage("❌ Error al registrar el turno: " + (data.error || "Error desconocido en el servidor."), true);
        }

    } catch (error) {
        console.error("Error al registrar turno:", error);
        showMessage("Error de conexión o al procesar la solicitud.", true);
    } finally {
        // Habilitar el botón de nuevo solo si NO fue exitoso
        if (response?.status !== 201) {
             confirmBtn.disabled = false;
             confirmBtn.textContent = "Confirmar Turno";
        }
    }
}

// --- 🔹 Inicialización (CORREGIDA) ---
document.addEventListener('DOMContentLoaded', () => {
    showStep("step1");
    
    // 💥 CORRECCIÓN CRUCIAL: Se activa la carga de especialidades
    loadSpecialties(); 
    
    generateCalendarUI(currentCalendarDate);

    // 🔹 Acción para el botón "X" de cerrar
    const closeBtn = document.querySelector(".close-btn");
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            // ✅ CORRECCIÓN SINTÁCTICA: Quitar el doble punto y coma y usar la global 'pacienteId'
            window.location.href = `/home/${pacienteId}`; 
        });
    }
});
