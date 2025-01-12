import uuid
from dataclasses import dataclass
from typing import Optional

from app.domain.data import TextData


@dataclass
class GenerationOptions:
    use_memory: bool
    response_json_schema: Optional[str] = None


@dataclass
class GenerationRequest:
    input: TextData
    options: GenerationOptions
    context_id: uuid


@dataclass
class GenerationResponse:
    generated_output: TextData
