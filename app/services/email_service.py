# services/email_service.py
import os
import resend
from flask import url_for  # ✅ IMPORT CORRECTO

resend.api_key = os.getenv("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")

def send_reset_email(email, token):
    reset_url = url_for("auth.reset_password", token=token, _external=True)

    print("🔐 RESET PASSWORD LINK:")
    print(reset_url)

    # SOLO enviar si es tu email (limitación Resend Free)
    if email != "jorsalda@gmail.com":
        print("⚠️ Resend Free: correo no enviado a", email)
        return None

    response = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": ["jorsalda@gmail.com"],
        "subject": "Recuperación de contraseña - TEST",
        "html": f"<a href='{reset_url}'>Restablecer contraseña</a>"
    })

    return response



