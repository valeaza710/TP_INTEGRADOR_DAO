// ====================================================
// Gestor Administrador - Conexión real con Flask API
// ====================================================

document.addEventListener("DOMContentLoaded", () => {

    // --- MAPAS DE CONFIGURACIÓN ---
    const TAB_HEADERS = {
        pacientes: ['Nombre', 'Apellido', 'DNI', 'Teléfono', 'Dirección'], 
        medicos: ['Matrícula', 'Nombre', 'Apellido'],          
        especialidades: ['ID', 'Nombre', ''], 
        enfermedades: ['ID', 'Nombre', 'Descripción'],
    };

    const TAB_ATTRIBUTES = {
        pacientes: ['nombre', 'apellido', 'dni', 'telefono', 'direccion'], 
        medicos: ['matricula', 'nombre', 'apellido'],
        especialidades: ['id', 'nombre'],
        enfermedades: ['id', 'nombre','descripcion'],
    };

// ... (El resto del código dentro de DOMContentLoaded) ...
    
    // -----------------------
    // CONFIGURACIÓN BASE
    // -----------------------
    const API_URLS = {
        pacientes: "/api/pacientes",
        medicos: "/api/medicos",
        especialidades: "/api/especialidades",
        enfermedades: "/api/enfermedades"
    };

    window.currentTab = "pacientes";
    let isEditing = false;
    let editingId = null;

    // -----------------------
    // CARGAR DATOS
    // -----------------------
    async function fetchData(resource) {
        try {
            const res = await fetch(`${API_URLS[resource]}/`);
            const json = await res.json();
            if (!json.success) throw new Error(json.error);
            return json.data;
        } catch (err) {
            console.error(err);
            showToast(`Error al obtener ${resource}`, "error");
            return [];
        }
    }

    // -----------------------
    // CAMBIO DE PESTAÑA
    // -----------------------
    window.changeTab = async function(tabName) {
        currentTab = tabName;

        // 1. Actualizar estilos de pestaña y título (Mismo que antes)
        document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
        document.getElementById(`${tabName}-tab`).classList.add("active");
        
        const displayTitles = {
            pacientes: 'Gestión de Pacientes',
            medicos: 'Gestión de Médicos',
            especialidades: 'Gestión de Especialidades',
            enfermedades: 'Gestión de Enfermedades'
        };
        document.getElementById("table-title").textContent = displayTitles[tabName] || tabName.toUpperCase();

        // 2. ***ACTUALIZAR ENCABEZADOS DE LA TABLA***
        const headers = TAB_HEADERS[tabName] || [];
        
        // El máximo de columnas de datos es 5
        for (let i = 0; i < 5; i++) {
            const headerElement = document.getElementById(`header-col-${i + 1}`);
            if (headerElement) {
                // Asigna el nombre, o deja vacío si no existe
                headerElement.textContent = headers[i] || ''; 
                
                // Muestra la columna si tiene un encabezado o si es una de las 2 primeras (mínimo)
                if (headers[i] || i < 2) { 
                    headerElement.style.display = 'table-cell';
                } else {
                    headerElement.style.display = 'none'; // Oculta si no hay encabezado
                }
            }
        }
        
        // 3. Cargar datos
        const tbody = document.getElementById("table-body");
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4">Cargando...</td></tr>`; // Colspan ahora es 6 (5 datos + 1 acción)

        const data = await fetchData(tabName);

        tbody.innerHTML = data.length
            ? data.map(item => renderRow(item, tabName)).join("") 
            : `<tr><td colspan="6" class="text-center py-4">No hay registros</td></tr>`;
    };

    // -----------------------
    // RENDERIZAR FILA
    // -----------------------
    function renderRow(item, type) {
            const attributes = TAB_ATTRIBUTES[type] || [];
        
        // Generar las celdas de datos (<td>)
        const cols = attributes
            .map(attr => {
                let value = item[attr];
                
                // Lógica especial para 'pacientes' para nombre completo si decides usarla
                // if (type === 'pacientes' && attr === 'nombre_completo') { ... }

                // Todas las celdas de datos deben tener px-6 py-4 y text-left/text-sm
                return `<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${value || "N/A"}</td>`;
            })
            .join("");

        // NOTA: No necesitamos rellenar con celdas ocultas (emptyCols) si la tabla está bien definida.
        // Simplemente pegamos las columnas de datos y luego la columna de Acciones.
        
        return `
            <tr>
                ${cols}
                
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"> 
                    <button onclick="editItem(${item.id})" class="text-blue-500">✏️</button>
                    <button onclick="deleteItem(${item.id})" class="text-red-500 ml-2">🗑️</button>
                </td>
            </tr>
        `;
    }

    // -----------------------
    // MODAL FORMULARIO
    // -----------------------
    window.openFormModal = function(type, title, data = {}) {
        isEditing = !!data.id;
        editingId = data.id || null;

        const modal = document.getElementById("form-modal");
        document.getElementById("form-title").textContent = title;

        document.getElementById("data-form").innerHTML = generateFormFields(type, data);
        modal.classList.remove("hidden");
    };

    window.closeFormModal = function() {
        document.getElementById("form-modal").classList.add("hidden");
        isEditing = false;
        editingId = null;
    };

    function generateFormFields(type, data) {
        const fieldsMap = {
            pacientes: ["nombre", "apellido", "dni", "telefono", "direccion"],
            medicos: ["nombre", "apellido", "matricula"],
            especialidades: ["nombre"],
            enfermedades: ["nombre", "descripcion"]
        };
        const fields = fieldsMap[type] || [];
        return fields.map(f => `
            <label class="block text-sm font-medium">${f}</label>
            <input type="text" name="${f}" value="${data[f] || ""}"
                   class="w-full border rounded p-2" required />
        `).join("");
    }

    // -----------------------
    // GUARDAR REGISTRO
    // -----------------------
    document.getElementById("modal-save-btn").addEventListener("click", async () => {
        const form = document.getElementById("data-form");
        const formData = Object.fromEntries(new FormData(form).entries());
        const method = isEditing ? "PUT" : "POST";
        const url = isEditing ? `${API_URLS[currentTab]}/${editingId}` : `${API_URLS[currentTab]}/`;

        try {
            const res = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });
            const json = await res.json();
            if (!json.success) throw new Error(json.error);

            showToast(json.message || "Guardado correctamente", "success");
            closeFormModal();
            changeTab(currentTab);
        } catch (err) {
            console.error(err);
            showToast("Error al guardar registro", "error");
        }
    });

    // -----------------------
    // EDITAR REGISTRO
    // -----------------------
    window.editItem = async function(id) {
        try {
            const res = await fetch(`${API_URLS[currentTab]}/${id}`);
            const json = await res.json();
            if (!json.success) throw new Error(json.error);

            openFormModal(currentTab, `Editar ${currentTab.slice(0, -1)}`, json.data);
        } catch (err) {
            console.error(err);
            showToast("Error al cargar registro", "error");
        }
    };

    // -----------------------
    // ELIMINAR REGISTRO
    // -----------------------
    window.deleteItem = async function(id) {
        if (!confirm("¿Seguro que desea eliminar este registro?")) return;
        try {
            const res = await fetch(`${API_URLS[currentTab]}/${id}`, { method: "DELETE" });
            const json = await res.json();
            if (!json.success) throw new Error(json.error);
            showToast("Eliminado correctamente", "success");
            changeTab(currentTab);
        } catch (err) {
            console.error(err);
            showToast("Error al eliminar registro", "error");
        }
    };

    // -----------------------
    // BUSCADOR
    // -----------------------
    // -----------------------
// BUSCADOR (CORREGIDO PARA VERIFICACIÓN DE URL)
// -----------------------
document.getElementById("searchInput").addEventListener("input", async e => {
    const search = e.target.value.trim();
    const tbody = document.getElementById("table-body");
    
    // 1. Si la caja de búsqueda está vacía, recargar la tabla completa
    if (!search) {
        return changeTab(currentTab); 
    }

    let url = null;
    let queryParam = null;

    // 2. Definición de las rutas de búsqueda para cada módulo
    switch (currentTab) {
        case "pacientes":
            // Opción 1: Buscar por DNI (Asumiendo que es el identificador principal)
            url = `/api/pacientes/buscar`;
            queryParam = `dni=${search}`;
            break;
            
        case "medicos":
            // Opción 2: Busca por Nombre
            url = `/api/medicos/buscar`;
            queryParam = `nombre=${search}`; 
            break;
            
        case "especialidades":
            url = `/api/especialidades/buscar`;
            queryParam = `nombre=${search}`;
            break;
            
        case "enfermedades":
            url = `/api/enfermedades/buscar`;
            queryParam = `nombre=${search}`;
            break;
    }
    
    // 3. Ejecución de la búsqueda
    if (url && queryParam) {
        try {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4">Buscando...</td></tr>`;
            
            // La URL final será, por ejemplo: /api/pacientes/buscar?dni=12345678
            const fullUrl = `${url}?${queryParam}`; 
            
            // Verifica en la consola qué URL está intentando usar
            console.log("Intentando buscar en URL:", fullUrl); 
            
            const res = await fetch(fullUrl);
            
            // Si el error es 404 (Not Found), fallará aquí
            if (!res.ok) { 
                throw new Error(`HTTP Error: ${res.status} al buscar en ${fullUrl}`);
            }

            const json = await res.json();
            
            if (!json.success) throw new Error(json.error || "Búsqueda fallida en la API.");
            
            tbody.innerHTML = json.data.length
                ? json.data.map(i => renderRow(i, currentTab)).join("")
                : `<tr><td colspan="6" class="text-center py-4">No se encontraron resultados para "${search}"</td></tr>`;

        } catch (error) {
            console.error("Error de búsqueda:", error);
            showToast("Error al realizar la búsqueda. Verifique la consola para detalles.", "error");
            tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-red-500">Error al cargar resultados.</td></tr>`;
        }
    } else {
        // En caso de que no haya ruta de búsqueda definida para la pestaña
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-gray-400">Búsqueda no implementada para ${currentTab}.</td></tr>`;
    }
});

    // -----------------------
    // TOASTS
    // -----------------------
    function showToast(message, type = "info") {
        const toast = document.createElement("div");
        toast.className = `fixed top-4 right-4 px-4 py-2 rounded shadow text-white ${
            type === "error" ? "bg-red-500" :
            type === "success" ? "bg-green-500" : "bg-gray-700"
        }`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // -----------------------
    // INICIO
    // -----------------------
    changeTab("pacientes");
});
