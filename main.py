import pandas as pd
import tkinter as tk
from escpos.printer import Usb

p = Usb(0x0416,0x5011)


df = pd.read_csv("products.csv")

root = tk.Tk()
root.title("Simple Point of Sale")
root.geometry("300x200")
added_product = tk.StringVar()
total_price = 0

def onclick():
    global df, total_price
    added_product_id = int(added_product.get())
    try:
        product_name =  df.loc[df['id'] == added_product_id].name.values[0]
        product_price = df.loc[df['id'] == added_product_id].price.values[0]
        newtext = f"{product_name}\t RM {product_price:.2f}\n"
        total_price += product_price
        textExample.insert(1.0, newtext)
    except:
        pass
    
    added_product.set("")

def onEnter(event):
    onclick()

def print_receipt():
    global total_price
    p.text("RECEIPT\n")
    p.text("________\n")
    p.text(textExample.get(1.0,tk.END))
    p.text(f"TOTAL:\t RM {total_price:.2f}")
    p.cut()
    total_price=0
    textExample.delete(1.0, tk.END)

textBox=tk.Entry(root, textvariable = added_product)
textBox.grid(row=0,column=0)
add_button = tk.Button(root, text="ADD", command=onclick)
add_button.grid(row=0, column=1)
print_button = tk.Button(root, text="PRINT", command=print_receipt)
print_button.grid(row=1, column=1)

textExample = tk.Text(root, width=20 ,height=10)
textExample.grid(row=1,column=0)


root.bind('<Return>', onEnter)


root.mainloop()
