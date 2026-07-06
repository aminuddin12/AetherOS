from enum import Enum
from pydantic import BaseModel

class RelationshipType(str, Enum):
    # Semantic
    DEPENDS_ON = "DEPENDS_ON"
    USES = "USES"
    IMPLEMENTS = "IMPLEMENTS"
    TESTS = "TESTS"
    PRODUCES = "PRODUCES"
    CONSUMES = "CONSUMES"
    DEPRECATED_BY = "DEPRECATED_BY"
    DOCUMENTS = "DOCUMENTS"
    EXPLAINS = "EXPLAINS"
    REFERENCES = "REFERENCES"
    SUPERSEDES = "SUPERSEDES"
    
    # Lineage
    GENERATED_FROM = "GENERATED_FROM"
    DERIVED_FROM = "DERIVED_FROM"
    IMPORTED_FROM = "IMPORTED_FROM"
    TRANSLATED_FROM = "TRANSLATED_FROM"
    SUMMARIZED_FROM = "SUMMARIZED_FROM"
    MERGED_FROM = "MERGED_FROM"
    FORKED_FROM = "FORKED_FROM"
    INSPIRED_BY = "INSPIRED_BY"

class ArtifactRelationship(BaseModel):
    source_uri: str
    target_uri: str
    relation_type: RelationshipType
