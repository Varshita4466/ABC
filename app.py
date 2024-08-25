from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

USER_ID = "john_doe_17091999"  

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        try:
            data = request.form.get('data', '[]')
            data = json.loads(data) 

            if not isinstance(data, list):
                raise ValueError("Input data must be a JSON array.")
            
            filter_type = request.form.get('filter_type', 'all')
            min_number = request.form.get('min_number', None)
            max_number = request.form.get('max_number', None)
            only_lowercase = request.form.get('only_lowercase', 'no') == 'yes'
            include_uppercase = request.form.get('include_uppercase', 'no') == 'yes'
            include_digits = request.form.get('include_digits', 'yes') == 'yes'
            exclude_special = request.form.get('exclude_special', 'no') == 'yes'
            filter_char = request.form.get('filter_char', None)
            filter_length = request.form.get('filter_length', None)

            numbers = [str(item) for item in data if isinstance(item, (int, float, str)) and str(item).isdigit()]
            alphabets = [str(item) for item in data if isinstance(item, str) and item.isalpha()]
            special_characters = [str(item) for item in data if isinstance(item, str) and not item.isalnum()]

            if min_number:
                min_number = int(min_number)
                numbers = [num for num in numbers if int(num) >= min_number]
            if max_number:
                max_number = int(max_number)
                numbers = [num for num in numbers if int(num) <= max_number]
            
            if only_lowercase:
                alphabets = [item for item in alphabets if item.islower()]
            if include_uppercase:
                alphabets = [item for item in alphabets if item.isupper() or item.islower()]
            if exclude_special:
                alphabets = [item for item in alphabets if item.isalnum()]

            if filter_char:
                filter_char = filter_char.lower()
                alphabets = [item for item in alphabets if filter_char in item.lower()]
                numbers = [item for item in numbers if filter_char in item]
            if filter_length:
                filter_length = int(filter_length)
                alphabets = [item for item in alphabets if len(item) == filter_length]
                numbers = [item for item in numbers if len(item) == filter_length]

            if filter_type == 'numbers':
                result_data = {"numbers": numbers}
            elif filter_type == 'alphabets':
                result_data = {"alphabets": alphabets}
            elif filter_type == 'combined':
                result_data = {"numbers": numbers, "alphabets": alphabets}
            elif filter_type == 'special_characters':
                result_data = {"special_characters": special_characters}
            else:
                result_data = {
                    "numbers": numbers,
                    "alphabets": alphabets,
                    "special_characters": special_characters
                }

            result = {
                "is_success": True,
                "user_id": USER_ID,
                "email": "john@xyz.com",
                "roll_number": "ABCD123",
                "data": result_data
            }
        except json.JSONDecodeError:
            result = {
                "is_success": False,
                "user_id": USER_ID,
                "error": "Invalid JSON data. Please enter a valid JSON array."
            }
        except Exception as e:
            result = {
                "is_success": False,
                "user_id": USER_ID,
                "error": str(e)
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
