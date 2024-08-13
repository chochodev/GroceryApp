from website.website_app import run_app

app = run_app()
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=False, host='0.0.0.0')