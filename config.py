from dotenv import dotenv_values
env = dotenv_values('.env')

settings = {
    'token': env["BOT_TOKEN"],
    'bot': 'Стёпка',
    'id': 8304,
    'prefix': '$'
}
