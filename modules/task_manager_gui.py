import tkinter as tk
from tkinter import ttk, messagebox

from .task_manager import TaskManager
from .simple_task import SimpleTask
from .daily_task import DailyTask
from .task_base import TaskStatus, Priority

class TaskManagerGUI:
    def __init__(self, root, manager: TaskManager, engine):
        self.root = root
        root.title("Task Manager")
        self.manager = manager
        self.engine = engine

        # Ensure tasks are saved on window close
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_style()
        self.create_widgets()
        self.refresh_tasks()

    def setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Treeview', rowheight=25, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=5)
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'))
        style.configure('Stats.TLabel', font=('Segoe UI', 12, 'bold'))

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        self.tab_tasks = ttk.Frame(notebook)
        self.tab_add = ttk.Frame(notebook)
        self.tab_stats = ttk.Frame(notebook)
        notebook.add(self.tab_tasks, text='\U0001F4CB Tasks')  # 📋
        notebook.add(self.tab_add, text='\u2795 Add Task')      # ➕
        notebook.add(self.tab_stats, text='\U0001F4CA Stats')   # 📊
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.create_tasks_tab()
        self.create_add_tab()
        self.create_stats_tab()

    def create_tasks_tab(self):
        lbl_daily = ttk.Label(self.tab_tasks, text="🔄 Daily Tasks", style='Header.TLabel')
        lbl_daily.pack(anchor='w', pady=(0,5))
        self.tree_daily = ttk.Treeview(self.tab_tasks, columns=('ID','Title','Status'), show='headings')
        for col in ('ID','Title','Status'):
            self.tree_daily.heading(col, text=col)
        self.tree_daily.pack(fill='x', pady=(0,10))

        lbl_simple = ttk.Label(self.tab_tasks, text="📋 Simple Tasks", style='Header.TLabel')
        lbl_simple.pack(anchor='w', pady=(10,5))
        self.tree_simple = ttk.Treeview(
            self.tab_tasks,
            columns=('ID','Title','Priority','Due','Status'),
            show='headings'
        )
        for col in ('ID','Title','Priority','Due','Status'):
            self.tree_simple.heading(col, text=col)
        self.tree_simple.pack(fill='x', pady=(0,10))

        frm_buttons = ttk.Frame(self.tab_tasks)
        frm_buttons.pack(fill='x', pady=5)
        ttk.Button(frm_buttons, text='Complete Task', command=self.complete_task).pack(side='left', padx=5)
        ttk.Button(frm_buttons, text='Remove Task', command=self.remove_task).pack(side='left', padx=5)
        ttk.Button(frm_buttons, text='Refresh', command=self.refresh_tasks).pack(side='left', padx=5)

    def create_add_tab(self):
        lbl = ttk.Label(self.tab_add, text="Add Simple Task", style='Header.TLabel')
        lbl.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,5))

        ttk.Label(self.tab_add, text="Title:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.entry_title = ttk.Entry(self.tab_add)
        self.entry_title.grid(row=1, column=1, sticky='we', pady=2)

        ttk.Label(self.tab_add, text="Description:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.entry_desc = ttk.Entry(self.tab_add)
        self.entry_desc.grid(row=2, column=1, sticky='we', pady=2)

        ttk.Label(self.tab_add, text="Time Limit (hrs):").grid(row=3, column=0, sticky='e', padx=5, pady=2)
        self.spin_hours = ttk.Spinbox(self.tab_add, from_=0, to=100)
        self.spin_hours.grid(row=3, column=1, sticky='we', pady=2)

        ttk.Label(self.tab_add, text="Priority:").grid(row=4, column=0, sticky='e', padx=5, pady=2)
        self.cmb_priority = ttk.Combobox(
            self.tab_add,
            values=[p.value.capitalize() for p in Priority],
            state='readonly'
        )
        self.cmb_priority.current(1)
        self.cmb_priority.grid(row=4, column=1, sticky='we', pady=2)

        ttk.Button(
            self.tab_add, text="Add Simple Task", command=self.add_simple
        ).grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Separator(self.tab_add, orient='horizontal').grid(
            row=6, column=0, columnspan=2, sticky='we', pady=10
        )

        lbl2 = ttk.Label(self.tab_add, text="Add Daily Task", style='Header.TLabel')
        lbl2.grid(row=7, column=0, columnspan=2, sticky='w', pady=(0,5))
        ttk.Label(self.tab_add, text="Title:").grid(row=8, column=0, sticky='e', padx=5, pady=2)
        self.entry_daily_title = ttk.Entry(self.tab_add)
        self.entry_daily_title.grid(row=8, column=1, sticky='we', pady=2)

        ttk.Label(self.tab_add, text="Description:").grid(row=9, column=0, sticky='e', padx=5, pady=2)
        self.entry_daily_desc = ttk.Entry(self.tab_add)
        self.entry_daily_desc.grid(row=9, column=1, sticky='we', pady=2)

        ttk.Button(
            self.tab_add, text="Add Daily Task", command=self.add_daily
        ).grid(row=10, column=0, columnspan=2, pady=10)

        self.tab_add.columnconfigure(1, weight=1)

    def create_stats_tab(self):
        self.lbl_stats = ttk.Label(self.tab_stats, text="", style='Stats.TLabel')
        self.lbl_stats.pack(anchor='center', pady=20)

    def refresh_tasks(self):
        for tree in (self.tree_daily, self.tree_simple):
            for row in tree.get_children():
                tree.delete(row)

        for tid, task in self.manager.get_tasks_by_type(DailyTask).items():
            status = "Completed" if task.get_status() == TaskStatus.DAILY_COMPLETED else "Pending"
            self.tree_daily.insert('', 'end', values=(tid, task.title, status))

        simple = self.manager.get_tasks_by_type(SimpleTask)
        order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        for tid, task in sorted(simple.items(), key=lambda x: order.get(x[1].priority, 3)):
            due = task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else '-'
            status_map = {
                TaskStatus.COMPLETED: "Completed",
                TaskStatus.EXPIRED: "Expired",
                TaskStatus.PENDING: "Pending"
            }
            self.tree_simple.insert(
                '', 'end',
                values=(
                    tid,
                    task.title,
                    task.priority.value.capitalize(),
                    due,
                    status_map.get(task.get_status(), 'Unknown')
                )
            )

        stats = self.manager.get_stats()
        self.lbl_stats.config(
            text=f"Total: {stats['total']}    Completed: {stats['completed']}    Pending: {stats['pending']}    Expired: {stats['expired']}"
        )

    def add_simple(self):
        title = self.entry_title.get().strip()
        if not title:
            messagebox.showerror("Error", "Title cannot be empty")
            return
        desc = self.entry_desc.get()
        hours = int(self.spin_hours.get() or 0)
        prio = Priority[self.cmb_priority.get().upper()]
        self.manager.add_simple_task(title, desc, hours or None, priority=prio)
        messagebox.showinfo("Success", "Simple task added")
        self.entry_title.delete(0, 'end')
        self.entry_desc.delete(0, 'end')
        self.spin_hours.delete(0, 'end')
        self.spin_hours.insert(0, '0')
        self.cmb_priority.current(1)
        self.refresh_tasks()

    def add_daily(self):
        title = self.entry_daily_title.get().strip()
        if not title:
            messagebox.showerror("Error", "Title cannot be empty")
            return
        desc = self.entry_daily_desc.get()
        self.manager.add_daily_task(title, desc)
        messagebox.showinfo("Success", "Daily task added")
        self.entry_daily_title.delete(0, 'end')
        self.entry_daily_desc.delete(0, 'end')
        self.refresh_tasks()

    def complete_task(self):
        selected = self.tree_simple.focus() or self.tree_daily.focus()
        if not selected:
            messagebox.showerror("Error", "Select a task first")
            return
        # Determine if it's simple or daily
        is_simple = selected in self.tree_simple.get_children()
        values = self.tree_simple.item(selected, 'values') if is_simple else self.tree_daily.item(selected, 'values')
        tid = values[0]
        if self.manager.complete_task(tid):
            # Reward player
            if is_simple:
                prio_str = values[2].lower()
                reward = {'low': 3, 'medium': 5, 'high': 7}.get(prio_str, 0)
            else:
                reward = 5
            self.engine.player.earn_money(reward)
            messagebox.showinfo("Success", f"Task completed. You earned ${reward}")
        else:
            # Penalty for failing to complete in time
            self.engine.player.health -= 10
            messagebox.showerror("Error", "Cannot complete this task. You lost 10 health points.")
        self.refresh_tasks()

    def remove_task(self):
        selected = self.tree_simple.focus() or self.tree_daily.focus()
        if not selected:
            messagebox.showerror("Error", "Select a task first")
            return
        values = self.tree_simple.item(selected, 'values') if selected in self.tree_simple.get_children() else self.tree_daily.item(selected, 'values')
        tid = values[0]
        if self.manager.remove_task(tid):
            # Penalty for removal (missed deadline)
            messagebox.showinfo("Removed", "Task removed.")
        else:
            messagebox.showerror("Error", "Task not found")
        self.refresh_tasks()

    def on_close(self):
        # Save tasks before closing
        try:
            if self.manager.data_file:
                self.manager.save_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
        finally:
            self.root.destroy()