import csv
import os
from datetime import datetime, timedelta

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup


FILE_NAME = "expenses.csv"


class ExpenseTracker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=10,
            **kwargs
        )

        self.create_csv_file()

        title = Label(
            text="Daily Expense Tracker",
            font_size=28,
            bold=True,
            size_hint_y=None,
            height=60
        )
        self.add_widget(title)

        self.category_input = TextInput(
            hint_text="Category e.g. Food, Transport",
            multiline=False,
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.category_input)

        self.description_input = TextInput(
            hint_text="Description e.g. Lunch, Bus fare",
            multiline=False,
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.description_input)

        self.amount_input = TextInput(
            hint_text="Amount",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.amount_input)

        add_button = Button(
            text="Add Expense",
            size_hint_y=None,
            height=60
        )
        add_button.bind(on_press=self.add_expense)
        self.add_widget(add_button)

        summary_buttons = GridLayout(
            cols=3,
            spacing=5,
            size_hint_y=None,
            height=60
        )

        week_button = Button(text="Week")
        month_button = Button(text="Month")
        year_button = Button(text="Year")

        week_button.bind(on_press=self.show_weekly_total)
        month_button.bind(on_press=self.show_monthly_total)
        year_button.bind(on_press=self.show_yearly_total)

        summary_buttons.add_widget(week_button)
        summary_buttons.add_widget(month_button)
        summary_buttons.add_widget(year_button)

        self.add_widget(summary_buttons)

        self.start_date_input = TextInput(
            hint_text="Start Date: YYYY-MM-DD",
            multiline=False,
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.start_date_input)

        self.end_date_input = TextInput(
            hint_text="End Date: YYYY-MM-DD",
            multiline=False,
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.end_date_input)

        range_button = Button(
            text="Check Custom Date Range",
            size_hint_y=None,
            height=60
        )
        range_button.bind(on_press=self.show_range_total)
        self.add_widget(range_button)

        self.total_label = Label(
            text="Total Spent: 0.00",
            font_size=20,
            bold=True,
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.total_label)

        self.summary_label = Label(
            text="Summary will appear here.",
            font_size=16,
            size_hint_y=None,
            height=60
        )
        self.add_widget(self.summary_label)

        self.scroll = ScrollView()

        self.expense_list = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        self.expense_list.bind(
            minimum_height=self.expense_list.setter("height")
        )

        self.scroll.add_widget(self.expense_list)
        self.add_widget(self.scroll)

        self.load_expenses()

    def create_csv_file(self):
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Description", "Amount"])

    def show_popup(self, title, message):
        popup_layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        popup_label = Label(text=message)

        close_button = Button(
            text="OK",
            size_hint_y=None,
            height=45
        )

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def add_expense(self, instance):
        category = self.category_input.text.strip()
        description = self.description_input.text.strip()
        amount_text = self.amount_input.text.strip()

        if not category or not description or not amount_text:
            self.show_popup(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        try:
            amount = float(amount_text)
        except ValueError:
            self.show_popup(
                "Invalid Amount",
                "Please enter a valid amount."
            )
            return

        date = datetime.now().strftime("%Y-%m-%d")

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description, amount])

        self.category_input.text = ""
        self.description_input.text = ""
        self.amount_input.text = ""

        self.load_expenses()

    def load_expenses(self):
        self.expense_list.clear_widgets()

        total = 0

        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)

            rows = list(reader)

        if not rows:
            self.expense_list.add_widget(
                Label(
                    text="No expenses added yet.",
                    size_hint_y=None,
                    height=40
                )
            )

        for row in reversed(rows):
            if len(row) == 4:
                date, category, description, amount = row

                try:
                    amount_float = float(amount)
                    total += amount_float
                except ValueError:
                    amount_float = 0

                expense_text = (
                    f"{date} | {category} | "
                    f"{description} | {amount_float:.2f}"
                )

                expense_item = Label(
                    text=expense_text,
                    size_hint_y=None,
                    height=45,
                    font_size=14
                )

                self.expense_list.add_widget(expense_item)

        self.total_label.text = f"Total Spent: {total:.2f}"

    def read_expenses(self):
        expenses = []

        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) == 4:
                    try:
                        expense_date = datetime.strptime(
                            row[0],
                            "%Y-%m-%d"
                        ).date()

                        amount = float(row[3])

                        expenses.append({
                            "date": expense_date,
                            "category": row[1],
                            "description": row[2],
                            "amount": amount
                        })

                    except ValueError:
                        pass

        return expenses

    def calculate_total_between_dates(self, start_date, end_date):
        total = 0
        expenses = self.read_expenses()

        for expense in expenses:
            if start_date <= expense["date"] <= end_date:
                total += expense["amount"]

        return total

    def show_weekly_total(self, instance):
        today = datetime.now().date()

        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        total = self.calculate_total_between_dates(
            start_of_week,
            end_of_week
        )

        self.summary_label.text = (
            f"This Week: {total:.2f}\n"
            f"{start_of_week} to {end_of_week}"
        )

    def show_monthly_total(self, instance):
        today = datetime.now().date()

        start_of_month = today.replace(day=1)

        if today.month == 12:
            end_of_month = today.replace(
                year=today.year + 1,
                month=1,
                day=1
            ) - timedelta(days=1)
        else:
            end_of_month = today.replace(
                month=today.month + 1,
                day=1
            ) - timedelta(days=1)

        total = self.calculate_total_between_dates(
            start_of_month,
            end_of_month
        )

        self.summary_label.text = (
            f"This Month: {total:.2f}\n"
            f"{start_of_month} to {end_of_month}"
        )

    def show_yearly_total(self, instance):
        today = datetime.now().date()

        start_of_year = today.replace(month=1, day=1)
        end_of_year = today.replace(month=12, day=31)

        total = self.calculate_total_between_dates(
            start_of_year,
            end_of_year
        )

        self.summary_label.text = (
            f"This Year: {total:.2f}\n"
            f"{start_of_year} to {end_of_year}"
        )

    def show_range_total(self, instance):
        start_date_text = self.start_date_input.text.strip()
        end_date_text = self.end_date_input.text.strip()

        try:
            start_date = datetime.strptime(
                start_date_text,
                "%Y-%m-%d"
            ).date()

            end_date = datetime.strptime(
                end_date_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            self.show_popup(
                "Invalid Date",
                "Please enter dates in this format: YYYY-MM-DD"
            )
            return

        if start_date > end_date:
            self.show_popup(
                "Invalid Range",
                "Start date cannot be after end date."
            )
            return

        total = self.calculate_total_between_dates(start_date, end_date)

        self.summary_label.text = (
            f"Custom Range: {total:.2f}\n"
            f"{start_date} to {end_date}"
        )


class ExpenseTrackerApp(App):
    def build(self):
        self.title = "Expense Tracker"
        return ExpenseTracker()


if __name__ == "__main__":
    ExpenseTrackerApp().run()
