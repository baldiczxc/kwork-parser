KWORK_URL = "https://kwork.ru/projects"

HEADERS = {
    'sec-ch-ua-platform': '"macOS"',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Origin': 'https://kwork.ru',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'en',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

MESSAGE_TEMPLATE = '''
📌 {title}
<blockquote>{description}</blockquote>
〰️〰️〰️〰️
💳 Бюджет:
От  {price_from} ₽  до {price_to} ₽
〰️〰️〰️〰️
'''