// ====================================================
// Gestor Administrador - Conexión real con Flask API
// ====================================================

document.addEventListener("DOMContentLoaded", () => {

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

        document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
        document.getElementById(`${tabName}-tab`).classList.add("active");
        document.getElementById("table-title").textContent = tabName.toUpperCase();

        const tbody = document.getElementById("table-body");
        tbody.innerHTML = `<tr><td colspan="4" class="text-center py-4">Cargando...</td></tr>`;

        const data = await fetchData(tabName);

        tbody.innerHTML = data.length
            ? data.map(item => renderRow(item)).join("")
            : `<tr><td colspan="4" class="text-center py-4">No hay registros</td></tr>`;
    };

    // -----------------------
    // RENDERIZAR FILA
    // -----------------------
    function renderRow(item) {
        const cols = Object.keys(item).slice(0, 3)
            .map(k => `<td class="px-6 py-4">${item[k]}</td>`)
            .join("");
        return `
            <tr>
                ${cols}
                <td class="px-6 py-4 text-center">
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
            enfermedades: ["nombre"]
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
    document.getElementById("searchInput").addEventListener("input", async e => {
        const search = e.target.value.trim();
        const tbody = document.getElementById("table-body");

        if (!search) return changeTab(currentTab);

        let url;
        if (currentTab === "pacientes") url = `/api/pacientes/buscar?dni=${search}`;
        else if (currentTab === "enfermedades") url = `/api/enfermedades/buscar?nombre=${search}`;
        else return;

        try {
            const res = await fetch(url);
            const json = await res.json();
            if (!json.success) throw new Error(json.error);
            tbody.innerHTML = json.data.map(i => renderRow(i)).join("");
        } catch {
            showToast("Error al buscar", "error");
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
