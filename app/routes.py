from io import BytesIO
from matplotlib import image, pyplot as plt
from openpyxl import Workbook
from openpyxl.chart import Reference, PieChart
from openpyxl.drawing.image import Image
from app import app
from flask import render_template, request, send_file, send_from_directory
from typing import List

from app.utils import is_prime

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

        simple_numbers: List[int] = [num for num in range(start, end+1) if num > 1]
        prime_numbers: List[int] = [num for num in simple_numbers if is_prime(num)]

        workbook = Workbook()
        sheet = workbook.active
        sheet['A1'] = 'Simple Numbers'
        sheet['B1'] = 'Prime Numbers'

        for i, num in enumerate(simple_numbers, start=2):
            sheet[f'A{i}'] = num

        for i, num in enumerate(prime_numbers, start=2):
            sheet[f'B{i}'] = num

        labels = ['Simple Numbers', 'Prime Numbers']
        sizes = [len(simple_numbers), len(prime_numbers)]
        colors = ['red', 'green']
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Simple and prime number comparison chart')

        chart_image_url: str = f'number_comparison_{len(simple_numbers)}_{len(prime_numbers)}.png'
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.savefig("static/" + chart_image_url)
        plt.close()

        img = Image(image_stream)
        img.anchor = 'D5'
        sheet.add_image(img)

        filename = f'number_comparison_{start}_{end}.xlsx'
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