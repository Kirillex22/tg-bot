import requests
import random
import time
import os

from aiogram.types import URLInputFile

from dotenv import load_dotenv
from messages import HELLO_REQUESTS as hello_bank
from messages import ECHO_MESSAGES as phrases
from messages import HELLO_MESSAGE

class TranslatorApiError(Exception):
    pass


class Dialog:
    hello_counter = 0
    start = time.time()


load_dotenv()

def get_recipe(keywords: list, temp="", recipes=list(), k=0) -> list:
    for i in keywords:
        k += 1
        temp += str(i)
        if k != len(keywords):
            temp += "%20"
    response = requests.get(
        f"https://api.edamam.com/api/recipes/v2?type=public&q={temp}&app_id={os.getenv('RECIPE_API_ID')}&app_key="
        f"{os.getenv('RECIPE_API_KEY')}")
    result = response.json()
    if result['hits']:
        for i in result['hits']:
            recipes.append([i['recipe']['label'], i['recipe']['images']['REGULAR']['url'], i['recipe']['url'],
                            i['recipe']['ingredientLines']])
    return recipes


def translator(text: str, language: str, url = os.getenv('TRANSL_URL')) -> str:
    querystring = {"to[0]": language, "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}
    payload = [{"Text": text}]
    headers = {
        "content-tye": "application/json",
        "X-RapidAPI-Key": os.getenv('TRANSL_API_KEY'),
        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers, params=querystring)
    return response.json()[0]['translations'][0]['text']


def message_builder(result: list, ans="", k=0) -> str:
    for i in random.SystemRandom().sample(result, 2):
        ing = ""
        ans += f"<b>{translator(i[0], 'ru')}</b> \n"
        ans += i[2] + "\n"
        ans += "\n" + "<b>Необходимые ингредиенты</b>: " + "\n" + "\n"
        for j in i[3]:
            k += 1
            if k < len(i[3]):
                ing += j + ", "
            else:
                ing += j + "."
        try:
            ans += translator(ing[:len(ing) // 2], "ru")
            ans += translator(ing[len(ing) // 2 - 1:len(ing)], "ru")
        except Exception:
            raise TranslatorApiError('API cannot send correct type of translated ingredients')
        ans += "\n" + "\n"
    return ans


def get_rand_image() -> str:
    req = requests.get(os.getenv('RAND_IMAGE_URL'))
    return req.json()['image']


def image_handler(url: str):
    image = URLInputFile(url)
    return image


def from_old_to_new(arg: int, type_i: str) -> tuple:
    match type_i:
        case "унций(я)":
            return str(2*arg), "столовых ложек(ки)"
        case "фунт(ов)":
            return str(453*arg), "г"
        case "пинт(а)":
            return str(568*arg), "мл"


def hello_builder(message: str) -> str:
    if message in hello_bank:
        if Dialog.hello_counter == 0:
            Dialog.hello_counter += 1
            Dialog.start = time.time()
            return HELLO_MESSAGE
        else:
            if time.time() - Dialog.start > 60:
                Dialog.start = time.time()
                Dialog.hello_counter = 0
                return HELLO_MESSAGE
            else:
                return f"Вы ведь здоровались со мной буквально <b>{int(time.time() - Dialog.start)} сек.</b> назад..."
    else:
        return random.choice(phrases)



