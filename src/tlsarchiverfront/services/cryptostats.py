import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from tlsarchiverfront import app
from tlsarchiverfront.tlsconsts import PROTOCOL_CONSTS, CIPHERSUITE_CONSTS


def get_protocols_stats():
    """ Return the stats about protocols usage """

    engine = sqlalchemy.create_engine(app.config['DB_URL'])
    Session = scoped_session(sessionmaker(bind=engine))

    s = Session()

    results = []

    # Total number of certificates
    result_proxy = s.execute("SELECT protocol, COUNT(*) as total FROM certificates WHERE NOT failed GROUP BY protocol ORDER BY total DESC")

    total_usage = result_proxy.fetchall()

    s.close()

    total_usage_count = sum([row[1] for row in total_usage])

    for protocol, total_usage in total_usage:
        results.append({
            'name': PROTOCOL_CONSTS.get(protocol, "Inconnu"),
            'total_usage': total_usage,
            'total_usage_pc': 100. * total_usage / total_usage_count,
        })

    return results

def get_ciphersuites_stats():
    """ Return the stats about ciphersuites usage """

    engine = sqlalchemy.create_engine(app.config['DB_URL'])
    Session = scoped_session(sessionmaker(bind=engine))

    s = Session()

    results = []

    result_proxy = s.execute("SELECT ciphersuite, COUNT(*) as total FROM certificates WHERE NOT failed GROUP BY ciphersuite ORDER BY total DESC")

    total_usage = result_proxy.fetchall()

    s.close()

    total_usage_count = sum([row[1] for row in total_usage])

    for ciphersuite, total_usage in total_usage:
        results.append({
            'name': CIPHERSUITE_CONSTS.get(ciphersuite, "Inconnu"),
            'total_usage': total_usage,
            'total_usage_pc': 100. * total_usage / total_usage_count,
        })

    return results


def result2dict(result, keys):
    """ Convert a list of values to a dict """
    for row in result:
        row_dict = {}
        for i, key in enumerate(keys):
            row_dict[key] = row[i]
        yield row_dict
