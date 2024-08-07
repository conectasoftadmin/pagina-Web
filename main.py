from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Parametros para enviar la información
EMAIL = ""
PASSWORD = ""
EMAIL_CONECTASOFT = ""
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    
    # Valida si se debe enviar el correo
    if request.method == "POST":

        # Acá se envía el correo con la notificación a conectasoft
        message_conectasoft = MIMEMultipart()
        message_conectasoft['From'] = EMAIL
        message_conectasoft['To'] = EMAIL_CONECTASOFT
        message_conectasoft['Subject'] = "Nuevo Cliente!!!!"
        body=(f"Nombre: {request.form['firstname']}, {request.form['lastname']}"
              f"\nEmail: {request.form['email']}.\nPhone: {request.form['phone']}"
              f"\nEmpresa: {request.form['company']}\nPais {request.form['country']}"
              f"\nMensaje: {request.form['message']}")
        message_conectasoft.attach(MIMEText(body, 'plain', 'utf-8'))
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, EMAIL_CONECTASOFT, message_conectasoft.as_string())
            server.quit()
        except Exception as e:
            print(f"Error to send the mail")

        # Acá se envía el correo de confirmación al cliente
        message_cliente = MIMEMultipart()
        message_cliente['From'] = EMAIL
        message_cliente['To'] = request.form['email']
        message_cliente['Subject'] = "Conectasoft se comunicara con usted!!!!"
        body=(f"Gracias por comunicarse con nostros \nVamos a validar la información que nos proporcionó y nos estaremos comunicando con usted.")
        message_cliente.attach(MIMEText(body, 'plain', 'utf-8'))
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, request.form['email'], message_cliente.as_string())
            server.quit()
        except Exception as e:
            print(f"Error to send the mail")

        return render_template("index.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)