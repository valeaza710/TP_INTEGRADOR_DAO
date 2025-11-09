let selectedSpecialty = "";
let selectedDoctor = "";

function selectSpecialty(specialty) {
  selectedSpecialty = specialty;
  document.getElementById("step1").classList.add("hidden");
  document.getElementById("step2").classList.remove("hidden");

  fetch(`/get_doctors/${specialty}`)
    .then(res => res.json())
    .then(doctors => {
      const select = document.getElementById("doctor-select");
      select.innerHTML = `<option value="all">Todos los médicos</option>`;
      doctors.forEach(d => {
        select.innerHTML += `<option value="${d}">${d}</option>`;
      });
    });
}

function goToCalendar() {
  selectedDoctor = document.getElementById("doctor-select").value;
  document.getElementById("step2").classList.add("hidden");
  document.getElementById("step3").classList.remove("hidden");
}

function goBack(step) {
  document.querySelectorAll(".step").forEach(s => s.classList.add("hidden"));
  document.getElementById(`step${step}`).classList.remove("hidden");
}

function loadSlots() {
  const date = document.getElementById("date-input").value;
  if (!date) return;

  fetch("/get_slots", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ specialty: selectedSpecialty, doctor: selectedDoctor, date })
  })
    .then(res => res.json())
    .then(slots => {
      const container = document.getElementById("slots");
      container.innerHTML = "";
      if (slots.length === 0) {
        container.innerHTML = "<p>No hay turnos disponibles para esta fecha.</p>";
        return;
      }
      slots.forEach(s => {
        const div = document.createElement("div");
        div.className = "slot";
        div.innerHTML = `<strong>${s.time}</strong> - ${s.doctor}<br><small>${s.location}</small>`;
        div.onclick = () => {
          alert(`Cita agendada con ${s.doctor} el ${date} a las ${s.time}`);
        };
        container.appendChild(div);
      });
    });
}
