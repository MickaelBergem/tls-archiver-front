import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from tlsarchiverfront import app


def get_stats():
    """ Return the list of certificates as a list of tuples, starting at the given page """

    engine = sqlalchemy.create_engine(app.config['DB_URL'])
    Session = scoped_session(sessionmaker(bind=engine))

    s = Session()

    results = {}

    # Total number of certificates
    result_proxy = s.execute("SELECT COUNT(*) FROM certificates WHERE NOT failed")
    results['total_certs'] = result_proxy.fetchone()[0]

    # Total number of distinct hosts
    result_proxy = s.execute("SELECT COUNT(DISTINCT host) FROM certificates")
    results['total_hosts'] = result_proxy.fetchone()[0]

    # Total number of distinct IPs
    result_proxy = s.execute("SELECT COUNT(DISTINCT ip) FROM certificates")
    results['unique_ips'] = result_proxy.fetchone()[0]

    s.close()

    return results
