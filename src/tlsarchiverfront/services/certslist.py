import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from tlsarchiverfront import app


def get_certificates_list(page=0, pagination=20):
    """ Return the list of certificates as a list of tuples, starting at the given page """

    engine = sqlalchemy.create_engine(app.config['DB_URL'])
    Session = scoped_session(sessionmaker(bind=engine))

    s = Session()

    # Execute the request
    result_proxy = s.execute(
        "SELECT id, host, ip, ciphersuite, protocol, failed, failure_error, timestamp FROM certificates LIMIT :limit OFFSET :offset",
        {
            'limit': pagination,
            'offset': page*pagination,
        }
    )

    result = result_proxy.fetchall()

    keys = result_proxy.keys()

    s.close()

    return result2dict(result, keys)


def result2dict(result, keys):
    """ Convert a list of values to a dict """
    for row in result:
        row_dict = {}
        for i, key in enumerate(keys):
            row_dict[key] = row[i]
        yield row_dict
