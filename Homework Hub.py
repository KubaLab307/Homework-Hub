import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# ============================================================
# HOMEWORK HUB V2
# ============================================================

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "homework_data.json"
)

homework = []

STATUS_COLORS = {
    "Not started": "#ff5c5c",
    "In progress": "#ffd84d",
    "Complete": "#55d66b"
}


# ============================================================
# DATA
# ============================================================

def load_homework():
    global homework

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                homework = json.load(file)
        except Exception:
            homework = []


def save_homework():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(homework, file, indent=4)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Homework Hub")
root.geometry("1000x700")
root.minsize(800, 600)

root.configure(bg="#f2f2f2")


# ============================================================
# TOP BAR
# ============================================================

top_bar = tk.Frame(
    root,
    bg="#ffffff",
    height=75
)

top_bar.pack(
    fill="x"
)

top_bar.pack_propagate(False)


title = tk.Label(
    top_bar,
    text="Homework Hub",
    font=("Helvetica", 25, "bold"),
    bg="#ffffff",
    fg="black"
)

title.pack(
    side="left",
    padx=25
)


add_button = tk.Button(
    top_bar,
    text="+  Add Homework",
    font=("Helvetica", 11, "bold"),
    bg="#e8e8e8",
    fg="black",
    activebackground="#d5d5d5",
    activeforeground="black",
    relief="flat",
    padx=18,
    pady=9,
    cursor="hand2"
)

add_button.pack(
    side="right",
    padx=20
)


# ============================================================
# SCROLLABLE MAIN AREA
# ============================================================

outer = tk.Frame(
    root,
    bg="#f2f2f2"
)

outer.pack(
    fill="both",
    expand=True
)

canvas = tk.Canvas(
    outer,
    bg="#f2f2f2",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    outer,
    orient="vertical",
    command=canvas.yview
)

content = tk.Frame(
    canvas,
    bg="#f2f2f2"
)

content.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas_window = canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


def resize_content(event):
    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    resize_content
)


# ============================================================
# DASHBOARD
# ============================================================

greeting = tk.Label(
    content,
    text="Your Homework",
    font=("Helvetica", 24, "bold"),
    bg="#f2f2f2",
    fg="black"
)

greeting.pack(
    anchor="w",
    padx=30,
    pady=(25, 15)
)


# ============================================================
# STAT WIDGETS
# ============================================================

stats_frame = tk.Frame(
    content,
    bg="#f2f2f2"
)

stats_frame.pack(
    fill="x",
    padx=25
)


def create_stat_widget(
    parent,
    title_text,
    number,
    color
):

    frame = tk.Frame(
        parent,
        bg="#ffffff",
        bd=0,
        highlightthickness=1,
        highlightbackground="#dddddd"
    )

    frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    dot = tk.Label(
        frame,
        text="●",
        font=("Helvetica", 25),
        fg=color,
        bg="#ffffff"
    )

    dot.pack(
        pady=(12, 0)
    )

    number_label = tk.Label(
        frame,
        text=str(number),
        font=("Helvetica", 23, "bold"),
        bg="#ffffff",
        fg="black"
    )

    number_label.pack()

    text_label = tk.Label(
        frame,
        text=title_text,
        font=("Helvetica", 10),
        bg="#ffffff",
        fg="black"
    )

    text_label.pack(
        pady=(0, 14)
    )

    return number_label


not_started_number = create_stat_widget(
    stats_frame,
    "Not Started",
    0,
    STATUS_COLORS["Not started"]
)

in_progress_number = create_stat_widget(
    stats_frame,
    "In Progress",
    0,
    STATUS_COLORS["In progress"]
)

complete_number = create_stat_widget(
    stats_frame,
    "Complete",
    0,
    STATUS_COLORS["Complete"]
)


# ============================================================
# FILTER
# ============================================================

filter_area = tk.Frame(
    content,
    bg="#f2f2f2"
)

filter_area.pack(
    fill="x",
    padx=30,
    pady=(30, 10)
)


tk.Label(
    filter_area,
    text="Homework",
    font=("Helvetica", 18, "bold"),
    bg="#f2f2f2",
    fg="black"
).pack(
    side="left"
)


filter_var = tk.StringVar(
    value="All"
)


filter_menu = tk.OptionMenu(
    filter_area,
    filter_var,
    "All",
    "Not started",
    "In progress",
    "Complete"
)

filter_menu.config(
    bg="#ffffff",
    fg="black",
    activebackground="#eeeeee",
    activeforeground="black",
    relief="flat",
    font=("Helvetica", 10),
    width=14
)

filter_menu.pack(
    side="right"
)


# ============================================================
# HOMEWORK LIST
# ============================================================

cards_frame = tk.Frame(
    content,
    bg="#f2f2f2"
)

cards_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=5
)


# ============================================================
# ADD / EDIT WINDOW
# ============================================================

def open_homework_window(index=None):

    editing = index is not None

    window = tk.Toplevel(root)

    window.title(
        "Edit Homework"
        if editing
        else
        "Add Homework"
    )

    window.geometry("460x560")
    window.resizable(False, False)

    window.configure(
        bg="#ffffff"
    )

    window.grab_set()

    if editing:

        item = homework[index]

    else:

        item = {
            "name": "",
            "due_date": "",
            "time_due": "",
            "subject": "",
            "teacher": "",
            "status": "Not started"
        }


    tk.Label(
        window,
        text="Edit Homework" if editing else "Add Homework",
        font=("Helvetica", 22, "bold"),
        bg="#ffffff",
        fg="black"
    ).pack(
        pady=(25, 20)
    )


    form = tk.Frame(
        window,
        bg="#ffffff"
    )

    form.pack(
        fill="both",
        expand=True,
        padx=35
    )


    def make_entry(
        label,
        value
    ):

        tk.Label(
            form,
            text=label,
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg="black"
        ).pack(
            anchor="w",
            pady=(7, 3)
        )

        entry = tk.Entry(
            form,
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="black",
            insertbackground="black",
            relief="solid",
            bd=1
        )

        entry.pack(
            fill="x",
            ipady=6
        )

        entry.insert(
            0,
            value
        )

        return entry


    name_entry = make_entry(
        "Homework name",
        item["name"]
    )

    due_entry = make_entry(
        "Due date  (DD/MM/YYYY)",
        item["due_date"]
    )

    time_entry = make_entry(
        "Time due",
        item["time_due"]
    )

    subject_entry = make_entry(
        "Subject",
        item["subject"]
    )

    teacher_entry = make_entry(
        "Teacher",
        item["teacher"]
    )


    tk.Label(
        form,
        text="Status",
        font=("Helvetica", 10, "bold"),
        bg="#ffffff",
        fg="black"
    ).pack(
        anchor="w",
        pady=(10, 3)
    )


    status_var = tk.StringVar(
        value=item["status"]
    )


    status_menu = tk.OptionMenu(
        form,
        status_var,
        "Not started",
        "In progress",
        "Complete"
    )

    status_menu.config(
        bg="#ffffff",
        fg="black",
        activebackground="#eeeeee",
        activeforeground="black",
        relief="solid",
        bd=1,
        font=("Helvetica", 11)
    )

    status_menu.pack(
        fill="x"
    )


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save():

        name = name_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Missing homework name",
                "Please enter a homework name."
            )

            return


        new_item = {
            "name": name,
            "due_date": due_entry.get().strip(),
            "time_due": time_entry.get().strip(),
            "subject": subject_entry.get().strip(),
            "teacher": teacher_entry.get().strip(),
            "status": status_var.get()
        }


        if editing:

            homework[index] = new_item

        else:

            homework.append(
                new_item
            )


        save_homework()

        refresh()

        window.destroy()


    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    button_area = tk.Frame(
        window,
        bg="#ffffff"
    )

    button_area.pack(
        fill="x",
        padx=35,
        pady=25
    )


    tk.Button(
        button_area,
        text="Cancel",
        command=window.destroy,
        font=("Helvetica", 10),
        bg="#eeeeee",
        fg="black",
        activebackground="#dddddd",
        activeforeground="black",
        relief="flat",
        padx=16,
        pady=8
    ).pack(
        side="left"
    )


    tk.Button(
        button_area,
        text="Save Homework",
        command=save,
        font=("Helvetica", 10, "bold"),
        bg="#dddddd",
        fg="black",
        activebackground="#cccccc",
        activeforeground="black",
        relief="flat",
        padx=16,
        pady=8
    ).pack(
        side="right"
    )


# ============================================================
# DELETE
# ============================================================

def delete_homework(index):

    answer = messagebox.askyesno(
        "Delete Homework",
        "Are you sure you want to delete this homework?"
    )

    if answer:

        homework.pop(index)

        save_homework()

        refresh()


# ============================================================
# CHANGE STATUS
# ============================================================

def cycle_status(index):

    statuses = [
        "Not started",
        "In progress",
        "Complete"
    ]

    current = homework[index]["status"]

    next_index = (
        statuses.index(current) + 1
    ) % len(statuses)

    homework[index]["status"] = (
        statuses[next_index]
    )

    save_homework()

    refresh()


# ============================================================
# CREATE HOMEWORK CARD
# ============================================================

def create_card(index, item):

    card = tk.Frame(
        cards_frame,
        bg="#ffffff",
        highlightthickness=1,
        highlightbackground="#dddddd"
    )

    card.pack(
        fill="x",
        pady=6
    )


    # Status dot

    tk.Label(
        card,
        text="●",
        font=("Helvetica", 23),
        fg=STATUS_COLORS[item["status"]],
        bg="#ffffff"
    ).pack(
        side="left",
        padx=(18, 12)
    )


    # Information

    info = tk.Frame(
        card,
        bg="#ffffff"
    )

    info.pack(
        side="left",
        fill="both",
        expand=True,
        pady=14
    )


    tk.Label(
        info,
        text=item["name"],
        font=("Helvetica", 14, "bold"),
        bg="#ffffff",
        fg="black",
        anchor="w"
    ).pack(
        fill="x"
    )


    details = []

    if item["subject"]:
        details.append(
            item["subject"]
        )

    if item["teacher"]:
        details.append(
            item["teacher"]
        )


    if details:

        tk.Label(
            info,
            text=" • ".join(details),
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="black",
            anchor="w"
        ).pack(
            fill="x",
            pady=(3, 0)
        )


    due = []

    if item["due_date"]:
        due.append(
            "Due " + item["due_date"]
        )

    if item["time_due"]:
        due.append(
            item["time_due"]
        )


    if due:

        tk.Label(
            info,
            text=" • ".join(due),
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg="black",
            anchor="w"
        ).pack(
            fill="x",
            pady=(4, 0)
        )


    # Buttons

    buttons = tk.Frame(
        card,
        bg="#ffffff"
    )

    buttons.pack(
        side="right",
        padx=15
    )


    tk.Button(
        buttons,
        text=item["status"],
        command=lambda i=index: cycle_status(i),
        font=("Helvetica", 9, "bold"),
        bg=STATUS_COLORS[item["status"]],
        fg="black",
        activebackground=STATUS_COLORS[item["status"]],
        activeforeground="black",
        relief="flat",
        padx=9,
        pady=5
    ).pack(
        pady=(0, 6)
    )


    small_buttons = tk.Frame(
        buttons,
        bg="#ffffff"
    )

    small_buttons.pack()


    tk.Button(
        small_buttons,
        text="Edit",
        command=lambda i=index: open_homework_window(i),
        font=("Helvetica", 9),
        bg="#eeeeee",
        fg="black",
        activebackground="#dddddd",
        activeforeground="black",
        relief="flat",
        padx=10
    ).pack(
        side="left",
        padx=2
    )


    tk.Button(
        small_buttons,
        text="Delete",
        command=lambda i=index: delete_homework(i),
        font=("Helvetica", 9),
        bg="#eeeeee",
        fg="black",
        activebackground="#dddddd",
        activeforeground="black",
        relief="flat",
        padx=10
    ).pack(
        side="left",
        padx=2
    )


# ============================================================
# REFRESH DASHBOARD
# ============================================================

def refresh(*args):

    for widget in cards_frame.winfo_children():
        widget.destroy()


    # Count statuses

    not_started = sum(
        1
        for item in homework
        if item["status"] == "Not started"
    )

    in_progress = sum(
        1
        for item in homework
        if item["status"] == "In progress"
    )

    complete = sum(
        1
        for item in homework
        if item["status"] == "Complete"
    )


    not_started_number.config(
        text=str(not_started)
    )

    in_progress_number.config(
        text=str(in_progress)
    )

    complete_number.config(
        text=str(complete)
    )


    # Filter

    selected = filter_var.get()

    visible = []

    for index, item in enumerate(homework):

        if selected == "All":

            visible.append(
                (index, item)
            )

        elif item["status"] == selected:

            visible.append(
                (index, item)
            )


    # Sort by date

    def date_sort(pair):

        try:

            return datetime.strptime(
                pair[1]["due_date"],
                "%d/%m/%Y"
            )

        except:

            return datetime.max


    visible.sort(
        key=date_sort
    )


    if not visible:

        tk.Label(
            cards_frame,
            text="No homework here yet.",
            font=("Helvetica", 15),
            bg="#f2f2f2",
            fg="black"
        ).pack(
            pady=70
        )

    else:

        for index, item in visible:

            create_card(
                index,
                item
            )


# ============================================================
# BUTTONS
# ============================================================

add_button.config(
    command=lambda: open_homework_window()
)

filter_var.trace_add(
    "write",
    refresh
)


# ============================================================
# START
# ============================================================

load_homework()

refresh()

root.mainloop()
