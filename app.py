import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Precompile regex patterns
TOKEN_SPECIFICATION = [
    ('NUMBER', re.compile(r'\d+(\.\d*)?')),  # Integer or decimal number
    ('ASSIGN', re.compile(r'=')),  # Assignment operator
    ('END', re.compile(r';')),  # Statement terminator
    ('ID', re.compile(r'[A-Za-z_][A-Za-z0-9_]*')),  # Identifiers
    ('OP', re.compile(r'[+\-*/]')),  # Arithmetic operators
    ('LPAREN', re.compile(r'\(')),  # Left parenthesis
    ('RPAREN', re.compile(r'\)')),  # Right parenthesis
    ('WHITESPACE', re.compile(r'\s+')),  # Skip whitespace
]

KEYWORDS = {"if", "else", "while", "return", "int", "float", "char"}

def tokenize(code):
    tokens = []
    index = 0
    while index < len(code):
        match = None
        for token_type, pattern in TOKEN_SPECIFICATION:
            match = pattern.match(code, index)
            if match:
                value = match.group(0)
                if token_type == 'WHITESPACE':  # Skip whitespace
                    index += len(value)
                    break
                elif token_type == 'ID' and value in KEYWORDS:
                    token_type = 'KEYWORD'
                tokens.append((token_type, value))
                index += len(value)
                break
        if not match:
           return jsonify({"error": f'Unexpected character: {code[index]} at index {index}'}), 400

    return tokens

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tokenize', methods=['POST'])
def tokenize_code():
    code = request.form.get('code', '')
    tokens = tokenize(code)
    return jsonify(tokens)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
