import tkinter as tk
from tkinter import ttk, messagebox
from database import db

class EditReservationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=12)
        self.controller = controller
        self.current_id = None

        title = ttk.Label(self, text="Edit Reservation", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0,10))

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10)

        labels = ["Name", "Flight Number", "Departure", "Destination", "Date (YYYY-MM-DD)", "Seat Number"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=6)
            ent = ttk.Entry(form, width=40)
            ent.grid(row=i, column=1, pady=6, padx=6)
            self.entries[label] = ent

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=12)

        update_btn = ttk.Button(btn_frame, text="Update", command=self.update)
        back_btn = ttk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("ReservationsPage"))

        update_btn.grid(row=0, column=0, padx=6)
        back_btn.grid(row=0, column=1, padx=6)

    def on_show(self, reservation_id=None):
        # Load reservation data into entries
        if reservation_id is None:
            messagebox.showerror("Error", "No reservation ID provided.")
            self.controller.show_frame("ReservationsPage")
            return
        self.current_id = reservation_id
        row = db.get_reservation(reservation_id)
        if not row:
            messagebox.showerror("Error", "Reservation not found.")
            self.controller.show_frame("ReservationsPage")
            return
        # row: (id, name, flight_number, departure, destination, date, seat_number)
        _, name, flight, dep, dest, date, seat = row
        self.entries["Name"].delete(0, tk.END)
        self.entries["Name"].insert(0, name)
        self.entries["Flight Number"].delete(0, tk.END)
        self.entries["Flight Number"].insert(0, flight)
        self.entries["Departure"].delete(0, tk.END)
        self.entries["Departure"].insert(0, dep)
        self.entries["Destination"].delete(0, tk.END)
        self.entries["Destination"].insert(0, dest)
        self.entries["Date (YYYY-MM-DD)"].delete(0, tk.END)
        self.entries["Date (YYYY-MM-DD)"].insert(0, date)
        self.entries["Seat Number"].delete(0, tk.END)
        self.entries["Seat Number"].insert(0, seat)

    def update(self):
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

        db.update_reservation(self.current_id, name, flight, departure, destination, date, seat)
        messagebox.showinfo("Updated", "Reservation updated.")
        self.controller.show_frame("ReservationsPage")
