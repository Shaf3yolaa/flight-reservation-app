import tkinter as tk
from tkinter import ttk, messagebox
from database import db

class ReservationsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=12)
        self.controller = controller

        title = ttk.Label(self, text="Reservations", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0,10))

        cols = ("id", "name", "flight", "departure", "destination", "date", "seat")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("flight", text="Flight No.")
        self.tree.heading("departure", text="Departure")
        self.tree.heading("destination", text="Destination")
        self.tree.heading("date", text="Date")
        self.tree.heading("seat", text="Seat")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=140)
        self.tree.column("flight", width=90, anchor="center")
        self.tree.column("departure", width=100)
        self.tree.column("destination", width=100)
        self.tree.column("date", width=90, anchor="center")
        self.tree.column("seat", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)

        refresh_btn = ttk.Button(btn_frame, text="Refresh", command=self.load_data)
        edit_btn = ttk.Button(btn_frame, text="Edit Selected", command=self.edit_selected)
        delete_btn = ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected)
        back_btn = ttk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("HomePage"))

        refresh_btn.grid(row=0, column=0, padx=6)
        edit_btn.grid(row=0, column=1, padx=6)
        delete_btn.grid(row=0, column=2, padx=6)
        back_btn.grid(row=0, column=3, padx=6)

    def on_show(self):
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = db.get_all_reservations()
        for r in rows:
            self.tree.insert("", "end", values=r)

    def get_selected_id(self):
        cur = self.tree.selection()
        if not cur:
            return None
        item = self.tree.item(cur[0])
        return item["values"][0]

    def edit_selected(self):
        selected_id = self.get_selected_id()
        if selected_id is None:
            messagebox.showwarning("No selection", "Please select a reservation to edit.")
            return
        self.controller.show_frame("EditReservationPage", reservation_id=selected_id)

    def delete_selected(self):
        selected_id = self.get_selected_id()
        if selected_id is None:
            messagebox.showwarning("No selection", "Please select a reservation to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reservation?"):
            db.delete_reservation(selected_id)
            messagebox.showinfo("Deleted", "Reservation deleted.")
            self.load_data()
