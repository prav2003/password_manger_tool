
from flask import Flask, request, jsonify
import mysql.connector
from utils.encryption import encrypt_password, decrypt_password
from flask_cors import CORS

fixed_key = b'JbzaiYlw_u8ZOML3HwV7G2xsDfDrxwDwftTU6uo2cjw='

app = Flask(__name__)
CORS(app)

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="127.0.0.1",  # Usually "localhost" if it's on your local machine
    user="root",
    password="12345",
    database="passworddatabase",
)
cursor = conn.cursor()

@app.route('/add-password', methods=['POST'])
def add_password():
    data = request.get_json()
    account = data.get("account")
    username = data.get("username")
    password = data.get("password")

    encrypted_password = encrypt_password(fixed_key, password)
    print(encrypted_password)

    insert_query = """
        INSERT INTO passwords (account, username, encrypted_password)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (account, username, encrypted_password))
    conn.commit()

    return jsonify({"message": "Password added successfully"})


@app.route('/get-password', methods=['GET'])
def get_password():
    account = request.args.get("account")

    select_query = """
        SELECT encrypted_password FROM passwords WHERE account = %s
    """
    cursor.execute(select_query, (account,))
    row = cursor.fetchone()

    if row:
        encrypted_password = row[0]
        decrypted_password = decrypt_password(fixed_key, encrypted_password)
        return jsonify({"message": f"Decrypted password for {account}: {decrypted_password}"})
    else:
        return jsonify({"message": f"No password found for {account}"})


if __name__ == '__main__':
    app.run()
    conn.close()