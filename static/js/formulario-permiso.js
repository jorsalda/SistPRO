// ============================================
// FORMULARIO DE PERMISOS - LÓGICA PROFESIONAL
// ============================================

class HistorialPermisos {
    constructor() {
        this.container = document.getElementById('contenedor-permisos');
        this.listaPermisos = document.getElementById('lista-permisos');
        this.selectDocente = document.getElementById('docente_id');
        this.mensajeSeleccion = document.getElementById('mensaje-seleccion');
        this.loading = document.getElementById('loading');
        this.sinPermisos = document.getElementById('sin-permisos');
        this.tituloDocente = document.getElementById('titulo-docente');

        this.permisosDocente = []; // Array para almacenar permisos actuales

        if (this.selectDocente && this.container) {
            this.init();
        } else {
            console.warn('Elementos del formulario no encontrados');
        }
    }

    init() {
        // Evento al cambiar docente
        this.selectDocente.addEventListener('change', (e) => {
            this.cargarHistorial(e.target.value);
        });

        // Cargar automáticamente si hay docente en URL
        this.cargarDesdeURL();

        // Configurar validación de fechas
        this.configurarValidacionFechas();
    }

    async cargarHistorial(docenteId) {
        if (!docenteId) {
            this.mostrarMensajeInicial();
            return;
        }

        this.mostrarCargando();

        try {
            const response = await fetch(`/permisos/api/permisos-docente/${docenteId}`);

            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.mostrarHistorial(data);
                this.permisosDocente = data.permisos; // Guardar para validación
            } else {
                this.mostrarError(data.error || 'Error al cargar los permisos');
            }

        } catch (error) {
            console.error('Error cargando historial:', error);
            this.mostrarError('Error de conexión con el servidor');
        }
    }

    mostrarCargando() {
        this.mensajeSeleccion.classList.add('d-none');
        this.loading.classList.remove('d-none');
        this.container.classList.add('d-none');
        this.sinPermisos.classList.add('d-none');
    }

    mostrarMensajeInicial() {
        this.mensajeSeleccion.classList.remove('d-none');
        this.mensajeSeleccion.className = 'alert alert-info';
        this.mensajeSeleccion.textContent = '👈 Seleccione un docente para ver su historial de permisos';
        this.loading.classList.add('d-none');
        this.container.classList.add('d-none');
    }

    mostrarHistorial(data) {
        this.loading.classList.add('d-none');

        if (data.total === 0) {
            this.sinPermisos.classList.remove('d-none');
            this.container.classList.add('d-none');
            return;
        }

        this.container.classList.remove('d-none');
        this.sinPermisos.classList.add('d-none');

        // Actualizar título
        this.tituloDocente.textContent = `Docente: ${data.docente}`;

        // Limpiar lista anterior
        this.listaPermisos.innerHTML = '';

        // Agregar cada permiso a la lista
        data.permisos.forEach(permiso => {
            const item = document.createElement('div');
            item.className = 'list-group-item';

            // Determinar color según tipo
            let badgeClass = 'bg-secondary';
            if (permiso.tipo.includes('Vacaciones')) badgeClass = 'bg-info';
            else if (permiso.tipo.includes('Enfermedad')) badgeClass = 'bg-danger';
            else if (permiso.tipo.includes('Capacitación')) badgeClass = 'bg-primary';
            else if (permiso.tipo.includes('Cumpleaños')) badgeClass = 'bg-success';
            else if (permiso.tipo.includes('Tiquetera')) badgeClass = 'bg-warning';

            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <span class="badge ${badgeClass}">${permiso.tipo}</span>
                        <small class="text-muted">${permiso.fecha_inicio} al ${permiso.fecha_fin}</small>
                        <br>
                        <small>${permiso.dias} días</small>
                    </div>
                    <div>
                        ${permiso.observacion ? `<small>${permiso.observacion}</small>` : ''}
                    </div>
                </div>
            `;
            this.listaPermisos.appendChild(item);
        });
    }

    mostrarError(mensaje) {
        this.loading.classList.add('d-none');
        this.mensajeSeleccion.textContent = mensaje;
        this.mensajeSeleccion.className = 'alert alert-danger';
        this.mensajeSeleccion.classList.remove('d-none');
        this.container.classList.add('d-none');
    }

    cargarDesdeURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const docenteId = urlParams.get('docente_id');

        if (docenteId && this.selectDocente) {
            this.selectDocente.value = docenteId;
            // Pequeño delay para asegurar que el DOM esté listo
            setTimeout(() => this.cargarHistorial(docenteId), 100);
        }
    }

    configurarValidacionFechas() {
        const hoy = new Date().toISOString().split('T')[0];
        const fechaInicio = document.getElementById('fecha_inicio');
        const fechaFin = document.getElementById('fecha_fin');

        if (fechaInicio && !fechaInicio.value) {
            fechaInicio.value = hoy;
            fechaInicio.min = hoy;
        }

        if (fechaFin && !fechaFin.value) {
            fechaFin.value = hoy;
        }

        // Validación de fechas en tiempo real
        fechaInicio.addEventListener('change', function() {
            fechaFin.min = this.value;
            if (fechaFin.value < this.value) {
                fechaFin.value = this.value;
            }
        });

        fechaFin.addEventListener('change', function() {
            if (this.value < fechaInicio.value) {
                alert('❌ La fecha de fin no puede ser anterior a la fecha de inicio');
                this.value = fechaInicio.value;
            }
        });
    }

    // Función para validar solapamiento de permisos
    validarSolapamiento(fechaInicio, fechaFin) {
        if (this.permisosDocente.length === 0) return null;

        const nuevaInicio = new Date(fechaInicio);
        const nuevaFin = new Date(fechaFin);

        for (const permiso of this.permisosDocente) {
            // Convertir fechas del historial (formato dd/mm/aaaa) a Date
            const [dia, mes, anio] = permiso.fecha_inicio.split('/');
            const existenteInicio = new Date(anio, mes - 1, dia);

            const [diaF, mesF, anioF] = permiso.fecha_fin.split('/');
            const existenteFin = new Date(anioF, mesF - 1, diaF);

            // Verificar solapamiento
            if ((nuevaInicio <= existenteFin && nuevaFin >= existenteInicio)) {
                return `⚠️ ADVERTENCIA: Este permiso se solapa con uno existente:
                        ${permiso.tipo} (${permiso.fecha_inicio} al ${permiso.fecha_fin})`;
            }
        }
        return null;
    }
}

// ============================================
// MANEJADOR DEL ENVÍO DEL FORMULARIO - VERSIÓN SIMPLIFICADA
// ============================================

class ManejadorFormularioPermiso {
    constructor(historial) {
        this.formulario = document.getElementById('form-permiso');
        this.historial = historial;

        if (this.formulario) {
            this.init();
        }
    }

    init() {
        // NO interceptamos el submit con preventDefault
        // Dejamos que el formulario se envíe de forma tradicional
        this.formulario.addEventListener('submit', (e) => this.validarAntesDeEnviar(e));
    }

    validarAntesDeEnviar(event) {
        // Validación básica
        if (!this.validarCamposRequeridos()) {
            event.preventDefault();
            return;
        }

        // Validar fechas
        const fechaInicio = document.getElementById('fecha_inicio').value;
        const fechaFin = document.getElementById('fecha_fin').value;

        if (new Date(fechaFin) < new Date(fechaInicio)) {
            alert('❌ Error: La fecha fin no puede ser anterior a la fecha inicio');
            event.preventDefault();
            return;
        }

        // Validar solapamiento
        const advertencia = this.historial.validarSolapamiento(fechaInicio, fechaFin);
        if (advertencia && !confirm(advertencia + "\n\n¿Desea continuar de todos modos?")) {
            event.preventDefault();
            return;
        }

        // Si pasa todas las validaciones, el formulario se envía normalmente
        // Mostrar loading en el botón mientras se envía
        const submitBtn = this.formulario.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Enviando...';
        submitBtn.disabled = true;

        // El formulario se enviará de forma tradicional
        // No hacemos fetch, dejamos que el navegador lo haga
    }

    validarCamposRequeridos() {
        const docenteId = document.getElementById('docente_id').value;
        const tipo = document.getElementById('tipo').value;
        const fechaInicio = document.getElementById('fecha_inicio').value;
        const fechaFin = document.getElementById('fecha_fin').value;

        if (!docenteId) {
            alert('⚠️ Por favor seleccione un docente');
            return false;
        }

        if (!tipo) {
            alert('⚠️ Por favor seleccione el tipo de permiso');
            return false;
        }

        if (!fechaInicio || !fechaFin) {
            alert('⚠️ Por favor complete las fechas');
            return false;
        }

        return true;
    }
}

// ============================================
// INICIALIZACIÓN CUANDO EL DOM ESTÉ LISTO
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar historial de permisos
    const historial = new HistorialPermisos();

    // Inicializar manejador del formulario
    new ManejadorFormularioPermiso(historial);
});