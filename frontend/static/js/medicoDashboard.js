/*
 * Archivo: app.js
 * Ubicación recomendada en Flask: static/js/
 */

document.addEventListener("DOMContentLoaded", () => {
    // Inicialización: Pestañas
    const tabs = document.querySelectorAll(".tab");
    const tabContents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            // Desactiva todas las pestañas
            tabs.forEach(t => t.classList.remove("active"));
            // Activa la pestaña clickeada
            tab.classList.add("active");
            
            // Muestra el contenido correspondiente
            const target = tab.getAttribute("data-tab");
            tabContents.forEach(c => c.classList.remove("active"));
            document.getElementById(target).classList.add("active");
        });
    });

    // Inicialización: Diálogo de Cancelación (Modal)
    const cancelDialog = document.getElementById("cancel-dialog");
    const closeDialogBtn = document.getElementById("close-dialog");
    const confirmCancelBtn = document.getElementById("confirm-cancel");
    let selectedId = null;

    // Abrir el modal al hacer clic en 'Cancelar'
    document.querySelectorAll(".btn-cancel").forEach(btn => {
        btn.addEventListener("click", (e) => {
            // Obtener el ID del item a cancelar (del atributo data-id de la tarjeta más cercana)
            selectedId = e.target.closest(".card").dataset.id;
            cancelDialog.style.display = "flex"; // Muestra el modal
        });
    });

    // Cerrar el modal
    closeDialogBtn.addEventListener("click", () => {
        cancelDialog.style.display = "none";
    });

    // Lógica para confirmar la cancelación y realizar la petición al backend de Flask
    confirmCancelBtn.addEventListener("click", async () => {
        if (selectedId) {
            try {
                // Envía la petición POST al endpoint /cancel de Flask
                const response = await fetch("/cancel", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ id: selectedId })
                });

                // Asumiendo que la respuesta es exitosa (código 200)
                if (response.ok) {
                    // Elimina el elemento de la interfaz (DOM)
                    const elementToRemove = document.querySelector(`[data-id="${selectedId}"]`);
                    if (elementToRemove) {
                         elementToRemove.remove();
                    } else {
                        console.error("Error: No se encontró el elemento para eliminar.");
                    }
                } else {
                    console.error("Error al cancelar el item en el servidor:", response.statusText);
                    // Aquí podrías mostrar un mensaje de error en el UI
                }

            } catch (error) {
                console.error("Error de red al intentar cancelar:", error);
                // Aquí podrías mostrar un mensaje de error de conexión en el UI
            }

            // Oculta el modal en ambos casos
            cancelDialog.style.display = "none";
            selectedId = null; // Resetea el ID seleccionado
        }
    });
});