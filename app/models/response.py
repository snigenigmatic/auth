"""Model representing the response after a student's authentication request."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import ProfileModel


class ResponseModel(BaseModel):
    """Model representing the response after a student's authentication request."""

    model_config = ConfigDict(strict=True)

    status: bool = Field(
        ...,
        title="Authentication Status",
        description="Indicates whether the authentication request was successful.",
        json_schema_extra={"example": True},
    )

    message: str = Field(
        ...,
        title="Authentication Message",
        description="A human-readable message providing information about the authentication status.",
        json_schema_extra={"example": "Login successful."},
    )

    timestamp: datetime = Field(
        ...,
        title="Authentication Timestamp",
        description="Timestamp of the authentication attempt with timezone info.",
        json_schema_extra={"example": "2024-07-28T22:30:10.103368+05:30"},
    )

    profile: ProfileModel | None = Field(
        None,
        title="User Profile Data",
        description="The user's profile data returned only if authentication succeeds and profile data was requested.",
    )


class MetricsResponseModel(BaseModel):
    """Model representing the response from the /metrics endpoint."""

    status: bool = Field(
        ...,
        title="Metrics Status",
        description="Indicates whether the metrics were retrieved successfully.",
        json_schema_extra={"example": True},
    )

    message: str = Field(
        ...,
        title="Metrics Message",
        description="A human-readable message providing information about the metrics retrieval.",
        json_schema_extra={"example": "Metrics retrieved successfully"},
    )

    timestamp: datetime = Field(
        ...,
        title="Metrics Timestamp",
        description="Timestamp of the metrics retrieval with timezone info.",
        json_schema_extra={"example": "2025-08-28T15:30:45.123456+05:30"},
    )

    metrics: dict = Field(
        ...,
        title="Metrics Data",
        description="Dictionary containing all current metric counters.",
        json_schema_extra={
            "example": {
                "auth_success_total": 150,
                "auth_failure_total": 12,
                "validation_error_total": 8,
                "pesu_academy_error_total": 5,
                "unhandled_exception_total": 0,
                "csrf_token_error_total": 2,
                "profile_fetch_error_total": 1,
                "profile_parse_error_total": 0,
                "csrf_token_refresh_success_total": 45,
                "csrf_token_refresh_failure_total": 1,
            }
        },
    )
