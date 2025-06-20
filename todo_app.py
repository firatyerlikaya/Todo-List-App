import tkinter as tk
from tkinter import messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from datetime import date, datetime
from ttkbootstrap.scrolled import ScrolledText
import json
import os

TASKS_FILE = "tasks.json"

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yapılacaklar Listesi")
        self.root.geometry("1100x650")

        self.priorities = ["Yüksek", "Normal", "Düşük"]
        self.sort_options = [
            "Eklenme Sırası", "Son Tarihe Göre (Yakın)", "Son Tarihe Göre (Uzak)",
            "Önceliğe Göre (Yüksekten Düşüğe)", "İsme Göre (A-Z)"
        ]
        
        self.tasks = {}
        self.current_list_name = None
        self.iid_map = {}

        main_frame = ttk.Frame(self.root, padding=(10, 10))
        main_frame.pack(fill=BOTH, expand=True)

        header_label = ttk.Label(main_frame, text="Yapılacaklar Listesi", font=("Helvetica", 18, "bold"), bootstyle=PRIMARY)
        header_label.pack(pady=(0, 10))

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=X, pady=(0, 10))
        control_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(control_frame, text="Aktif Liste:").grid(row=0, column=0, padx=(0, 5), sticky='w')
        self.list_combobox = ttk.Combobox(control_frame, state="readonly", width=20)
        self.list_combobox.grid(row=0, column=1, sticky='ew')
        self.list_combobox.bind("<<ComboboxSelected>>", self.on_list_selected)

        ttk.Label(control_frame, text="Sırala:").grid(row=1, column=0, padx=(0, 5), pady=(5,0), sticky='w')
        self.sort_combobox = ttk.Combobox(control_frame, state="readonly", values=self.sort_options, width=25)
        self.sort_combobox.grid(row=1, column=1, pady=(5,0), sticky='ew')
        self.sort_combobox.set("Eklenme Sırası")
        self.sort_combobox.bind("<<ComboboxSelected>>", self.populate_treeview)
        
        # --- GÜNCELLEME: Butonların grid pozisyonları yeniden düzenlendi ---
        add_list_btn = ttk.Button(control_frame, text="Yeni Liste", command=self.add_new_list, bootstyle=(INFO, OUTLINE))
        add_list_btn.grid(row=0, column=2, padx=(10, 5), sticky='nsew')
        
        delete_list_btn = ttk.Button(control_frame, text="Listeyi Sil", command=self.delete_current_list, bootstyle=(DANGER, OUTLINE))
        delete_list_btn.grid(row=0, column=3, sticky='nsew')
        
        self.light_theme_btn = ttk.Button(control_frame, text="☀️", command=lambda: self.change_theme('litera'), bootstyle=PRIMARY, width=3)
        self.light_theme_btn.grid(row=1, column=2, padx=(10, 5), pady=(5,0), sticky="nsew")

        self.dark_theme_btn = ttk.Button(control_frame, text="🌙", command=lambda: self.change_theme('darkly'), bootstyle=OUTLINE, width=3)
        self.dark_theme_btn.grid(row=1, column=3, pady=(5,0), sticky="nsew")


        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=BOTH, expand=True, pady=5)
        
        columns = ('due_date', 'priority')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
        self.tree.heading('#0', text='Görev Adı'); self.tree.heading('due_date', text='Son Tarih'); self.tree.heading('priority', text='Öncelik')
        self.tree.column('#0', width=400); self.tree.column('due_date', width=120, anchor=CENTER); self.tree.column('priority', width=100, anchor=CENTER)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.edit_task)
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=X, pady=10)
        self.task_entry = ttk.Entry(entry_frame, font=("Helvetica", 12))
        self.task_entry.pack(side=LEFT, fill=X, expand=True)
        self.task_entry.bind("<Return>", lambda e: self.add_task(is_subtask=False))
        
        options_frame = ttk.Frame(entry_frame)
        options_frame.pack(side=RIGHT, padx=(10, 0))
        priority_label = ttk.Label(options_frame, text="Öncelik:")
        priority_label.pack(side=LEFT, padx=(0, 5))
        self.priority_var = tk.StringVar(self.root)
        self.priority_var.set("Normal")
        priority_menu = ttk.OptionMenu(options_frame, self.priority_var, "Normal", *self.priorities)
        priority_menu.pack(side=LEFT, padx=(0, 10))
        date_label = ttk.Label(options_frame, text="Son Tarih:")
        date_label.pack(side=LEFT, padx=(0, 5))
        self.date_entry = ttk.DateEntry(options_frame, dateformat="%Y-%m-%d", firstweekday=1)
        self.date_entry.pack(side=LEFT)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(5, 0))
        add_btn = ttk.Button(button_frame, text="Görev Ekle", command=lambda: self.add_task(is_subtask=False), bootstyle=SUCCESS)
        add_btn.pack(side=LEFT, expand=True, fill=X, padx=2)
        self.add_subtask_btn = ttk.Button(button_frame, text="Alt Görev Ekle", command=lambda: self.add_task(is_subtask=True), state=DISABLED)
        self.add_subtask_btn.pack(side=LEFT, expand=True, fill=X, padx=2)
        delete_btn = ttk.Button(button_frame, text="Görevi Sil", command=self.delete_task, bootstyle=DANGER)
        delete_btn.pack(side=LEFT, expand=True, fill=X, padx=2)
        complete_btn = ttk.Button(button_frame, text="Tamamlandı", command=self.mark_as_complete, bootstyle=INFO)
        complete_btn.pack(side=LEFT, expand=True, fill=X, padx=2)
        incomplete_btn = ttk.Button(button_frame, text="Tamamlanmadı", command=self.mark_as_incomplete, bootstyle=SECONDARY)
        incomplete_btn.pack(side=LEFT, expand=True, fill=X, padx=2)
        clear_btn = ttk.Button(button_frame, text="Tamamlananları Temizle", command=self.clear_completed_tasks, bootstyle=WARNING)
        clear_btn.pack(side=LEFT, expand=True, fill=X, padx=2)
        delete_all_btn = ttk.Button(button_frame, text="Tümünü Sil", command=self.delete_all_tasks, bootstyle=(DANGER, OUTLINE))
        delete_all_btn.pack(side=LEFT, expand=True, fill=X, padx=2)
        
        self.load_tasks()
        self.change_theme('litera')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_theme(self, theme_name):
        self.root.style.theme_use(theme_name)
        if theme_name == 'litera':
            self.light_theme_btn.config(bootstyle=PRIMARY)
            self.dark_theme_btn.config(bootstyle=OUTLINE)
        else:
            self.light_theme_btn.config(bootstyle=OUTLINE)
            self.dark_theme_btn.config(bootstyle=PRIMARY)
        self.populate_treeview()
        
    def load_tasks(self):
        def complete_task_data(task_list):
            for task in task_list:
                task.setdefault("priority", "Normal"); task.setdefault("due_date", None)
                task.setdefault("notes", ""); task.setdefault("completed", False)
                task.setdefault("subtasks", [])
                if task["subtasks"]: complete_task_data(task["subtasks"])
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list): self.tasks = {"Genel": data}
                    else: self.tasks = data
                except json.JSONDecodeError: self.tasks = {}
        if not self.tasks: self.tasks = {"Genel": []}
        for task_list in self.tasks.values(): complete_task_data(task_list)
        self.update_list_combobox()

    def save_tasks(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def update_list_combobox(self):
        list_names = list(self.tasks.keys())
        self.list_combobox["values"] = list_names
        if list_names:
            if self.current_list_name not in list_names: self.current_list_name = list_names[0]
            self.list_combobox.set(self.current_list_name)
            self.on_list_selected()
        else:
            self.list_combobox.set(""); self.current_list_name = None; self.populate_treeview()
    
    def on_list_selected(self, event=None):
        self.current_list_name = self.list_combobox.get()
        self.sort_combobox.set("Eklenme Sırası")
        self.populate_treeview()
    
    def populate_treeview(self, event=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        self.iid_map.clear()
        if not self.current_list_name or self.current_list_name not in self.tasks: return
        task_list = self.tasks[self.current_list_name]
        def sort_recursively(tasks):
            sort_by = self.sort_combobox.get()
            if sort_by == "Eklenme Sırası": pass
            else:
                priority_map = {"Yüksek": 0, "Normal": 1, "Düşük": 2}
                reverse_order = (sort_by == "Son Tarihe Göre (Uzak)")
                def get_sort_key(task):
                    if sort_by == "İsme Göre (A-Z)": return task['text'].lower()
                    if sort_by.startswith("Önceliğe"): return priority_map.get(task['priority'], 99)
                    if sort_by.startswith("Son Tarihe"):
                        has_date = task['due_date'] is not None
                        if not has_date: return (1, None)
                        return (0, datetime.strptime(task['due_date'], "%Y-%m-%d"))
                    return None
                tasks.sort(key=get_sort_key, reverse=reverse_order)
            for task in tasks:
                if task.get("subtasks"): sort_recursively(task["subtasks"])
            return tasks
        sorted_task_list = sort_recursively(list(task_list))
        def _insert_items(parent_node, tasks):
            for i, task in enumerate(tasks):
                task_id = f"{parent_node}-{id(task)}"; self.iid_map[task_id] = task
                note_icon = "📝" if task.get("notes") else ""
                task_display_text = f"{note_icon} {task['text']}"
                tags = ['completed'] if task.get('completed') else []
                item = self.tree.insert(parent_node, END, iid=task_id, text=task_display_text, values=(task.get('due_date', ''), task.get('priority', '')), tags=tags, open=True)
                if task.get("subtasks"): _insert_items(item, task["subtasks"])
        _insert_items('', sorted_task_list)
        style = ttk.Style.get_instance()
        colors = style.colors
        self.tree.tag_configure('completed', foreground=colors.secondary)

    def on_tree_select(self, event):
        self.add_subtask_btn.config(state=NORMAL if self.tree.selection() else DISABLED)

    def add_task(self, is_subtask=False):
        if not self.current_list_name:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görev listesi seçin veya oluşturun."); return
        task_text = self.task_entry.get()
        if not task_text:
            messagebox.showwarning("Uyarı", "Lütfen bir görev girin."); return
        new_task = {"text": task_text.strip(), "completed": False, "priority": self.priority_var.get(), "due_date": self.date_entry.entry.get() or None, "notes": "", "subtasks": []}
        if is_subtask:
            selected_iid = self.tree.focus()
            if not selected_iid:
                messagebox.showwarning("Uyarı", "Lütfen bir üst görev seçin."); return
            self.iid_map.get(selected_iid)["subtasks"].append(new_task)
        else:
            self.tasks[self.current_list_name].append(new_task)
        self.populate_treeview(); self.task_entry.delete(0, tk.END); self.date_entry.entry.delete(0, tk.END)
    
    def find_task_and_parent_list(self, task_to_find):
        if not task_to_find: return None, None
        def _search(current_list):
            for task in current_list:
                if task is task_to_find: return current_list
                found_in_sub = _search(task.get("subtasks", []))
                if found_in_sub: return found_in_sub
            return None
        return task_to_find, _search(self.tasks.get(self.current_list_name, []))

    def delete_task(self):
        selected_iids = self.tree.selection()
        if not selected_iids: return
        is_sure = messagebox.askyesno("Onay", f"{len(selected_iids)} adet görevi (ve tüm alt görevlerini) silmek istediğinizden emin misiniz?")
        if is_sure:
            for iid in selected_iids:
                task_to_delete = self.iid_map.get(iid)
                task, parent_list = self.find_task_and_parent_list(task_to_delete)
                if task and parent_list is not None: parent_list.remove(task)
            self.populate_treeview()

    def mark_as_complete(self):
        selected_iids = self.tree.selection()
        if not selected_iids: return
        for iid in selected_iids:
            task = self.iid_map.get(iid)
            if task: task['completed'] = True
        self.populate_treeview()
    
    def mark_as_incomplete(self):
        selected_iids = self.tree.selection()
        if not selected_iids: return
        for iid in selected_iids:
            task = self.iid_map.get(iid)
            if task: task['completed'] = False
        self.populate_treeview()

    def clear_completed_tasks(self):
        if not self.current_list_name: return
        is_sure = messagebox.askyesno("Onay", f"'{self.current_list_name}' listesindeki tüm biten görevleri temizlemek istediğinizden emin misiniz?")
        if not is_sure: return
        def _clear_recursive(task_list):
            new_list = [task for task in task_list if not task['completed']]
            for task in new_list:
                task['subtasks'] = _clear_recursive(task.get('subtasks', []))
            return new_list
        self.tasks[self.current_list_name] = _clear_recursive(self.tasks[self.current_list_name])
        self.populate_treeview()
        
    def delete_all_tasks(self):
        if not self.current_list_name or not self.tasks[self.current_list_name]: return
        is_sure = messagebox.askyesno("DİKKAT", f"'{self.current_list_name}' listesindeki TÜM görevleri kalıcı olarak silmek istediğinizden emin misiniz?", icon='warning')
        if is_sure:
            self.tasks[self.current_list_name].clear(); self.populate_treeview()

    def edit_task(self, event):
        selected_iid = self.tree.focus()
        if not selected_iid: return
        task_info = self.iid_map.get(selected_iid)
        if not task_info: return
        
        self.edit_win = ttk.Toplevel(title="Görevi Düzenle")
        self.edit_win.geometry("500x500")
        edit_frame = ttk.Frame(self.edit_win, padding=20)
        edit_frame.pack(fill=BOTH, expand=True)
        ttk.Label(edit_frame, text="Görev Metni:").pack(anchor=W)
        edit_entry = ttk.Entry(edit_frame, font=("Helvetica", 12))
        edit_entry.insert(0, task_info["text"])
        edit_entry.pack(fill=X, pady=(0, 10)); edit_entry.focus_set()
        ttk.Label(edit_frame, text="Son Tarih:").pack(anchor=W)
        edit_date_entry = ttk.DateEntry(edit_frame, dateformat="%Y-%m-%d", firstweekday=1)
        if task_info.get("due_date"):
            edit_date_entry.entry.delete(0, END); edit_date_entry.entry.insert(0, task_info["due_date"])
        edit_date_entry.pack(fill=X, pady=(0, 10))
        ttk.Label(edit_frame, text="Notlar:").pack(anchor=W)
        notes_text = ScrolledText(edit_frame, height=10, wrap=WORD)
        notes_text.pack(fill=BOTH, expand=True, pady=(0, 15))
        notes_text.insert(END, task_info.get("notes", ""))
        def save_changes(): self.update_task(task_info, edit_entry.get(), edit_date_entry.entry.get(), notes_text.get("1.0", END))
        ttk.Button(edit_frame, text="Kaydet", command=save_changes, bootstyle=SUCCESS).pack(fill=X)
        self.edit_win.transient(self.root); self.edit_win.grab_set(); self.root.wait_window(self.edit_win)

    def update_task(self, task_to_update, new_text, new_date, new_notes):
        new_text = new_text.strip()
        if new_date:
            try: datetime.strptime(new_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz tarih formatı...", parent=self.edit_win); return
        if new_text:
            task_to_update["text"] = new_text
            task_to_update["due_date"] = new_date if new_date else None
            task_to_update["notes"] = new_notes.strip()
            self.populate_treeview(); self.edit_win.destroy()
        else:
            messagebox.showwarning("Uyarı", "Görev metni boş olamaz.", parent=self.edit_win)
    
    def on_closing(self):
        self.save_tasks(); self.root.destroy()

    def add_new_list(self):
        dialog = ttk.Toplevel(title="Yeni Liste Oluştur")
        dialog_frame = ttk.Frame(dialog, padding=10)
        dialog_frame.pack(fill=BOTH, expand=True)
        ttk.Label(dialog_frame, text="Yeni Listenin Adı:").pack(pady=(0,5))
        new_list_entry = ttk.Entry(dialog_frame, width=30)
        new_list_entry.pack(pady=5, padx=10); new_list_entry.focus_set()
        def save_new_list(event=None):
            new_name = new_list_entry.get().strip()
            if not new_name:
                messagebox.showerror("Hata", "Liste adı boş olamaz.", parent=dialog); return
            if new_name in self.tasks:
                messagebox.showerror("Hata", "Bu isimde bir liste zaten mevcut.", parent=dialog); return
            self.tasks[new_name] = []; self.current_list_name = new_name
            self.update_list_combobox(); dialog.destroy()
        new_list_entry.bind("<Return>", save_new_list)
        ttk.Button(dialog_frame, text="Oluştur", command=save_new_list, bootstyle=SUCCESS).pack(pady=10)
        dialog.transient(self.root); dialog.grab_set(); dialog.resizable(False, False); self.root.wait_window(dialog)

    def delete_current_list(self):
        if not self.current_list_name:
            messagebox.showerror("Hata", "Silinecek bir liste seçili değil."); return
        if len(self.tasks) <= 1:
            messagebox.showwarning("Uyarı", "Son listeyi silemezsiniz."); return
        is_sure = messagebox.askyesno("LİSTEYİ SİL", f"'{self.current_list_name}' listesini ve içindeki tüm görevleri kalıcı olarak silmek istediğinizden emin misiniz?", icon='warning')
        if is_sure:
            del self.tasks[self.current_list_name]; self.current_list_name = None; self.update_list_combobox()

if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = TodoListApp(root)
    root.mainloop()