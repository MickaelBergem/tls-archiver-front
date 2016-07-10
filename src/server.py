from tlsarchiverfront import app as application


if __name__ == '__main__':
    if application.debug:
        application.run(debug=True)
    else:
        application.run(host='0.0.0.0')
