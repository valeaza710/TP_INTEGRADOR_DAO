let selectedSpecialty = "";
let selectedDoctor = "";
let currentCalendarDate = new Date();
let selectedDate = null;

// Referencias a elementos UI clave
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

/**
 * Muestra el paso deseado y actualiza la UI.
 * @param {string} stepId - ID del paso a mostrar (e.g., "step1").
 */
function showStep(stepId) {
    [step1, step2, step3].forEach(step => {
        if (step) {
            step.classList.add("hidden");
        }
    });

    const targetStep = document.getElementById(stepId);
    if (targetStep) {
        targetStep.classList.remove("hidden");
    }

    // Actualizar Header y botón de Volver
    const stepNumber = parseInt(stepId.replace("step", ""));
    dialogDescription.textContent = descriptions[stepId];
    
    if (stepNumber > 1) {
        backButton.classList.remove("hidden");
        backButton.setAttribute("onclick", `goBack(${stepNumber - 1})`);
    } else {
        backButton.classList.add("hidden");
    }
}


// --- PASO 1: SELECCIONAR ESPECIALIDAD ---
function selectSpecialty(specialty, element) {
    selectedSpecialty = specialty;
    
    // Marcar la tarjeta seleccionada (para el CSS)
    document.querySelectorAll(".specialty-card").forEach(card => card.classList.remove("selected"));
    element.classList.add("selected");

    selectedSpecialtyName.textContent = specialty;
    
    // Cargar Doctores
    fetch(`/api/doctores/${specialty}`) 
        .then(res => res.json())
        .then(doctors => {
            doctorSelect.innerHTML = `<option value="all">Todos los médicos de la especialidad</option>`;
            doctors.forEach(d => {
                doctorSelect.innerHTML += `<option value="${d}">${d}</option>`;
            });
            showStep("step2");
        })
        .catch(error => {
            console.error("Error al cargar doctores:", error);
            // Mostrar mensaje de error o continuar al paso 2 sin doctores cargados
            showStep("step2");
        });
}


// --- PASO 2: SELECCIÓN DE DOCTOR Y AVANCE ---
function goToCalendar() {
    selectedDoctor = doctorSelect.value;
    showStep("step3");
    
    // Generar la visualización inicial del calendario (solo si es necesario)
    generateCalendarUI(new Date()); 
}


// --- PASO 3: NAVEGACIÓN Y CALENDARIO ---
function goBack(targetStepNumber) {
    showStep(`step${targetStepNumber}`);
    
    // Limpiar estados al regresar (opcional)
    if (targetStepNumber === 1) {
        selectedDoctor = "all";
        selectedSpecialty = "";
        selectedDate = null;
    } else if (targetStepNumber === 2) {
        selectedDate = null;
        slotsContainer.innerHTML = '<div class="info-message">Por favor, selecciona una fecha.</div>';
    }
}

// Lógica básica para simular un calendario visual
function generateCalendarUI(currentDate) {
    const monthLabel = document.getElementById("month-label");
    const datesGrid = document.getElementById("calendar-dates-grid");
    
    // Simulación: establecer la fecha actual en el input
    // Para ver los días y que tu CSS funcione, esto debe ser dinámico.
    // Para simplificar, solo mostramos el mes y el input date sigue controlando la fecha real.
    
    monthLabel.textContent = currentDate.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
    
    // Implementación más compleja del calendario visual va aquí.
    // Por ahora, solo asegúrate de que el contenedor de la cuadrícula no esté vacío
    if (datesGrid) {
        datesGrid.innerHTML = `
            <div class="date-item date-padding">27</div>
            <div class="date-item date-padding">28</div>
            <div class="date-item date-padding">29</div>
            <div class="date-item date-padding">30</div>
            <div class="date-item">1</div>
            <div class="date-item">2</div>
            <div class="date-item">3</div>
            <div class="date-item selected">4</div>
            <div class="date-item">5</div>
            <div class="date-item">6</div>
            <div class="date-item">7</div>
            <div class="date-item">8</div>
            <div class="date-item">9</div>
            <div class="date-item">10</div>
            <div class="date-item">...</div>
        `;
    }
}


// --- PASO 3: CARGAR TURNOS ---
function loadSlots() {
    const date = dateInput.value;
    if (!date) return;

    // Formatear la fecha para la visualización del título
    const dateParts = date.split('-');
    const formattedDate = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]).toLocaleDateString('es-ES', { day: 'numeric', month: 'long' });
    slotsDateDisplay.textContent = formattedDate;

    // Llamada a la API de turnos (POST)
    fetch("/api/turnos", { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ specialty: selectedSpecialty, doctor: selectedDoctor, date: date })
    })
    .then(res => res.json())
    .then(slots => {
        slotsContainer.innerHTML = "";
        
        if (slots.length === 0) {
            slotsContainer.innerHTML = '<div id="no-slots-message" class="info-message text-center py-8">No hay turnos disponibles para esta fecha.</div>';
            return;
        }

        slots.forEach(s => {
            const slotCard = document.createElement("button");
            slotCard.className = "slot-card w-full p-3 border border-border rounded-lg text-left group";
            slotCard.innerHTML = `
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="icon-placeholder w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                            <i class="fas fa-user h-5 w-5 text-primary"></i>
                        </div>
                        <div class="slot-details">
                            <strong>${s.time}</strong>
                            <p class="doctor-name">${s.doctor}</p>
                            <span class="location hidden">${s.location}</span>
                        </div>
                    </div>
                </div>
            `;
            slotCard.onclick = () => confirmAppointment(s);
            slotsContainer.appendChild(slotCard);
        });
    })
    .catch(error => {
        console.error("Error al cargar turnos:", error);
        slotsContainer.innerHTML = '<div class="error-message">Error al cargar turnos. Intente de nuevo.</div>';
    });
}

function confirmAppointment(slot) {
    // 1. Limpiar selecciones anteriores y marcar la actual
    document.querySelectorAll(".slot-card").forEach(card => card.classList.remove("selected"));
    event.currentTarget.classList.add("selected");

    const date = dateInput.value;
    
    // 2. Aquí iría la llamada final para AGENDAR
    fetch("/api/agendar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            specialty: selectedSpecialty, 
            doctor: slot.doctor, 
            date: date, 
            time: slot.time,
            location: slot.location 
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(`Cita agendada exitosamente: ${data.message}`);
        // Opcional: Cerrar la modal o redirigir
    })
    .catch(error => {
        console.error("Error al confirmar cita:", error);
        alert("Error al confirmar la cita. Intente de nuevo.");
    });
}

function generateCalendarUI(date) {
    const monthLabel = document.getElementById("month-label");
    const datesGrid = document.getElementById("calendar-dates-grid");
    datesGrid.innerHTML = ""; // Limpiar cuadrícula

    const year = date.getFullYear();
    const month = date.getMonth(); // 0-11
    
    // Configuración regional
    const locale = 'es-ES';

    // 1. Etiqueta del Mes
    monthLabel.textContent = date.toLocaleDateString(locale, { month: 'long', year: 'numeric' });

    // 2. Determinar el primer día del mes (0 = Domingo, 1 = Lunes)
    const firstDayOfMonth = new Date(year, month, 1);
    // getDay() devuelve 0 (domingo) a 6 (sábado). Queremos 0 para Lunes.
    let startingDayOfWeek = firstDayOfMonth.getDay();
    // Ajuste para que Lunes sea 0 y Domingo sea 6
    startingDayOfWeek = (startingDayOfWeek === 0) ? 6 : startingDayOfWeek - 1; 
    
    // 3. Obtener el número de días en el mes
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // 4. Días de relleno (del mes anterior)
    let paddingDays = startingDayOfWeek;
    for (let i = 0; i < paddingDays; i++) {
        const div = document.createElement("div");
        div.className = "date-item date-padding";
        datesGrid.appendChild(div);
    }

    // 5. Días del Mes Actual
    const today = new Date();
    today.setHours(0, 0, 0, 0); 

    for (let day = 1; day <= daysInMonth; day++) {
        const div = document.createElement("div");
        const dayDate = new Date(year, month, day);
        const dayDateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        
        div.textContent = day;
        div.className = "date-item";
        div.setAttribute('data-date', dayDateString);
        
        // Determinar si es día pasado o si está seleccionado
        const isPastDay = dayDate < today;
        const isSelected = selectedDate && dayDateString === selectedDate;

        if (isPastDay) {
            div.classList.add("past-day");
        } else {
            div.onclick = () => selectDay(dayDateString, div);
            
            if (isSelected) {
                div.classList.add("selected");
            }
        }
        
        datesGrid.appendChild(div);
    }
}

/**
 * Maneja la selección de un día en el calendario.
 */
function selectDay(dateString, element) {
    if (element.classList.contains("past-day")) return;

    // 1. Limpiar la selección anterior
    document.querySelectorAll(".date-item").forEach(d => d.classList.remove("selected"));
    
    // 2. Aplicar la nueva selección (Clase CSS)
    element.classList.add("selected");
    
    // 3. Almacenar la fecha seleccionada
    selectedDate = dateString; 
    
    // 4. Actualizar el input type="date" oculto
    document.getElementById("date-input").value = dateString; 
    
    // 5. Cargar los turnos
    loadSlots();
}

/**
 * Navega al mes anterior y regenera el calendario.
 */
function prevMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
    generateCalendarUI(currentCalendarDate);
}

/**
 * Navega al mes siguiente y regenera el calendario.
 */
function nextMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
    generateCalendarUI(currentCalendarDate);
}

// ... (El resto de tus funciones: loadSlots, confirmAppointment) ...


// Inicializar la aplicación para mostrar el primer paso y el calendario
document.addEventListener('DOMContentLoaded', () => {
    showStep("step1");
    // Inicializa el calendario al cargar
    generateCalendarUI(currentCalendarDate); 
});
