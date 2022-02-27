import json

with open("app/config/config.json") as json_data_file:
    config_obj = json.load(json_data_file)
# secret key for JWT
SECRET_KEY = config_obj["secret"]
ALGORITHM = config_obj["ALGORITHM"]
db_config = config_obj["db"]
# config DB
db_server = db_config["db_server"]
db_username = db_config["username"]
db_password = db_config["password"]

ACCESS_TOKEN_EXPIRE_MINUTES = config_obj["ACCESS_TOKEN_EXPIRE_MINUTES"]
