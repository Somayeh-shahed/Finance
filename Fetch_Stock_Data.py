import pandas as pd
import yfinance as yf
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, filedialog
import datetime

class StockAPP:
    def __init__(self,root):
        self.root = root
        self.root.title("Stock Data")
        self.root.geometry("300x350")

        #Stock Name
        tk.Label(root, text = "Stock Lable:").pack(pady = 5)
        self.ticker_entry = tk.Entry(root)
        self.ticker_entry.pack( pady = 5)

        #Stock Start Date
        tk.Label(root, text = "Start Date(YYYY-MM-DD):").pack(pady = 5)
        self.start_date = tk.Entry(root)
        self.start_date.pack( pady = 5)

        #Stock End Date
        tk.Label(root, text = "End Date(YYYY-MM-DD):").pack(pady = 5)
        self.end_date = tk.Entry(root)
        self.end_date.pack( pady = 5)

        #Saving path
        tk.Label(root, text = "Saving path:").pack(pady = 5)
        self.file_path = tk.StringVar(value="stock_data.csv")

        self.start_date.pack( pady = 5)
        tk.Entry(root, textvariable = self.file_path, state="readonly").pack(pady=5)
        tk.Button(root, text ="File Path", command = self.choose_file).pack(pady=5)
        tk.Button(root, text = "Fetch and Save", command = self.fetch_and_save).pack(pady=5)

    def choose_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"),("All files","*.*")])
        if file_path:
            self.file_path.set(file_path)


    def fetch_stock_data(self, ticker, start_date, end_date):
        try:
            # بررسی فرمت تاریخ
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
            datetime.datetime.strptime(end_date, "%Y-%m-%d")

            # دریافت داده‌های سهام
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)

            if data.empty:
                raise ValueError(f"No data found for {ticker} in the specified data range.")

            # انتخاب ستون‌های مورد نظر
            data = data[["Open", "High", "Low", "Close", "Volume"]]
            data["Date"] = data.index
            data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]
            return data

        except ValueError as ve:
            raise ValueError(f"Error: {str(ve)}")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

    def fetch_and_save(self):
        try:
            ticker = self.ticker_entry.get().strip().upper()
            start_date = self.start_date.get().strip()
            end_date = self.end_date.get().strip()
            output_file = self.file_path.get()

            if not ticker or not start_date or not end_date or not output_file:
                messagebox.showerror("خطا", "لطفاً تمام فیلدها را پر کنید!")
                return

            # دریافت داده‌ها
            data = self.fetch_stock_data(ticker, start_date, end_date)

            # ذخیره در فایل CSV
            data.to_csv(output_file, index=False)
            messagebox.showinfo("Done",f"{ticker}'s data is successfully saved at {output_file}")


        except Exception as e:
            messagebox.showerror("Error", str(e))
    
if __name__ == "__main__":
        root = tk.Tk()
        app = StockAPP(root)
        root.mainloop()
