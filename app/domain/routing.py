from dataclasses import dataclass

from app.domain.data import OptionData, TextData


@dataclass
class RoutingRequest:
    input: TextData
    options: list[OptionData]


@dataclass
class RoutingResponse:
    selected_option: OptionData
    is_fallback: bool
