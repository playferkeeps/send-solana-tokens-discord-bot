from sqlalchemy import create_engine
from dotenv import dotenv_values
config = dotenv_values(".env")
databasehost = config['DATABASE_HOST']
databaseuser = config['DATABASE_USER']
databasename= config['DATABASE_NAME']
databasepw = config['DATABASE_PASSWORD']
engine = create_engine(
    "mysql+pymysql://{}:{}@{}".format(databaseuser,databasepw,databasehost,databasename), 
    connect_args= dict(host="{}".format(databasehost), port=3306), 
    echo=True)
