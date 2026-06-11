import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import calendar

# ---------------------------------------------------------------------------
# Conversion data
# ---------------------------------------------------------------------------

DAY_NAMES = {
    0: "Moonday",   # Monday
    1: "Toilday",   # Tuesday
    2: "Wealday",   # Wednesday
    3: "Oathday",   # Thursday
    4: "Fireday",   # Friday
    5: "Starday",   # Saturday
    6: "Sunday",    # Sunday
}

# Ordered list — index+1 == Gregorian month number (1:1 mapping)
MONTH_LIST = [
    "Abadius",   # 1  Jan  31 days
    "Calistril", # 2  Feb  28/29 days
    "Pharast",   # 3  Mar  31 days
    "Gozran",    # 4  Apr  30 days
    "Desnus",    # 5  May  31 days
    "Sarenith",  # 6  Jun  30 days
    "Erastus",   # 7  Jul  31 days
    "Arodus",    # 8  Aug  31 days
    "Rova",      # 9  Sep  30 days
    "Lamashan",  # 10 Oct  31 days
    "Neth",      # 11 Nov  30 days
    "Kuthona",   # 12 Dec  31 days
]

MONTH_NAMES = {i + 1: name for i, name in enumerate(MONTH_LIST)}

YEAR_OFFSET = 1032


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ordinal_suffix(day: int) -> str:
    """Return the ordinal suffix for a day number (1st, 2nd, 3rd, 4th...)."""
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")


def days_in_golarion_month(pf_year: int, pf_month: int) -> int:
    """
    Return the number of days in a Golarion month.
    Uses the equivalent Gregorian year (pf_year + YEAR_OFFSET) for leap-year
    calculation so that Calistril (Feb) gets 29 days on leap years.
    """
    greg_year = pf_year + YEAR_OFFSET
    return calendar.monthrange(greg_year, pf_month)[1]


def format_pathfinder_date(date: datetime.date) -> str:
    """Convert a Python date object to a Pathfinder-formatted date string."""
    day_name = DAY_NAMES[date.weekday()]
    month_name = MONTH_NAMES[date.month]
    pf_year = date.year - YEAR_OFFSET
    day = date.day
    suffix = ordinal_suffix(day)
    return f"{day_name}, {day}{suffix} of {month_name}, in the year {pf_year} IA"


def format_golarion_date(pf_year: int, pf_month: int, pf_day: int) -> str:
    """Build the output string from native Golarion inputs."""
    greg_year = pf_year + YEAR_OFFSET
    greg_date = datetime.date(greg_year, pf_month, pf_day)
    day_name = DAY_NAMES[greg_date.weekday()]
    month_name = MONTH_NAMES[pf_month]
    suffix = ordinal_suffix(pf_day)
    return f"{day_name}, {pf_day}{suffix} of {month_name}, in the year {pf_year} IA"


def golarion_delta(pf_year: int, pf_month: int, pf_day: int, delta: int) -> str:
    """Apply a day delta to a Golarion date and return the formatted result."""
    greg_year = pf_year + YEAR_OFFSET
    base = datetime.date(greg_year, pf_month, pf_day)
    adjusted = base + datetime.timedelta(days=delta)
    new_pf_year = adjusted.year - YEAR_OFFSET
    return format_golarion_date(new_pf_year, adjusted.month, adjusted.day)


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

BG = "#d0d0d0"
ACCENT = "#4a4a8a"
ACCENT_DARK = "#3a3a7a"
ORANGE = "#e07020"
RESULT_FG = "#1a1a5a"
DELTA_FG = "#1a5a1a"
CLOSE_BG = "#8a2a2a"
CLOSE_HOVER = "#aa4a4a"


class PathfinderCalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pathfinder Calendar Converter")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Tab 1 state
        self._selected_date: datetime.date | None = None

        self._build_ui()
        self._center_window()

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------

    def _build_ui(self):
        # ── Notebook (tabs) ──────────────────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background="#b0b0b0", foreground="#1a1a1a",
                        padding=[10, 4], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

        nb = ttk.Notebook(self)
        nb.pack(padx=12, pady=(10, 0), fill="both", expand=True)

        tab1 = tk.Frame(nb, bg=BG)
        tab2 = tk.Frame(nb, bg=BG)
        nb.add(tab1, text="  Gregorian → Golarion  ")
        nb.add(tab2, text="  Golarion Calendar  ")

        self._build_tab1(tab1)
        self._build_tab2(tab2)

        # ── Shared Close button ───────────────────────────────────────────────
        close_btn = tk.Button(
            self,
            text="Close",
            font=("Segoe UI", 10, "bold"),
            bg=CLOSE_BG,
            fg="white",
            activebackground=CLOSE_HOVER,
            activeforeground="white",
            width=12,
            command=self.destroy,
        )
        close_btn.pack(pady=(8, 14))

    # ── Tab 1: Gregorian → Golarion ─────────────────────────────────────────

    def _build_tab1(self, parent):
        cal_frame = tk.LabelFrame(
            parent, text="Select a Date", font=("Segoe UI", 10),
            bg=BG, fg="#2a2a2a", padx=8, pady=8,
        )
        cal_frame.pack(padx=16, pady=(10, 8))

        self.cal = Calendar(
            cal_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            font=("Segoe UI", 10),
            background=ACCENT,
            foreground="white",
            headersbackground=ACCENT_DARK,
            headersforeground="white",
            selectbackground=ORANGE,
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

        result_frame = tk.LabelFrame(
            parent, text="Pathfinder Date", font=("Segoe UI", 10),
            bg=BG, fg="#2a2a2a", padx=8, pady=8,
        )
        result_frame.pack(padx=16, pady=(0, 8), fill="x")

        self.result_var = tk.StringVar(value="— select a date above —")
        tk.Label(
            result_frame, textvariable=self.result_var,
            font=("Segoe UI", 11, "bold"), bg=BG, fg=RESULT_FG,
            wraplength=420, justify="center",
        ).pack()

        self._build_delta_section(parent, mode="greg")

    # ── Tab 2: Native Golarion calendar ─────────────────────────────────────

    def _build_tab2(self, parent):
        sel_frame = tk.LabelFrame(
            parent, text="Select a Golarion Date", font=("Segoe UI", 10),
            bg=BG, fg="#2a2a2a", padx=12, pady=10,
        )
        sel_frame.pack(padx=16, pady=(10, 8), fill="x")

        # Month
        tk.Label(sel_frame, text="Month:", font=("Segoe UI", 10),
                 bg=BG, fg="#2a2a2a").grid(row=0, column=0, sticky="e", padx=(0, 4))
        self.gol_month_var = tk.StringVar(value=MONTH_LIST[0])
        self.month_cb = ttk.Combobox(
            sel_frame, textvariable=self.gol_month_var,
            values=MONTH_LIST, state="readonly", width=12,
            font=("Segoe UI", 10),
        )
        self.month_cb.grid(row=0, column=1, padx=(0, 16), sticky="w")
        self.month_cb.bind("<<ComboboxSelected>>", self._on_month_or_year_changed)

        # Day
        tk.Label(sel_frame, text="Day:", font=("Segoe UI", 10),
                 bg=BG, fg="#2a2a2a").grid(row=0, column=2, sticky="e", padx=(0, 4))
        self.gol_day_var = tk.StringVar(value="1")
        self.day_cb = ttk.Combobox(
            sel_frame, textvariable=self.gol_day_var,
            values=[str(d) for d in range(1, 32)],
            state="readonly", width=5,
            font=("Segoe UI", 10),
        )
        self.day_cb.grid(row=0, column=3, padx=(0, 16), sticky="w")
        self.day_cb.bind("<<ComboboxSelected>>", self._on_golarion_changed)

        # Year
        tk.Label(sel_frame, text="Year (IA):", font=("Segoe UI", 10),
                 bg=BG, fg="#2a2a2a").grid(row=0, column=4, sticky="e", padx=(0, 4))
        self.gol_year_var = tk.StringVar(value="994")
        year_entry = tk.Entry(
            sel_frame, textvariable=self.gol_year_var,
            font=("Segoe UI", 10), width=7, justify="center",
        )
        year_entry.grid(row=0, column=5, sticky="w")
        self.gol_year_var.trace_add("write", self._on_month_or_year_changed)

        # Result
        result2_frame = tk.LabelFrame(
            parent, text="Golarion Date", font=("Segoe UI", 10),
            bg=BG, fg="#2a2a2a", padx=8, pady=8,
        )
        result2_frame.pack(padx=16, pady=(0, 8), fill="x")

        self.gol_result_var = tk.StringVar(value="— select a date above —")
        tk.Label(
            result2_frame, textvariable=self.gol_result_var,
            font=("Segoe UI", 11, "bold"), bg=BG, fg=RESULT_FG,
            wraplength=420, justify="center",
        ).pack()

        self._build_delta_section(parent, mode="gol")

    # ── Shared delta builder ─────────────────────────────────────────────────

    def _build_delta_section(self, parent, mode: str):
        delta_frame = tk.LabelFrame(
            parent, text="Delta (days offset)", font=("Segoe UI", 10),
            bg=BG, fg="#2a2a2a", padx=8, pady=8,
        )
        delta_frame.pack(padx=16, pady=(0, 10), fill="x")

        inner = tk.Frame(delta_frame, bg=BG)
        inner.pack()

        tk.Label(inner, text="Delta:", font=("Segoe UI", 10),
                 bg=BG, fg="#2a2a2a").grid(row=0, column=0, padx=(0, 6), sticky="e")

        if mode == "greg":
            self.delta_var = tk.StringVar()
            self.delta_var.trace_add("write", self._on_delta_changed)
            dvar = self.delta_var
        else:
            self.gol_delta_var = tk.StringVar()
            self.gol_delta_var.trace_add("write", self._on_gol_delta_changed)
            dvar = self.gol_delta_var

        tk.Entry(
            inner, textvariable=dvar,
            font=("Segoe UI", 10), width=10, justify="center",
        ).grid(row=0, column=1, sticky="w")

        if mode == "greg":
            self.delta_result_var = tk.StringVar(value="")
            rvar = self.delta_result_var
        else:
            self.gol_delta_result_var = tk.StringVar(value="")
            rvar = self.gol_delta_result_var

        tk.Label(
            delta_frame, textvariable=rvar,
            font=("Segoe UI", 11, "bold"), bg=BG, fg=DELTA_FG,
            wraplength=420, justify="center",
        ).pack(pady=(6, 0))

    # -----------------------------------------------------------------------
    # Event handlers — Tab 1
    # -----------------------------------------------------------------------

    def _on_date_selected(self, _event=None):
        date_str = self.cal.get_date()
        self._selected_date = datetime.date.fromisoformat(date_str)
        self.result_var.set(format_pathfinder_date(self._selected_date))
        self.delta_var.set("")
        self.delta_result_var.set("")

    def _on_delta_changed(self, *_args):
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

    # -----------------------------------------------------------------------
    # Event handlers — Tab 2
    # -----------------------------------------------------------------------

    def _on_month_or_year_changed(self, *_args):
        """
        When month or year changes, recalculate the max days for that month
        (respecting leap years for Calistril/Feb), clamp the selected day if
        needed, then recalculate the date output.
        """
        year_raw = self.gol_year_var.get().strip()
        try:
            pf_year = int(year_raw)
            if pf_year <= 0:
                raise ValueError
        except ValueError:
            # Can't determine days yet — just refresh the output
            self._on_golarion_changed()
            return

        try:
            pf_month = MONTH_LIST.index(self.gol_month_var.get()) + 1
        except ValueError:
            self._on_golarion_changed()
            return

        max_days = days_in_golarion_month(pf_year, pf_month)
        new_values = [str(d) for d in range(1, max_days + 1)]
        self.day_cb["values"] = new_values

        # Clamp current day selection if it exceeds the new month's length
        try:
            current_day = int(self.gol_day_var.get())
        except ValueError:
            current_day = 1
        if current_day > max_days:
            self.gol_day_var.set(str(max_days))

        self._on_golarion_changed()

    def _on_golarion_changed(self, *_args):
        """Recalculate the Golarion date output."""
        # Clear delta whenever base date changes
        if hasattr(self, "gol_delta_var"):
            self.gol_delta_var.set("")
        if hasattr(self, "gol_delta_result_var"):
            self.gol_delta_result_var.set("")

        year_raw = self.gol_year_var.get().strip()
        if not year_raw:
            self.gol_result_var.set("— enter a year —")
            return

        try:
            pf_year = int(year_raw)
            if pf_year <= 0:
                raise ValueError
        except ValueError:
            self.gol_result_var.set("Error — year must be a positive integer")
            return

        try:
            pf_month = MONTH_LIST.index(self.gol_month_var.get()) + 1
            pf_day = int(self.gol_day_var.get())
        except (ValueError, IndexError):
            self.gol_result_var.set("Error")
            return

        # Validate day against actual month length
        max_days = days_in_golarion_month(pf_year, pf_month)
        if not (1 <= pf_day <= max_days):
            self.gol_result_var.set("Error — invalid day for selected month/year")
            return

        try:
            result = format_golarion_date(pf_year, pf_month, pf_day)
        except Exception:
            self.gol_result_var.set("Error")
            return

        self.gol_result_var.set(result)

    def _on_gol_delta_changed(self, *_args):
        """Live delta calculation for Tab 2."""
        year_raw = self.gol_year_var.get().strip()
        raw = self.gol_delta_var.get().strip()

        if raw == "" or raw in ("-", "+"):
            self.gol_delta_result_var.set("")
            return

        try:
            pf_year = int(year_raw)
            if pf_year <= 0:
                raise ValueError
            pf_month = MONTH_LIST.index(self.gol_month_var.get()) + 1
            pf_day = int(self.gol_day_var.get())
            delta = int(raw)
        except (ValueError, IndexError):
            self.gol_delta_result_var.set("Error")
            return

        try:
            result = golarion_delta(pf_year, pf_month, pf_day, delta)
        except Exception:
            self.gol_delta_result_var.set("Error")
            return

        self.gol_delta_result_var.set(result)

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

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
