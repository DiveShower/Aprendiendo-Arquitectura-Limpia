# 🏛️ Aprendiendo Arquitectura Limpia (Clean Architecture)
### *A Craftsman's Guide to Software Structure and Design* — Robert C. Martin ("Uncle Bob")

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-blueviolet)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

¡Bienvenido al repositorio **Aprendiendo Arquitectura Limpia**! 

Este proyecto es una **masterclass interactiva en Jupyter Notebook** diseñada meticulosamente para aprender, internalizar y aplicar los conceptos fundamentales de la **Arquitectura Limpia** propuesta por Robert C. Martin (*Uncle Bob*), utilizando como fuentes de estudio directas:
* 📘 **Arquitectura Limpia**: Guía para el artesano de la estructura y el diseño del software (Edición oficial en español).
* 📕 **Clean Architecture**: A Craftsman's Guide to Software Structure and Design (Edición original en inglés).

---

## 🎯 Metodología Pedagógica: Aprende Haciendo

Cada módulo del cuaderno [**`Aprende_Clean_Architecture.ipynb`**](./Aprende_Clean_Architecture.ipynb) sigue una estructura progresiva en **5 fases** para garantizar un aprendizaje profundo sin sobrecarga teórica:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CICLO DE CADA MÓDULO                            │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 📖 Explicación Teórica Intermedia (Conceptos, analogías y reglas)   │
│ 2. 🎮 Actividad No-Code (Tablero interactivo Drag & Drop temático)     │
│ 3. 💻 Código Demostrativo (Ejemplo funcional en Python de referencia)  │
│ 4. 🛠️ Cuadro de Práctica de Código (Plantilla activa SIN resolver)     │
│ 5. ✅ Tests Automáticos (assert / unittest activos en la misma celda)  │
│ 6. 💡 Pistas y Solución (Desplegable <details> opcional para consultar)│
└────────────────────────────────────────────────────────────────────────┘
```

1. **📖 Explicación de Extensión Intermedia**: Ni definiciones simplistas de una línea ni parrafadas abrumadoras. Explicamos el *porqué* de cada decisión, sus costos en el mundo real y las reglas arquitectónicas exactas de Uncle Bob.
2. **🎮 Actividad Previa No-Code (Drag & Drop en cada módulo)**: Tableros interactivos (HTML5 + CSS + JavaScript) ejecutables directamente en el cuaderno. Puedes arrastrar tarjetas o hacer clic para clasificarlas, recibiendo feedback y evaluación instantánea antes de tocar el código.
3. **💻 Código Demostrativo**: Ejemplos claros de referencia construidos con Python moderno (`dataclasses`, `abc`, `typing`, `Decimal`).
4. **🛠️ Práctica Activa (Tú programas)**: Todos los cuadros de laboratorio comienzan **sin resolver** (con `# TODOs`, firmas de métodos y `NotImplementedError`), acompañados de una suite de tests automáticos (`assert` y `unittest`) que evalúan tu código en milisegundos al pulsar **Shift + Enter**.
5. **💡 Pistas y Solución**: Desplegable colapsable al final de cada ejercicio para destrabarte si lo necesitas.

---

## 🗺️ Contenido de los Módulos

```
                                      ▲
                                      │
                ┌────────────────────────────────────────────────────────┐
                │ 🔵 4. FRAMEWORKS & DRIVERS                             │
                │     (Web, DB, UI, Dispositivos, Frameworks externos)   │
                │                                                        │
                │     ┌────────────────────────────────────────────┐     │
                │     │ 🟢 3. INTERFACE ADAPTERS                   │     │
                │     │     (Controllers, Presenters, Gateways)    │     │
                │     │                                            │     │
                │     │     ┌────────────────────────────────┐     │     │
                │     │     │ 🔴 2. APPLICATION BUSINESS     │     │     │
                │     │     │      (Casos de Uso)            │     │     │
                │     │     │                                │     │     │
                │     │     │     ┌────────────────────┐     │     │     │
                │     │     │     │ 🟡 1. ENTERPRISE   │     │     │     │
                │     │     │     │     (Entidades)    │     │     │     │
                │     │     │     └────────────────────┘     │     │     │
                │     │     └────────────────────────────────┘     │     │
                │     └────────────────────────────────────────────┘     │
                └────────────────────────────────────────────────────────┘
                                      │
                          ═══ THE DEPENDENCY RULE ═══
               (Las dependencias SOLO apuntan hacia el centro)
```

| Módulo | Tema Principal | Actividad No-Code (Drag & Drop) | Laboratorio de Código |
| :--- | :--- | :--- | :--- |
| **0. Fundamentos** | ¿Qué es Arquitectura? Comportamiento vs. Estructura y la Matriz de Eisenhower. | 🎮 Clasificación de tareas en los 4 cuadrantes de Eisenhower. | Separar regla de negocio pura de una función espagueti con I/O. |
| **1. Principios SOLID** | SOLID vistos con ojos de Arquitecto (SRP, OCP, LSP, ISP, DIP). | 🎮 Diagnóstico y mapeo de violaciones SOLID en equipos reales. | Refactorizar procesador de cobros aplicando DIP e ISP. |
| **2. El Núcleo** | Reglas Críticas, Entidades, Casos de Uso (Interactors) y DTOs. | 🎮 El Triángulo del Núcleo (Entidades vs. Casos de Uso vs. DTOs). | Entidad `Prestamo` con reglas financieras y DTOs desacoplados. |
| **3. Círculos y Fronteras** | *The Dependency Rule*, cruce de fronteras y Puertos abstractos. | 🎮 Clasificación en los 4 Círculos de Clean Architecture. | Caso de uso `AprobarPrestamoUseCase` conectado mediante Puertos. |
| **4. Adaptadores de Interfaz** | El Patrón *Humble Object*, Presenters y ViewModels. | 🎮 Separación entre Objeto Inteligente y Objeto Humilde. | `PrestamoPresenter` que formatea datos sin condicionales en la UI. |
| **5. Screaming Architecture** | Arquitectura que grita el dominio. La Base de Datos y la Web son detalles. | 🎮 ¿Qué es Arquitectura Esencial y qué es un Detalle/Plugin? | Conectar controladores CLI y Web REST al mismo caso de uso. |
| **6. El Componente Main** | El *Composition Root*, inyección de dependencias e inversión de control. | 🎮 Qué responsabilidades corresponden a `Main` y cuáles NO. | Contenedor de arranque que cablea adaptadores y casos de uso. |
| **7. Test Boundary** | Pruebas unitarias de negocio que corren en milisegundos sin levantar BD. | 🎮 Pruebas de Clean Architecture vs. Pruebas lentas y frágiles. | **Gran Desafío Integrador**: Apertura de cuentas con `unittest`. |
| **8. Empaquetado** | *Package by Component*, pragmatismo y Checklist del Arquitecto. | — | Checklist de autoevaluación para proyectos profesionales. |

---

## 🚀 Puesta en Marcha (Instalación Rápida)

### 1. Clonar el repositorio
```bash
git clone https://github.com/DiveShower/Aprendiendo-Arquitectura-Limpia.git
cd Aprendiendo-Arquitectura-Limpia
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
Instala los paquetes necesarios desde `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Registrar el Kernel en Jupyter
```bash
python -m ipykernel install --user --name clean-arch-venv --display-name "Python (.venv Clean Architecture)"
```

### 5. Abrir el Cuaderno
Abre el proyecto en **VS Code**, **JupyterLab** o **Jupyter Notebook**:
```bash
code .
```
Abre el archivo [**`Aprende_Clean_Architecture.ipynb`**](./Aprende_Clean_Architecture.ipynb), asegúrate de que el kernel seleccionado en la esquina superior derecha sea **`Python (.venv Clean Architecture)`** y ¡comienza a aprender pulsando **Shift + Enter** en cada celda!

---

## 🛡️ El Checklist del Arquitecto Limpio
Antes de dar por terminado un módulo en tus proyectos, audítalo con estas 6 preguntas:
- [ ] **Independencia de Frameworks:** ¿El núcleo de la aplicación puede ejecutarse sin importar Django, Flask, FastAPI o Spring?
- [ ] **Independencia de Base de Datos:** ¿Puedes cambiar de PostgreSQL a MongoDB o a un archivo en memoria modificando únicamente adaptadores externos?
- [ ] **Independencia de UI:** ¿Puedes cambiar la interfaz web por una consola CLI sin alterar una sola línea del caso de uso?
- [ ] **Testeabilidad sin I/O:** ¿Tus pruebas unitarias de negocio corren en milisegundos sin levantar conexiones de red ni bases de datos?
- [ ] **Regla de Dependencia:** ¿Todas las flechas de importación en el código fuente apuntan de afuera hacia adentro?
- [ ] **DTOs en las Fronteras:** ¿Estás usando Request/Response models en lugar de pasar directamente las entidades a la vista?

---

## 📚 Bibliografía y Créditos
* **Robert C. Martin ("Uncle Bob")**: *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Prentice Hall, 2017.
* **Robert C. Martin**: *Arquitectura Limpia: Guía para el artesano de la estructura y el diseño del software*, Anaya Multimedia, 2018.

---
Hecho con fines educativos y de artesanía de software. ¡Disfruta el aprendizaje! 🚀
