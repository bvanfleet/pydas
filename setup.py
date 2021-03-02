from collections import defaultdict
from setuptools import setup


def get_extra_requires(path, add_all=True):
    """
    Get additional installation requirements from an external requirements.txt file.

    Note: This code was taken from Han Xiao
    https://hanxiao.io/2019/11/07/A-Better-Practice-for-Managing-extras-require-Dependencies-in-Python/
    """
    with open(path) as fp:
        extra_deps = defaultdict(set)
        for k in fp:
            if k.strip() and not k.startswith('#'):
                tags = set()
                if ':' in k:
                    k, v = k.split(':')
                    tags.update(vv.strip() for vv in v.split(','))
                for t in tags:
                    extra_deps[t].add(k)

        # add tag `all` at the end
        if add_all:
            extra_deps['all'] = {vv for v in extra_deps.values() for vv in v}

    return extra_deps


# Adding the dependencies here for GitHub
setup(
    name="pyDAS",
    install_requires=[
        "alembic==1.4.3",
        "blinker==1.4",
        "dependency-injector==4.27.0",
        "Flask==1.1.2",
        "Flask-Cors==3.0.8",
        "flask-swagger-ui==3.25.0",
        "requests==2.24.0",
        "SQLAlchemy==1.3.18"
    ],
    extras_require=get_extra_requires('extra-requirements.txt')
)
