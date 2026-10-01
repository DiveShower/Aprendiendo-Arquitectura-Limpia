# -*- coding: utf-8 -*-
"""
Módulo de widgets interactivos para la Masterclass de Clean Architecture.
Contiene:
1. Tableros Drag & Drop de clasificación conceptual (con marcadores neutrales sin pistas visuales).
2. Cuestionarios de Opción Múltiple (Multiple Choice) técnicos, rigurosos y basados en Clean Architecture.
"""

import json
from IPython.display import HTML, display


def _generar_tablero_html(widget_id: str, title: str, subtitle: str, items: list, zones: list, quiz: list = None) -> str:
    """
    Genera el HTML5, CSS y JavaScript para el desafío interactivo compuesto:
    - Tablero Drag & Drop (arrastrar o clic).
    - Cuestionario Multiple Choice de criterio arquitectónico.
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

    # Generación de la sección Multiple Choice si existe
    quiz_html = ""
    if quiz:
        quiz_cards = ""
        for q_idx, q in enumerate(quiz):
            opts_html = ""
            for opt in q["opciones"]:
                opts_html += f"""
                <label class="{widget_id}-q-opt" data-qid="{q_idx}" data-opid="{opt['id']}" 
                       style="display: flex; align-items: flex-start; gap: 10px; padding: 9px 12px; margin-bottom: 6px; background: #252538; border: 1px solid #45475a; border-radius: 8px; cursor: pointer; transition: all 0.15s ease; user-select: none;">
                    <input type="radio" name="{widget_id}-q{q_idx}" value="{opt['id']}" style="margin-top: 3px; accent-color: #89b4fa; cursor: pointer;">
                    <span style="font-size: 0.88rem; line-height: 1.35; color: #cdd6f4;"><strong>{opt['id']})</strong> {opt['texto']}</span>
                </label>
                """

            quiz_cards += f"""
            <div id="{widget_id}-qbox-{q_idx}" style="background: #181825; border: 1px solid #313244; border-radius: 10px; padding: 16px; margin-bottom: 14px;">
                <div style="font-weight: 700; color: #fab387; font-size: 0.95rem; margin-bottom: 6px;">
                    {q['titulo']}
                </div>
                <div style="color: #cdd6f4; font-size: 0.9rem; margin-bottom: 12px; line-height: 1.45;">
                    {q['pregunta']}
                </div>
                <div class="{widget_id}-options-group" data-qid="{q_idx}">
                    {opts_html}
                </div>
                <div id="{widget_id}-qexp-{q_idx}" style="display: none; margin-top: 10px; padding: 12px; border-radius: 8px; font-size: 0.85rem; line-height: 1.45; border-left: 4px solid #89b4fa; background: #1e1e2e;">
                    <div style="color: #a6e3a1; font-weight: bold; margin-bottom: 4px;">💡 Fundamento Teórico (Clean Architecture):</div>
                    <div style="color: #cdd6f4; margin-bottom: 8px;">{q['fundamento']}</div>
                    <div style="color: #f38ba8; font-weight: bold; margin-bottom: 2px;">⚠️ Análisis de los Distractores:</div>
                    <div style="color: #a6adc8;">{q['por_que_distractores']}</div>
                </div>
            </div>
            """

        quiz_html = f"""
        <div style="margin-top: 24px; border-top: 2px dashed #45475a; padding-top: 18px;">
            <div style="text-align: center; margin-bottom: 14px;">
                <h5 style="margin: 0 0 4px 0; color: #fab387; font-size: 1.15rem;">📝 Desafío de Criterio Arquitectónico (Opción Múltiple)</h5>
                <p style="margin: 0; color: #a6adc8; font-size: 0.84rem;">Evalúa cada decisión técnica según los principios estrictos de Uncle Bob. Sin zonas grises ni respuestas de broma.</p>
            </div>
            {quiz_cards}
            <div style="display: flex; gap: 10px; align-items: center; justify-content: center; margin-bottom: 10px;">
                <button id="{widget_id}-btn-check-quiz" style="background: #fab387; color: #11111b; border: none; padding: 8px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.88rem;">
                    📝 Validar Cuestionario
                </button>
                <button id="{widget_id}-btn-reset-quiz" style="background: #45475a; color: #cdd6f4; border: none; padding: 8px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.88rem;">
                    🔄 Reintentar Cuestionario
                </button>
            </div>
            <div id="{widget_id}-feedback-quiz" style="display: none; padding: 10px; border-radius: 8px; text-align: center; font-size: 0.9rem; font-weight: 500;"></div>
        </div>
        """

    # Serializar respuestas correctas para JS
    quiz_answers_json = json.dumps({str(idx): q["correcta"] for idx, q in enumerate(quiz)}) if quiz else "{}"

    return f"""
<div id="{widget_id}-container" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 920px; margin: 12px auto; padding: 18px; border-radius: 12px; background: #1e1e2e; color: #cdd6f4; box-shadow: 0 8px 24px rgba(0,0,0,0.35); border: 1px solid #313244;">
    <div style="text-align: center; margin-bottom: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #89b4fa; font-size: 1.25rem;">{title}</h4>
        <p style="margin: 0; color: #a6adc8; font-size: 0.9rem;">{subtitle}</p>
    </div>

    <!-- SECCIÓN 1: DRAG & DROP -->
    <div style="margin-bottom: 16px;">
        <div style="font-weight: 600; margin-bottom: 6px; color: #f9e2af; font-size: 0.88rem;">📦 Parte 1: Clasificación Conceptual ({len(items)} situaciones):</div>
        <div id="{widget_id}-bank" style="display: flex; flex-wrap: wrap; gap: 8px; min-height: 60px; padding: 10px; border: 2px dashed #45475a; border-radius: 8px; background: #181825;">
            {items_html}
        </div>
    </div>

    <!-- ZONAS DE DESTINO -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; margin-bottom: 16px;">
        {zones_html}
    </div>

    <!-- BOTONES Y FEEDBACK DRAG & DROP -->
    <div style="display: flex; gap: 10px; align-items: center; justify-content: center; margin-bottom: 10px;">
        <button id="{widget_id}-btn-check" style="background: #a6e3a1; color: #11111b; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.88rem;">
            ✅ Comprobar Clasificación
        </button>
        <button id="{widget_id}-btn-reset" style="background: #45475a; color: #cdd6f4; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.88rem;">
            🔄 Reiniciar Tablero
        </button>
    </div>

    <div id="{widget_id}-feedback" style="display: none; padding: 10px; border-radius: 8px; text-align: center; font-size: 0.9rem; font-weight: 500;"></div>

    <!-- SECCIÓN 2: MULTIPLE CHOICE QUIZ -->
    {quiz_html}
</div>

<script>
(function() {{
    const container = document.getElementById('{widget_id}-container');
    if (!container) return;

    // --- LÓGICA DRAG & DROP ---
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

    // --- LÓGICA MULTIPLE CHOICE ---
    const btnCheckQuiz = container.querySelector('#{widget_id}-btn-check-quiz');
    const btnResetQuiz = container.querySelector('#{widget_id}-btn-reset-quiz');
    const feedbackQuiz = container.querySelector('#{widget_id}-feedback-quiz');
    const quizAnswers = {quiz_answers_json};

    if (btnCheckQuiz) {{
        btnCheckQuiz.addEventListener('click', () => {{
            let answeredCount = 0;
            let correctQuizCount = 0;
            const totalQuestions = Object.keys(quizAnswers).length;

            for (let qIdx = 0; qIdx < totalQuestions; qIdx++) {{
                const selectedRadio = container.querySelector(`input[name="{widget_id}-q${{qIdx}}"]:checked`);
                if (selectedRadio) {{
                    answeredCount++;
                }}
            }}

            if (answeredCount < totalQuestions) {{
                feedbackQuiz.style.display = 'block';
                feedbackQuiz.style.background = '#fab387';
                feedbackQuiz.style.color = '#11111b';
                feedbackQuiz.innerHTML = `⚠️ Has respondido <strong>${{answeredCount}} de ${{totalQuestions}}</strong> preguntas. Selecciona una opción en cada pregunta antes de validar.`;
                return;
            }}

            for (let qIdx = 0; qIdx < totalQuestions; qIdx++) {{
                const selectedRadio = container.querySelector(`input[name="{widget_id}-q${{qIdx}}"]:checked`);
                const userChoice = selectedRadio ? selectedRadio.value : null;
                const correctChoice = quizAnswers[String(qIdx)];
                const expBox = container.querySelector(`#{widget_id}-qexp-${{qIdx}}`);

                if (expBox) expBox.style.display = 'block';

                const optLabels = container.querySelectorAll(`.{widget_id}-q-opt[data-qid="${{qIdx}}"]`);
                optLabels.forEach(lbl => {{
                    const opid = lbl.dataset.opid;
                    if (opid === correctChoice) {{
                        lbl.style.background = '#1e382b';
                        lbl.style.border = '2px solid #a6e3a1';
                        lbl.style.color = '#a6e3a1';
                        lbl.style.opacity = '1';
                    }} else if (opid === userChoice && userChoice !== correctChoice) {{
                        lbl.style.background = '#3e2330';
                        lbl.style.border = '2px solid #f38ba8';
                        lbl.style.color = '#f38ba8';
                        lbl.style.opacity = '1';
                    }} else {{
                        lbl.style.background = '#252538';
                        lbl.style.border = '1px solid #45475a';
                        lbl.style.color = '#a6adc8';
                        lbl.style.opacity = '0.5';
                    }}
                }});

                if (userChoice === correctChoice) {{
                    correctQuizCount++;
                }}
            }}

            feedbackQuiz.style.display = 'block';
            if (correctQuizCount === totalQuestions) {{
                feedbackQuiz.style.background = '#a6e3a1';
                feedbackQuiz.style.color = '#11111b';
                feedbackQuiz.innerHTML = `🎉 <strong>¡SOBRESALIENTE! (${{correctQuizCount}}/${{totalQuestions}})</strong> Criterio arquitectónico perfecto. Lee los fundamentos para consolidar el aprendizaje.`;
            }} else {{
                feedbackQuiz.style.background = '#f38ba8';
                feedbackQuiz.style.color = '#11111b';
                feedbackQuiz.innerHTML = `Puntaje: <strong>${{correctQuizCount}} / ${{totalQuestions}}</strong> correctas. Analiza los fundamentos teóricos y las explicaciones de los distractores para afianzar el concepto.`;
            }}
        }});
    }}

    if (btnResetQuiz) {{
        btnResetQuiz.addEventListener('click', () => {{
            const totalQuestions = Object.keys(quizAnswers).length;
            for (let qIdx = 0; qIdx < totalQuestions; qIdx++) {{
                const radios = container.querySelectorAll(`input[name="{widget_id}-q${{qIdx}}"]`);
                radios.forEach(r => r.checked = false);

                const optLabels = container.querySelectorAll(`.{widget_id}-q-opt[data-qid="${{qIdx}}"]`);
                optLabels.forEach(lbl => {{
                    lbl.style.background = '#252538';
                    lbl.style.border = '1px solid #45475a';
                    lbl.style.color = '#cdd6f4';
                    lbl.style.opacity = '1';
                }});

                const expBox = container.querySelector(`#{widget_id}-qexp-${{qIdx}}`);
                if (expBox) expBox.style.display = 'none';
            }}
            if (feedbackQuiz) feedbackQuiz.style.display = 'none';
        }});
    }}
}})();
</script>
"""


# ==============================================================================
# CONFIGURACIÓN COMPLETA DE LOS 8 DESAFÍOS (DRAG & DROP + MULTIPLE CHOICE)
# ==============================================================================

DESAFIOS_CONFIG = {
    0: {
        "id": "dd0",
        "title": "🎮 Desafío 0: Matriz de Eisenhower y los Dos Valores del Software",
        "subtitle": "Clasifica las situaciones en sus cuadrantes y demuestra criterio arquitectónico",
        "items": [
            {"id": 1, "text": "📌 Caída imprevista del servidor de base de datos en entorno de producción", "target": "c1"},
            {"id": 2, "text": "📌 Refactorizar para separar reglas de negocio de la base de datos", "target": "c2"},
            {"id": 3, "text": "📌 Definir interfaces abstractas para desacoplar pasarelas de pago externas", "target": "c2"},
            {"id": 4, "text": "📌 Modificar con prisa el color de un botón para una demo comercial en 20 minutos", "target": "c3"},
            {"id": 5, "text": "📌 Duplicar un bloque de código temporalmente para salir del paso en la entrega de hoy", "target": "c3"},
            {"id": 6, "text": "📌 Debatir durante 3 horas sobre el uso de comillas simples o dobles en el linter", "target": "c4"}
        ],
        "zones": [
            {"id": "c1", "title": "🚨 Cuadrante 1", "subtitle": "Urgente e Importante (Emergencias)", "color": "#f38ba8"},
            {"id": "c2", "title": "🏛️ Cuadrante 2", "subtitle": "Importante, No Urgente (Arquitectura)", "color": "#a6e3a1"},
            {"id": "c3", "title": "⏰ Cuadrante 3", "subtitle": "Urgente, No Importante (Presión operativa)", "color": "#f9e2af"},
            {"id": "c4", "title": "🗑️ Cuadrante 4", "subtitle": "Ni Urgente ni Importante (Desperdicio)", "color": "#6c7086"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 0.1: El Dilema Fundamental de los Dos Valores del Software",
                "pregunta": "Según Robert C. Martin (Cap. 2), todo software proporciona dos valores a la organización: Comportamiento (funcionalidad actual) y Estructura (arquitectura y facilidad de cambio). ¿Cuál es la relación de jerarquía indiscutible entre ambos y qué ocurre si se prioriza el Comportamiento sobre la Estructura?",
                "opciones": [
                    {"id": "A", "texto": "El Comportamiento tiene mayor jerarquía que la Estructura; si el programa no cumple las funciones de hoy, la empresa quiebra inmediatamente y la arquitectura carece de sentido."},
                    {"id": "B", "texto": "La Estructura tiene un valor superior al Comportamiento; un programa que funciona pero no se puede cambiar queda obsoleto cuando el negocio cambia (su valor cae a cero), mientras que un programa defectuoso pero fácil de modificar puede adaptarse y perfeccionarse rápidamente."},
                    {"id": "C", "texto": "Ambos valores poseen idéntica jerarquía técnica en todo momento, debiendo resolverse cualquier conflicto incorporando más desarrolladores al proyecto."},
                    {"id": "D", "texto": "La Estructura solo es importante en la primera versión del sistema (v1.0); tras la puesta en producción, el Comportamiento absorbe el 100% de la importancia."}
                ],
                "correcta": "B",
                "fundamento": "En el Cap. 2 ('A Tale of Two Values'), Uncle Bob expone: si un software funciona pero es imposible de modificar ante nuevas demandas del negocio, su valor práctico se anula cuando el entorno cambia. En cambio, un software imperfecto pero con una arquitectura limpia y flexible se corrige con bajo costo. Por ende, la arquitectura (facilidad de cambio) es el valor primordial.",
                "por_que_distractores": "A: Es la falacia comercial común que degrada sistemas hasta volverlos inmodificables. C: Viola la ley de Brooks (sumar programadores a un proyecto retrasado lo retrasa más). D: Niega la naturaleza evolutiva del software."
            },
            {
                "titulo": "Pregunta 0.2: La Matriz de Eisenhower en la Priorización Técnica",
                "pregunta": "En el Capítulo 2, Uncle Bob adapta la Matriz de Eisenhower a la ingeniería de software. ¿En qué cuadrante reside la Arquitectura y cuál es el error sistemático que cometen los equipos que terminan con bases de código degradadas?",
                "opciones": [
                    {"id": "A", "texto": "La Arquitectura reside en el Cuadrante 1 (Urgente e Importante); el error de los equipos es considerarla una emergencia imprevista en lugar de planificarla."},
                    {"id": "B", "texto": "La Arquitectura reside en el Cuadrante 2 (Importante, pero No Urgente); el error sistemático consiste en capitular ante las presiones del Cuadrante 3 (Urgente, pero No Importante), sacrificando el diseño a largo plazo por features apresuradas."},
                    {"id": "C", "texto": "La Arquitectura reside en el Cuadrante 3 (Urgente, pero No Importante); el error de los equipos es dedicarle demasiadas horas en sprint planning."},
                    {"id": "D", "texto": "La Arquitectura reside en el Cuadrante 4 (Ni Urgente ni Importante); el error es realizar refactorizaciones sobre módulos que ya están compilando sin errores."}
                ],
                "correcta": "B",
                "fundamento": "Uncle Bob explica que las tareas arquitectónicas casi nunca tienen la urgencia del día impuesta por clientes apresurados (pertenecen al Cuadrante 2). La falla crítica de los equipos radica en permitir que tareas del Cuadrante 3 (urgencias operativas de bajo impacto estructural) desplacen y destruyan la inversión en la arquitectura.",
                "por_que_distractores": "A: Confunde arquitectura con apagar incendios en producción. C y D: Catalogan erróneamente la arquitectura como prescindible o no importante."
            }
        ]
    },
    1: {
        "id": "dd1",
        "title": "🎮 Desafío 1: Diagnóstico de Principios SOLID en la Arquitectura",
        "subtitle": "Identifica los síntomas de diseño y evalúa las definiciones arquitectónicas formales",
        "items": [
            {"id": 1, "text": "📌 Finanzas modificó el cálculo de horas extra y alteró sin querer los reportes de Operaciones", "target": "srp"},
            {"id": 2, "text": "📌 Para soportar un nuevo proveedor de pagos tuvimos que editar 8 clases con condicionales if", "target": "ocp"},
            {"id": 3, "text": "📌 Una clase de pedidos importa directamente el cliente SDK concreto de un servicio externo", "target": "dip"},
            {"id": 4, "text": "📌 Un cliente que solo consulta saldo está obligado a implementar 12 métodos que no utiliza", "target": "isp"},
            {"id": 5, "text": "📌 Una subclase lanza una excepción inesperada al recibir un argumento válido para su clase base", "target": "lsp"},
            {"id": 6, "text": "📌 Definir una interfaz PasarelaPago para que el procesador no conozca librerías externas", "target": "dip"}
        ],
        "zones": [
            {"id": "srp", "title": "👤 SRP", "subtitle": "Responsabilidad Única (Actores)", "color": "#f9e2af"},
            {"id": "ocp", "title": "🔓 OCP", "subtitle": "Abierto/Cerrado (Extensión)", "color": "#a6e3a1"},
            {"id": "lsp", "title": "📐 LSP", "subtitle": "Sustitución de Liskov (Contratos)", "color": "#89dceb"},
            {"id": "isp", "title": "✂️ ISP", "subtitle": "Segregación de Interfaces", "color": "#cba6f7"},
            {"id": "dip", "title": "🔄 DIP", "subtitle": "Inversión de Dependencias", "color": "#f38ba8"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 1.1: El Verdadero Significado de SRP a Nivel Arquitectónico",
                "pregunta": "Uncle Bob subraya en el Capítulo 7 que el Principio de Responsabilidad Única (SRP) es el principio más incomprendido de SOLID. ¿Cuál es la formulación arquitectónica precisa que Uncle Bob estipula para evitar este error?",
                "opciones": [
                    {"id": "A", "texto": "\"Cada función o clase debe limitarse estrictamente a una única línea de ejecución o a un solo método público.\""},
                    {"id": "B", "texto": "\"Un módulo debe ser responsable ante un único actor (stakeholder, departamento o usuario que representa una fuente de cambio).\" Si dos actores distintos demandan lógicas sobre el mismo módulo, deben segregarse en módulos independientes."},
                    {"id": "C", "texto": "\"Cada archivo de código debe contener únicamente una estructura de datos sin funciones asociadas.\""},
                    {"id": "D", "texto": "\"Un componente de software debe desplegarse en un único contenedor o proceso aislado del sistema operativo.\""}
                ],
                "correcta": "B",
                "fundamento": "En el Cap. 7, Uncle Bob enfatiza: \"'Un módulo debe hacer una sola cosa' es una regla para funciones pequeñas, no para SRP. La versión formal de SRP es: Un módulo debe ser responsable ante uno, y solo uno, actor'. Si la clase Empleado contiene el método calcularPago() [usado por Finanzas] y reportarHoras() [usado por Operaciones], un cambio de Finanzas puede romper Operaciones, violando SRP.",
                "por_que_distractores": "A: Confunde SRP con la regla de funciones de Clean Code. C: Confunde SRP con la prohibición de métodos. D: Confunde un principio de diseño lógico con topología de despliegue físico."
            },
            {
                "titulo": "Pregunta 1.2: Inversión de Dependencias (DIP) y Flujos de Control",
                "pregunta": "En una arquitectura procedimental clásica, las dependencias de código fuente siguen la misma dirección del flujo de control en ejecución. Según el Principio de Inversión de Dependencias (DIP, Cap. 11), ¿qué sucede en la relación entre el Caso de Uso de negocio y el Repositorio de base de datos?",
                "opciones": [
                    {"id": "A", "texto": "El flujo de control se invierte: la base de datos toma la iniciativa e invoca al caso de uso mediante polling de eventos."},
                    {"id": "B", "texto": "La dependencia de código fuente se invierte en contra del flujo de control: el caso de uso define y es dueño de la interfaz (puerto), y el código de la base de datos depende de esa interfaz para implementarla."},
                    {"id": "C", "texto": "Se elimina la necesidad de escribir interfaces, permitiendo que ambas clases se comuniquen directamente mediante llamadas a funciones globales sin tipado."},
                    {"id": "D", "texto": "El caso de uso debe heredar directamente de la clase ORM de la base de datos para acceder a sus métodos de persistencia."}
                ],
                "correcta": "B",
                "fundamento": "En el Cap. 11, Uncle Bob ilustra que el polimorfismo orientado a objetos permite crear una 'inversión de dependencias': en tiempo de ejecución, el caso de uso invoca al repositorio (el flujo de control va de adentro hacia afuera), pero en el código fuente, la clase de persistencia importa e implementa la interfaz del caso de uso (la dependencia apunta hacia adentro).",
                "por_que_distractores": "A: Confunde invertir la dependencia del código fuente con invertir el flujo de ejecución (lo cual no ocurre). C: Destruye el desacoplamiento. D: Es una violación flagrante de Clean Architecture y DIP."
            }
        ]
    },
    2: {
        "id": "dd2",
        "title": "🎮 Desafío 2: Entidades vs. Casos de Uso vs. DTOs",
        "subtitle": "Distingue los componentes del núcleo de negocio y sus barreras de aislamiento",
        "items": [
            {"id": 1, "text": "📌 Regla de cálculo de cuota mensual según amortización francesa", "target": "ent"},
            {"id": 2, "text": "📌 Validar que el saldo de la cuenta no supere el límite de descubierto acordado", "target": "ent"},
            {"id": 3, "text": "📌 Orquestar: buscar préstamo, verificar solicitante, aprobar y persistir", "target": "uc"},
            {"id": 4, "text": "📌 Coordinar el flujo entre la pasarela de pago y la cuenta de destino", "target": "uc"},
            {"id": 5, "text": "📌 SolicitudPrestamoRequest (id_cliente, monto, plazo_meses)", "target": "dto"},
            {"id": 6, "text": "📌 SolicitudPrestamoResponse (exito, mensaje, total_a_devolver)", "target": "dto"}
        ],
        "zones": [
            {"id": "ent", "title": "🌟 Entidades", "subtitle": "Reglas Críticas de Empresa", "color": "#f9e2af"},
            {"id": "uc", "title": "⚙️ Casos de Uso", "subtitle": "Reglas de la Aplicación", "color": "#f38ba8"},
            {"id": "dto", "title": "📦 DTOs (Request / Response)", "subtitle": "Estructuras de Datos Planas", "color": "#a6e3a1"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 2.1: La Autonomía de las Reglas Críticas de Negocio (Entidades)",
                "pregunta": "En los Capítulos 19 y 20, Robert C. Martin clasifica las reglas de negocio en 'Reglas Críticas de Empresa' (Entidades) y 'Reglas de la Aplicación' (Casos de Uso). ¿Cuál es la prueba conceptual irrefutable para determinar si una regla pertenece a una Entidad?",
                "opciones": [
                    {"id": "A", "texto": "La regla requiere consultar una tabla SQL con más de 10.000 registros para ser evaluada."},
                    {"id": "B", "texto": "La regla existiría y tendría pleno sentido económico/operativo para el negocio incluso si no existieran computadoras ni software (ej. calculada manualmente por empleados con lápiz y papel)."},
                    {"id": "C", "texto": "La regla está decorada con anotaciones de serialización JSON para ser enviada por la red."},
                    {"id": "D", "texto": "La regla valida exclusivamente el formato de las cabeceras HTTP de una petición entrante."}
                ],
                "correcta": "B",
                "fundamento": "Uncle Bob define las 'Critical Business Rules' (Cap. 19) como aquellas políticas intrínsecas al negocio que hacen o ahorran dinero, independientemente de si están computarizadas o no. Un banco cobraba intereses y verificaba saldos antes de que existieran las computadoras. Esas reglas y los datos que operan forman las Entidades puras.",
                "por_que_distractores": "A: Mezcla persistencia con lógica de dominio. C: Confunde transporte de datos con negocio. D: Describe responsabilidades de controladores web."
            },
            {
                "titulo": "Pregunta 2.2: La Fuga de Entidades en las Fronteras de los Casos de Uso",
                "pregunta": "En el flujo de entrada y salida de un Caso de Uso (Cap. 20), ¿por qué es una mala práctica arquitectónica hacer que el Caso de Uso reciba objetos HttpRequest o retorne las instancias directas de las Entidades hacia la presentación?",
                "opciones": [
                    {"id": "A", "texto": "Porque los navegadores web modernos no son capaces de interpretar objetos nativos de Python o Java."},
                    {"id": "B", "texto": "Porque pasar HttpRequest ata el caso de uso al protocolo web impidiendo reusarlo (ej. en CLI o colas), y retornar la Entidad acopla la vista a su estructura interna permitiendo que la UI invoque métodos de negocio o altere su estado eludiendo el caso de uso."},
                    {"id": "C", "texto": "Porque Clean Architecture exige que todas las respuestas de un caso de uso sean cadenas de texto serializadas en XML."},
                    {"id": "D", "texto": "Porque las Entidades consumen un 80% más de memoria que los modelos Request/Response DTOs."}
                ],
                "correcta": "B",
                "fundamento": "En el Cap. 20 ('Request and Response Models'), Uncle Bob explica que los DTOs aíslan el caso de uso. Si el caso de uso recibe HttpRequest, no puedes probarlo sin simular la web ni ejecutarlo desde un batch. Si devuelves la Entidad a la vista, la vista puede mutar los campos de la entidad o crear dependencias transitivas entre la UI y el modelo de negocio.",
                "por_que_distractores": "A: Inventa una restricción técnica inexistente. C: Promueve anti-patrones obsoletos. D: Cita métricas de rendimiento sin fundamento técnico."
            }
        ]
    },
    3: {
        "id": "dd3",
        "title": "🎮 Desafío 3: Los 4 Círculos Concéntricos de Clean Architecture",
        "subtitle": "Ubica componentes en sus círculos y valida la Regla de Dependencia",
        "items": [
            {"id": 1, "text": "📌 Entidad CuentaBancaria con reglas de validación de saldo", "target": "c1"},
            {"id": 2, "text": "📌 TransferirDineroUseCase (orquestador del flujo de negocio)", "target": "c2"},
            {"id": 3, "text": "📌 Interfaz abstracta CuentaRepositoryPort (puerto del caso de uso)", "target": "c2"},
            {"id": 4, "text": "📌 TransferenciaPresenter (transforma respuesta de negocio a ViewModel)", "target": "c3"},
            {"id": 5, "text": "📌 HttpWebController (recibe y parsea JSON)", "target": "c3"},
            {"id": 6, "text": "📌 Base de Datos PostgreSQL y sentencias SQL", "target": "c4"},
            {"id": 7, "text": "📌 Framework FastAPI / Flask / Django", "target": "c4"}
        ],
        "zones": [
            {"id": "c1", "title": "🟡 1. Entidades", "subtitle": "Enterprise Business Rules", "color": "#f9e2af"},
            {"id": "c2", "title": "🔴 2. Casos de Uso", "subtitle": "Application Business Rules", "color": "#f38ba8"},
            {"id": "c3", "title": "🟢 3. Adaptadores", "subtitle": "Controllers, Presenters", "color": "#a6e3a1"},
            {"id": "c4", "title": "🔵 4. Frameworks", "subtitle": "DB, Web, Dispositivos", "color": "#89b4fa"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 3.1: El Alcance Estricto de la Regla de Dependencia",
                "pregunta": "El diagrama de los círculos concéntricos (Cap. 22) se rige por la Regla de Dependencia. ¿Cuál es el significado formal de esta regla sobre los identificadores y elementos de código?",
                "opciones": [
                    {"id": "A", "texto": "\"Las dependencias de código fuente solo pueden apuntar hacia adentro: nada en un círculo interno puede mencionar o importar el nombre de nada que pertenezca a un círculo externo (clases, funciones, librerías o esquemas).\""},
                    {"id": "B", "texto": "\"Las capas externas solo pueden comunicarse con las capas internas a través de llamadas de red HTTP REST.\""},
                    {"id": "C", "texto": "\"El código de la base de datos debe ser el centro del diagrama concéntrico, y las entidades deben importar los modelos relacionales.\""},
                    {"id": "D", "texto": "\"Los círculos internos pueden depender de librerías externas siempre que esas librerías tengan más de 10.000 estrellas en GitHub.\""}
                ],
                "correcta": "A",
                "fundamento": "Uncle Bob es categórico en el Cap. 22: 'The name of something declared in an outer circle must not be mentioned by the code in an inner circle. That includes functions, classes, variables, or any other named software entity.' Las dependencias de código fuente solo van hacia adentro.",
                "por_que_distractores": "B: Confunde fronteras de código en memoria con microservicios de red. C: Es la antítesis de Clean Architecture (arquitectura centrada en BD). D: Es una regla arbitraria sin rigor técnico."
            },
            {
                "titulo": "Pregunta 3.2: Cruce de Fronteras Polimórfico (Output Ports)",
                "pregunta": "Cuando un Caso de Uso necesita persistir un cambio o entregar el resultado formateado a un Presenter, ¿dónde debe residir formalmente la interfaz abstracta (puerto) que permite este cruce de frontera sin infringir la Regla de Dependencia?",
                "opciones": [
                    {"id": "A", "texto": "La interfaz debe residir en el Círculo 4 (Frameworks) para que el motor de base de datos la gestione directamente."},
                    {"id": "B", "texto": "La interfaz debe residir dentro del Círculo 2 (Casos de Uso), y las clases concretas de los círculos externos (3 y 4) deben implementar dicha interfaz."},
                    {"id": "C", "texto": "La interfaz debe residir en un archivo de configuración JSON cargado dinámicamente en el sistema operativo."},
                    {"id": "D", "texto": "No deben usarse interfaces; el caso de uso debe instanciar directamente el Presenter o la Base de Datos con la palabra clave 'new'."}
                ],
                "correcta": "B",
                "fundamento": "En el Cap. 22 (diagrama de 'Crossing Boundaries'), el caso de uso interactúa con el Input Boundary y el Output Boundary. Ambas interfaces residen dentro de la capa del Caso de Uso. El Presenter y el Repositorio de la capa externa implementan estas interfaces, garantizando que todas las flechas de dependencia del código fuente apunten hacia el centro.",
                "por_que_distractores": "A: Haría que el caso de uso importe el Círculo 4, violando la Regla de Dependencia. C: Carece de tipado estático y compilabilidad. D: Acopla rígidamente e impide el testing unitario."
            }
        ]
    },
    4: {
        "id": "dd4",
        "title": "🎮 Desafío 4: El Patrón Humble Object (Presenters y ViewModels)",
        "subtitle": "Separa responsabilidades testeables de infraestructura pasiva",
        "items": [
            {"id": 1, "text": "📌 Presenter: transformar Decimal('14400.00') a '$ 14.400,00 ARS'", "target": "intel"},
            {"id": 2, "text": "📌 Presenter: evaluar condiciones de respuesta para asignar la etiqueta 'APROBADO'", "target": "intel"},
            {"id": 3, "text": "📌 Presenter: determinar si el color de la alerta visual debe ser verde o rojo", "target": "intel"},
            {"id": 4, "text": "📌 Vista: imprimir por consola la variable viewModel.total_formateado", "target": "humilde"},
            {"id": 5, "text": "📌 Template HTML: estampar {{ viewModel.estado }} sin ningún condicional if", "target": "humilde"},
            {"id": 6, "text": "📌 Socket SQL: enviar bytes del string query directamente al puerto de la base de datos", "target": "humilde"}
        ],
        "zones": [
            {"id": "intel", "title": "🧠 Objeto Inteligente", "subtitle": "Presenter / ViewModel (Testeable)", "color": "#a6e3a1"},
            {"id": "humilde", "title": "🙈 Objeto Humilde", "subtitle": "Vista / UI / I/O puro (Sin lógica)", "color": "#f9e2af"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 4.1: Justificación del Patrón Humble Object en la Interfaz de Usuario",
                "pregunta": "En el patrón Humble Object (Cap. 23), ¿cuál es la razón técnica primordial para segregar una frontera en dos componentes, uno 'Inteligente' y otro 'Humilde'?",
                "opciones": [
                    {"id": "A", "texto": "Para que los diseñadores gráficos puedan escribir código de base de datos directamente en las plantillas HTML."},
                    {"id": "B", "texto": "Porque la Vista es difícil de testear de forma automatizada sin herramientas visuales lentas y frágiles; al vaciarla de lógica y trasladar todas las decisiones al Presenter (fácil de testear), la Vista queda tan 'humilde' que no requiere pruebas complejas."},
                    {"id": "C", "texto": "Para duplicar intencionalmente las clases del sistema y cumplir con métricas de volumen de código."},
                    {"id": "D", "texto": "Porque los navegadores web modernos rechazan páginas HTML que no incluyan un objeto ViewModel serializado en base64."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 23 ('The Humble Object Pattern'). Uncle Bob explica que las GUIs son complejas de probar de forma desatendida. Al crear un Presenter que opera sobre datos puros y produce un ViewModel con cadenas de texto y booleanos ya resueltos, el Presenter se prueba con tests unitarios instantáneos, y la Vista solo se limita a pintar esos valores en pantalla sin bifurcaciones condicionales.",
                "por_que_distractores": "A: Mezcla capas destructivamente. C: Promueve malas prácticas. D: Es un absurdo técnico sin relación con la web."
            },
            {
                "titulo": "Pregunta 4.2: La Naturaleza Estricta del ViewModel",
                "pregunta": "¿Cuál de las siguientes afirmaciones describe con absoluta fidelidad lo que DEBE y lo que NUNCA DEBE contener un ViewModel según la arquitectura limpia de Uncle Bob?",
                "opciones": [
                    {"id": "A", "texto": "Debe contener métodos que ejecuten consultas a la base de datos relacional y transacciones monetarias."},
                    {"id": "B", "texto": "Debe ser puramente una estructura de datos pasiva con datos primitivos formateados (strings, flags booleanas, floats); NUNCA debe contener métodos con bifurcaciones condicionales ('if/else'), reglas de negocio ni referencias a Entidades."},
                    {"id": "C", "texto": "Debe contener exclusivamente objetos de sesión HTTP de frameworks web y cookies criptográficas."},
                    {"id": "D", "texto": "Debe contener las sentencias SQL de actualización de la cuenta bancaria del usuario."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 23. Uncle Bob aclara que el ViewModel es solo una estructura de datos ('a simple data structure'). Si el ViewModel contiene lógica o métodos de decisión, entonces requeriría sus propias pruebas de negocio complejas y la frontera perdería su valor. Toda la decisión la toma el Presenter; el ViewModel solo almacena el resultado final listo para mostrar.",
                "por_que_distractores": "A y D: Violación masiva que mete persistencia en la vista. C: Ata el ViewModel a un protocolo de transporte efímero."
            }
        ]
    },
    5: {
        "id": "dd5",
        "title": "🎮 Desafío 5: Arquitectura Gritante (Screaming) y la Política de Detalles",
        "subtitle": "Distingue lo esencial del negocio de los plugins e implementaciones accesorias",
        "items": [
            {"id": 1, "text": "📌 Reglas de scoring crediticio y cálculo de capacidad de endeudamiento", "target": "arch"},
            {"id": 2, "text": "📌 Caso de uso de Apertura de Cuenta Bancaria con depósito inicial", "target": "arch"},
            {"id": 3, "text": "📌 Políticas de comisiones por descubierto y topes de extracción diaria", "target": "arch"},
            {"id": 4, "text": "📌 Motor de Base de Datos relacional PostgreSQL", "target": "det"},
            {"id": 5, "text": "📌 Mecanismo de entrega Web HTTP / Framework FastAPI", "target": "det"},
            {"id": 6, "text": "📌 Driver de conexión a red o librería ORM", "target": "det"}
        ],
        "zones": [
            {"id": "arch", "title": "🏛️ Arquitectura Esencial", "subtitle": "Reglas de Negocio (Screaming Architecture)", "color": "#f9e2af"},
            {"id": "det", "title": "🔌 Detalles Periféricos", "subtitle": "Plugins intercambiables (DB, Web, Frameworks)", "color": "#89b4fa"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 5.1: El Concepto de \"Screaming Architecture\"",
                "pregunta": "En el Capítulo 21, Uncle Bob plantea que la arquitectura debe \"gritar\" el dominio del negocio. ¿Cuál de las siguientes estructuras de proyecto refleja fielmente este mandato arquitectónico?",
                "opciones": [
                    {"id": "A", "texto": "Un directorio raíz dividido en: /controllers, /models, /views, /middlewares, /routes (esquema genérico impuesto por el framework)."},
                    {"id": "B", "texto": "Un directorio raíz dividido en los componentes del dominio: /prestamos, /cuentas, /pagos, /clientes, donde cada componente expone sus entidades y casos de uso de negocio con total independencia del framework web utilizado."},
                    {"id": "C", "texto": "Un directorio con un único archivo script monolítico de 10.000 líneas para asegurar que todo el código se compile al mismo tiempo."},
                    {"id": "D", "texto": "Un directorio organizado según los servidores físicos donde se desplegará cada archivo binario."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 21 ('Screaming Architecture'). Uncle Bob argumenta que si la estructura de carpetas grita '¡Rails!' o '¡Spring!', la arquitectura está supeditada al framework. Si la arquitectura grita '¡Sistema de Préstamos!', el dominio está en primer plano y los frameworks son meros plugins intercambiables.",
                "por_que_distractores": "A: Es el antipatrón clásico de empaquetado por capa tecnológica donde el negocio queda sepultado. C: Es código espagueti inmanejable. D: Confunde topología de servidores con arquitectura de software."
            },
            {
                "titulo": "Pregunta 5.2: La Política de Detalles: Retrasar Decisiones Técnicas",
                "pregunta": "Uno de los mayores beneficios de reconocer que la Web, los Frameworks y las Bases de Datos son 'Detalles' (Cap. 15 y 30) es la capacidad de posponer decisiones. ¿Cuál es la ventaja estratégica de posponer la elección de una base de datos específica al inicio del proyecto?",
                "opciones": [
                    {"id": "A", "texto": "Permite a los desarrolladores evitar escribir pruebas unitarias hasta el final del desarrollo."},
                    {"id": "B", "texto": "Permite avanzar en el desarrollo y validación de las reglas de negocio y casos de uso con repositorios en memoria, postergando la elección tecnológica hasta contar con la mayor información real sobre carga, concurrencia y costos."},
                    {"id": "C", "texto": "Garantiza que el software nunca necesite una base de datos en ningún momento de su existencia comercial."},
                    {"id": "D", "texto": "Obliga a que todo el software deba reescribirse obligatoriamente en C++ antes de ir a producción."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 15 ('What is Architecture?') y Cap. 30. Uncle Bob sostiene: 'Una buena arquitectura maximiza la cantidad de decisiones no tomadas'. Si desacoplas el negocio de la base de datos, puedes comenzar a desarrollar inmediatamente, iterar el negocio y decidir si necesitas SQL, NoSQL o un motor en memoria cuando conozcas las métricas reales del sistema.",
                "por_que_distractores": "A: Falso (las pruebas se escriben desde el día 1 gracias a repositorios en memoria). C: Falso (la persistencia se conecta más tarde). D: Disparate sin relación técnica."
            }
        ]
    },
    6: {
        "id": "dd6",
        "title": "🎮 Desafío 6: Las Fronteras del Componente Main",
        "subtitle": "Determina qué responsabilidades corresponden a la raíz de composición",
        "items": [
            {"id": 1, "text": "📌 Instanciar la base de datos concreta PostgresCuentaRepository", "target": "main_si"},
            {"id": 2, "text": "📌 Inyectar el repositorio concreto dentro del caso de uso", "target": "main_si"},
            {"id": 3, "text": "📌 Leer variables de entorno (prod vs test) y configurar plugins", "target": "main_si"},
            {"id": 4, "text": "📌 Calcular si el cliente califica para un préstamo bancario", "target": "main_no"},
            {"id": 5, "text": "📌 Validar si el saldo es suficiente para la extracción", "target": "main_no"},
            {"id": 6, "text": "📌 Formatear el mensaje de salida con símbolos de moneda y colores", "target": "main_no"}
        ],
        "zones": [
            {"id": "main_si", "title": "🔌 Pertenece a Main", "subtitle": "Composition Root / Cableado", "color": "#a6e3a1"},
            {"id": "main_no", "title": "🚫 NUNCA debe estar en Main", "subtitle": "Reglas de Negocio / Presentación", "color": "#f38ba8"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 6.1: El Papel de Main como \"Composition Root\"",
                "pregunta": "En el Capítulo 26, Uncle Bob presenta al componente Main como el componente más externo y detallado. ¿Cuál es su misión exclusiva dentro de una arquitectura limpia?",
                "opciones": [
                    {"id": "A", "texto": "Ejecutar los algoritmos críticos de cálculo de impuestos y comisiones del sistema."},
                    {"id": "B", "texto": "Actuar como la raíz de composición (Composition Root): leer configuraciones externas, instanciar los adaptadores concretos, inyectarlos en los casos de uso y ceder el control al controlador inicial."},
                    {"id": "C", "texto": "Servir de cortafuegos de red para bloquear peticiones HTTP maliciosas."},
                    {"id": "D", "texto": "Reemplazar a las clases de Entidad para centralizar todas las variables del sistema en un solo punto."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 26 ('The Main Component'). Main es el punto de entrada que crea las fábricas, inicializa las bases de datos concretas, inyecta las dependencias en los casos de uso y arranca el sistema. No contiene lógica de negocio; es el pegamento de más bajo nivel que arma el rompecabezas.",
                "por_que_distractores": "A: Viola las fronteras de negocio. C: Confunde infraestructura de red con código de inicio. D: Destruye el encapsulamiento de dominio."
            },
            {
                "titulo": "Pregunta 6.2: La Protección del Núcleo ante Cambios de Infraestructura",
                "pregunta": "Si tu empresa decide migrar de un motor SQL relacional a un servicio en la nube NoSQL de alta concurrencia, ¿qué componentes del sistema deben verse afectados según las fronteras de Clean Architecture?",
                "opciones": [
                    {"id": "A", "texto": "Se deben modificar las Entidades y reescribir todos los Casos de Uso desde cero."},
                    {"id": "B", "texto": "Únicamente se crea una nueva implementación del puerto repositorio (ej. MongoRepository) y se actualiza el cableado en el componente Main; las Entidades y Casos de Uso permanecen 100% intactos."},
                    {"id": "C", "texto": "Se deben cambiar los modelos Request y Response DTOs para que incluyan sintaxis BSON de MongoDB."},
                    {"id": "D", "texto": "Se debe eliminar el Presenter porque las bases NoSQL renderizan el HTML directamente."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 26. Este es el gran triunfo de Clean Architecture: el caso de uso solo conoce la interfaz (puerto) y Main se encarga de inyectar la implementación. Cambiar de Postgres a Mongo solo implica crear el nuevo plugin de persistencia y cambiar una línea en Main.",
                "por_que_distractores": "A: Demuestra un diseño acoplado y frágil. C: Viola el aislamiento de los DTOs con tipos de terceros. D: Afirmación sin sustento técnico."
            }
        ]
    },
    7: {
        "id": "dd7",
        "title": "🎮 Desafío 7: Test Boundary en Clean Architecture",
        "subtitle": "Identifica las pruebas que respetan los límites arquitectónicos de Uncle Bob",
        "items": [
            {"id": 1, "text": "📌 Probar el Caso de Uso inyectando un Repositorio en Memoria (Fake)", "target": "clean_t"},
            {"id": 2, "text": "📌 Probar las reglas críticas de la Entidad directamente en memoria", "target": "clean_t"},
            {"id": 3, "text": "📌 Probar el Presenter comprobando que el ViewModel tenga las cadenas formateadas", "target": "clean_t"},
            {"id": 4, "text": "📌 Levantar un contenedor Docker con PostgreSQL real para probar un cálculo de suma", "target": "fragil_t"},
            {"id": 5, "text": "📌 Abrir un navegador con Selenium para comprobar una regla de negocio del caso de uso", "target": "fragil_t"},
            {"id": 6, "text": "📌 Probar la UI haciendo que la prueba dependa del esquema de tablas de la base de datos", "target": "fragil_t"}
        ],
        "zones": [
            {"id": "clean_t", "title": "⚡ Pruebas en Clean Architecture", "subtitle": "Aisladas, corren en milisegundos (Puertos)", "color": "#a6e3a1"},
            {"id": "fragil_t", "title": "🐢 Pruebas Frágiles / Acopladas", "subtitle": "Dependen de sockets, red o servidores", "color": "#f38ba8"}
        ],
        "quiz": [
            {
                "titulo": "Pregunta 7.1: El Problema de las Pruebas Frágiles (The Fragile Test Problem)",
                "pregunta": "En el Capítulo 28 ('The Test Boundary'), Uncle Bob advierte sobre la fragilidad de las suites de prueba. ¿Qué diseño de tests provoca este síndrome y qué consecuencia crítica acarrea para el equipo?",
                "opciones": [
                    {"id": "A", "texto": "Escribir tests unitarios que se ejecutan en 5 milisegundos en memoria RAM."},
                    {"id": "B", "texto": "Acoplar las pruebas a detalles volátiles como la estructura del DOM/HTML de la interfaz de usuario o esquemas específicos de bases de datos. Ante cualquier cambio cosmético, decenas de pruebas fallan, lo que lleva al equipo a desactivar o dejar de mantener la suite de pruebas."},
                    {"id": "C", "texto": "Utilizar aserciones estrictas sobre los cálculos financieros de las entidades."},
                    {"id": "D", "texto": "Probar casos de uso utilizando dobles de prueba (Fakes/Mocks) desacoplados de la red."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 28 ('The Test Boundary'). Cuando las pruebas dependen de la UI o de las tablas de la BD, cualquier cambio cosmético rompe los tests sin que haya un error de negocio real. Con el tiempo, el equipo pierde la confianza en la suite, la considera un estorbo y deja de ejecutarla, perdiendo su red de seguridad.",
                "por_que_distractores": "A y D: Describen la práctica correcta y recomendada en Clean Architecture. C: Es una buena práctica para validar reglas críticas."
            },
            {
                "titulo": "Pregunta 7.2: La API de Pruebas (Testing API)",
                "pregunta": "¿Cuál es el rol arquitectónico de la 'Testing API' recomendada por Uncle Bob en el Capítulo 28?",
                "opciones": [
                    {"id": "A", "texto": "Es un endpoint REST expuesto a los usuarios para que prueben funcionalidades beta en producción."},
                    {"id": "B", "texto": "Es un superpuerto que otorga a los tests acceso directo a los casos de uso y permite verificar el sistema sorteando la UI, la seguridad efímera y la infraestructura, permitiendo que la arquitectura se refactorice sin romper las pruebas."},
                    {"id": "C", "texto": "Es una librería de terceros obligatoria para compilar programas en Python."},
                    {"id": "D", "texto": "Es un procedimiento almacenado dentro del servidor de base de datos que borra todas las tablas cada medianoche."}
                ],
                "correcta": "B",
                "fundamento": "Cap. 28. Uncle Bob define la Testing API como una capa de abstracción dedicada a las pruebas: permite a la suite ejecutar cualquier caso de uso con datos estructurados, verificar invariantes de negocio y mockear puertos externos con rapidez extrema, sin que los tests se rompan si cambia el diseño visual o el framework web.",
                "por_que_distractores": "A: Describe un canal de beta-testing de producto, no una Testing API arquitectónica. C y D: Son afirmaciones sin sentido técnico."
            }
        ]
    }
}


def obtener_html_desafio(num: int) -> str:
    """Devuelve el código HTML autónomo para el desafío interactivo especificado."""
    cfg = DESAFIOS_CONFIG[num]
    return _generar_tablero_html(cfg["id"], cfg["title"], cfg["subtitle"], cfg["items"], cfg["zones"], cfg.get("quiz", []))


def cargar_desafio_0():
    """Actividad No-Code Módulo 0: Matriz de Eisenhower y los Dos Valores del Software"""
    display(HTML(obtener_html_desafio(0)))


def cargar_desafio_1():
    """Actividad No-Code Módulo 1: Diagnóstico de Principios SOLID en la Arquitectura"""
    display(HTML(obtener_html_desafio(1)))


def cargar_desafio_2():
    """Actividad No-Code Módulo 2: Entidades vs. Casos de Uso vs. DTOs"""
    display(HTML(obtener_html_desafio(2)))


def cargar_desafio_3():
    """Actividad No-Code Módulo 3: Los 4 Círculos Concéntricos de Clean Architecture"""
    display(HTML(obtener_html_desafio(3)))


def cargar_desafio_4():
    """Actividad No-Code Módulo 4: El Patrón Humble Object (Presenters y ViewModels)"""
    display(HTML(obtener_html_desafio(4)))


def cargar_desafio_5():
    """Actividad No-Code Módulo 5: Arquitectura Gritante (Screaming) y la Política de Detalles"""
    display(HTML(obtener_html_desafio(5)))


def cargar_desafio_6():
    """Actividad No-Code Módulo 6: Las Fronteras del Componente Main"""
    display(HTML(obtener_html_desafio(6)))


def cargar_desafio_7():
    """Actividad No-Code Módulo 7: Test Boundary en Clean Architecture"""
    display(HTML(obtener_html_desafio(7)))
