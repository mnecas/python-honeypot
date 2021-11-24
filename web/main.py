from smth import create_app

app = create_app()

from smth import routes

if __name__ == '__main__':
    app.run(debug=True)
