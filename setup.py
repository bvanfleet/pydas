from setuptools import setup

# Adding the dependencies here for GitHub
setup(
    name="pyDAS",
    install_requires=[
        "alembic==1.4.3",
        "blinker==1.4",
        "boto3==1.16.46",
        "dependency-injector==4.27.0",
        "firebase-admin==4.5.1",
        "Flask==1.1.2",
        "Flask-Cors==3.0.8",
        "flask-swagger-ui==3.25.0",
        "google-cloud-firestore==2.0.2",
        "ipfshttpclient==0.7.0a1",
        "mysqlclient==2.0.1",
        "nltk==3.5",
        "requests==2.24.0",
        "SQLAlchemy==1.3.18"
    ]
)
