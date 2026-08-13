import httpx
from typing import List, Dict, Optional

BASE_URL = "https://api.open5e.com/v2"


async def fetch_races() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/races/", timeout=5.0)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar raças (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à Open5e")

        except httpx.HTTPStatusError as e:
            raise Exception(f"Open5e retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar raças: {e}")


async def fetch_classes() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/classes/", timeout=5.0)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar classes (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à Open5e")

        except httpx.HTTPStatusError as e:
            raise Exception(f"Open5e retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar classes: {e}")


async def fetch_backgrounds() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/backgrounds/", timeout=5.0)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar antecedentes (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à Open5e")

        except httpx.HTTPStatusError as e:
            raise Exception(f"Open5e retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar antecedentes: {e}")


async def fetch_spells(character_class: Optional[str] = None, level: Optional[int] = None) -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            params = {}
            if character_class:
                params["classes__name"] = character_class
            if level is not None:
                params["level"] = level

            response = await client.get(
                f"{BASE_URL}/spells/",
                params=params,
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar magias (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à Open5e")

        except httpx.HTTPStatusError as e:
            raise Exception(f"Open5e retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar magias: {e}")


async def fetch_items() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/items/", timeout=5.0)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar itens (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à Open5e")

        except httpx.HTTPStatusError as e:
            raise Exception(f"Open5e retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar itens: {e}")


async def fetch_race_by_id(race_id: str) -> Dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/races/{race_id}/",
                timeout=5.0
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise Exception(f"Raça '{race_id}' não encontrada")
            raise Exception(f"Erro {e.response.status_code}")

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar raça (>5s)")

        except Exception as e:
            raise Exception(f"Erro ao buscar raça: {e}")
