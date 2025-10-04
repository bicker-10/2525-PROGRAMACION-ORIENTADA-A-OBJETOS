import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class UniversityTodoApp:
    def __init__(self, root):
        """
        Inicializa la aplicación de lista de tareas universitarias.
        """
        self.root = root
        self.root.title(" Gestor de Tareas Universitarias")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f8ff')  # Fondo azul pastel

        # Materias universitarias específicas
        self.subjects = [
            "Estadística",
            "POO",
            "Sistemas Operativos",
            "Matemáticas",
            "Física"
        ]

        # Tipos de actividades para cada materia
        self.task_types = [
            "Foro para presentar",
            "Examen para presentar",
            "Tarea para entregar",
            "Proyecto para presentar",
            "Laboratorio para entregar",
            "Práctica para presentar",
            "Investigación para entregar",
            "Taller para participar",
            "Seminario para asistir",
            "Exposición para preparar"
        ]

        # Prioridades
        self.priorities = ["Alta", "Media", "Baja"]

        # Lista para almacenar las tareas
        self.tasks = []
        # Diccionario para mapear items del Treeview a IDs de tareas
        self.item_to_task_id = {}

        # Configurar el estilo con colores pastel
        self.setup_styles()

        # Crear widgets
        self.create_widgets()

        # Configurar eventos
        self.setup_bindings()

        # Cargar algunas tareas de ejemplo
        self.load_sample_tasks()

    def setup_styles(self):
        """Configura los estilos para los widgets con colores pastel."""
        style = ttk.Style()

        # Configurar tema con colores pastel
        style.theme_use('clam')

        # Configurar colores pastel para los botones
        style.configure('PastelGreen.TButton',
                        background='#98FB98',  # Verde pastel
                        foreground='#2E8B57',
                        font=('Arial', 10, 'bold'),
                        padding=(10, 5))

        style.configure('PastelBlue.TButton',
                        background='#ADD8E6',  # Azul pastel
                        foreground='#000080',
                        font=('Arial', 10, 'bold'),
                        padding=(10, 5))

        style.configure('PastelPink.TButton',
                        background='#FFB6C1',  # Rosa pastel
                        foreground='#8B008B',
                        font=('Arial', 10, 'bold'),
                        padding=(10, 5))

        style.configure('PastelOrange.TButton',
                        background='#FFDAB9',  # Naranja pastel
                        foreground='#FF8C00',
                        font=('Arial', 10, 'bold'),
                        padding=(10, 5))

        style.configure('PastelPurple.TButton',
                        background='#D8BFD8',  # Morado pastel
                        foreground='#4B0082',
                        font=('Arial', 10, 'bold'),
                        padding=(10, 5))

        style.configure('PastelYellow.TButton',
                        background='#FFFACD',  # Amarillo pastel
                        foreground='#B8860B',
                        font=('Arial', 10, 'bold'),
                        padding=(10, 5))

        style.configure('PastelCyan.TButton',
                        background='#E0FFFF',  # Cian pastel
                        foreground='#008B8B',
                        font=('Arial', 10, 'bold'),
                        padding=(10, 5))

        # Configurar estilo para el Treeview
        style.configure('Pastel.Treeview',
                        background='#FFFFFF',
                        foreground='#333333',
                        fieldbackground='#FFFFFF',
                        font=('Arial', 9))

        style.configure('Pastel.Treeview.Heading',
                        background='#E6E6FA',
                        foreground='#4B0082',
                        font=('Arial', 10, 'bold'))

    def create_widgets(self):
        """Crea y coloca todos los widgets en la ventana."""
        # Frame principal con fondo pastel
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título con emoji y estilo mejorado
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = tk.Label(title_frame, text=" Gestor de Tareas Universitarias - ¡Organiza tu Semestre!",
                               font=("Arial", 16, "bold"),
                               bg='#E6E6FA',  # Lavanda pastel
                               fg='#4B0082',  # Índigo
                               padx=20, pady=10,
                               relief='raised', bd=2)
        title_label.pack(fill=tk.X)

        # Frame para el formulario de nueva tarea
        form_frame = tk.LabelFrame(main_frame, text=" Agregar Nueva Tarea Universitaria",
                                   font=("Arial", 11, "bold"),
                                   bg='#F0F8FF',  # Azul alice
                                   fg='#2E8B57',  # Verde mar
                                   relief='groove', bd=2)
        form_frame.pack(fill=tk.X, pady=(0, 15), padx=5)

        # Configurar grid para el formulario
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Materia
        tk.Label(form_frame, text=" Materia:", bg='#F0F8FF', font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=8, padx=10)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(form_frame, textvariable=self.subject_var,
                                          values=self.subjects, width=25, font=("Arial", 10))
        self.subject_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(5, 15))

        # Tipo de tarea
        tk.Label(form_frame, text=" Tipo de Actividad:", bg='#F0F8FF', font=("Arial", 10, "bold")).grid(
            row=0, column=2, sticky=tk.W, pady=8, padx=10)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(form_frame, textvariable=self.type_var,
                                       values=self.task_types, width=25, font=("Arial", 10))
        self.type_combo.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=8, padx=(5, 10))

        # Descripción de la tarea
        tk.Label(form_frame, text=" Descripción específica:", bg='#F0F8FF', font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=8, padx=10)
        self.desc_entry = ttk.Entry(form_frame, font=("Arial", 10), width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=8, padx=(5, 10))

        # Fecha de entrega y prioridad
        tk.Label(form_frame, text=" Fecha de entrega (YYYY-MM-DD):", bg='#F0F8FF', font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=8, padx=10)
        self.date_entry = ttk.Entry(form_frame, width=18, font=("Arial", 10))
        self.date_entry.grid(row=2, column=1, sticky=tk.W, pady=8, padx=(5, 15))
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(form_frame, text="⚡ Prioridad:", bg='#F0F8FF', font=("Arial", 10, "bold")).grid(
            row=2, column=2, sticky=tk.W, pady=8, padx=10)
        self.priority_var = tk.StringVar(value="Media")
        priority_frame = tk.Frame(form_frame, bg='#F0F8FF')
        priority_frame.grid(row=2, column=3, sticky=tk.W, pady=8, padx=(5, 10))

        for i, priority in enumerate(self.priorities):
            tk.Radiobutton(priority_frame, text=priority, value=priority,
                           variable=self.priority_var, font=("Arial", 10),
                           bg='#F0F8FF', activebackground='#F0F8FF').grid(
                row=0, column=i, padx=(0, 15))

        # Frame para botones principales
        button_main_frame = ttk.Frame(form_frame)
        button_main_frame.grid(row=3, column=0, columnspan=4, pady=(15, 10))

        # BOTÓN PRINCIPAL: Añadir Tarea (Verde pastel)
        self.add_button = ttk.Button(button_main_frame, text=" Añadir Nueva Tarea",
                                     command=self.add_task, style='PastelGreen.TButton')
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Botón para limpiar formulario
        self.clear_form_button = ttk.Button(button_main_frame, text="🧹 Limpiar Formulario",
                                            command=self.clear_form, style='PastelYellow.TButton')
        self.clear_form_button.pack(side=tk.LEFT, padx=5)

        # Frame para la lista de tareas
        list_frame = tk.LabelFrame(main_frame, text=" Lista de Tareas Universitarias (15 tareas de ejemplo)",
                                   font=("Arial", 11, "bold"),
                                   bg='#F0F8FF',
                                   fg='#2E8B57',
                                   relief='groove', bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10), padx=5)

        # Treeview para mostrar tareas con estilo pastel
        columns = ("subject", "type", "description", "due_date", "priority", "status")
        self.tasks_tree = ttk.Treeview(list_frame, columns=columns, show="headings",
                                       height=15, style='Pastel.Treeview')

        # Configurar columnas
        self.tasks_tree.heading("subject", text=" Materia")
        self.tasks_tree.heading("type", text=" Tipo de Actividad")
        self.tasks_tree.heading("description", text=" Descripción")
        self.tasks_tree.heading("due_date", text=" Fecha Entrega")
        self.tasks_tree.heading("priority", text=" Prioridad")
        self.tasks_tree.heading("status", text=" Estado")

        self.tasks_tree.column("subject", width=120, anchor='center')
        self.tasks_tree.column("type", width=150, anchor='center')
        self.tasks_tree.column("description", width=280, anchor='w')
        self.tasks_tree.column("due_date", width=110, anchor='center')
        self.tasks_tree.column("priority", width=90, anchor='center')
        self.tasks_tree.column("status", width=100, anchor='center')

        # Configurar tags para colores pastel
        self.tasks_tree.tag_configure('completed', background='#F5F5F5', foreground='#808080')
        self.tasks_tree.tag_configure('urgent', background='#FFE4E1', foreground='#DC143C')
        self.tasks_tree.tag_configure('high', background='#FFE4E1')
        self.tasks_tree.tag_configure('medium', background='#FFF8DC')
        self.tasks_tree.tag_configure('low', background='#F0FFF0')

        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar Treeview y scrollbar
        self.tasks_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        # Frame para botones de acción PRINCIPALES
        action_frame = tk.LabelFrame(main_frame, text=" Acciones de Gestión de Tareas",
                                     font=("Arial", 11, "bold"),
                                     bg='#F0F8FF',
                                     fg='#2E8B57',
                                     relief='groove', bd=2)
        action_frame.pack(fill=tk.X, pady=(5, 10), padx=5)

        # PRIMERA FILA DE BOTONES PRINCIPALES
        row1_frame = tk.Frame(action_frame, bg='#F0F8FF')
        row1_frame.pack(fill=tk.X, pady=5)

        # BOTÓN ESPECIAL: "¡Ya cumplí!" - Celebración
        self.celebrate_button = ttk.Button(row1_frame, text=" ¡Ya cumplí! (Marcar como Entregado)",
                                           command=self.mark_completed_with_celebration,
                                           state="disabled",
                                           style='PastelCyan.TButton')
        self.celebrate_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        # BOTÓN: Marcar como Entregado normal
        self.complete_button = ttk.Button(row1_frame, text=" Marcar como Entregado",
                                          command=self.mark_completed,
                                          state="disabled",
                                          style='PastelBlue.TButton')
        self.complete_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        # SEGUNDA FILA DE BOTONES
        row2_frame = tk.Frame(action_frame, bg='#F0F8FF')
        row2_frame.pack(fill=tk.X, pady=5)

        self.delete_button = ttk.Button(row2_frame, text="️ Eliminar Tarea",
                                        command=self.delete_task,
                                        state="disabled",
                                        style='PastelPink.TButton')
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.edit_button = ttk.Button(row2_frame, text=" Editar Tarea",
                                      command=self.edit_task,
                                      state="disabled",
                                      style='PastelOrange.TButton')
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.duplicate_button = ttk.Button(row2_frame, text=" Duplicar Tarea",
                                           command=self.duplicate_task,
                                           state="disabled",
                                           style='PastelPurple.TButton')
        self.duplicate_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        # TERCERA FILA DE BOTONES ADICIONALES
        extra_buttons_frame = tk.LabelFrame(main_frame, text="🔧 Herramientas Adicionales",
                                            font=("Arial", 11, "bold"),
                                            bg='#F0F8FF',
                                            fg='#2E8B57',
                                            relief='groove', bd=2)
        extra_buttons_frame.pack(fill=tk.X, pady=(5, 10), padx=5)

        row3_frame = tk.Frame(extra_buttons_frame, bg='#F0F8FF')
        row3_frame.pack(fill=tk.X, pady=5)

        self.filter_button = ttk.Button(row3_frame, text=" Filtrar por Materia",
                                        command=self.filter_by_subject,
                                        style='PastelPurple.TButton')
        self.filter_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.show_all_button = ttk.Button(row3_frame, text=" Mostrar Todas las Tareas",
                                          command=self.show_all_tasks,
                                          style='PastelGreen.TButton')
        self.show_all_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.sort_date_button = ttk.Button(row3_frame, text=" Ordenar por Fecha",
                                           command=self.sort_by_date,
                                           style='PastelYellow.TButton')
        self.sort_date_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.clear_completed_button = ttk.Button(row3_frame, text=" Limpiar Entregadas",
                                                 command=self.clear_completed_tasks,
                                                 style='PastelPink.TButton')
        self.clear_completed_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        # Estadísticas
        stats_frame = tk.Frame(main_frame, bg='#E6E6FA', relief='raised', bd=2)
        stats_frame.pack(fill=tk.X, pady=(10, 0), padx=5)

        self.stats_label = tk.Label(stats_frame, text="", font=("Arial", 10, "bold"),
                                    bg='#E6E6FA', fg='#4B0082', pady=8)
        self.stats_label.pack()

        self.update_stats()

    def clear_form(self):
        """Limpia el formulario de entrada."""
        self.subject_var.set('')
        self.type_var.set('')
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.priority_var.set("Media")
        self.desc_entry.focus()
        messagebox.showinfo("Formulario limpiado", " El formulario ha sido limpiado")

    def setup_bindings(self):
        """Configura los eventos del teclado."""
        self.desc_entry.bind("<Return>", lambda event: self.add_task())
        self.tasks_tree.bind("<Double-1>", lambda event: self.mark_completed())
        self.tasks_tree.bind("<Delete>", lambda event: self.delete_task())
        self.tasks_tree.bind("<<TreeviewSelect>>", self.on_task_select)

    def load_sample_tasks(self):
        """Carga 15 tareas de ejemplo para demostración."""
        sample_tasks = [
            # Estadística (3 tareas)
            {
                "subject": "Estadística",
                "type": "Examen para presentar",
                "description": "Examen parcial de probabilidad y estadística descriptiva",
                "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": False
            },
            {
                "subject": "Estadística",
                "type": "Foro para presentar",
                "description": "Participar en foro sobre distribuciones normales",
                "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "priority": "Media",
                "completed": False
            },
            {
                "subject": "Estadística",
                "type": "Tarea para entregar",
                "description": "Resolver problemas de intervalo de confianza",
                "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": False
            },

            # POO (3 tareas)
            {
                "subject": "POO",
                "type": "Proyecto para presentar",
                "description": "Sistema de gestión de biblioteca con Java y MySQL",
                "due_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": False
            },
            {
                "subject": "POO",
                "type": "Laboratorio para entregar",
                "description": "Práctica de herencia, polimorfismo y encapsulamiento",
                "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": False
            },
            {
                "subject": "POO",
                "type": "Exposición para preparar",
                "description": "Preparar exposición sobre patrones de diseño",
                "due_date": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "priority": "Media",
                "completed": False
            },

            # Sistemas Operativos (3 tareas)
            {
                "subject": "Sistemas Operativos",
                "type": "Foro para presentar",
                "description": "Debate sobre algoritmos de planificación de procesos",
                "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "priority": "Media",
                "completed": False
            },
            {
                "subject": "Sistemas Operativos",
                "type": "Tarea para entregar",
                "description": "Ejercicios de gestión de memoria y paginación",
                "due_date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": False
            },
            {
                "subject": "Sistemas Operativos",
                "type": "Taller para participar",
                "description": "Taller práctico de comandos Linux avanzados",
                "due_date": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
                "priority": "Media",
                "completed": False
            },

            # Matemáticas (3 tareas)
            {
                "subject": "Matemáticas",
                "type": "Examen para presentar",
                "description": "Examen de cálculo diferencial e integral",
                "due_date": (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": False
            },
            {
                "subject": "Matemáticas",
                "type": "Práctica para presentar",
                "description": "Problemas de álgebra lineal y matrices",
                "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "priority": "Media",
                "completed": False
            },
            {
                "subject": "Matemáticas",
                "type": "Investigación para entregar",
                "description": "Investigación sobre aplicaciones de ecuaciones diferenciales",
                "due_date": (datetime.now() + timedelta(days=12)).strftime("%Y-%m-%d"),
                "priority": "Baja",
                "completed": False
            },

            # Física (3 tareas)
            {
                "subject": "Física",
                "type": "Laboratorio para entregar",
                "description": "Informe de práctica de movimiento armónico simple",
                "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": False
            },
            {
                "subject": "Física",
                "type": "Seminario para asistir",
                "description": "Seminario sobre aplicaciones de la termodinámica",
                "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "priority": "Media",
                "completed": False
            },
            {
                "subject": "Física",
                "type": "Proyecto para presentar",
                "description": "Proyecto de investigación sobre ondas electromagnéticas",
                "due_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
                "priority": "Alta",
                "completed": True  # Una tarea ya completada de ejemplo
            }
        ]

        for task in sample_tasks:
            self.add_task_from_data(task)

    def add_task_from_data(self, task_data):
        """Añade una tarea desde un diccionario de datos."""
        task_id = len(self.tasks)
        task_data["id"] = task_id
        self.tasks.append(task_data)

        # Añadir al Treeview
        self.add_task_to_treeview(task_data)
        self.update_stats()

    def add_task(self):
        """Añade una nueva tarea desde el formulario."""
        subject = self.subject_var.get().strip()
        task_type = self.type_var.get().strip()
        description = self.desc_entry.get().strip()
        due_date = self.date_entry.get().strip()
        priority = self.priority_var.get()

        # Validaciones
        if not all([subject, task_type, description, due_date]):
            messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Por favor, usa el formato YYYY-MM-DD para la fecha.")
            return

        # Crear nueva tarea
        new_task = {
            "subject": subject,
            "type": task_type,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "completed": False
        }

        self.add_task_from_data(new_task)

        # Limpiar formulario
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.focus()

        messagebox.showinfo("Éxito", " Tarea añadida correctamente!")

    def on_task_select(self, event):
        """Maneja la selección de tareas."""
        selection = self.tasks_tree.selection()
        if selection:
            self.complete_button.config(state="normal")
            self.delete_button.config(state="normal")
            self.edit_button.config(state="normal")
            self.duplicate_button.config(state="normal")
            self.celebrate_button.config(state="normal")
        else:
            self.complete_button.config(state="disabled")
            self.delete_button.config(state="disabled")
            self.edit_button.config(state="disabled")
            self.duplicate_button.config(state="disabled")
            self.celebrate_button.config(state="disabled")

    def get_task_id_from_item(self, item_id):
        """Obtiene el ID de la tarea a partir del item del Treeview."""
        return self.item_to_task_id.get(item_id, None)

    def mark_completed_with_celebration(self):
        """Marca la tarea como completada con un mensaje de celebración."""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para celebrar!")
            return

        item_id = selection[0]
        task_id = self.get_task_id_from_item(item_id)

        if task_id is not None and 0 <= task_id < len(self.tasks):
            task = self.tasks[task_id]

            if not task["completed"]:
                task["completed"] = True



                import random
                message = random.choice(celebration_messages)
                messagebox.showinfo("¡Celebración!", f"{message}\n\nTarea: {task['description']}")

                # Actualizar la visualización
                self.refresh_task_display()
                self.update_stats()
            else:
                messagebox.showinfo("Ya estaba completa", "Esta tarea ya estaba marcada como entregada")

    def mark_completed(self):
        """Marca la tarea seleccionada como completada o pendiente."""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para cambiar su estado.")
            return

        item_id = selection[0]
        task_id = self.get_task_id_from_item(item_id)

        if task_id is not None and 0 <= task_id < len(self.tasks):
            task = self.tasks[task_id]
            task["completed"] = not task["completed"]

            # Mostrar mensaje de confirmación
            estado = "entregada" if task["completed"] else "pendiente"
            messagebox.showinfo("Estado actualizado", f"Tarea marcada como {estado}")

            # Actualizar la visualización
            self.refresh_task_display()
            self.update_stats()

    def delete_task(self):
        """Elimina la tarea seleccionada."""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para eliminar.")
            return

        item_id = selection[0]
        task_id = self.get_task_id_from_item(item_id)

        if task_id is not None:
            # Obtener información de la tarea para el mensaje de confirmación
            task_description = self.tasks[task_id]["description"]

            confirm = messagebox.askyesno("Confirmar eliminación",
                                          f"¿Estás seguro de eliminar la tarea:\n\"{task_description}\"?")
            if confirm:
                # Eliminar la tarea de la lista
                if 0 <= task_id < len(self.tasks):
                    self.tasks.pop(task_id)

                # Reindexar las tareas restantes
                for i, task in enumerate(self.tasks):
                    task["id"] = i

                # Actualizar la visualización
                self.refresh_task_display()
                self.update_stats()
                messagebox.showinfo("Eliminada", " Tarea eliminada correctamente")

    def edit_task(self):
        """Permite editar la tarea seleccionada."""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para editar.")
            return

        item_id = selection[0]
        task_id = self.get_task_id_from_item(item_id)

        if task_id is not None and 0 <= task_id < len(self.tasks):
            task = self.tasks[task_id]
            # Crear ventana de edición
            self.create_edit_window(task, task_id)

    def create_edit_window(self, task, task_id):
        """Crea una ventana para editar una tarea."""
        edit_window = tk.Toplevel(self.root)
        edit_window.title(" Editar Tarea Universitaria")
        edit_window.geometry("400x350")
        edit_window.configure(bg='#f0f8ff')
        edit_window.transient(self.root)
        edit_window.grab_set()

        # Frame principal
        edit_frame = tk.Frame(edit_window, bg='#f0f8ff', padx=20, pady=20)
        edit_frame.pack(fill=tk.BOTH, expand=True)

        # Campos de edición
        tk.Label(edit_frame, text=" Materia:", bg='#f0f8ff', font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        subject_var = tk.StringVar(value=task["subject"])
        subject_combo = ttk.Combobox(edit_frame, textvariable=subject_var, values=self.subjects, width=25)
        subject_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        tk.Label(edit_frame, text=" Tipo de Actividad:", bg='#f0f8ff', font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar(value=task["type"])
        type_combo = ttk.Combobox(edit_frame, textvariable=type_var, values=self.task_types, width=25)
        type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        tk.Label(edit_frame, text=" Descripción:", bg='#f0f8ff', font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        desc_var = tk.StringVar(value=task["description"])
        desc_entry = ttk.Entry(edit_frame, textvariable=desc_var, width=30)
        desc_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        tk.Label(edit_frame, text=" Fecha (YYYY-MM-DD):", bg='#f0f8ff', font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        date_var = tk.StringVar(value=task["due_date"])
        date_entry = ttk.Entry(edit_frame, textvariable=date_var)
        date_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        tk.Label(edit_frame, text="⚡ Prioridad:", bg='#f0f8ff', font=("Arial", 10, "bold")).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        priority_var = tk.StringVar(value=task["priority"])
        priority_frame = tk.Frame(edit_frame, bg='#f0f8ff')
        priority_frame.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        for i, priority in enumerate(self.priorities):
            tk.Radiobutton(priority_frame, text=priority, value=priority,
                           variable=priority_var, font=("Arial", 10),
                           bg='#f0f8ff', activebackground='#f0f8ff').grid(
                row=0, column=i, padx=(0, 10))

        # Botones
        button_frame = tk.Frame(edit_frame, bg='#f0f8ff')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        def save_changes():
            # Validar fecha
            try:
                datetime.strptime(date_var.get(), "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Fecha inválida", "Por favor, usa el formato YYYY-MM-DD para la fecha.")
                return

            # Actualizar la tarea
            task.update({
                "subject": subject_var.get(),
                "type": type_var.get(),
                "description": desc_var.get(),
                "due_date": date_var.get(),
                "priority": priority_var.get()
            })

            # Actualizar la visualización
            self.refresh_task_display()
            edit_window.destroy()
            messagebox.showinfo("Éxito", " Tarea actualizada correctamente!")

        ttk.Button(button_frame, text=" Guardar Cambios", command=save_changes,
                   style='PastelGreen.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Cancelar", command=edit_window.destroy,
                   style='PastelPink.TButton').pack(side=tk.LEFT, padx=5)

    def duplicate_task(self):
        """Duplica la tarea seleccionada."""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para duplicar.")
            return

        item_id = selection[0]
        task_id = self.get_task_id_from_item(item_id)

        if task_id is not None and 0 <= task_id < len(self.tasks):
            original_task = self.tasks[task_id].copy()

            # Crear nueva tarea duplicada
            new_task = {
                "subject": original_task["subject"],
                "type": original_task["type"],
                "description": f"Copia de: {original_task['description']}",
                "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "priority": original_task["priority"],
                "completed": False
            }

            self.add_task_from_data(new_task)
            messagebox.showinfo("Duplicada", " Tarea duplicada correctamente")

    def filter_by_subject(self):
        """Filtra las tareas por materia."""
        # Crear ventana de selección de materia
        filter_window = tk.Toplevel(self.root)
        filter_window.title(" Filtrar por Materia")
        filter_window.geometry("300x200")
        filter_window.configure(bg='#f0f8ff')
        filter_window.transient(self.root)

        tk.Label(filter_window, text="Selecciona una materia:", bg='#f0f8ff',
                 font=("Arial", 11, "bold")).pack(pady=15)

        subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(filter_window, textvariable=subject_var, values=self.subjects,
                                     font=("Arial", 10))
        subject_combo.pack(pady=10)

        def apply_filter():
            subject = subject_var.get()
            if subject:
                # Limpiar Treeview
                for item in self.tasks_tree.get_children():
                    self.tasks_tree.delete(item)

                # Limpiar mapeo
                self.item_to_task_id.clear()

                # Añadir solo tareas de la materia seleccionada
                for task in self.tasks:
                    if task["subject"] == subject:
                        self.add_task_to_treeview(task)

                filter_window.destroy()
                messagebox.showinfo("Filtro aplicado", f"Mostrando tareas de: {subject}")

        button_frame = tk.Frame(filter_window, bg='#f0f8ff')
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text=" Aplicar Filtro", command=apply_filter,
                   style='PastelBlue.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Cancelar", command=filter_window.destroy,
                   style='PastelPink.TButton').pack(side=tk.LEFT, padx=5)

    def show_all_tasks(self):
        """Muestra todas las tareas."""
        self.refresh_task_display()
        messagebox.showinfo("Mostrar todas", " Mostrando todas las tareas")

    def sort_by_date(self):
        """Ordena las tareas por fecha de entrega."""
        self.tasks.sort(key=lambda x: x["due_date"])

        # Reindexar
        for i, task in enumerate(self.tasks):
            task["id"] = i

        self.refresh_task_display()
        messagebox.showinfo("Ordenado", " Tareas ordenadas por fecha de entrega")

    def clear_completed_tasks(self):
        """Elimina todas las tareas marcadas como completadas."""
        completed_tasks = [t for t in self.tasks if t["completed"]]

        if not completed_tasks:
            messagebox.showinfo("Sin tareas completadas", "No hay tareas entregadas para limpiar.")
            return

        confirm = messagebox.askyesno("Confirmar limpieza",
                                      f"¿Estás seguro de eliminar {len(completed_tasks)} tarea(s) entregada(s)?")
        if confirm:
            # Mantener solo las tareas no completadas
            self.tasks = [t for t in self.tasks if not t["completed"]]

            # Reindexar
            for i, task in enumerate(self.tasks):
                task["id"] = i

            self.refresh_task_display()
            self.update_stats()
            messagebox.showinfo("Limpieza completada", f"🧹 Se eliminaron {len(completed_tasks)} tarea(s) entregada(s)")

    def refresh_task_display(self):
        """Actualiza toda la visualización del Treeview."""
        # Limpiar Treeview
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)

        # Limpiar mapeo
        self.item_to_task_id.clear()

        # Añadir todas las tareas
        for task in self.tasks:
            self.add_task_to_treeview(task)

    def add_task_to_treeview(self, task):
        """Añade una tarea individual al Treeview."""
        status = "Entregado" if task["completed"] else "Pendiente"

        # Determinar etiquetas para prioridad y estado
        priority_text = task["priority"]
        if task["completed"]:
            status_text = " " + status
        else:
            status_text = " " + status

            # Marcar como urgente si la fecha está próxima
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
            days_until_due = (due_date - datetime.now()).days
            if days_until_due <= 1:
                priority_text = " " + priority_text
            elif days_until_due <= 3:
                priority_text = " " + priority_text

        item_id = self.tasks_tree.insert("", tk.END, values=(
            task["subject"],
            task["type"],
            task["description"],
            task["due_date"],
            priority_text,
            status_text
        ))

        # Aplicar color según el estado y prioridad
        if task["completed"]:
            self.tasks_tree.item(item_id, tags=("completed",))
        else:
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
            days_until_due = (due_date - datetime.now()).days
            if days_until_due <= 1:
                self.tasks_tree.item(item_id, tags=("urgent",))
            elif task["priority"] == "Alta":
                self.tasks_tree.item(item_id, tags=("high",))
            elif task["priority"] == "Media":
                self.tasks_tree.item(item_id, tags=("medium",))
            else:
                self.tasks_tree.item(item_id, tags=("low",))

        # Almacenar el mapeo entre item del Treeview y ID de tarea
        self.item_to_task_id[item_id] = task["id"]

    def update_stats(self):
        """Actualiza las estadísticas mostradas."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed

        # Contar tareas urgentes (vencen en 1 día o menos)
        urgent = 0
        for task in self.tasks:
            if not task["completed"]:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                days_until_due = (due_date - datetime.now()).days
                if days_until_due <= 1:
                    urgent += 1

        stats_text = (f"Estadísticas: Total: {total} |  Entregados: {completed} | "
                      f" Pendientes: {pending} |  Urgentes: {urgent}")

        self.stats_label.config(text=stats_text)


def main():
    """Función principal."""
    root = tk.Tk()
    app = UniversityTodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()