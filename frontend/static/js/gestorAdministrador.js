// --- Datos de Mockup (Simulación de la Base de Datos) ---

let currentActiveTab = 'pacientes';
let isEditing = false;
let currentItemId = null;

const MOCK_DATA = {
    pacientes: [
        { id: 1, nombre: 'María', apellido: 'García', dni: '12345678', edad: 35, fechaNac: '1989-05-14', email: 'maria.garcia@email.com' },
        { id: 2, nombre: 'Juan', apellido: 'Pérez', dni: '87654321', edad: 42, fechaNac: '1982-10-22', email: 'juan.perez@email.com' },
        { id: 3, nombre: 'Ana', apellido: 'López', dni: '11223344', edad: 28, fechaNac: '1997-03-01', email: 'ana.lopez@email.com' },
    ],
    medicos: [
        { id: 101, nombre: 'Dr. Roberto', apellido: 'Díaz', matricula: 'M1234', especialidad: 'Cardiología', horarios: 'L-V 8:00-16:00' },
        { id: 102, nombre: 'Dra. Sofía', apellido: 'Gómez', matricula: 'M5678', especialidad: 'Pediatría', horarios: 'M-J 10:00-18:00' },
    ],
    especialidades: [
        { id: 201, nombre: 'Cardiología' },
        { id: 202, nombre: 'Pediatría' },
        { id: 203, nombre: 'Dermatología' },
    ],
    enfermedades: [
        { id: 301, nombre: 'Gripe Común' },
        { id: 302, nombre: 'Hipertensión' },
        { id: 303, nombre: 'Diabetes Tipo 2' },
    ]
};

// --- Funciones de Utilidad y UI ---

const showToast = (message, type = 'success') => {
    // Implementación de showToast
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    let bgColor = 'bg-green-500';
    if (type === 'error') bgColor = 'bg-red-500';
    if (type === 'info') bgColor = 'bg-blue-500';

    toast.className = `${bgColor} text-white px-4 py-3 rounded-lg shadow-xl mb-2 flex items-center justify-between opacity-0 transition-opacity duration-300`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-4 opacity-70 hover:opacity-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
    `;
    
    container.appendChild(toast);
    setTimeout(() => { toast.classList.remove('opacity-0'); }, 10); 
    setTimeout(() => { toast.classList.add('opacity-0'); }, 4000);
    setTimeout(() => { toast.remove(); }, 4300);
};

// --- Navegación de Pestañas ---

window.changeTab = (tabName) => {
    currentActiveTab = tabName;
    // 1. Actualizar estilos de las pestañas
    document.querySelectorAll('.tab-item').forEach(tab => {
        if (tab.dataset.target === tabName) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    // 2. Renderizar contenido (Inyecta la tabla y el input de búsqueda)
    const contentContainer = document.getElementById('content-container');
    contentContainer.innerHTML = renderTabContent(tabName);

    // 3. Inicializar listeners y datos
    
    // ** ARREGLO CLAVE PARA LA BÚSQUEDA **
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        // Aseguramos que solo haya un listener por si se adjuntó previamente (aunque el elemento fue recreado)
        searchInput.removeEventListener('input', searchItems); 
        searchInput.addEventListener('input', searchItems);
        // Limpiamos el campo de búsqueda al cambiar de pestaña
        searchInput.value = '';
    }

    // 4. Renderizar datos de la tabla 
    if (tabName === 'pacientes') {
        renderPatientTable(MOCK_DATA.pacientes); 
    } else {
        const tbody = document.getElementById('table-body');
        if(tbody) {
            tbody.innerHTML = renderGenericTable(MOCK_DATA[tabName], tabName);
        }
    }
};

/**
 * Renderiza la estructura de la pestaña actual.
 */
const renderTabContent = (tabName) => {
    let title = '';
    let placeholder = '';
    
    switch (tabName) {
        case 'pacientes':
            title = 'Gestión de Pacientes';
            placeholder = 'Buscar por nombre, apellido o DNI...';
            return `
                <div class="bg-white shadow overflow-hidden sm:rounded-lg p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold text-gray-900 flex items-center">
                           ${title}
                        </h2>
                        <button 
                            id="new-item-btn" 
                            onclick="openFormModal('pacientes', 'Registrar Nuevo Paciente')" 
                            class="bg-teal-500 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-teal-600 transition-colors duration-150 flex items-center"
                        >
                            + Nuevo Paciente
                        </button>
                    </div>
                    <input type="text" id="search-input" placeholder="${placeholder}" class="p-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 w-full mb-6">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead>
                                <tr id="table-head">
                                    ${renderTableHeader(tabName)}
                                </tr>
                            </thead>
                            <tbody id="table-body" class="bg-white divide-y divide-gray-200">
                                </tbody>
                        </table>
                    </div>
                </div>
            `;
        case 'medicos':
            title = 'Gestión de Médicos';
            placeholder = 'Buscar por nombre, apellido o matrícula...';
            break;
        case 'especialidades':
            title = 'Gestión de Especialidades';
            placeholder = 'Buscar por nombre de especialidad...';
            break;
        case 'enfermedades':
            title = 'Gestión de Enfermedades';
            placeholder = 'Buscar por nombre de enfermedad...';
            break;
    }

    // Estructura genérica para Médicos, Especialidades y Enfermedades
    return `
        <div class="bg-white shadow overflow-hidden sm:rounded-lg p-6">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-gray-900">${title}</h2>
                <button 
                    id="new-item-btn" 
                    onclick="openFormModal('${tabName}', 'Registrar Nueva ${tabName.slice(0, -1).charAt(0).toUpperCase() + tabName.slice(0, -1).slice(1)}')" 
                    class="bg-teal-500 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-teal-600 transition-colors duration-150 flex items-center"
                >
                    + Nueva ${tabName.slice(0, -1).charAt(0).toUpperCase() + tabName.slice(0, -1).slice(1)}
                </button>
            </div>
            <input type="text" id="search-input" placeholder="${placeholder}" class="p-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 w-full mb-6">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead>
                        <tr id="table-head">
                            ${renderTableHeader(tabName)}
                        </tr>
                    </thead>
                    <tbody id="table-body" class="bg-white divide-y divide-gray-200">
                        </tbody>
                </table>
            </div>
        </div>
    `;
};

// --- Renderizado de Tablas ---

const renderTableHeader = (tabName) => {
    switch (tabName) {
        case 'pacientes':
            return `
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Apellido</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">DNI</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Edad</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha Nac.</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            `;
        case 'medicos':
             return `
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Apellido</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Matrícula</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Especialidad</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Horarios</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            `;
        case 'especialidades':
        case 'enfermedades':
            return `
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            `;
        default:
            return '';
    }
}

/**
 * Renderiza la tabla de pacientes.
 */
const renderPatientTable = (data) => {
    const tbody = document.getElementById('table-body');
    if (!tbody) return;
    tbody.innerHTML = ''; 

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-8 text-gray-500">No se encontraron pacientes.</td></tr>`;
        return;
    }

    data.forEach(item => {
        const row = tbody.insertRow();
        row.className = 'hover:bg-gray-50 transition-colors';
        row.innerHTML = `
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">${item.nombre}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.apellido}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.dni}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.edad}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.fechaNac.split('-').reverse().join('/')}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.email}</td>
            <td class="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-2">
                    <button onclick="editItem('${item.id}')" class="text-indigo-600 hover:text-indigo-900 px-2 py-1 border border-indigo-200 rounded-md text-xs font-semibold hover:bg-indigo-50 transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                    </button>
                    <button onclick="deleteItem('${item.id}')" class="text-red-600 hover:text-red-900 px-2 py-1 border border-red-200 rounded-md text-xs font-semibold hover:bg-red-50 transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                </div>
            </td>
        `;
    });
};


/**
 * Renderiza una tabla genérica (Médicos, Especialidades, Enfermedades).
 */
const renderGenericTable = (data, tabName) => {
    if (data.length === 0) {
        // Aseguramos que el colspan sea correcto para centrar el mensaje.
        const colspan = tabName === 'medicos' ? 6 : 2;
        return `<tr><td colspan="${colspan}" class="text-center py-8 text-gray-500">No se encontraron ${tabName}.</td></tr>`;
    }

    return data.map(item => {
        let cells = '';
        const id = item.id;

        // Note: 'pacientes' is handled by renderPatientTable, so we skip it here.
        if (tabName === 'medicos') {
            cells = `
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">${item.nombre}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.apellido}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.matricula}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.especialidad}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${item.horarios}</td>
            `;
        } else if (tabName === 'especialidades' || tabName === 'enfermedades') {
            cells = `<td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">${item.nombre}</td>`;
        }
        
        return `
            <tr class="hover:bg-gray-50 transition-colors">
                ${cells}
                <td class="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                        <button onclick="editItem('${id}')" class="text-indigo-600 hover:text-indigo-900 px-2 py-1 border border-indigo-200 rounded-md text-xs font-semibold hover:bg-indigo-50 transition-colors">
                            Editar
                        </button>
                        <button onclick="deleteItem('${id}')" class="text-red-600 hover:text-red-900 px-2 py-1 border border-red-200 rounded-md text-xs font-semibold hover:bg-red-50 transition-colors">
                            Eliminar
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
};

/**
 * Lógica de búsqueda genérica.
 */
const searchItems = () => {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const allItems = MOCK_DATA[currentActiveTab];
    
    // Si no hay datos, salimos
    if (!allItems || allItems.length === 0) {
        const tbody = document.getElementById('table-body');
        if (tbody) {
            const colspan = currentActiveTab === 'medicos' ? 6 : (currentActiveTab === 'pacientes' ? 7 : 2);
            tbody.innerHTML = `<tr><td colspan="${colspan}" class="text-center py-8 text-gray-500">No se encontraron resultados.</td></tr>`;
        }
        return;
    }

    const fieldsToSearch = Object.keys(allItems[0] || {}).filter(key => key !== 'id' && key !== 'fechaNac');
    
    const filtered = allItems.filter(item => {
        return fieldsToSearch.some(key => 
            String(item[key]).toLowerCase().includes(searchTerm)
        );
    });

    // Renderiza la tabla filtrada
    if (currentActiveTab === 'pacientes') {
        renderPatientTable(filtered);
    } else {
        const tbody = document.getElementById('table-body');
        if (tbody) {
             tbody.innerHTML = renderGenericTable(filtered, currentActiveTab);
        }
    }
};

// --- Lógica del Modal (Registro/Edición) ---

const openFormModal = (itemType, title, item = null) => {
    isEditing = !!item;
    currentItemId = item ? item.id : null;

    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-form-body').innerHTML = renderForm(itemType, item);

    const modal = document.getElementById('form-modal');
    // ** Corrección para mostrar el modal quitando clases de invisibilidad
    modal.classList.remove('pointer-events-none', 'opacity-0');
    modal.querySelector('#modal-content-area').classList.remove('scale-95');

    // Asignar el listener de guardado
    document.getElementById('modal-save-btn').onclick = () => handleSave(itemType);
};

const closeFormModal = () => {
    const modal = document.getElementById('form-modal');
    modal.classList.add('opacity-0');
    modal.querySelector('#modal-content-area').classList.add('scale-95');
    setTimeout(() => {
        modal.classList.add('pointer-events-none');
    }, 300);
};

const renderForm = (itemType, item = {}) => {
    // Función de ayuda para crear campos de formulario
    const createField = (id, label, type = 'text', value = '', required = true, placeholder = '') => `
        <div class="mb-4">
            <label for="${id}" class="block text-sm font-medium text-gray-700">${label}</label>
            <input type="${type}" id="${id}" name="${id}" value="${value || ''}" 
                   class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-teal-500 focus:border-teal-500" 
                   ${required ? 'required' : ''} placeholder="${placeholder}">
        </div>
    `;

    switch (itemType) {
        case 'pacientes':
            return `
                <form id="${itemType}-form">
                    ${createField('nombre', 'Nombre', 'text', item.nombre)}
                    ${createField('apellido', 'Apellido', 'text', item.apellido)}
                    ${createField('dni', 'DNI/Cédula', 'text', item.dni)}
                    ${createField('edad', 'Edad', 'number', item.edad)}
                    ${createField('fechaNac', 'Fecha de Nacimiento', 'date', item.fechaNac)}
                    ${createField('email', 'Email', 'email', item.email)}
                </form>
            `;
        case 'medicos':
            return `
                <form id="${itemType}-form">
                    ${createField('nombre', 'Nombre', 'text', item.nombre)}
                    ${createField('apellido', 'Apellido', 'text', item.apellido)}
                    ${createField('matricula', 'Matrícula', 'text', item.matricula)}
                    ${createField('especialidad', 'Especialidad', 'text', item.especialidad, true, 'Ej: Cardiología')}
                    ${createField('horarios', 'Horarios (Ej: L-V 8:00-16:00)', 'text', item.horarios, false)}
                </form>
            `;
        case 'especialidades':
        case 'enfermedades':
             return `
                <form id="${itemType}-form">
                    ${createField('nombre', 'Nombre de la ' + (itemType === 'especialidades' ? 'Especialidad' : 'Enfermedad'), 'text', item.nombre)}
                </form>
            `;
        default:
             return `<p>Error: Tipo de formulario no reconocido.</p>`;
    }
};

// --- Lógica de CRUD (Local Mock) ---

const handleSave = (itemType) => {
    const form = document.getElementById(itemType + '-form');
    // Simple validación de HTML5 antes de guardar
    if (!form.checkValidity()) {
        form.reportValidity(); // Muestra los mensajes de error del navegador
        return;
    }

    const formData = new FormData(form);
    const newItem = {};
    formData.forEach((value, key) => newItem[key] = value);

    if (isEditing) {
        // Lógica de Modificar (Actualizar)
        // Convertimos a String para la comparación si el ID es un número
        const index = MOCK_DATA[itemType].findIndex(item => String(item.id) === String(currentItemId));
        if (index !== -1) {
            MOCK_DATA[itemType][index] = { ...MOCK_DATA[itemType][index], ...newItem };
            showToast(`Ítem modificado exitosamente.`, 'success');
        }
    } else {
        // Lógica de Registrar (Nuevo)
        // Generar un ID simple local (asegura que sea un string si otros son strings)
        newItem.id = String(Date.now()); 
        MOCK_DATA[itemType].push(newItem);
        showToast(`Nuevo ítem registrado exitosamente.`, 'success');
    }

    closeFormModal();
    changeTab(itemType); // Recargar la tabla
};

window.editItem = (id) => {
    // Aseguramos que el ID se compare como string
    const item = MOCK_DATA[currentActiveTab].find(i => String(i.id) === String(id));
    const title = 'Modificar ' + currentActiveTab.slice(0, -1).charAt(0).toUpperCase() + currentActiveTab.slice(0, -1).slice(1);
    openFormModal(currentActiveTab, title, item);
};

window.deleteItem = (id) => {
    if (confirm(`¿Estás seguro de que quieres eliminar este ítem?`)) {
        MOCK_DATA[currentActiveTab] = MOCK_DATA[currentActiveTab].filter(item => String(item.id) !== String(id));
        showToast(`Ítem eliminado.`, 'error');
        changeTab(currentActiveTab); // Recargar la tabla
    }
};

// --- Inicialización ---

document.addEventListener('DOMContentLoaded', () => {
    // Carga inicial de la pestaña "Pacientes"
    changeTab('pacientes'); 
});

// ** EXPOSICIONES GLOBALES CORRECTAS PARA EL HTML **
window.changeTab = changeTab;
window.editItem = editItem;
window.deleteItem = deleteItem;
window.closeFormModal = closeFormModal;
window.openFormModal = openFormModal; // ¡Esta es la clave para que el botón de registro funcione!