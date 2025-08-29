# sales_graphics.py
from matplotlib import pyplot as plt
from fpdf import FPDF


def plot_sales_data(salespersons, sales):
    """
    Generates a bar chart for sales data.
    """
    if not sales:
        return "No data available to plot."
    plt.bar(salespersons, sales, color="#4CAF50")
    plt.xlabel("Salesperson ID")
    plt.ylabel("Sales Amount")
    plt.title("Sales Performance")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def generate_pdf_report(salespersons, sales, timestamps, filename="sales_report.pdf"):
    """
    Generates a PDF report summarizing sales data.
    """
    if not sales:
        return "No sales data available for report generation."

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Sales Performance Report", 0, 1, "C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(200, 10, "Sales Summary", 0, 1)

    pdf.set_font("Arial", "", 10)
    pdf.ln(10)
    for salesperson_id, sales_amount, timestamp in zip(salespersons, sales, timestamps):
        pdf.cell(100, 10, f"Salesperson ID: {salesperson_id}", 0)
        pdf.cell(100, 10, f"Sales Amount: ${sales_amount:.2f}", 0, 1)

    total = sum(sales)
    average = total / len(sales)
    pdf.ln(10)
    pdf.cell(200, 10, "Statistics Summary", 0, 1)
    pdf.cell(100, 10, f"Total Sales: ${total:.2f}", 0, 1)
    pdf.cell(100, 10, f"Average Sales: ${average:.2f}", 0, 1)
    pdf.cell(100, 10, f"Maximum Sales: ${max(sales):.2f}", 0, 1)
    pdf.cell(100, 10, f"Minimum Sales: ${min(sales):.2f}", 0, 1)

    pdf.output(filename)
    return f"PDF report saved as {filename}"
