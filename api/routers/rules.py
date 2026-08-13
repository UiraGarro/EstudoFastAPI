from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
from api.database import get_session
from api.models import Race, CharacterClass, Background, Item, Spell
from api.utils.open5e import fetch_races, fetch_classes, fetch_backgrounds, fetch_items, fetch_spells, fetch_race_by_id

router = APIRouter(prefix="/rules", tags=["rules"])


# RAÇAS

@router.get("/races")
async def get_races(session: Session = Depends(get_session)):
    cached = session.exec(select(Race)).all()

    if cached:
        return [{"name": r.name, "id": r.open5e_id} for r in cached]

    try:
        races = await fetch_races()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for race in races:
        db_race = Race(name=race["name"], open5e_id=race["index"])
        session.add(db_race)

    session.commit()
    return races


@router.get("/races/{race_id}")
async def get_race_by_id(race_id: str, session: Session = Depends(get_session)):
    cached = session.exec(select(Race).where(Race.open5e_id == race_id)).first()

    if cached:
        return {"name": cached.name, "id": cached.open5e_id}

    try:
        race = await fetch_race_by_id(race_id)
    except Exception as e:
        raise HTTPException(status_code=404 if "não encontrada" in str(e) else 503, detail=str(e))

    db_race = Race(name=race["name"], open5e_id=race["index"])
    session.add(db_race)
    session.commit()

    return {"name": race["name"], "id": race["index"]}


@router.post("/races/refresh")
async def refresh_races(session: Session = Depends(get_session)):
    all_races = session.exec(select(Race)).all()
    for race in all_races:
        session.delete(race)
    session.commit()

    try:
        races = await fetch_races()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for race in races:
        db_race = Race(name=race["name"], open5e_id=race["index"])
        session.add(db_race)

    session.commit()
    return {"message": "Cache atualizado", "total": len(races)}


# CLASSES

@router.get("/classes")
async def get_classes(session: Session = Depends(get_session)):
    cached = session.exec(select(CharacterClass)).all()

    if cached:
        return [{"name": c.name, "id": c.open5e_id} for c in cached]

    try:
        classes = await fetch_classes()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for cls in classes:
        hit_die = cls.get("hit_die", "d8")
        if isinstance(hit_die, str):
            hit_die_num = int(hit_die.replace("d", ""))
        else:
            hit_die_num = 8

        db_class = CharacterClass(name=cls["name"], open5e_id=cls["index"], hit_die=hit_die_num)
        session.add(db_class)

    session.commit()
    return classes


@router.post("/classes/refresh")
async def refresh_classes(session: Session = Depends(get_session)):
    all_classes = session.exec(select(CharacterClass)).all()
    for cls in all_classes:
        session.delete(cls)
    session.commit()

    try:
        classes = await fetch_classes()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for cls in classes:
        hit_die = cls.get("hit_die", "d8")
        if isinstance(hit_die, str):
            hit_die_num = int(hit_die.replace("d", ""))
        else:
            hit_die_num = 8

        db_class = CharacterClass(name=cls["name"], open5e_id=cls["index"], hit_die=hit_die_num)
        session.add(db_class)

    session.commit()
    return {"message": "Cache atualizado", "total": len(classes)}


# BACKGROUNDS

@router.get("/backgrounds")
async def get_backgrounds(session: Session = Depends(get_session)):
    cached = session.exec(select(Background)).all()

    if cached:
        return [{"name": b.name, "id": b.open5e_id} for b in cached]

    try:
        backgrounds = await fetch_backgrounds()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for bg in backgrounds:
        db_bg = Background(name=bg["name"], open5e_id=bg["index"])
        session.add(db_bg)

    session.commit()
    return backgrounds


@router.post("/backgrounds/refresh")
async def refresh_backgrounds(session: Session = Depends(get_session)):
    all_bgs = session.exec(select(Background)).all()
    for bg in all_bgs:
        session.delete(bg)
    session.commit()

    try:
        backgrounds = await fetch_backgrounds()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for bg in backgrounds:
        db_bg = Background(name=bg["name"], open5e_id=bg["index"])
        session.add(db_bg)

    session.commit()
    return {"message": "Cache atualizado", "total": len(backgrounds)}


# ITENS

@router.get("/items")
async def get_items(session: Session = Depends(get_session)):
    """Busca itens com cache"""
    cached = session.exec(select(Item)).all()

    if cached:
        return [{"name": i.name, "id": i.open5e_id} for i in cached]

    try:
        items = await fetch_items()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for item in items:
        db_item = Item(name=item["name"], open5e_id=item["index"])
        session.add(db_item)

    session.commit()
    return items


@router.post("/items/refresh")
async def refresh_items(session: Session = Depends(get_session)):
    """Força atualização de cache de itens"""
    all_items = session.exec(select(Item)).all()
    for item in all_items:
        session.delete(item)
    session.commit()

    try:
        items = await fetch_items()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for item in items:
        db_item = Item(name=item["name"], open5e_id=item["index"])
        session.add(db_item)

    session.commit()
    return {"message": "Cache atualizado", "total": len(items)}


# MAGIAS

@router.get("/spells")
async def get_spells(character_class: Optional[str] = None, level: Optional[int] = None,session: Session = Depends(get_session)):
    try:
        spells = await fetch_spells(character_class=character_class, level=level)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    for spell in spells:
        db_spell = Spell(
            name=spell["name"],
            open5e_id=spell["index"],
            level=spell.get("level", 0)
        )
        session.add(db_spell)

    session.commit()
    return spells
