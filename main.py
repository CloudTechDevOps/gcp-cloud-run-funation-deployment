from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Cloud Run Demo</title>
        <style>
            body {{
                background: #f5f5f5;
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 80px;
            }}

            .card {{
                width: 700px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,.2);
            }}

            h1 {{
                color: #4285F4;
            }}

            h2 {{
                color: green;
            }}

            table {{
                width:100%;
                border-collapse:collapse;
                margin-top:20px;
            }}

            td,th {{
                border:1px solid #ddd;
                padding:12px;
            }}

            th {{
                background:#4285F4;
                color:white;
            }}

            .footer {{
                margin-top:20px;
                color:gray;
            }}
        </style>
    </head>

    <body>

        <div class="card">

            <h1>🚀 Google Cloud Run</h1>

            <h2>Python Flask Application</h2>

            <table>

                <tr>
                    <th>Application</th>
                    <td>Cloud Run Demo</td>
                </tr>

                <tr>
                    <th>Status</th>
                    <td>Running Successfully ✅</td>
                </tr>

                <tr>
                    <th>Environment</th>
                    <td>{os.getenv("ENVIRONMENT","Development")}</td>
                </tr>

                <tr>
                    <th>Current Time</th>
                    <td>{datetime.now()}</td>
                </tr>

            </table>

            <div class="footer">
                Deployed on Google Cloud Run
            </div>

        </div>

    </body>
    </html>
    """

@app.route("/health")
def health():
    return {
        "status":"Healthy"
    }

if __name__=="__main__":
    port=int(os.environ.get("PORT",8080))
    app.run(host="0.0.0.0",port=port)
