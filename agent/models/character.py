from pydantic import BaseModel
from typing import Literal, Optional


from agent.models.enums import EntityType


class CharacterCreate(BaseModel):
    name: str
    entity_type: EntityType = "character"
    description: Optional[str] = None
    image_prompt: Optional[str] = None
    voice_description: Optional[str] = None  # max ~30 words
    reference_image_url: Optional[str] = None
    media_id: Optional[str] = None



class NativeCharacterCreate(BaseModel):
    project_id: str
    name: str = "Untitled character"


class NativeCharacter(BaseModel):
    project_id: str
    character_id: str


class NativeCharacterPromptCreate(BaseModel):
    project_id: str
    character_id: str
    prompt: str
    model: Literal["NARWHAL"] = "NARWHAL"
    seed: int = 1


class NativeCharacterPrompt(BaseModel):
    project_id: str
    character_id: str
    media_id: str
    workflow_id: str


class NativeCharacterVoiceAttach(BaseModel):
    project_id: str
    character_id: str
    voice_id: str









class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    entity_type: Optional[EntityType] = None
    description: Optional[str] = None
    image_prompt: Optional[str] = None
    voice_description: Optional[str] = None
    reference_image_url: Optional[str] = None
    media_id: Optional[str] = None


class Character(BaseModel):
    id: str
    name: str
    slug: Optional[str] = None
    entity_type: EntityType = "character"
    description: Optional[str] = None
    image_prompt: Optional[str] = None
    voice_description: Optional[str] = None
    reference_image_url: Optional[str] = None
    media_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
