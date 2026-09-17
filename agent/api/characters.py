from fastapi import APIRouter, HTTPException
from uuid import UUID
from agent.services.flow_client import get_flow_client
from agent.models.character import (
    Character,
    CharacterCreate,
    CharacterUpdate,
    NativeCharacter,
    NativeCharacterCreate,
    NativeCharacterPromptCreate,
    NativeCharacterPrompt,
    NativeCharacterVoiceAttach,
)
from agent.sdk.persistence.sqlite_repository import SQLiteRepository
from agent.utils.slugify import slugify

router = APIRouter(prefix="/characters", tags=["characters"])


def _get_repo() -> SQLiteRepository:
    return SQLiteRepository()


@router.post("/native", response_model=NativeCharacter)
async def create_native(body: NativeCharacterCreate):
    try:
        project_id = str(UUID(body.project_id))
    except ValueError as exc:
        raise HTTPException(422, "project_id must be a UUID") from exc
    client = get_flow_client()
    if not client.connected:
        raise HTTPException(503, "Extension not connected")
    result = await client.create_native_character(project_id, body.name)
    if result.get("error") or (
        isinstance(result.get("status"), int) and result["status"] >= 400
    ):
        raise HTTPException(
            result.get("status", 502), result.get("error", result.get("data"))
        )
    return result["data"]




@router.post("/native/prompt", response_model=NativeCharacterPrompt)
async def generate_native_prompt(body: NativeCharacterPromptCreate):
    try:
        project_id = str(UUID(body.project_id))
        character_id = str(UUID(body.character_id))
    except ValueError as exc:
        raise HTTPException(
            422, "project_id and character_id must be UUIDs") from exc
    client = get_flow_client()
    if not client.connected:
        raise HTTPException(503, "Extension not connected")
    result = await client.generate_native_character_prompt(
        project_id, character_id, body.prompt, body.model, body.seed)
    if result.get("error") or (
        isinstance(result.get("status"), int) and result["status"] >= 400
    ):
        raise HTTPException(
            result.get("status", 502), result.get("error", result.get("data")))
    return result["data"]


@router.post("/native/voice")
async def attach_native_voice(body: NativeCharacterVoiceAttach):
    try:
        project_id = str(UUID(body.project_id))
        character_id = str(UUID(body.character_id))
    except ValueError as exc:
        raise HTTPException(
            422, "project_id and character_id must be UUIDs") from exc
    client = get_flow_client()
    if not client.connected:
        raise HTTPException(503, "Extension not connected")
    result = await client.attach_native_catalog_voice(
        project_id, character_id, body.voice_id)
    if result.get("error") or (
        isinstance(result.get("status"), int) and result["status"] >= 400
    ):
        raise HTTPException(
            result.get("status", 502), result.get("error", result.get("data")))
    return {"project_id": project_id, "character_id": character_id,
            "voice_id": body.voice_id}




@router.post("", response_model=Character)
async def create(body: CharacterCreate):
    repo = _get_repo()
    return await repo.create_character(**body.model_dump(exclude_none=True))


@router.get("", response_model=list[Character])
async def list_all():
    repo = _get_repo()
    rows = await repo.list("character", order_by="created_at DESC")
    return [repo._row_to_character(r) for r in rows]


@router.get("/{cid}", response_model=Character)
async def get(cid: str):
    repo = _get_repo()
    c = await repo.get_character(cid)
    if not c:
        raise HTTPException(404, "Character not found")
    return c






@router.patch("/{cid}", response_model=Character)
async def update(cid: str, body: CharacterUpdate):
    repo = _get_repo()
    updates = body.model_dump(exclude_unset=True)
    if "name" in updates:
        updates["slug"] = slugify(updates["name"])
    row = await repo.update("character", cid, **updates)
    if not row:
        raise HTTPException(404, "Character not found")
    return repo._row_to_character(row)


@router.delete("/{cid}")
async def delete(cid: str):
    repo = _get_repo()
    if not await repo.delete_character(cid):
        raise HTTPException(404, "Character not found")
    return {"ok": True}
