from ._github import get_code_from_file
from src.common import config


class Contract:
    def __init__(self, token):
        self.token = token

    async def get_contract_code(self, username: str, repo: str, filename: str) -> str:
        code = await get_code_from_file(username, repo, filename, self.token)

        return code

    async def get_jetton_minter_contract(self) -> str:
        code = await self.get_contract_code(
            username='ton-blockchain',
            repo='token-contract',
            filename='ft/jetton-minter.fc'
        )

        return code


contract = Contract(token=config.GITHUB_API_KEY)
