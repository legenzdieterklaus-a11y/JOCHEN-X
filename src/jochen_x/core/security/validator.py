"""Centralised input validation for public API boundaries.

The ``InputValidator`` provides reusable validation methods that
enforce Zero Trust on all incoming data.  Every public API in the
runtime uses these validators to reject invalid inputs at the system
boundary, before any processing occurs.

All validation failures raise ``InputValidationError`` with the
offending field name and a human-readable reason.  The validator is
stateless and all methods are class methods for convenient use
without instantiation.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Any, TypeVar

from jochen_x.core.exceptions.security import InputValidationError

__all__ = ["InputValidator"]

_T = TypeVar("_T")
_E = TypeVar("_E", bound=Enum)

_DEFAULT_COMPONENT = "InputValidator"
_MAX_STRING_LENGTH = 1_048_576


class InputValidator:
    """Stateless input validation utility.

    Provides class methods for validating common input types at
    public API boundaries.  All methods raise
    ``InputValidationError`` on invalid input.
    """

    @classmethod
    def validate_not_none(
        cls,
        value: Any,
        field_name: str,
        *,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that *value* is not ``None``.

        Args:
            value: The value to validate.
            field_name: Name of the field being validated.
            component: Originating component name.

        Raises:
            InputValidationError: If *value* is ``None``.

        """
        if value is None:
            raise InputValidationError(
                field_name,
                "must not be None",
                component=component,
            )

    @classmethod
    def validate_type(
        cls,
        value: Any,
        field_name: str,
        expected_type: type[_T],
        *,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that *value* is an instance of *expected_type*.

        Args:
            value: The value to validate.
            field_name: Name of the field being validated.
            expected_type: The expected type.
            component: Originating component name.

        Raises:
            InputValidationError: If *value* is not an instance of
                *expected_type*.

        """
        if not isinstance(value, expected_type):
            raise InputValidationError(
                field_name,
                f"expected {expected_type.__name__}, got {type(value).__name__}",
                component=component,
            )

    @classmethod
    def validate_string(
        cls,
        value: str,
        field_name: str,
        *,
        min_length: int = 0,
        max_length: int = _MAX_STRING_LENGTH,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate a string value.

        Args:
            value: The string to validate.
            field_name: Name of the field being validated.
            min_length: Minimum allowed length (inclusive).
            max_length: Maximum allowed length (inclusive).
            component: Originating component name.

        Raises:
            InputValidationError: If validation fails.

        """
        if not isinstance(value, str):
            raise InputValidationError(
                field_name,
                f"expected str, got {type(value).__name__}",
                component=component,
            )
        if len(value) < min_length:
            raise InputValidationError(
                field_name,
                f"length must be at least {min_length}",
                component=component,
            )
        if len(value) > max_length:
            raise InputValidationError(
                field_name,
                f"length must not exceed {max_length}",
                component=component,
            )

    @classmethod
    def validate_pattern(
        cls,
        value: str,
        field_name: str,
        pattern: re.Pattern[str],
        *,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that a string matches a compiled regex pattern.

        Args:
            value: The string to validate.
            field_name: Name of the field being validated.
            pattern: Compiled regex the string must match.
            component: Originating component name.

        Raises:
            InputValidationError: If validation fails.

        """
        cls.validate_type(value, field_name, str, component=component)
        if not pattern.match(value):
            raise InputValidationError(
                field_name,
                f"must match pattern '{pattern.pattern}'",
                component=component,
            )

    @classmethod
    def validate_non_empty_string(
        cls,
        value: str,
        field_name: str,
        *,
        max_length: int = _MAX_STRING_LENGTH,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that *value* is a non-empty string.

        Args:
            value: The string to validate.
            field_name: Name of the field being validated.
            max_length: Maximum allowed length (inclusive).
            component: Originating component name.

        Raises:
            InputValidationError: If *value* is not a string, is
                empty, or exceeds *max_length*.

        """
        cls.validate_string(
            value,
            field_name,
            min_length=1,
            max_length=max_length,
            component=component,
        )

    @classmethod
    def validate_int(
        cls,
        value: int,
        field_name: str,
        *,
        min_value: int | None = None,
        max_value: int | None = None,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate an integer value.

        Args:
            value: The integer to validate.
            field_name: Name of the field being validated.
            min_value: Minimum allowed value (inclusive).
            max_value: Maximum allowed value (inclusive).
            component: Originating component name.

        Raises:
            InputValidationError: If validation fails.

        """
        if not isinstance(value, int) or isinstance(value, bool):
            raise InputValidationError(
                field_name,
                f"expected int, got {type(value).__name__}",
                component=component,
            )
        if min_value is not None and value < min_value:
            raise InputValidationError(
                field_name,
                f"must be at least {min_value}",
                component=component,
            )
        if max_value is not None and value > max_value:
            raise InputValidationError(
                field_name,
                f"must not exceed {max_value}",
                component=component,
            )

    @classmethod
    def validate_positive_int(
        cls,
        value: int,
        field_name: str,
        *,
        max_value: int | None = None,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that *value* is a positive integer (>= 1).

        Args:
            value: The integer to validate.
            field_name: Name of the field being validated.
            max_value: Maximum allowed value (inclusive).
            component: Originating component name.

        Raises:
            InputValidationError: If validation fails.

        """
        cls.validate_int(
            value,
            field_name,
            min_value=1,
            max_value=max_value,
            component=component,
        )

    @classmethod
    def validate_non_negative_int(
        cls,
        value: int,
        field_name: str,
        *,
        max_value: int | None = None,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that *value* is a non-negative integer (>= 0).

        Args:
            value: The integer to validate.
            field_name: Name of the field being validated.
            max_value: Maximum allowed value (inclusive).
            component: Originating component name.

        Raises:
            InputValidationError: If validation fails.

        """
        cls.validate_int(
            value,
            field_name,
            min_value=0,
            max_value=max_value,
            component=component,
        )

    @classmethod
    def validate_float(
        cls,
        value: float,
        field_name: str,
        *,
        min_value: float | None = None,
        max_value: float | None = None,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate a finite float value.

        NaN and infinite values are always rejected (Zero Trust).

        Args:
            value: The float to validate.
            field_name: Name of the field being validated.
            min_value: Minimum allowed value (inclusive).
            max_value: Maximum allowed value (inclusive).
            component: Originating component name.

        Raises:
            InputValidationError: If validation fails.

        """
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InputValidationError(
                field_name,
                f"expected float, got {type(value).__name__}",
                component=component,
            )
        float_val = float(value)
        if float_val != float_val:  # noqa: PLR0124
            raise InputValidationError(
                field_name,
                "NaN is not allowed",
                component=component,
            )
        if abs(float_val) == float("inf"):
            raise InputValidationError(
                field_name,
                "infinity is not allowed",
                component=component,
            )
        if min_value is not None and float_val < min_value:
            raise InputValidationError(
                field_name,
                f"must be at least {min_value}",
                component=component,
            )
        if max_value is not None and float_val > max_value:
            raise InputValidationError(
                field_name,
                f"must not exceed {max_value}",
                component=component,
            )

    @classmethod
    def validate_enum_value(
        cls,
        value: Enum,
        field_name: str,
        enum_type: type[_E],
        *,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that *value* is a member of *enum_type*.

        Args:
            value: The value to validate.
            field_name: Name of the field being validated.
            enum_type: The expected enum type.
            component: Originating component name.

        Raises:
            InputValidationError: If *value* is not a member of
                *enum_type*.

        """
        if not isinstance(value, enum_type):
            valid_values = ", ".join(m.name for m in enum_type)
            raise InputValidationError(
                field_name,
                f"must be a {enum_type.__name__} member ({valid_values})",
                component=component,
            )

    @classmethod
    def validate_collection_not_empty(
        cls,
        value: Any,
        field_name: str,
        *,
        component: str = _DEFAULT_COMPONENT,
    ) -> None:
        """Validate that *value* is a non-empty collection.

        Args:
            value: The collection to validate.
            field_name: Name of the field being validated.
            component: Originating component name.

        Raises:
            InputValidationError: If *value* is empty or has no
                ``__len__`` method.

        """
        if not hasattr(value, "__len__"):
            raise InputValidationError(
                field_name,
                "must be a collection with a length",
                component=component,
            )
        if len(value) == 0:
            raise InputValidationError(
                field_name,
                "must not be empty",
                component=component,
            )
