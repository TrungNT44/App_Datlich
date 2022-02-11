import json

with open("app/config/config.json") as json_data_file:
    config_obj = json.load(json_data_file)
# secret key for JWT
SECRET = config_obj["secret"]
db_config = config_obj["db"]
# config DB
tns = db_config["tns"]
db_username = db_config["username"]
db_password = db_config["password"]
db_url = 'oracle://{user}:{password}@{sid}'.format(
    user=db_username,
    password=db_password,
    sid=tns
)
db_url = db_url.replace('SID', 'SERVICE_NAME')
access_token_expire_second = config_obj["access_token_expire_second"]
