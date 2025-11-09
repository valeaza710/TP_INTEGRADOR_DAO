document.addEventListener('DOMContentLoaded', () => {
    // 1. Seleccionar todos los botones de "Cancelar Cita"
    const cancelButtons = document.querySelectorAll('.cancel-btn');

    // 2. Iterar sobre los botones y añadir un "event listener" a cada uno
    cancelButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            // Obtener la tarjeta de cita padre
            const card = event.target.closest('.appointment-card');
            // Obtener el ID de la cita (p. ej., "1" o "2")
            const appointmentId = card.getAttribute('data-appointment-id');
            const doctorName = card.querySelector('.doctor-name').textContent;

            // Mostrar un mensaje de confirmación
            const confirmation = confirm(`¿Estás seguro de que quieres cancelar la cita con ${doctorName}? (ID: ${appointmentId})`);

            if (confirmation) {
                // Si el usuario confirma, simular la acción de cancelación.
                // En una aplicación real, aquí harías una petición AJAX (fetch) a Flask
                // para decirle al servidor que elimine la cita de la base de datos.
                
                console.log(`[JS] Solicitud de cancelación enviada para la Cita ID: ${appointmentId}`);

                // SIMULACIÓN: Eliminar visualmente la tarjeta de la interfaz
                card.style.opacity = '0.5';
                card.innerHTML = `<p style="text-align: center; color: #dc3545;">Cita con ${doctorName} Cancelada.</p>`;
                card.classList.add('cancelled');

            } else {
                console.log(`[JS] Cancelación de cita con ${doctorName} abortada.`);
            }
        });
    });

});