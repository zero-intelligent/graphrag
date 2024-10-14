# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A module containing 'Finding' and 'CommunityReport' models."""

from collections.abc import Awaitable, Callable
from enum import Enum
from typing import Any

import pyarrow as pa
from datashaper import VerbCallbacks
from typing_extensions import TypedDict

from graphrag.index.cache import PipelineCache

ExtractedEntity = dict[str, Any]
StrategyConfig = dict[str, Any]
RowContext = dict[str, Any]
EntityTypes = list[str]
Claim = dict[str, Any]


class Finding(TypedDict):
    """Finding class definition."""

    summary: str
    explanation: str


class CommunityReport(TypedDict):
    """Community report class definition."""

    community: str | int
    title: str
    summary: str
    full_content: str
    full_content_json: str
    rank: float
    level: int
    rank_explanation: str
    findings: list[Finding]

CommunityReport_schema = pa.schema([
    ("community", pa.string()),  # 可以根据需要调整为 pa.int32() 或 pa.int64()
    ("title", pa.string()),
    ("summary", pa.string()),
    ("full_content", pa.string()),
    ("full_content_json", pa.string()),
    ("rank", pa.float64()),
    ("level", pa.int32()),  # 可以根据具体要求调整
    ("rank_explanation", pa.string()),
    ("findings", pa.list_(pa.map_(pa.string(), pa.string())))  # findings 是一个 list[Finding]，用 list_ 表示
])


CommunityReportsStrategy = Callable[
    [
        str | int,
        str,
        int,
        VerbCallbacks,
        PipelineCache,
        StrategyConfig,
    ],
    Awaitable[CommunityReport | None],
]


class CreateCommunityReportsStrategyType(str, Enum):
    """CreateCommunityReportsStrategyType class definition."""

    graph_intelligence = "graph_intelligence"

    def __repr__(self):
        """Get a string representation."""
        return f'"{self.value}"'
