import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime

# --- Conversion Maps ---
DAY_NAMES = {
    0: "Moonday",   # Monday
    1: "Toilday",   # Tuesday
    2: "Wealday",   # Wednesday
    3: "Oathday",   # Thursday
    4: "Fireday",   # Friday
    5: "Starday",   # Saturday
    6: "Sunday",    # Sunday
}

MONTH_NAMES = {
    1:  "Abadius",
    2:  "Calistril",
    3:  "Pharast",
    4:  "Gozran",
    5:  "Desnus",
    6:  "Sarenith",
    7:  "Erastus",
    8:  "Arodus",
    9:  "Rova",
    10: "Lamashan",
    11: "Neth",
    12: "Kuthona",
}

YEAR_OFFSET = 1032


def ordinal_suffix(day: int) -> str:
    """Return the ordinal suffix for a day number (1st, 2nd, 3rd, 4th...)."""
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")


def format_pathfinder_date(date: datetime.date) -> str:
    """Convert a Python date object to a Pathfinder-formatted date string."""
    day_name = DAY_NAMES[date.weekday()]
    month_name = MONTH_NAMES[date.month]
    pf_year = date.year - YEAR_OFFSET
    day = date.day
    suffix = ordinal_suffix(day)
    return f"{day_name}, {day}{suffix} of {month_name}, in the year {pf_year} IA"


class PathfinderCalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pathfinder Calendar Converter")
        self.resizable(False, False)
        self.configure(bg="#d0d0d0")

        self._selected_date: datetime.date | None = None

        self._build_ui()
        self._center_window()

    def _build_ui(self):
        pad = {"padx": 16, "pady": 8}

        # ── Title label ──────────────────────────────────────────────────────
        title_lbl = tk.Label(
            self,
            text="Pathfinder Date Converter",
            font=("Segoe UI", 14, "bold"),
            bg="#d0d0d0",
            fg="#2a2a2a",
        )
        title_lbl.pack(**pad)

        # ── Calendar widget ───────────────────────────────────────────────────
        cal_frame = tk.LabelFrame(
            self,
            text="Select a Date",
            font=("Segoe UI", 10),
            bg="#d0d0d0",
            fg="#2a2a2a",
            padx=8,
            pady=8,
        )
        cal_frame.pack(padx=16, pady=(0, 8))

        self.cal = Calendar(
            cal_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            font=("Segoe UI", 10),
            background="#4a4a8a",
            foreground="white",
            headersbackground="#3a3a7a",
            headersforeground="white",
            selectbackground="#e07020",
            selectforeground="white",
            normalbackground="#f5f5f5",
            normalforeground="#1a1a1a",
            weekendbackground="#e8e8f8",
            weekendforeground="#1a1a1a",
            othermonthbackground="#cccccc",
            othermonthforeground="#888888",
        )
        self.cal.pack()
        self.cal.bind("<<CalendarSelected>>", self._on_date_selected)

        # ── Converted date output ─────────────────────────────────────────────
        result_frame = tk.LabelFrame(
            self,
            text="Pathfinder Date",
            font=("Segoe UI", 10),
            bg="#d0d0d0",
            fg="#2a2a2a",
            padx=8,
            pady=8,
        )
        result_frame.pack(padx=16, pady=(0, 8), fill="x")

        self.result_var = tk.StringVar(value="— select a date above —")
        result_lbl = tk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Segoe UI", 11, "bold"),
            bg="#d0d0d0",
            fg="#1a1a5a",
            wraplength=420,
            justify="center",
        )
        result_lbl.pack()

        # ── Delta section ─────────────────────────────────────────────────────
        delta_frame = tk.LabelFrame(
            self,
            text="Delta (days offset)",
            font=("Segoe UI", 10),
            bg="#d0d0d0",
            fg="#2a2a2a",
            padx=8,
            pady=8,
        )
        delta_frame.pack(padx=16, pady=(0, 8), fill="x")

        delta_inner = tk.Frame(delta_frame, bg="#d0d0d0")
        delta_inner.pack()

        delta_caption = tk.Label(
            delta_inner,
            text="Delta:",
            font=("Segoe UI", 10),
            bg="#d0d0d0",
            fg="#2a2a2a",
        )
        delta_caption.grid(row=0, column=0, padx=(0, 6), sticky="e")

        self.delta_var = tk.StringVar()
        self.delta_var.trace_add("write", self._on_delta_changed)

        delta_entry = tk.Entry(
            delta_inner,
            textvariable=self.delta_var,
            font=("Segoe UI", 10),
            width=10,
            justify="center",
        )
        delta_entry.grid(row=0, column=1, sticky="w")

        self.delta_result_var = tk.StringVar(value="")
        delta_result_lbl = tk.Label(
            delta_frame,
            textvariable=self.delta_result_var,
            font=("Segoe UI", 11, "bold"),
            bg="#d0d0d0",
            fg="#1a5a1a",
            wraplength=420,
            justify="center",
        )
        delta_result_lbl.pack(pady=(6, 0))

        # ── Close button ──────────────────────────────────────────────────────
        close_btn = tk.Button(
            self,
            text="Close",
            font=("Segoe UI", 10, "bold"),
            bg="#8a2a2a",
            fg="white",
            activebackground="#aa4a4a",
            activeforeground="white",
            width=12,
            command=self.destroy,
        )
        close_btn.pack(pady=(4, 16))

    # ── Event handlers ────────────────────────────────────────────────────────

    def _on_date_selected(self, _event=None):
        """Called when the user picks a date on the calendar."""
        date_str = self.cal.get_date()          # "yyyy-mm-dd"
        self._selected_date = datetime.date.fromisoformat(date_str)
        self.result_var.set(format_pathfinder_date(self._selected_date))

        # Clear delta field and result
        self.delta_var.set("")
        self.delta_result_var.set("")

    def _on_delta_changed(self, *_args):
        """Called live whenever the delta entry changes."""
        if self._selected_date is None:
            self.delta_result_var.set("")
            return

        raw = self.delta_var.get().strip()

        if raw == "" or raw in ("-", "+"):
            self.delta_result_var.set("")
            return

        try:
            delta = int(raw)
        except ValueError:
            self.delta_result_var.set("Error")
            return

        adjusted = self._selected_date + datetime.timedelta(days=delta)
        self.delta_result_var.set(format_pathfinder_date(adjusted))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = PathfinderCalendarApp()
    app.mainloop()
