import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, INFO

class HomePage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        # Title
        title = tb.Label(
            self,
            text="Welcome to AirBridge Reservations",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=10)

        subtitle = tb.Label(
            self,
            text="Book your flights and manage your reservations easily.",
            font=("Segoe UI", 11)
        )
        subtitle.pack(pady=(0,20))

        # Frame that holds the cards
        card_frame = tb.Frame(self)
        card_frame.pack(pady=10)

        # -----------------------
        # Book Flight card
        # -----------------------
        book_btn = tb.Button(
            card_frame,
            text="✈️ Book a Flight",
            bootstyle=PRIMARY,
            width=20,
            command=lambda: controller.show_frame("BookingPage")
        )
        book_btn.grid(row=0, column=0, padx=20, ipadx=10, ipady=15)

        book_desc = tb.Label(
            card_frame,
            text="Reserve a new flight ticket by entering your details.",
            font=("Segoe UI", 9)
        )
        book_desc.grid(row=1, column=0, padx=20, pady=(5,15))

        # -----------------------
        # View Reservations card
        # -----------------------
        view_btn = tb.Button(
            card_frame,
            text="📋 View Reservations",
            bootstyle=INFO,
            width=20,
            command=lambda: controller.show_frame("ReservationsPage")
        )
        view_btn.grid(row=0, column=1, padx=20, ipadx=10, ipady=15)

        view_desc = tb.Label(
            card_frame,
            text="See, edit, or delete your existing reservations.",
            font=("Segoe UI", 9)
        )
        view_desc.grid(row=1, column=1, padx=20, pady=(5,15))
