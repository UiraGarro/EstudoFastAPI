import httpx
from typing import List, Dict, Optional

BASE_URL = "https://www.dnd5eapi.co/api/2014"


async def fetch_races() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/races", timeout=5.0)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            return [
                {
                    "index": r.get("index"),
                    "name": r.get("name"),
                    "description": r.get("desc", "")
                }
                for r in results
            ]

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar raças (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à D&D 5e API")

        except httpx.HTTPStatusError as e:
            raise Exception(f"D&D 5e API retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar raças: {e}")


async def fetch_classes() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/classes", timeout=5.0)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            return [
                {
                    "index": c.get("index"),
                    "name": c.get("name"),
                    "hit_die": c.get("hit_die", 8)
                }
                for c in results
            ]

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar classes (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à D&D 5e API")

        except httpx.HTTPStatusError as e:
            raise Exception(f"D&D 5e API retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar classes: {e}")


async def fetch_backgrounds() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/backgrounds", timeout=5.0)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            return [
                {
                    "index": b.get("index"),
                    "name": b.get("name"),
                    "description": b.get("desc", "")
                }
                for b in results
            ]

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar antecedentes (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à D&D 5e API")

        except httpx.HTTPStatusError as e:
            raise Exception(f"D&D 5e API retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar antecedentes: {e}")


async def fetch_spells(
    character_class: Optional[str] = None,
    level: Optional[int] = None
) -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/spells", timeout=5.0)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            spells = [
                {
                    "index": s.get("index"),
                    "name": s.get("name"),
                    "level": s.get("level", 0),
                    "description": s.get("desc", "")
                }
                for s in results
            ]

            if level is not None:
                spells = [s for s in spells if s.get("level") == level]

            return spells

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar magias (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à D&D 5e API")

        except httpx.HTTPStatusError as e:
            raise Exception(f"D&D 5e API retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar magias: {e}")


async def fetch_items() -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/equipment", timeout=5.0)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            return [
                {
                    "index": i.get("index"),
                    "name": i.get("name"),
                    "description": i.get("desc", "")
                }
                for i in results
            ]

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar itens (>5s)")

        except httpx.ConnectError:
            raise Exception("Não conseguiu conectar à D&D 5e API")

        except httpx.HTTPStatusError as e:
            raise Exception(f"D&D 5e API retornou erro: {e.response.status_code}")

        except Exception as e:
            raise Exception(f"Erro ao buscar itens: {e}")


async def fetch_race_by_id(race_id: str) -> Dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/races/{race_id}",
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()

            return {
                "index": data.get("index"),
                "name": data.get("name"),
                "description": data.get("desc", "")
            }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise Exception(f"Raça '{race_id}' não encontrada")
            raise Exception(f"Erro {e.response.status_code}")

        except httpx.TimeoutException:
            raise Exception("Timeout ao buscar raça (>5s)")

        except Exception as e:
            raise Exception(f"Erro ao buscar raça: {e}")
