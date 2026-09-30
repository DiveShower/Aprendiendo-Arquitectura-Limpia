# -*- coding: utf-8 -*-
"""
Módulo de widgets interactivos (Drag & Drop) para la Masterclass de Clean Architecture.
Permite mantener las celdas del cuaderno limpias y compactas, aislando el código HTML5/CSS/JavaScript.
"""

from IPython.display import HTML, display


def _generar_tablero_html(widget_id: str, title: str, subtitle: str, items: list, zones: list) -> str:
    """
    Genera el HTML5, CSS y JavaScript para un tablero Drag & Drop autónomo.
    Soporta arrastrar y soltar nativo, y clic-para-asignar (ideal para trackpads y pantallas táctiles).
    """
    items_html = ""
    for item in items:
        items_html += f"""
            <div class="{widget_id}-item" draggable="true" data-id="{item['id']}" data-target="{item['target']}" 
                 style="background: #313244; color: #cdd6f4; padding: 7px 11px; border-radius: 6px; cursor: grab; font-size: 0.84rem; border: 1px solid #585b70; user-select: none; transition: transform 0.15s ease;">
                {item['text']}
            </div>
        """

    zones_html = ""
    for zone in zones:
        color = zone.get('color', '#89b4fa')
        zones_html += f"""
        <div class="{widget_id}-zone" data-zone="{zone['id']}" 
             style="background: #181825; border: 2px solid {color}; border-radius: 8px; padding: 10px; min-height: 140px; display: flex; flex-direction: column;">
            <div style="color: {color}; font-weight: bold; font-size: 0.85rem; margin-bottom: 6px; border-bottom: 1px solid #313244; padding-bottom: 4px;">
                {zone['title']}<br><span style="font-size: 0.74rem; color: #a6adc8; font-weight: normal;">{zone['subtitle']}</span>
            </div>
            <div class="{widget_id}-slot" style="flex: 1; display: flex; flex-direction: column; gap: 6px; min-height: 80px;"></div>
        </div>
        """

    return f"""
<div id="{widget_id}-container" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 920px; margin: 12px auto; padding: 18px; border-radius: 12px; background: #1e1e2e; color: #cdd6f4; box-shadow: 0 8px 24px rgba(0,0,0,0.35); border: 1px solid #313244;">
    <div style="text-align: center; margin-bottom: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #89b4fa; font-size: 1.25rem;">{title}</h4>
        <p style="margin: 0; color: #a6adc8; font-size: 0.9rem;">{subtitle}</p>
    </div>

    <!-- BANCO DE ELEMENTOS -->
    <div style="margin-bottom: 16px;">
        <div style="font-weight: 600; margin-bottom: 6px; color: #f9e2af; font-size: 0.88rem;">📦 Elementos a clasificar ({len(items)} tarjetas):</div>
        <div id="{widget_id}-bank" style="display: flex; flex-wrap: wrap; gap: 8px; min-height: 60px; padding: 10px; border: 2px dashed #45475a; border-radius: 8px; background: #181825;">
            {items_html}
        </div>
    </div>

    <!-- ZONAS DE DESTINO -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; margin-bottom: 16px;">
        {zones_html}
    </div>

    <!-- BOTONES Y FEEDBACK -->
    <div style="display: flex; gap: 10px; align-items: center; justify-content: center; margin-bottom: 10px;">
        <button id="{widget_id}-btn-check" style="background: #a6e3a1; color: #11111b; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.88rem;">
            ✅ Comprobar Respuestas
        </button>
        <button id="{widget_id}-btn-reset" style="background: #45475a; color: #cdd6f4; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.88rem;">
            🔄 Reiniciar
        </button>
    </div>

    <div id="{widget_id}-feedback" style="display: none; padding: 10px; border-radius: 8px; text-align: center; font-size: 0.9rem; font-weight: 500;"></div>
</div>

<script>
(function() {{
    const container = document.getElementById('{widget_id}-container');
    if (!container) return;

    let selectedItem = null;
    let draggedItem = null;

    const items = container.querySelectorAll('.{widget_id}-item');
    const zones = container.querySelectorAll('.{widget_id}-zone');
    const bank = container.querySelector('#{widget_id}-bank');
    const btnCheck = container.querySelector('#{widget_id}-btn-check');
    const btnReset = container.querySelector('#{widget_id}-btn-reset');
    const feedback = container.querySelector('#{widget_id}-feedback');

    items.forEach(item => {{
        item.addEventListener('dragstart', (e) => {{
            draggedItem = item;
            e.dataTransfer.setData('text/plain', item.dataset.id);
            item.style.opacity = '0.5';
        }});

        item.addEventListener('dragend', () => {{
            if (draggedItem) draggedItem.style.opacity = '1';
            draggedItem = null;
        }});

        item.addEventListener('click', (e) => {{
            e.stopPropagation();
            if (selectedItem === item) {{
                item.style.outline = 'none';
                selectedItem = null;
            }} else {{
                if (selectedItem) selectedItem.style.outline = 'none';
                selectedItem = item;
                item.style.outline = '3px solid #89b4fa';
            }}
        }});
    }});

    zones.forEach(zone => {{
        const slot = zone.querySelector('.{widget_id}-slot');

        zone.addEventListener('dragover', (e) => {{
            e.preventDefault();
            zone.style.background = '#252538';
        }});

        zone.addEventListener('dragleave', () => {{
            zone.style.background = '#181825';
        }});

        zone.addEventListener('drop', (e) => {{
            e.preventDefault();
            zone.style.background = '#181825';
            if (draggedItem) {{
                slot.appendChild(draggedItem);
                draggedItem.style.opacity = '1';
                draggedItem = null;
            }}
        }});

        zone.addEventListener('click', () => {{
            if (selectedItem) {{
                slot.appendChild(selectedItem);
                selectedItem.style.outline = 'none';
                selectedItem = null;
            }}
        }});
    }});

    bank.addEventListener('dragover', (e) => {{
        e.preventDefault();
        bank.style.background = '#252538';
    }});
    bank.addEventListener('dragleave', () => {{
        bank.style.background = '#181825';
    }});
    bank.addEventListener('drop', (e) => {{
        e.preventDefault();
        bank.style.background = '#181825';
        if (draggedItem) {{
            bank.appendChild(draggedItem);
            draggedItem.style.opacity = '1';
            draggedItem = null;
        }}
    }});
    bank.addEventListener('click', () => {{
        if (selectedItem) {{
            bank.appendChild(selectedItem);
            selectedItem.style.outline = 'none';
            selectedItem = null;
        }}
    }});

    btnReset.addEventListener('click', () => {{
        items.forEach(item => {{
            bank.appendChild(item);
            item.style.border = '1px solid #585b70';
            item.style.background = '#313244';
            item.style.color = '#cdd6f4';
            item.style.outline = 'none';
        }});
        feedback.style.display = 'none';
        if (selectedItem) selectedItem = null;
    }});

    btnCheck.addEventListener('click', () => {{
        let correctCount = 0;
        let totalItems = items.length;
        let unplaced = 0;

        items.forEach(item => {{
            const parentZone = item.closest('.{widget_id}-zone');
            if (!parentZone) {{
                unplaced++;
                item.style.border = '1px solid #585b70';
                item.style.background = '#313244';
                return;
            }}
            const currentZone = parentZone.dataset.zone;
            const targetZone = item.dataset.target;

            if (currentZone === targetZone) {{
                correctCount++;
                item.style.border = '2px solid #a6e3a1';
                item.style.background = '#1e382b';
                item.style.color = '#a6e3a1';
            }} else {{
                item.style.border = '2px solid #f38ba8';
                item.style.background = '#3e2330';
                item.style.color = '#f38ba8';
            }}
        }});

        feedback.style.display = 'block';
        if (unplaced > 0) {{
            feedback.style.background = '#fab387';
            feedback.style.color = '#11111b';
            feedback.innerHTML = `⚠️ Aún tienes <strong>${{unplaced}}</strong> tarjeta(s) sin clasificar en el banco. ¡Ubica todas para comprobar!`;
        }} else if (correctCount === totalItems) {{
            feedback.style.background = '#a6e3a1';
            feedback.style.color = '#11111b';
            feedback.innerHTML = `🎉 <strong>¡PERFECTO! (${{correctCount}}/${{totalItems}})</strong> Has clasificado todos los conceptos con total precisión arquitectónica.`;
        }} else {{
            feedback.style.background = '#f38ba8';
            feedback.style.color = '#11111b';
            feedback.innerHTML = `Puntaje: <strong>${{correctCount}} / ${{totalItems}}</strong> aciertos. Revisa las tarjetas con borde rojo y vuelve a intentar.`;
        }}
    }});
}})();
</script>
"""


# ==============================================================================
# DATOS Y GENERACIÓN DE CADA DESAFÍO
# ==============================================================================

DESAFIOS_CONFIG = {
    0: {
        "id": "dd0",
        "title": "🎮 Desafío 0: Matriz de Eisenhower en Software",
        "subtitle": "Clasifica cada tarea en su cuadrante correcto",
        "items": [
            {"id": 1, "text": "🔥 Caída total de la base de datos en producción", "target": "c1"},
            {"id": 2, "text": "🏛️ Refactorizar para separar reglas de negocio de la base de datos", "target": "c2"},
            {"id": 3, "text": "📐 Definir interfaces abstractas para desacoplar pasarelas de pago", "target": "c2"},
            {"id": 4, "text": "⏰ El cliente pide cambiar el color de un botón para una demo en 20 minutos", "target": "c3"},
            {"id": 5, "text": "🩹 Copiar y pegar 50 líneas de código duplicado para salir del paso hoy", "target": "c3"},
            {"id": 6, "text": "🌀 Debatir por 3 horas sobre cambiar las comillas de simple a doble en el linter", "target": "c4"}
        ],
        "zones": [
            {"id": "c1", "title": "🚨 Cuadrante 1", "subtitle": "Urgente e Importante (Emergencias)", "color": "#f38ba8"},
            {"id": "c2", "title": "🏛️ Cuadrante 2", "subtitle": "Importante, No Urgente (Arquitectura)", "color": "#a6e3a1"},
            {"id": "c3", "title": "⏰ Cuadrante 3", "subtitle": "Urgente, No Importante (Presión diaria)", "color": "#f9e2af"},
            {"id": "c4", "title": "🗑️ Cuadrante 4", "subtitle": "Ni Urgente ni Importante (Desperdicio)", "color": "#6c7086"}
        ]
    },
    1: {
        "id": "dd1",
        "title": "🎮 Desafío 1: Diagnóstico de Principios SOLID",
        "subtitle": "Arrastra cada síntoma o solución a su principio SOLID correspondiente",
        "items": [
            {"id": 1, "text": "👥 Finanzas modificó el cálculo de horas y rompió los reportes de Operaciones", "target": "srp"},
            {"id": 2, "text": "🔓 Para soportar MercadoPago tuvimos que editar 8 archivos con 'if pasarela == ...'", "target": "ocp"},
            {"id": 3, "text": "🔄 La clase de Pedidos importa directamente el cliente SDK concreto de Twilio", "target": "dip"},
            {"id": 4, "text": "📏 Un cliente que solo consulta saldo está obligado a implementar 12 métodos que no usa", "target": "isp"},
            {"id": 5, "text": "⚠️ Una subclase lanza una excepción imprevista cuando se usa en lugar de su clase padre", "target": "lsp"},
            {"id": 6, "text": "🔌 Definir una interfaz PasarelaPago para que el procesador no conozca librerías externas", "target": "dip"}
        ],
        "zones": [
            {"id": "srp", "title": "👤 SRP", "subtitle": "Responsabilidad Única (Actores)", "color": "#f9e2af"},
            {"id": "ocp", "title": "🔓 OCP", "subtitle": "Abierto/Cerrado (Extensión)", "color": "#a6e3a1"},
            {"id": "lsp", "title": "📐 LSP", "subtitle": "Sustitución de Liskov (Contratos)", "color": "#89dceb"},
            {"id": "isp", "title": "✂️ ISP", "subtitle": "Segregación de Interfaces", "color": "#cba6f7"},
            {"id": "dip", "title": "🔄 DIP", "subtitle": "Inversión de Dependencias", "color": "#f38ba8"}
        ]
    },
    2: {
        "id": "dd2",
        "title": "🎮 Desafío 2: Entidades vs. Casos de Uso vs. DTOs",
        "subtitle": "Arrastra cada elemento a su categoría del núcleo de negocio",
        "items": [
            {"id": 1, "text": "🌟 Regla de cálculo de cuota mensual según amortización francesa", "target": "ent"},
            {"id": 2, "text": "🌟 Validar que el saldo de la cuenta no supere el límite de descubierto", "target": "ent"},
            {"id": 3, "text": "⚙️ Orquestar: buscar préstamo, verificar solicitante, aprobar y persistir", "target": "uc"},
            {"id": 4, "text": "⚙️ Coordinar el flujo entre la pasarela de pago y la cuenta de destino", "target": "uc"},
            {"id": 5, "text": "📦 SolicitudPrestamoRequest (id_cliente, monto, plazo_meses)", "target": "dto"},
            {"id": 6, "text": "📦 SolicitudPrestamoResponse (exito, mensaje, total_a_devolver)", "target": "dto"}
        ],
        "zones": [
            {"id": "ent", "title": "🌟 Entidades", "subtitle": "Reglas Críticas de Empresa", "color": "#f9e2af"},
            {"id": "uc", "title": "⚙️ Casos de Uso", "subtitle": "Reglas de la Aplicación", "color": "#f38ba8"},
            {"id": "dto", "title": "📦 DTOs (Request / Response)", "subtitle": "Estructuras de Datos Planas", "color": "#a6e3a1"}
        ]
    },
    3: {
        "id": "dd3",
        "title": "🎮 Desafío 3: Los 4 Círculos Concéntricos",
        "subtitle": "Ubica cada componente en su capa correspondiente según Uncle Bob",
        "items": [
            {"id": 1, "text": "🏷️ Entidad CuentaBancaria con reglas de saldo", "target": "c1"},
            {"id": 2, "text": "⚙️ TransferirDineroUseCase (orquestador)", "target": "c2"},
            {"id": 3, "text": "⚙️ Puerto abstracto CuentaRepositoryPort (interfaz)", "target": "c2"},
            {"id": 4, "text": "🔌 TransferenciaPresenter (convierte a ViewModel)", "target": "c3"},
            {"id": 5, "text": "🔌 FakeHttpWebController (recibe y parsea JSON)", "target": "c3"},
            {"id": 6, "text": "💾 Base de Datos PostgreSQL y tablas SQL", "target": "c4"},
            {"id": 7, "text": "🌐 Framework FastAPI / Flask / Django", "target": "c4"}
        ],
        "zones": [
            {"id": "c1", "title": "🟡 1. Entidades", "subtitle": "Enterprise Business Rules", "color": "#f9e2af"},
            {"id": "c2", "title": "🔴 2. Casos de Uso", "subtitle": "Application Business Rules", "color": "#f38ba8"},
            {"id": "c3", "title": "🟢 3. Adaptadores", "subtitle": "Controllers, Presenters", "color": "#a6e3a1"},
            {"id": "c4", "title": "🔵 4. Frameworks", "subtitle": "DB, Web, Dispositivos", "color": "#89b4fa"}
        ]
    },
    4: {
        "id": "dd4",
        "title": "🎮 Desafío 4: El Patrón Humble Object",
        "subtitle": "Separa la lógica testeable de la infraestructura tonta",
        "items": [
            {"id": 1, "text": "🧠 Presenter: transformar Decimal('14400') a '$ 14,400.00'", "target": "intel"},
            {"id": 2, "text": "🧠 Determinar si la etiqueta dice 'APROBADO' o 'DENEGADO'", "target": "intel"},
            {"id": 3, "text": "🧠 Decidir si el color de la UI es verde o rojo", "target": "intel"},
            {"id": 4, "text": "🙈 Vista: imprimir por consola la variable viewModel.total_formateado", "target": "humilde"},
            {"id": 5, "text": "🙈 Template HTML: estampar {{ viewModel.estado }} sin ningún 'if'", "target": "humilde"},
            {"id": 6, "text": "🙈 Socket SQL: enviar bytes del string query al puerto de PostgreSQL", "target": "humilde"}
        ],
        "zones": [
            {"id": "intel", "title": "🧠 Objeto Inteligente", "subtitle": "Presenter / ViewModel (Testeable)", "color": "#a6e3a1"},
            {"id": "humilde", "title": "🙈 Objeto Humilde", "subtitle": "Vista / UI / I/O puro (Sin lógica)", "color": "#f9e2af"}
        ]
    },
    5: {
        "id": "dd5",
        "title": "🎮 Desafío 5: Núcleo vs. Detalles",
        "subtitle": "Distingue lo que grita tu arquitectura de las herramientas accesorias",
        "items": [
            {"id": 1, "text": "🏛️ Reglas de scoring crediticio y cálculo de capacidad de pago", "target": "arch"},
            {"id": 2, "text": "🏛️ Caso de uso de Apertura de Cuenta Bancaria con depósito inicial", "target": "arch"},
            {"id": 3, "text": "🏛️ Políticas de comisiones y límites de sobregiro", "target": "arch"},
            {"id": 4, "text": "🔌 Motor de Base de Datos relacional PostgreSQL", "target": "det"},
            {"id": 5, "text": "🔌 Mecanismo de entrega Web HTTP / Framework FastAPI", "target": "det"},
            {"id": 6, "text": "🔌 Driver de conexión o librería ORM", "target": "det"}
        ],
        "zones": [
            {"id": "arch", "title": "🏛️ Arquitectura Esencial", "subtitle": "Reglas de Negocio (Screaming Architecture)", "color": "#f9e2af"},
            {"id": "det", "title": "🔌 Detalles Periféricos", "subtitle": "Plugins intercambiables (DB, Web, Frameworks)", "color": "#89b4fa"}
        ]
    },
    6: {
        "id": "dd6",
        "title": "🎮 Desafío 6: Las Fronteras del Componente Main",
        "subtitle": "Determina qué responsabilidades corresponden a la raíz de composición",
        "items": [
            {"id": 1, "text": "🔌 Instanciar la base de datos concreta PostgresCuentaRepository", "target": "main_si"},
            {"id": 2, "text": "🔌 Inyectar el repositorio concreto dentro del caso de uso", "target": "main_si"},
            {"id": 3, "text": "🔌 Leer variables de entorno (prod vs test) y configurar plugins", "target": "main_si"},
            {"id": 4, "text": "🚫 Calcular si el cliente califica para un préstamo bancario", "target": "main_no"},
            {"id": 5, "text": "🚫 Validar si el saldo es suficiente para la extracción", "target": "main_no"},
            {"id": 6, "text": "🚫 Formatear el mensaje de salida con símbolos de moneda y colores", "target": "main_no"}
        ],
        "zones": [
            {"id": "main_si", "title": "🔌 Pertenece a Main", "subtitle": "Composition Root / Cableado", "color": "#a6e3a1"},
            {"id": "main_no", "title": "🚫 NUNCA debe estar en Main", "subtitle": "Reglas de Negocio / Presentación", "color": "#f38ba8"}
        ]
    },
    7: {
        "id": "dd7",
        "title": "🎮 Desafío 7: Test Boundary en Clean Architecture",
        "subtitle": "Identifica las pruebas que respetan los límites arquitectónicos",
        "items": [
            {"id": 1, "text": "⚡ Probar el Caso de Uso inyectando un Repositorio en Memoria (Fake)", "target": "clean_t"},
            {"id": 2, "text": "⚡ Probar las reglas críticas de la Entidad directamente en memoria", "target": "clean_t"},
            {"id": 3, "text": "⚡ Probar el Presenter comprobando que el ViewModel tenga las cadenas formateadas", "target": "clean_t"},
            {"id": 4, "text": "🐢 Levantar un contenedor Docker con PostgreSQL real para probar un cálculo de suma", "target": "fragil_t"},
            {"id": 5, "text": "🐢 Abrir un navegador con Selenium para comprobar una regla de negocio del caso de uso", "target": "fragil_t"},
            {"id": 6, "text": "🐢 Probar la UI haciendo que la prueba dependa del esquema de tablas de la base de datos", "target": "fragil_t"}
        ],
        "zones": [
            {"id": "clean_t", "title": "⚡ Pruebas en Clean Architecture", "subtitle": "Aisladas, corren en milisegundos (Puertos)", "color": "#a6e3a1"},
            {"id": "fragil_t", "title": "🐢 Pruebas Frágiles / Acopladas", "subtitle": "Dependen de sockets, red o servidores", "color": "#f38ba8"}
        ]
    }
}


def obtener_html_desafio(num: int) -> str:
    """Devuelve el código HTML autónomo para el desafío interactivo especificado."""
    cfg = DESAFIOS_CONFIG[num]
    return _generar_tablero_html(cfg["id"], cfg["title"], cfg["subtitle"], cfg["items"], cfg["zones"])


def cargar_desafio_0():
    """Actividad No-Code Módulo 0: Matriz de Eisenhower en Software"""
    display(HTML(obtener_html_desafio(0)))


def cargar_desafio_1():
    """Actividad No-Code Módulo 1: Diagnóstico de Violaciones SOLID"""
    display(HTML(obtener_html_desafio(1)))


def cargar_desafio_2():
    """Actividad No-Code Módulo 2: Entidades vs. Casos de Uso vs. DTOs"""
    display(HTML(obtener_html_desafio(2)))


def cargar_desafio_3():
    """Actividad No-Code Módulo 3: Los 4 Círculos Concéntricos"""
    display(HTML(obtener_html_desafio(3)))


def cargar_desafio_4():
    """Actividad No-Code Módulo 4: El Patrón Humble Object"""
    display(HTML(obtener_html_desafio(4)))


def cargar_desafio_5():
    """Actividad No-Code Módulo 5: Núcleo vs. Detalles"""
    display(HTML(obtener_html_desafio(5)))


def cargar_desafio_6():
    """Actividad No-Code Módulo 6: Las Fronteras del Componente Main"""
    display(HTML(obtener_html_desafio(6)))


def cargar_desafio_7():
    """Actividad No-Code Módulo 7: Test Boundary en Clean Architecture"""
    display(HTML(obtener_html_desafio(7)))
