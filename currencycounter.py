import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime as dt

class CurrencyConverter:
    def __init__(self, url):
        self.url = url
        self.rates = self.fetch_conversion_rates()

    def fetch_conversion_rates(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            rates = {
                'USD': data['rates']['USD'],
                'INR': data['rates']['INR'],
                'EUR': data['rates']['EUR'],  # Add EUR here
            }
            return rates
        except requests.RequestException as e:
            messagebox.showerror('Error', f'Failed to fetch currency rates: {e}')
            return {}
        
    def convert(self, amount, base_currency, des_currency):
        if base_currency == des_currency:
            return amount

        base_rate = self.rates.get(base_currency, 1)
        des_rate = self.rates.get(des_currency, 1)

         # Convert to base currency (e.g., EUR)
        amount_in_base = amount / base_rate

        # Convert from base currency to destination
        converted_amount = amount_in_base * des_rate

        return '{:,.2f}'.format(converted_amount)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=100, height=40, corner_radius=20, color="#52595D", hover_color="#63676B"):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent['bg'])
        self.command = command
        self.color = color
        self.hover_color = hover_color
        self.corner_radius = corner_radius

        self.round_rect = self.create_rounded_rect(0, 0, width, height, radius=corner_radius, fill=color)
        self.text = self.create_text(width // 2, height // 2, text=text, fill="white", font=("calibri", 12))

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            (x1 + radius, y1), (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
            (x2, y2 - radius), (x2, y2), (x2 - radius, y2), (x1 + radius, y2),
            (x1, y2), (x1, y2 - radius), (x1, y1 + radius), (x1, y1)
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.itemconfig(self.round_rect, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.round_rect, fill=self.color)


class CurrencyConverterApp(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.title('Currency Converter')
        self.geometry('400x450')
        self.config(bg='#3A3B3C')
        self.converter = converter
        self.create_widgets()

    def create_widgets(self):
        # Title label
        tk.Label(self, text='Currency Converter', bg='#3A3B3C', fg='white', font=('franklin gothic medium', 20), relief='sunken').place(x=200, y=35, anchor='center')
         # Date Label
        tk.Label(self, text=f'{dt.datetime.now():%A, %B %d, %Y}', bg='#3A3B3C', fg='white', font=('calibri', 10)).place(
            x=0, y=430, anchor='sw')

        # Version Label
        tk.Label(self, text='v1.1', bg='#3A3B3C', fg='white', font=('calibri', 10)).place(x=400, y=430, anchor='se')
        # Amount label and entry
        tk.Label(self, text='Input Amount:', bg='#3A3B3C', fg='white', font=('franklin gothic book', 15)).place(x=200, y=80, anchor='center')
        self.amount_entry = tk.Entry(self, width=25)
        self.amount_entry.place(x=200, y=110, anchor='center')

        # From currency label and combobox
        tk.Label(self, text='From:', bg='#3A3B3C', fg='white', font=('franklin gothic book', 15)).place(x=200, y=140, anchor='center')
        self.from_currency = ttk.Combobox(self, state='readonly', values=['USD', 'INR','EUR'], width=20)
        self.from_currency.set('USD')
        self.from_currency.place(x=200, y=170, anchor='center')

        # To currency label and combobox
        tk.Label(self, text='To:', bg='#3A3B3C', fg='white', font=('franklin gothic book', 15)).place(x=200, y=200, anchor='center')
        self.to_currency = ttk.Combobox(self, state='readonly', values=['USD', 'INR','EUR'], width=20)
        self.to_currency.set('INR')
        self.to_currency.place(x=200, y=230, anchor='center')

        # Convert and Clear buttons with rounded corners
        RoundedButton(self, text='Convert', command=self.convert_currency, width=100, height=40).place(x=150, y=280, anchor='center')
        RoundedButton(self, text='Clear', command=self.clear_fields, width=100, height=40, color="red", hover_color="#FF5555").place(x=250, y=280, anchor='center')

        # Result label
        self.result_label = tk.Label(self, text='', bg='#52595D', fg='white', font=('calibri', 12), relief='sunken', width=40)
        self.result_label.place(x=200, y=340, anchor='center')

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency.get()
            to_currency = self.to_currency.get()

            if not from_currency or not to_currency:
                raise ValueError('Please select both currencies.')

            converted_amount = self.converter.convert(amount, from_currency, to_currency)
            self.result_label.config(text=f'{amount:,} {from_currency} = {converted_amount} {to_currency}')

        except ValueError as e:
            messagebox.showwarning('Invalid Input', f'Error: {e}')

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.result_label.config(text='')


if __name__ == '__main__':
    converter = CurrencyConverter('https://open.er-api.com/v6/latest/USD')
    app = CurrencyConverterApp(converter)
    app.mainloop()
