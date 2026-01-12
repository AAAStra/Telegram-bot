import requests
import json
import asyncio
import config

HEADERS = {
    'X-Key': f'Key {config.API_KEY}',
    'X-Secret': f'Secret {config.SECRET_KEY}',
}

URL = "https://api.fusionbrain.ai/"

async def generate(prompt):
    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {
            "query": prompt
        }
    }

    files = {
        'model_id': (None, '4'),
        'params': (None, json.dumps(params), 'application/json')
    }

    response = requests.post(
        URL + 'key/api/v1/text2image/run',
        headers=HEADERS,
        files=files
    )

    # 🔍 Диагностика, чтобы видеть реальные ошибки
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    if response.status_code != 200:
        print("FusionBrain error:", response.status_code, response.text)
        return None

    try:
        data = response.json()
    except Exception as e:
        print("JSON parse error:", e)
        print("Response text:", response.text)
        return None

    attempts = 40
    while attempts > 0:
        response = requests.get(
            URL + 'key/api/v1/text2image/status/' + data["uuid"],
            headers=HEADERS
        )

        print("STATUS CHECK:", response.status_code)
        print("TEXT CHECK:", response.text)

        data = response.json()

        if data['status'] == 'DONE':
            return data['images']

        attempts -= 1
        await asyncio.sleep(3)

    return None
