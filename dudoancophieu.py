from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import requests
import tkinter as tk
from tkinter import ttk, messagebox

# Nhập API Key của bạn từ Alpha Vantage
API_KEY = "F32TSTBNX5L1QRRB"  # Thay YOUR_API_KEY bằng API Key thực tế của bạn

# Hàm lấy dữ liệu giá cổ phiếu hàng ngày từ Alpha Vantage
def get_daily_stock_price(symbol):  # Đổi tên hàm thành "get_daily_stock_price"
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # Phương thức lấy dữ liệu hàng ngày
        "symbol": symbol,                  # Mã cổ phiếu
        "apikey": API_KEY                   # API Key của bạn
    }
    response = requests.get(url, params=params)
    
    # Kiểm tra nếu phản hồi hợp lệ
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]  # Trả về dữ liệu giá cổ phiếu theo ngày
        else:
            return None
    else:
        return None

# Hàm lấy dữ liệu giá cổ phiếu hàng ngày từ Alpha Vantage
def get_daily_stock_price(symbol):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        else:
            return None
    else:
        return None

# Hàm hiển thị dữ liệu lên bảng và đồ thị
def display_stock_data():
    symbol = entry.get()
    stock_data = get_daily_stock_price(symbol)
    
    # Xóa dữ liệu cũ trong bảng
    for row in tree.get_children():
        tree.delete(row)
    
    if stock_data:
        dates = []
        open_prices = []
        close_prices = []
        
        # Hiển thị dữ liệu lên bảng và thu thập thông tin để vẽ đồ thị
        for date, metrics in list(stock_data.items())[:10]:  # Lấy 10 ngày gần nhất
            tree.insert("", "end", values=(
                date,
                metrics["1. open"],
                metrics["2. high"],
                metrics["3. low"],
                metrics["4. close"],
                metrics["5. volume"]
            ))
            dates.append(date)
            open_prices.append(float(metrics["1. open"]))
            close_prices.append(float(metrics["4. close"]))
        
        # Cập nhật đồ thị
        plot_graph(dates, open_prices, close_prices)
    else:
        messagebox.showerror("Lỗi", "Không thể lấy dữ liệu cổ phiếu. Vui lòng kiểm tra mã cổ phiếu.")

# Hàm vẽ đồ thị
def plot_graph(dates, open_prices, close_prices):
    fig.clear()  # Xóa đồ thị cũ
    
    # Vẽ đồ thị
    ax = fig.add_subplot(111)
    ax.plot(dates, open_prices, label="Giá mở cửa", marker="o")
    ax.plot(dates, close_prices, label="Giá đóng cửa", marker="x")
    ax.set_title("Xu hướng giá cổ phiếu")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Giá")
    ax.legend()
    ax.grid(True)
    ax.invert_xaxis()  # Đảo ngược trục X để hiển thị từ ngày mới nhất

    # Sửa lỗi nhãn bị đè
    ax.set_xticks(range(0, len(dates), 2))  # Hiển thị nhãn cách mỗi 2 ngày
    ax.set_xticklabels(dates[::2], rotation=45, ha='right')

    
    # Cập nhật Canvas
    canvas.draw()

# Giao diện Tkinter
root = tk.Tk()
root.title("Bảng giá cổ phiếu và đồ thị")

# Khung nhập mã cổ phiếu
frame_top = tk.Frame(root)
frame_top.pack(pady=10)
label = tk.Label(frame_top, text="Nhập mã cổ phiếu (ví dụ: AAPL):")
label.pack(side=tk.LEFT, padx=5)
entry = tk.Entry(frame_top)
entry.pack(side=tk.LEFT, padx=5)
button = tk.Button(frame_top, text="Hiển thị giá cổ phiếu", command=display_stock_data)
button.pack(side=tk.LEFT, padx=5)

# Khung hiển thị bảng và đồ thị
frame_main = tk.Frame(root)
frame_main.pack(padx=10, pady=10)

# Bảng Treeview
columns = ("Date", "Open", "High", "Low", "Close", "Volume")
tree = ttk.Treeview(frame_main, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(side=tk.LEFT)

# Thanh cuộn cho bảng
scrollbar = ttk.Scrollbar(frame_main, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Khung đồ thị
frame_graph = tk.Frame(frame_main)
frame_graph.pack(side=tk.LEFT, padx=10)

# Tạo đồ thị Matplotlib
fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack()

root.mainloop()