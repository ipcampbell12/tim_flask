from website import create_app


app = create_app()


# only run app if you run it, not just import it
# otherwise would run on import
if __name__ == '__main__':
    # automatically rerun everytime you make a change to the code
    app.run(debug=True)
