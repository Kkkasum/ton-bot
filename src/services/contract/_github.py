import aiohttp
import base64


async def get_code_from_file(username: str, repo: str, filename: str, token: str) -> str | None:
    url = f'https://api.github.com/repos/{username}/{repo}/contents/{filename}'
    headers = {
        'Autorization': f'token {token}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            if resp.status != 200:
                return

            res = await resp.json()

            content_bytes = base64.b64decode(res['content'])
            content = content_bytes.decode('utf-8')

    return content
