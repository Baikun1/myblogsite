from django.shortcuts import render
import json, base64,markdown, re, random, string, csv, csv, re, socket, random
from pytz import timezone, all_timezones
from urllib.parse import quote, unquote
from io import StringIO
import numpy as np
from datetime import datetime
def home(request):
    tools = [
        {'name': 'Color Palette Generator', 'url': 'color_palette_generator', 'icon': 'fas fa-palette'},
        {'name': 'Matrix Determinant', 'url': 'matrix_determinant', 'icon': 'fas fa-th'},
        {'name': 'Text Summarizer', 'url': 'text_summarizer', 'icon': 'fas fa-file-alt'},
        {'name': 'DNS Lookup', 'url': 'dns_lookup', 'icon': 'fas fa-globe'},
        {'name': 'IP Validator', 'url': 'ip_validator', 'icon': 'fas fa-check-circle'},
        {'name': 'Currency Converter', 'url': 'currency_converter', 'icon': 'fas fa-money-bill'},
        {'name': 'Length Converter', 'url': 'length_converter', 'icon': 'fas fa-ruler'},
        {'name': 'Caesar Cipher', 'url': 'caesar_cipher', 'icon': 'fas fa-lock'},
        {'name': 'Temperature Converter', 'url': 'temperature_converter', 'icon': 'fas fa-thermometer-half'},
        {'name': 'JSON to CSV', 'url': 'json_to_csv', 'icon': 'fas fa-file-csv'},
        {'name': 'CSV to JSON', 'url': 'csv_to_json', 'icon': 'fas fa-file-json'},
        {'name': 'Anagram Checker', 'url': 'anagram_checker', 'icon': 'fas fa-swap'},
        {'name': 'URL Tool', 'url': 'url_tool', 'icon': 'fas fa-link'},
        {'name': 'Password Generator', 'url': 'password_generator', 'icon': 'fas fa-key'},
        {'name': 'Joke Generator', 'url': 'joke_generator', 'icon': 'fas fa-laugh'},
        {'name': 'Math Quiz', 'url': 'math_quiz', 'icon': 'fas fa-question'},
        {'name': 'Periodic Table', 'url': 'periodic_table', 'icon': 'fas fa-atom'},
        {'name': 'Timezone Converter', 'url': 'timezone_converter', 'icon': 'fas fa-clock'},
        {'name': 'Countdown Timer', 'url': 'countdown_timer', 'icon': 'fas fa-hourglass-half'},
        {'name': 'Regex Tester', 'url': 'regex_tester', 'icon': 'fas fa-search'},
        {'name': 'Markdown Previewer', 'url': 'markdown_previewer', 'icon': 'fas fa-file-alt'},
        {'name': 'Base64 Tool', 'url': 'base64_tool', 'icon': 'fas fa-code'},
        {'name': 'Unit Converter', 'url': 'unit_converter', 'icon': 'fas fa-ruler-combined'},
        {'name': 'Age Calculator', 'url': 'age_calculator', 'icon': 'fas fa-calendar-alt'},
        {'name': 'BMI Calculator', 'url': 'bmi_calculator', 'icon': 'fas fa-weight'},
        {'name': 'Loan Calculator', 'url': 'loan_calculator', 'icon': 'fas fa-calculator'},
        {'name': 'Text Counter', 'url': 'text_counter', 'icon': 'fas fa-file-alt'},
        {'name': 'Case Converter', 'url': 'case_converter', 'icon': 'fas fa-font'},
        {'name': 'Palindrome Checker', 'url': 'palindrome_checker', 'icon': 'fas fa-check'},
        {'name': 'Basic Calculator', 'url': 'basic_calculator', 'icon': 'fas fa-calculator'},
        {'name': 'Prime Checker', 'url': 'prime_checker', 'icon': 'fas fa-check-circle'},
        {'name': 'JSON Formatter', 'url': 'json_formatter', 'icon': 'fas fa-file-json'},
    ]
    return render(request, 'tools/home.html', {'tools': tools})

def color_palette_generator(request):
    palette = None
    if request.method == "POST":
        palette = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(5)]

    return render(request, 'tools/color_palette_generator.html', {'palette': palette})


def matrix_determinant(request):
    result = None
    error = None
    if request.method == "POST":
        matrix_data = request.POST.get("matrix_data", "")  # Example input: "1,2;3,4"
        try:
            matrix = np.array([[float(num) for num in row.split(",")] for row in matrix_data.split(";")])
            result = np.linalg.det(matrix)
        except Exception:
            error = "Invalid matrix input!"

    return render(request, 'tools/matrix_determinant.html', {'result': result, 'error': error})

def text_summarizer(request):
    summary = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        word_limit = int(request.POST.get("word_limit", 50))

        words = text.split()
        summary = ' '.join(words[:word_limit])

    return render(request, 'tools/text_summarizer.html', {'summary': summary})

def dns_lookup(request):
    ip_address = None
    error = None
    if request.method == "POST":
        domain = request.POST.get("domain", "")
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            error = "Invalid domain name!"

    return render(request, 'tools/dns_lookup.html', {'ip_address': ip_address, 'error': error})


def ip_validator(request):
    is_valid = None
    if request.method == "POST":
        ip_address = request.POST.get("ip_address", "")
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        is_valid = bool(re.match(pattern, ip_address))

    return render(request, 'tools/ip_validator.html', {'is_valid': is_valid})

def currency_converter(request):
    result = None
    if request.method == "POST":
        value = float(request.POST.get("value", 0))
        from_currency = request.POST.get("from_currency")
        to_currency = request.POST.get("to_currency")

        conversion_rates = {
            "USD": 1,
            "EUR": 0.85,
            "INR": 74.5,
            "GBP": 0.75,
        }

        if from_currency in conversion_rates and to_currency in conversion_rates:
            result = value * conversion_rates[to_currency] / conversion_rates[from_currency]

    return render(request, 'tools/currency_converter.html', {'result': result})


def length_converter(request):
    result = None
    if request.method == "POST":
        value = float(request.POST.get("value", 0))
        from_unit = request.POST.get("from_unit")
        to_unit = request.POST.get("to_unit")

        conversion_rates = {
            "meters": 1,
            "kilometers": 0.001,
            "miles": 0.000621371,
            "feet": 3.28084,
        }

        if from_unit in conversion_rates and to_unit in conversion_rates:
            result = value * conversion_rates[to_unit] / conversion_rates[from_unit]

    return render(request, 'tools/length_converter.html', {'result': result})

def caesar_cipher(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        shift = int(request.POST.get("shift", 0))
        operation = request.POST.get("operation")

        if operation == "encode":
            result = ''.join(chr((ord(char) - 97 + shift) % 26 + 97) if char.isalpha() else char for char in text.lower())
        elif operation == "decode":
            result = ''.join(chr((ord(char) - 97 - shift) % 26 + 97) if char.isalpha() else char for char in text.lower())

    return render(request, 'tools/caesar_cipher.html', {'result': result})

def temperature_converter(request):
    result = None
    if request.method == "POST":
        value = float(request.POST.get("value", 0))
        conversion_type = request.POST.get("conversion_type")

        if conversion_type == "CtoF":
            result = (value * 9/5) + 32
        elif conversion_type == "FtoC":
            result = (value - 32) * 5/9

    return render(request, 'tools/temperature_converter.html', {'result': result})


def json_to_csv(request):
    result = None
    error = None
    if request.method == "POST":
        json_data = request.POST.get("json_data", "")
        try:
            data = json.loads(json_data)
            if isinstance(data, list):
                output = StringIO()
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                result = output.getvalue()
            else:
                error = "JSON should be an array of objects!"
        except Exception:
            error = "Invalid JSON format!"

    return render(request, 'tools/json_to_csv.html', {'result': result, 'error': error})


def csv_to_json(request):
    result = None
    error = None
    if request.method == "POST":
        csv_data = request.POST.get("csv_data", "")
        try:
            csv_file = StringIO(csv_data)
            reader = csv.DictReader(csv_file)
            result = json.dumps([row for row in reader], indent=4)
        except Exception:
            error = "Invalid CSV format!"

    return render(request, 'tools/csv_to_json.html', {'result': result, 'error': error})


def anagram_checker(request):
    is_anagram = None
    if request.method == "POST":
        text1 = request.POST.get("text1", "").replace(" ", "").lower()
        text2 = request.POST.get("text2", "").replace(" ", "").lower()
        is_anagram = sorted(text1) == sorted(text2)

    return render(request, 'tools/anagram_checker.html', {'is_anagram': is_anagram})


def url_tool(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        operation = request.POST.get("operation")

        if operation == "encode":
            result = quote(text)
        elif operation == "decode":
            result = unquote(text)

    return render(request, 'tools/url_tool.html', {'result': result})


def password_generator(request):
    password = None
    if request.method == "POST":
        length = int(request.POST.get("length", 8))
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choices(characters, k=length))

    return render(request, 'tools/password_generator.html', {'password': password})


def joke_generator(request):
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the math book look sad? Because it had too many problems.",
        # Add more jokes...
    ]
    joke = random.choice(jokes)
    return render(request, 'tools/joke_generator.html', {'joke': joke})

def math_quiz(request):
    question = None
    answer = None
    result = None
    if request.method == "POST":
        user_answer = request.POST.get("user_answer")
        correct_answer = request.POST.get("correct_answer")

        if user_answer and correct_answer:
            result = "tools/Correct!" if int(user_answer) == int(correct_answer) else "Incorrect!"

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(["+", "-", "*"])
    question = f"{num1} {operation} {num2}"
    answer = eval(question)

    return render(request, 'tools/math_quiz.html', {'question': question, 'answer': answer, 'result': result})


def periodic_table(request):
    elements = [
        {"name": "Hydrogen", "symbol": "H", "atomic_number": 1},
        {"name": "Helium", "symbol": "He", "atomic_number": 2},
        # Add more elements...
    ]
    return render(request, 'tools/periodic_table.html', {'elements': elements})


def timezone_converter(request):
    converted_time = None
    error = None
    if request.method == "POST":
        from_tz = request.POST.get("from_tz")
        to_tz = request.POST.get("to_tz")
        time_string = request.POST.get("time")  # Format: YYYY-MM-DD HH:MM

        try:
            from_zone = timezone(from_tz)
            to_zone = timezone(to_tz)
            naive_time = datetime.strptime(time_string, "%Y-%m-%d %H:%M")
            from_time = from_zone.localize(naive_time)
            converted_time = from_time.astimezone(to_zone)
        except Exception:
            error = "Invalid input or time zone!"

    return render(request, 'tools/timezone_converter.html', {'converted_time': converted_time, 'error': error, 'timezones': all_timezones})


def countdown_timer(request):
    remaining_time = None
    if request.method == "POST":
        target_date = request.POST.get("target_date")  # Format: YYYY-MM-DD HH:MM
        if target_date:
            target_datetime = datetime.strptime(target_date, "%Y-%m-%d %H:%M")
            now = datetime.now()
            remaining_time = target_datetime - now

    return render(request, 'tools/countdown_timer.html', {'remaining_time': remaining_time})


def regex_tester(request):
    matches = None
    error = None
    if request.method == "POST":
        pattern = request.POST.get("pattern", "")
        test_string = request.POST.get("test_string", "")

        try:
            matches = re.findall(pattern, test_string)
        except re.error:
            error = "Invalid regex pattern!"

    return render(request, 'tools/regex_tester.html', {'matches': matches, 'error': error})


def markdown_previewer(request):
    html_content = None
    if request.method == "POST":
        markdown_text = request.POST.get("markdown_text", "")
        html_content = markdown.markdown(markdown_text)

    return render(request, 'tools/markdown_previewer.html', {'html_content': html_content})

def base64_tool(request):
    result = None
    error = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        operation = request.POST.get("operation")

        try:
            if operation == "encode":
                result = base64.b64encode(text.encode()).decode()
            elif operation == "decode":
                result = base64.b64decode(text.encode()).decode()
        except Exception:
            error = "Invalid input for Base64 decoding!"

    return render(request, 'tools/base64_tool.html', {'result': result, 'error': error})



def unit_converter(request):
    result = None
    if request.method == "POST":
        value = float(request.POST.get("value", 0))
        unit_from = request.POST.get("unit_from")
        unit_to = request.POST.get("unit_to")

        conversion_factors = {
            ("meters", "kilometers"): 0.001,
            ("kilometers", "meters"): 1000,
            ("grams", "kilograms"): 0.001,
            ("kilograms", "grams"): 1000,
        }
        factor = conversion_factors.get((unit_from, unit_to))
        if factor:
            result = value * factor
        else:
            result = "Invalid Conversion"

    return render(request, 'tools/unit_converter.html', {'result': result})

def currency_converter(request):
    result = None
    rates = {"USD": 1, "INR": 74.5, "EUR": 0.85}  # Example rates
    if request.method == "POST":
        amount = float(request.POST.get("amount", 0))
        from_currency = request.POST.get("from_currency")
        to_currency = request.POST.get("to_currency")

        if from_currency in rates and to_currency in rates:
            result = amount * (rates[to_currency] / rates[from_currency])
        else:
            result = "Invalid Currency"

    return render(request, 'tools/currency_converter.html', {'result': result})

from datetime import date

def age_calculator(request):
    age = None
    if request.method == "POST":
        dob = request.POST.get("dob")  # Format: YYYY-MM-DD
        if dob:
            dob_date = date.fromisoformat(dob)
            today = date.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

    return render(request, 'tools/age_calculator.html', {'age': age})

def bmi_calculator(request):
    bmi = None
    category = None
    if request.method == "POST":
        weight = float(request.POST.get("weight", 0))
        height = float(request.POST.get("height", 1))
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 24.9:
            category = "Normal weight"
        elif bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

    return render(request, 'tools/bmi_calculator.html', {'bmi': bmi, 'category': category})

def loan_calculator(request):
    emi = None
    if request.method == "POST":
        principal = float(request.POST.get("principal", 0))
        rate = float(request.POST.get("rate", 0)) / 100 / 12
        tenure = int(request.POST.get("tenure", 1)) * 12

        emi = (principal * rate * (1 + rate) ** tenure) / ((1 + rate) ** tenure - 1)

    return render(request, 'tools/loan_calculator.html', {'emi': emi})

def text_counter(request):
    word_count = 0
    char_count = 0
    if request.method == "POST":
        text = request.POST.get("text", "")
        word_count = len(text.split())
        char_count = len(text)

    return render(request, 'tools/text_counter.html', {'word_count': word_count, 'char_count': char_count})

def case_converter(request):
    converted_text = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        case_type = request.POST.get("case_type")

        if case_type == "upper":
            converted_text = text.upper()
        elif case_type == "lower":
            converted_text = text.lower()
        elif case_type == "title":
            converted_text = text.title()

    return render(request, 'tools/case_converter.html', {'converted_text': converted_text})

def palindrome_checker(request):
    is_palindrome = None
    if request.method == "POST":
        text = request.POST.get("text", "").replace(" ", "").lower()
        is_palindrome = text == text[::-1]

    return render(request, 'tools/palindrome_checker.html', {'is_palindrome': is_palindrome})

def basic_calculator(request):
    result = None
    if request.method == "POST":
        num1 = float(request.POST.get("num1", 0))
        num2 = float(request.POST.get("num2", 0))
        operation = request.POST.get("operation")

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide" and num2 != 0:
            result = num1 / num2

    return render(request, 'tools/basic_calculator.html', {'result': result})

def prime_checker(request):
    is_prime = None
    if request.method == "POST":
        num = int(request.POST.get("num", 0))
        is_prime = all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)) and num > 1

    return render(request, 'tools/prime_checker.html', {'is_prime': is_prime})


def json_formatter(request):
    formatted_json = None
    error = None
    if request.method == "POST":
        raw_json = request.POST.get("json_data", "")
        try:
            parsed = json.loads(raw_json)
            formatted_json = json.dumps(parsed, indent=4)
        except json.JSONDecodeError:
            error = "Invalid JSON format!"

    return render(request, 'tools/json_formatter.html', {'formatted_json': formatted_json, 'error': error})
