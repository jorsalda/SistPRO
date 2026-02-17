# run.py (sin cambios necesarios si ya funciona)
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

