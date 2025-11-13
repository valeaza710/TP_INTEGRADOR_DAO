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
 */
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

// --- 🔹 PASO 1: CARGAR Y SELECCIONAR ESPECIALIDAD ---
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

function selectSpecialty(specialty, element) {
    selectedSpecialty = specialty;
    document.querySelectorAll(".specialty-card").forEach(card => card.classList.remove("selected"));
    element.classList.add("selected");
    selectedSpecialtyName.textContent = specialty;

    // Cargar doctores de esa especialidad
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
            showStep("step2");
        });
}

// --- 🔹 PASO 2: DOCTOR ---
function goToCalendar() {
    selectedDoctor = doctorSelect.value;
    showStep("step3");
    generateCalendarUI(new Date());
}

// --- 🔹 VOLVER ATRÁS ---
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

// --- 🔹 CALENDARIO ---
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

// --- 🔹 TURNOS DISPONIBLES ---
function loadSlots() {
    const date = dateInput.value;
    if (!date) return;

    fetch("/api/turnos/slots", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ specialty: selectedSpecialty, doctor: selectedDoctor, date })
    })
        .then(res => res.json())
        .then(slots => {
            slotsContainer.innerHTML = "";
            if (slots.length === 0) {
                slotsContainer.innerHTML = '<div class="info-message text-center py-8">No hay turnos disponibles para esta fecha.</div>';
                return;
            }

            slots.forEach(s => {
                const slotCard = document.createElement("button");
                slotCard.className = "slot-card";
                slotCard.innerHTML = `<strong>${s.time}</strong> - ${s.doctor}`;
                slotCard.onclick = () => confirmAppointment(s);
                slotsContainer.appendChild(slotCard);
            });
        });
}

// --- 🔹 CONFIRMAR TURNO ---
function confirmAppointment(slot) {
    const date = dateInput.value;
    const currentUserId = 1; // <- reemplazar con tu lógica real

    fetch("/api/turnos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            fecha: date,
            hora: slot.time,
            id_paciente: currentUserId,
            id_estado_turno: 1,
            id_horario_medico: slot.id_horario_medico
        })
    })
        .then(res => res.json())
        .then(data => {
            alert("✅ Cita agendada exitosamente");
        })
        .catch(err => {
            console.error("Error al agendar:", err);
            alert("❌ No se pudo agendar la cita");
        });
}

// --- 🔹 INICIALIZACIÓN ---
document.addEventListener('DOMContentLoaded', () => {
    showStep("step1");
    loadSpecialties(); // 👈 acá cargamos las especialidades desde tu BD
    generateCalendarUI(currentCalendarDate);
});
