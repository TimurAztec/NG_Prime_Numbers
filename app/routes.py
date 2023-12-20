from io import BytesIO
import os
from matplotlib import image, pyplot as plt
from openpyxl import Workbook
from openpyxl.chart import Reference, PieChart
from openpyxl.drawing.image import Image
from app import app
from flask import render_template, request, send_file, send_from_directory
from typing import List
import concurrent.futures

from app.utils import generate_numbers

@app.route('/', methods=['GET'])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return "ERROR: {}".format(str(e))
    
@app.route('/generateChart', methods=['POST'])
def generateChart():
    try:
        start = int(request.form['start'])
        end = int(request.form['end'])
        filename = f'number_comparison_{start}_{end}.xlsx'
        if os.path.exists(f"static/{filename}"):
            return render_template('result.html', filename=filename, chart_image_url=f'number_comparison_{start}_{end}.png')

        simple_numbers, prime_numbers = generate_numbers(start, end)

        average_simple = sum(simple_numbers) / len(simple_numbers) if simple_numbers else 0
        average_prime = sum(prime_numbers) / len(prime_numbers) if prime_numbers else 0
        total_sum = sum(simple_numbers) + sum(prime_numbers)

        workbook = Workbook()
        sheet = workbook.active
        sheet['A1'] = 'Simple Numbers'
        sheet['B1'] = 'Prime Numbers'

        sheet['D1'] = 'Average of Simple Numbers'
        sheet['E1'] = 'Average of Prime Numbers'
        sheet['F1'] = 'Total Sum'
        sheet['D2'] = average_simple
        sheet['E2'] = average_prime
        sheet['F2'] = total_sum

        def write_numbers_to_column(column, value):
            for i, num in enumerate(value, start=2):
                sheet[f'{column}{i}'] = num

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(write_numbers_to_column("A", simple_numbers), range(start, end + 1))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(write_numbers_to_column("B", prime_numbers), range(start, end + 1))

        labels = ['Simple Numbers', 'Prime Numbers']
        sizes = [len(simple_numbers), len(prime_numbers)]
        colors = ['red', 'green']
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Simple and prime number comparison chart')
        plt.text(0, 0, f'Avg Simple: {round(average_simple)}\nAvg Prime: {round(average_prime)}\nTotal Sum: {round(total_sum)}',
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=6)

        chart_image_url: str = f'number_comparison_{start}_{end}.png'
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.savefig("static/" + chart_image_url)
        plt.close()

        img = Image(image_stream)
        img.anchor = 'D5'
        sheet.add_image(img)

        workbook.save("static/" + filename)

        return render_template('result.html', filename=filename, chart_image_url=chart_image_url)
    except Exception as e:
        return "ERROR: {}".format(str(e))
    
@app.route('/download/<filename>')
def download(filename: str):
    try:
        return send_file("../static/" + filename, as_attachment=True)
    except Exception as e:
        return "ERROR: {}".format(str(e))