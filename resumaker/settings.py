from json import loads

with open('env.json') as env_file:
    ENV_VAR = loads(env_file.read())
