# sales_data.py
import os
import datetime


class SalesDataManager:
    def __init__(self):
        self.salespersons = []
        self.sales = []
        self.timestamps = []

    def add_or_update_salesperson(self, salesperson_id, sales_amount):
        """
        Adds or updates sales data for a salesperson.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if salesperson_id in self.salespersons:
            index = self.salespersons.index(salesperson_id)
            self.sales[index] += sales_amount
            self.timestamps[index] = timestamp
            return f"Updated sales data for {salesperson_id}. New total: ${self.sales[index]:.2f}"
        else:
            self.salespersons.append(salesperson_id)
            self.sales.append(sales_amount)
            self.timestamps.append(timestamp)
            return f"Added sales data for {salesperson_id} successfully!"

    def delete_salesperson(self, salesperson_id):
        """
        Deletes sales data for a salesperson.
        """
        if salesperson_id in self.salespersons:
            index = self.salespersons.index(salesperson_id)
            del self.salespersons[index]
            del self.sales[index]
            del self.timestamps[index]
            return f"Deleted data for salesperson {salesperson_id}."
        return f"Salesperson ID {salesperson_id} not found."

    def save_data_to_file(self, filename="sales_data.txt"):
        """
        Saves sales data to a file.
        """
        try:
            with open(filename, 'w') as file:
                for salesperson_id, sales_amount, timestamp in zip(self.salespersons, self.sales, self.timestamps):
                    file.write(f"{salesperson_id}, {sales_amount}, {timestamp}\n")
            return f"Data saved to {filename}"
        except Exception as e:
            return f"Error saving data: {e}"

    def restore_data(self, filename="sales_data.txt"):
        """
        Restores sales data from a file.
        """
        if not os.path.exists(filename):
            return f"File '{filename}' does not exist."
        try:
            with open(filename, 'r') as file:
                self.salespersons.clear()
                self.sales.clear()
                self.timestamps.clear()
                for line in file:
                    salesperson_id, sales_amount, timestamp = line.strip().split(", ")
                    self.salespersons.append(salesperson_id)
                    self.sales.append(float(sales_amount))
                    self.timestamps.append(timestamp)
            return f"Data restored from {filename}"
        except Exception as e:
            return f"Error restoring data: {e}"

    def calculate_statistics(self):
        """
        Calculates total, average, maximum, and minimum sales.
        """
        if not self.sales:
            return None
        total = sum(self.sales)
        average = total / len(self.sales)
        max_sales = max(self.sales)
        min_sales = min(self.sales)
        return total, average, max_sales, min_sales

    def count_sales_above_target(self, target):
        """
        Counts the number of salespersons exceeding the target.
        """
        return sum(1 for sale in self.sales if sale > target)
