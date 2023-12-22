# NG_Prime_Numbers

## Overview

The NG_Prime_Numbers is a Python application that generates statistical information for numbers within a specified range. The program outputs the statistics in an .xlsx file, providing a convenient way to analyze and visualize numerical data.

## Features

- **Input Range:** Specify the range of numbers to analyze.
- **Statistics Generated:** The program calculates various statistics, including simple numbers, prime numbers, and Fibonacci numbers.
- **Output Format:** The results are exported to an .xlsx file for easy viewing and further analysis.
- **User-Friendly:** Simple and easy-to-use web interface.

## Requirements

- Python 3.x
- Required Python packages: `openpyxl`, `flask`, `python-dotenv`, `SQLAlchemy`

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/TimurAztec/NG_Prime_Numbers.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd NG_Prime_Numbers
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the program:**

    ```bash
    python .
    ```

5. **Go to specified localhost port in your preffered web browser (http://127.0.0.1:8080 by default)**

## Example

Suppose you want to analyze numbers in the range from 1 to 100. Running the program will create an .xlsx file (`number_comparison_[range].xlsx`) containing statistics for simple numbers, prime numbers, and Fibonacci numbers within that range.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to contribute and enhance the functionality! If you encounter any issues or have suggestions for improvement, please open an issue or create a pull request.

Happy analyzing!
