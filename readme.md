# Drawing Mini App Bot - Start guide

This is a simple drawing (like a raffle) bot, that can help manage, participate and draw winners.
The bot code can lead you to understand about how integrate a bot with a mini app (webapp).

This project is built using Python, using @pyTelebramBotAPI library, that runs a Telebram Bot (server side), and Vanilla Javascript to implement a Telegram Mini App (client side).

## Features
Usability:
- Create, manage, participate and draw winners for a drawing raffle.

Learn as a developer:
- How to integrate a Telegram Bot with a Telegram Mini App (webapp)
- Miniframework for server and client side (see this template:)
    - Server side: python bot with pyTelegramBotAPI, as well as a simple CRUD and a miniframework (organize your code in a simple but strong way, using modules and classes, placing your code in the right place)
    - Client side: vanilla javascript, in a very simple "miniframework" to develop a SPA (Single Page Application) like app.

## How to use (setup step-by-step)

1. Deploy webapp directory into a web server or run it locally and use some tunnel service like ngrok to make it https.
    1.1. Ngrok like:
        - to run a localhost server, you can use the following command at webapp directory: `python -m http.server 8080` (change 8080 to the port that you want to use)
        - you can use the following command: `ngrok http 8080` (change 8080 to the port that you are using)
        - it will generate a https url, that you can use to configure your bot.

    or

    1.2. Netlify like:
        - create a account at https://app.netlify.com/
        - upload into netlify and it will generate a https url, that you can use to configure your bot.

    or

    1.3. Use our webapp used in this project:
        - https://drawing-mini-app-bot.netlify.app/

2. Setting variables to the bot:
    2.1. Paste the webapp url into the file `App/Utils/Constants.py` (WEBAPP_URL variable)

    2.2. Create a Telegram Bot using BotFather (https://t.me/botfather)
        2.2.1 Create a bot using BotFather (https://t.me/botfather)
        2.2.2 Copy the bot token
        2.2.3. Paste the bot token into the file `App/Config/config.py` (BOT_TOKEN variable)

    2.3. Create a Telegram Group or Channel and add its id into `App/Utils/Constants.py` (CLOUD_ID variable)
        2.3.1. Remember to add the bot into the group or channel

3. Run the bot using the following command at top directory: `python -m bot.py`



## Understanding the code and some concepts

- Telegram bot will be responsible to receive commands (directly by user or by the webapp) and send messages to the user.
- Telegram webapp will be responsible only to receive data from bot and use it to show to the user anything that is needed.
- **COMUNICATION**:
    - Bot will send data via GET (query string in url) to the webapp. In our case it's sent in a stringified JSON format.
    - Mini App will send data via sendData() function, and bot receives as a user special type of message:
`@bot.message_handler(content_types="web_app_data")
    def answer(msg):`
        - Note that answer() function is called when bot receives a message that fits in filter (content_types="web_app_data")

Having this in mind, you can look at the code and understand how webapp have data from bot and how bot have data from webapp.

### Understanding server miniframework

C:.
├───Components
├───Config
├───Database
├───Utils
└── bot.py

- Components: contains different menus. Like main_menu.py contains a MainMenu class, that is responsible to show the main menu and handle its commands; get_my_drawings.py > GetMyDrawings class: get drawings from user from database, organize into a object like data, and send this stringfied data to webapp by markup_webapp_button() function (App/Utils/markups.py).
- Config: contains config.py file, that contains sensitive data like bot token.
- Database: contains database.py file, that holds DB class, and is responsible to connect to database and execute queries. There are also some common methods to execute CRUD.
    - Like "model" in MVC, Draw.py, fro example, contains a Draw class, that is responsible to hold data from a draw, and also to execute CRUD operations related to a draw.
- Utils: 
    - funcitons.py: some common functions that can be used in any part of the code, like dict_to_url_params().
    - markups.py: contains functions to create markups (like keyboard or inline buttons) to be used in bot messages, as well a function to create a keyboard button that will send data to webapp (or open a webapp with custom data).
    - constants.py: contains some constants that can be used in any part of the code, like WEBAPP_URL, CLOUD_ID, etc.


## License
This project is licensed under the MIT license. See the LICENSE file for more information.