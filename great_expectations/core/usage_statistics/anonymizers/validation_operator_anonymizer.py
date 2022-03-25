from typing import Any, Optional

from great_expectations.core.usage_statistics.anonymizers.action_anonymizer import (
    ActionAnonymizer,
)
from great_expectations.core.usage_statistics.anonymizers.base import BaseAnonymizer
from great_expectations.validation_operators.validation_operators import (
    ValidationOperator,
)


class ValidationOperatorAnonymizer(BaseAnonymizer):
    def __init__(self, salt: Optional[str] = None) -> None:
        super().__init__(salt=salt)

        self._action_anonymizer = ActionAnonymizer(salt=salt)

    def anonymize(
        self,
        validation_operator_obj: ValidationOperator,
        validation_operator_name: str,
    ) -> Any:
        anonymized_info_dict: dict = {
            "anonymized_name": self._anonymize_string(validation_operator_name)
        }
        actions_dict: dict = validation_operator_obj.actions

        anonymized_info_dict.update(
            self._anonymize_object_info(
                object_=validation_operator_obj,
                anonymized_info_dict=anonymized_info_dict,
            )
        )

        if actions_dict:
            anonymized_info_dict["anonymized_action_list"] = [
                self._action_anonymizer.anonymize(
                    action_name=action_name, action_obj=action_obj
                )
                for action_name, action_obj in actions_dict.items()
            ]

        return anonymized_info_dict

    @staticmethod
    def can_handle(obj: object, **kwargs) -> bool:
        return (
            isinstance(obj, ValidationOperator) and "validation_operator_name" in kwargs
        )
