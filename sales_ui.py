import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.ttk import Treeview
from sales_data import SalesDataManager
from sales_graphics import plot_sales_data, generate_pdf_report


class SalesUI:
    def __init__(self, root):
        self.root = root
        self.manager = SalesDataManager()
        self.setup_ui()

    def setup_ui(self):
        self.root.title(" Sales Performance Analyzer ")
        self.root.geometry("900x500")
        self.root.configure(bg="#f5f5f5")

        title_label = tk.Label(
            self.root, text="Sales Performance Analyzer", font=("Arial", 18, "bold"), fg="#4CAF50", bg="#f5f5f5"
        )
        title_label.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#f5f5f5")
        button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(button_frame, text="Add Sales Data", command=self.add_sales_data, bg="#4CAF50", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(button_frame, text="Delete Row", command=self.delete_row, bg="#FF0000", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(button_frame, text="Save Data", command=self.save_data, bg="#2196F3", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(button_frame, text="Restore Data", command=self.restore_data, bg="#FF5722", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(button_frame, text="Generate PDF Report", command=self.generate_pdf, bg="#FFC107", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(button_frame, text="Plot Sales Data", command=self.plot_data, bg="#FF5722", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(button_frame, text="Calculate Statistics", command=self.calculate_statistics, bg="#FFC107", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(button_frame, text="Salespersons Exceeding Target", command=self.sales_above_target, bg="#4CAF50", fg="white",
                  font=("Arial", 12), width=25).pack(pady=5)
        tk.Button(button_frame, text="Underperforming Salesperson", command=self.underperforming_sales, bg="#FF5722", fg="white",
                  font=("Arial", 12), width=25).pack(pady=5)
        tk.Button(button_frame, text="Exit", command=self.root.quit, bg="#f44336", fg="white",
                  font=("Arial", 12), width=20).pack(pady=5)

        table_frame = tk.Frame(self.root, bg="#f5f5f5")
        table_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        tk.Label(table_frame, text="Sales Data Overview", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#4CAF50").pack()

        self.sales_table = Treeview(table_frame, columns=("ID", "Sales", "Time"), show="headings", height=6)
        self.sales_table.heading("ID", text="Salesperson ID")
        self.sales_table.heading("Sales", text="Sales Amount")
        self.sales_table.heading("Time", text="Timestamp")
        self.sales_table.pack(fill=tk.BOTH, expand=True)

    def add_sales_data(self):
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Add Sales Data")
        tk.Label(entry_window, text="Enter Salesperson ID:").grid(row=0, column=0, padx=10, pady=10)
        id_entry = tk.Entry(entry_window)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(entry_window, text="Enter Sales Amount:").grid(row=1, column=0, padx=10, pady=10)
        amount_entry = tk.Entry(entry_window)
        amount_entry.grid(row=1, column=1, padx=10, pady=10)

        def submit():
            salesperson_id = id_entry.get().strip()
            sales_amount = amount_entry.get().strip()

            try:
                sales_amount = float(sales_amount)
                if sales_amount <= 0:
                    raise ValueError
            except ValueError:
                self.update_status("Error: Sales Amount must be a positive number.")
                return

            message = self.manager.add_or_update_salesperson(salesperson_id, sales_amount)
            self.update_table()
            self.update_status(message)
            entry_window.destroy()

        tk.Button(entry_window, text="Submit", command=submit, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def delete_row(self):
        selected_item = self.sales_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No row selected!")
            return
        salesperson_id = self.sales_table.item(selected_item, "values")[0]
        message = self.manager.delete_salesperson(salesperson_id)
        self.update_table()
        messagebox.showinfo("Delete Row", message)

    def update_table(self):
        for row in self.sales_table.get_children():
            self.sales_table.delete(row)
        for salesperson_id, sales_amount, timestamp in zip(self.manager.salespersons, self.manager.sales, self.manager.timestamps):
            self.sales_table.insert("", "end", values=(salesperson_id, f"${sales_amount:.2f}", timestamp))

    def save_data(self):
        message = self.manager.save_data_to_file()
        self.update_status(message)

    def restore_data(self):
        message = self.manager.restore_data()
        self.update_table()
        self.update_status(message)

    def calculate_statistics(self):
        stats = self.manager.calculate_statistics()
        if not stats:
            messagebox.showinfo("Statistics", "No sales data available.")
            return
        total, average, max_sales, min_sales = stats
        messagebox.showinfo("Statistics", f"Total: {total}\nAverage: {average}\nMax: {max_sales}\nMin: {min_sales}")

    def plot_data(self):
        plot_sales_data(self.manager.salespersons, self.manager.sales)

    def generate_pdf(self):
        message = generate_pdf_report(self.manager.salespersons, self.manager.sales, self.manager.timestamps)
        messagebox.showinfo("Generate PDF", message)

    def sales_above_target(self):
        target = simpledialog.askfloat("Target Sales", "Enter targeted sales:")
        if target is None:
            return
        count = self.manager.count_sales_above_target(target)
        messagebox.showinfo("Sales Above Target", f"Number of salespersons exceeding target: {count}")

    def underperforming_sales(self):
        target = simpledialog.askfloat("Target Sales", "What is your targeted sales:")
        if target is None:
            return
        underperformers = [
            (salesperson_id, sales_amount)
            for salesperson_id, sales_amount in zip(self.manager.salespersons, self.manager.sales)
            if sales_amount < target
        ]
        if underperformers:
            result = "\n".join(f"ID: {salesperson_id}, Sales: ${sales_amount:.2f}" for salesperson_id, sales_amount in underperformers)
            messagebox.showinfo("Underperforming Salesperson(s)", f"Salespersons below target:\n\n{result}")
        else:
            messagebox.showinfo("Underperforming Salesperson(s)", "All salespersons met or exceeded the target!")

    def update_status(self, message):
        print(message)
