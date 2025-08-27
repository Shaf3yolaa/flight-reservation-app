import tkinter as tk
from tkinter import ttk, messagebox
from database import db

class BookingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=12)
        self.controller = controller

        title = ttk.Label(self, text="Book a Flight", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0,10))

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10)

        # Labels and entries
        labels = ["Name", "Flight Number", "Departure", "Destination", "Date (YYYY-MM-DD)", "Seat Number"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=6)
            ent = ttk.Entry(form, width=40)
            ent.grid(row=i, column=1, pady=6, padx=6)
            self.entries[label] = ent

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=12)

        submit_btn = ttk.Button(btn_frame, text="Submit", command=self.submit)
        back_btn = ttk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("HomePage"))

        submit_btn.grid(row=0, column=0, padx=6)
        back_btn.grid(row=0, column=1, padx=6)

    def on_show(self):

        for e in self.entries.values():
            e.delete(0, tk.END)

    def submit(self):
        name = self.entries["Name"].get().strip()
        flight = self.entries["Flight Number"].get().strip()
        departure = self.entries["Departure"].get().strip()
        destination = self.entries["Destination"].get().strip()
        date = self.entries["Date (YYYY-MM-DD)"].get().strip()
        seat = self.entries["Seat Number"].get().strip()

        if not (name and flight and departure and destination and date and seat):
            messagebox.showwarning("Missing Data", "Please fill out all fields.")
            return

        try:
            parts = date.split("-")
            if len(parts) != 3 or not all(p.isdigit() for p in parts):
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
            return

        db.add_reservation(name, flight, departure, destination, date, seat)
        messagebox.showinfo("Success", "Reservation added.")
        self.controller.show_frame("ReservationsPage")
