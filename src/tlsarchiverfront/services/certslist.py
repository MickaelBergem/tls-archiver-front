import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from tlsarchiverfront import app
from tlsarchiverfront.tlsconsts import PROTOCOL_CONSTS, CIPHERSUITE_CONSTS


def get_certificates_list(page=0, pagination=20):
    """ Return the list of certificates as a list of tuples, starting at the given page """

    engine = sqlalchemy.create_engine(app.config['DB_URL'])
    Session = scoped_session(sessionmaker(bind=engine))

    s = Session()

    # Execute the request
    result_proxy = s.execute(
        "SELECT id, host, ip, ciphersuite, protocol, failed, failure_error, timestamp"
        " FROM certificates"
        " LIMIT :limit OFFSET :offset",
        {
            'limit': pagination,
            'offset': page*pagination,
        }
    )

    result = result_proxy.fetchall()
    keys = result_proxy.keys()
    s.close()

    return result2dict(result, keys)


def get_hosts_list(page=0, pagination=20):
    """
    Return a dict with:
    - the list of hosts currently processed
    - the list of other hosts, as a list of tuples
    """

    engine = sqlalchemy.create_engine(app.config['DB_URL'])
    Session = scoped_session(sessionmaker(bind=engine))

    ret = {}

    s = Session()

    # Execute the request
    result_proxy = s.execute(
        "SELECT id, host, started_on, finished"
        " FROM hosts"
        " WHERE NOT finished AND started_on IS NOT NULL"
        " ORDER BY started_on ASC",
        {
            'limit': pagination,
            'offset': page*pagination,
        }
    )
    result = result_proxy.fetchall()
    keys = result_proxy.keys()
    ret['processing'] = list(result2dict(result, keys))

    # Execute the request
    result_proxy = s.execute(
        "SELECT id, host, started_on, finished"
        " FROM hosts"
        " WHERE finished OR started_on IS NULL"
        " ORDER BY finished DESC, started_on DESC"
        " LIMIT :limit OFFSET :offset",
        {
            'limit': pagination,
            'offset': page*pagination,
        }
    )
    result = result_proxy.fetchall()
    keys = result_proxy.keys()
    ret['others'] = result2dict(result, keys)

    s.close()

    return ret


def result2dict(result, keys):
    """ Convert a list of values to a dict """
    for row in result:
        row_dict = {}
        for i, key in enumerate(keys):
            if key == 'protocol':
                row_dict[key] = PROTOCOL_CONSTS.get(row[i], "Unknown: {}".format(row[i]))
            elif key == 'ciphersuite':
                row_dict[key] = CIPHERSUITE_CONSTS.get(row[i], "Unknown: {}".format(row[i]))
            else:
                row_dict[key] = row[i]
        yield row_dict
