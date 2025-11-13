let currentCalendarDate = new Date();
let selectedDate = null;
let selectedSlot = null;
let selectedSpecialty = null;
let selectedDoctor = null;

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
    // Reemplazamos alert() por console.log/error, ya que alert está prohibido.
    if (isError) {
        console.error("Mensaje de Error:", message);
        // Si necesitas un modal para el usuario, debes implementarlo en HTML/CSS.
        // Por ahora, solo se usa la consola.
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
    // NOTA: Esta función no se usa si las especialidades se cargan con Jinja en el HTML (como en tu 'agendarCita.html'). 
    // Mantengo la función si tienes la intención de usarla.
    const specialtiesContainer = document.getElementById("specialty-list");
    // Verificación para evitar sobreescribir el contenido de Jinja
    if (specialtiesContainer && specialtiesContainer.children.length === 0) {
        specialtiesContainer.innerHTML = "<p>Cargando especialidades...</p>";

        try {
            const res = await fetch("/api/especialidades/");
            const data = await res.json();
            if (!data.success) throw new Error(data.error || "Error al obtener especialidades");

            specialtiesContainer.innerHTML = "";

            data.data.forEach(especialidad => {
                const card = document.createElement("button"); // Usar button para accesibilidad
                card.className = "specialty-card p-4 border border-border rounded-lg text-left group";
                card.setAttribute('data-specialty', especialidad.nombre);
                card.innerHTML = `<p class="font-medium text-foreground">${especialidad.nombre}</p>`;
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
    // El ID de la especialidad sería mejor aquí, pero usamos el nombre por simplicidad de la URL
    fetch(`/api/medicos/por_especialidad/${encodeURIComponent(specialty)}`)
        .then(res => res.json())
        .then(response => {
            const doctors = response.data || [];
            const doctorSelect = document.getElementById("doctor-select");
            doctorSelect.innerHTML = '<option value="all">Todos los médicos de la especialidad</option>';

            doctors.forEach(d => {
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
    // Aseguramos que el calendario se renderice con la fecha actual al entrar al paso 3
    generateCalendarUI(currentCalendarDate); 
}

// --- 🔹 Volver atrás ---
function goBack(targetStepNumber) {
    showStep(`step${targetStepNumber}`);
    if (targetStepNumber === 1) {
        selectedDoctor = "all";
        selectedSpecialty = null; // Usar null para resetear
    } else if (targetStepNumber === 2) {
        selectedDate = null;
        slotsContainer.innerHTML = '<div class="info-message">Por favor, selecciona una fecha.</div>';
        document.getElementById("confirm-btn")?.remove(); // Remover botón de confirmación
    }
}

// --- 🔹 Generar calendario ---
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
        // Formato YYYY-MM-DD
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
    document.getElementById("date-input").value = dateString; // Sincroniza el input oculto
    slotsDateDisplay.textContent = new Date(dateString).toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    loadSlots();
}

function prevMonth() {
    // Solo permitir ir al pasado si no se está en el mes actual
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const newDate = new Date(currentCalendarDate);
    newDate.setMonth(newDate.getMonth() - 1);

    if (newDate.getMonth() < currentMonth && newDate.getFullYear() <= currentYear) {
        // No permitir ir al mes pasado si es el mes actual
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
        // Limpieza de turno anterior y botón de confirmación
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
            btn.className = "slot-btn";
            btn.textContent = `${slot.time} - ${slot.doctor}`;
            btn.onclick = () => selectSlot(slot, btn);
            slotsContainer.appendChild(btn);
        });
    } catch (error) {
        console.error("Error al cargar turnos:", error);
        slotsContainer.innerHTML = `<p class="text-sm text-red-500">Error al cargar turnos. Intente de nuevo.</p>`;
    }
}

// --- 🔹 Seleccionar slot ---
function selectSlot(slot, button) {
    selectedSlot = slot;
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

// --- 🔹 Registrar turno real ---
async function registerTurno() {
    if (!selectedSlot || !selectedDate) {
        showMessage("Por favor selecciona un horario.", true);
        return;
    }

    // FIX: Convertir la variable global (que ahora es una cadena) a un número entero.
    const pacienteId = parseInt(GLOBAL_PACIENTE_ID, 10); 

    if (pacienteId === 0 || isNaN(pacienteId)) {
        showMessage("Error: No se detecta un paciente logueado o el ID no es válido. Redirigiendo a login...", true);
        window.location.href = "/login"; // Redirigir si no hay ID válido
        return;
    }

    try {
        const response = await fetch("/api/turnos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id_paciente: pacienteId, 
                id_turno: selectedSlot.id_turno,
                doctor_id: selectedSlot.doctor_id || 1, // Usar doctor_id del slot si existe
                fecha: selectedDate,
                hora: selectedSlot.time
            })
        });

        const data = await response.json();
        if (data.success) {
            showMessage("✅ Turno registrado correctamente");
            // Redirigir al home después de un registro exitoso, o cerrar el modal
            window.location.href = "/home"; 
        } else {
            showMessage("❌ Error al registrar el turno: " + (data.error || "Desconocido"), true);
        }
    } catch (error) {
        console.error("Error al registrar turno:", error);
        showMessage("Error al registrar turno.", true);
    }
}

// --- 🔹 REDIRECCIÓN AL CERRAR MODAL ---

function setupCloseButton() {
    // 1. Obtener el botón de cerrar (la cruz 'x')
    const closeButton = document.querySelector('.close-btn');

    if (closeButton) {
        // 2. Agregar el listener para redirigir
        closeButton.addEventListener('click', function(event) {
            event.preventDefault(); 
            
            // 3. Redirigir a la URL de home
            window.location.href = '/home'; 
            
            // Alternativa: Si solo quieres cerrar el modal sin recargar
            // Nota: En este contexto, volver a /home es lo que pediste.
        });
    }
}

// 4. Llamar a la nueva función en el DOMContentLoaded

document.addEventListener('DOMContentLoaded', () => {
    showStep("step1");
    loadSpecialties(); 
    generateCalendarUI(currentCalendarDate);
    
    // 🚨 Nueva inicialización
    setupCloseButton(); 

// --- 🔹 Inicialización ---
document.addEventListener('DOMContentLoaded', () => {
    showStep("step1");
    // Ya no llamamos loadSpecialties() porque las especialidades vienen en el HTML por Jinja
    generateCalendarUI(currentCalendarDate);


    // 🔹 Acción para el botón "X" de cerrar
    const closeBtn = document.querySelector(".close-btn");
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            window.location.href = "/home";
        });
    }
});

