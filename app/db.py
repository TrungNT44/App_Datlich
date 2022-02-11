from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
#import app.app_config as config

# engine1 = create_engine(
#     config.db_url,
#     convert_unicode=False,
#     pool_recycle=10,
#     pool_size=50,
#     echo=True
# )
# Ket noi den CSDL Khao sat sinh vien
server = 'DESKTOP-4059RIE\SQLSERVER2019'
database = 'University'
username = 'sa'
password = 'Dell1234'
driver = 'ODBC Driver 17 for SQL Server'
params = urllib.parse.quote_plus("'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password")

Database_con = f'mssql://{username}:{password}@{server}/{database}?driver={driver}'
engine = create_engine(Database_con)
#con = engine.connect()

#data = pd.read_sql_query("select * from dbo.file_khaosat_hd_giangday", con)
#print(data)
#engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
#engine = create_engine('mssql+pyodbc://sa:Dell1234@DESKTOP-4059RIE\SQLSERVER2019?driver=SQL+Server+Native+Client+11.0')
#engine = create_engine('mssql+pyodbc://sa:Dell1234@localhost/University?driver=ODBC+Driver+17+for+SQL+Server')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

