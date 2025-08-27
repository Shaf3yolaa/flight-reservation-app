import ttkbootstrap as tb
from home import HomePage
from booking import BookingPage
from reservations import ReservationsPage
from edit_reservation import EditReservationPage
from database import db


class App(tb.Window):
    def __init__(self):
        super().__init__(
            title="Flight Reservation App",
            themename="cosmo",
            size=(800, 520),
            resizable=(False, False)
        )

     
        container = tb.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name: str, **kwargs):
        frame = self.frames[page_name]

        if hasattr(frame, "on_show"):
            frame.on_show(**kwargs)
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
