from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template with shadow border
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #333333;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, button:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
        }
        button {
            background-color: #007bff;
            color: #ffffff;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Group Messenger</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Target Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter target group chat ID" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Login and send messages
@app.route("/", methods=["GET", "POST"])
def instagram_messenger():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            group_id = request.form["group_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Validate and read message file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("instagram_messenger"))

            # Initialize Instagram client
            cl = Client()
            print("[INFO] Logging in...")
            cl.login(username, password)
            print("[SUCCESS] Logged in!")

            # Send messages to group chat
            for message in messages:
                print(f"[INFO] Sending message to group {group_id}: {message}")
                cl.direct_send(message, thread_ids=[group_id])
                print(f"[SUCCESS] Message sent: {message}")
                time.sleep(delay)

            flash("All messages sent successfully!", "success")
            return redirect(url_for("instagram_messenger"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("instagram_messenger"))

    # Render form
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
              