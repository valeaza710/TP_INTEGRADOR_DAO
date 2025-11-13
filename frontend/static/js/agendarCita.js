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
    specialtiesContainer.innerHTML = "<p>Cargando especialidades...</p>";

    try {
        const res = await fetch("/api/especialidades/");
        const data = await res.json();
        if (!data.success) throw new Error(data.error || "Error al obtener especialidades");

        specialtiesContainer.innerHTML = "";

        data.data.forEach(especialidad => {
            const card = document.createElement("div");
            card.className = "specialty-card";
            card.textContent = especialidad.nombre;
            card.onclick = () => selectSpecialty(especialidad.nombre, card);
            specialtiesContainer.appendChild(card);
        });
    } catch (err) {
        console.error("❌ Error cargando especialidades:", err);
        specialtiesContainer.innerHTML = "<p class='text-red-500'>Error al cargar especialidades.</p>";
    }
}

// --- 🔹 PASO 1: Seleccionar especialidad ---
function selectSpecialty(specialty, element) {
    selectedSpecialty = specialty;
    document.querySelectorAll(".specialty-card").forEach(card => card.classList.remove("selected"));
    element.classList.add("selected");
    selectedSpecialtyName.textContent = specialty;

    // Cargar doctores
    fetch(`/api/medicos/por_especialidad/${specialty}`)
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
    generateCalendarUI(new Date());
}

// --- 🔹 Volver atrás ---
function goBack(targetStepNumber) {
    showStep(`step${targetStepNumber}`);
    if (targetStepNumber === 1) {
        selectedDoctor = "all";
        selectedSpecialty = "";
        selectedDate = null;
    } else if (targetStepNumber === 2) {
        selectedDate = null;
        slotsContainer.innerHTML = '<div class="info-message">Por favor, selecciona una fecha.</div>';
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
    loadSlots();
}

function prevMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
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
        const slotsContainer = document.getElementById("slots");
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
    }
}

// --- 🔹 Seleccionar slot ---
function selectSlot(slot, button) {
    selectedSlot = slot;
    document.querySelectorAll(".slot-btn").forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    if (!document.getElementById("confirm-btn")) {
        const confirmBtn = document.createElement("button");
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
        alert("Por favor selecciona un horario.");
        return;
    }

    try {
        const response = await fetch("/api/turnos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                paciente_id: 1, // <- reemplazar con ID del usuario logueado
                doctor_id: selectedSlot.doctor_id || 1,
                fecha: selectedDate,
                hora: selectedSlot.time
            })
        });

        const data = await response.json();
        if (data.success) {
            alert("✅ Turno registrado correctamente");
            goBack(1);
        } else {
            alert("❌ Error al registrar el turno: " + (data.error || "Desconocido"));
        }
    } catch (error) {
        console.error("Error al registrar turno:", error);
        alert("Error al registrar turno.");
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
    loadSpecialties();
    generateCalendarUI(currentCalendarDate);

    // 🔹 Acción para el botón "X" de cerrar
    const closeBtn = document.querySelector(".close-btn");
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            window.location.href = "/home";
            // Volvemos al paso 1 y reseteamos los valores
            selectedSpecialty = null;
            selectedDoctor = null;
            selectedDate = null;
            selectedSlot = null;

            showStep("step1");
            document.getElementById("specialty-list").scrollIntoView({ behavior: "smooth" });
        });
    }

});

