import inspect
from typing import List, Type, TypeVar

from typemock._utils import methods
from typemock.api import MemberType, MissingHint, MissingTypeHintsError

T = TypeVar('T')


def _validate_method_annotations(clazz, missing: List[MissingHint]):
    for func_entry in methods(clazz):
        func = func_entry.func
        name = func_entry.name
        sig = inspect.signature(func_entry.func)
        if len(sig.parameters) > 0:
            annotations = func.__annotations__
            for param_name in sig.parameters:
                if param_name == "self":
                    continue
                else:
                    if param_name not in annotations:
                        missing.append(
                            MissingHint(
                                path=[name, param_name],
                                member_type=MemberType.ARG
                            )
                        )
            if "return" not in annotations:
                missing.append(
                    MissingHint(
                        path=[name],
                        member_type=MemberType.RETURN
                    )
                )


def _validate_attributes(clazz: Type[T], missing: List[MissingHint]):
    pass


def get_missing_class_type_hints(clazz) -> List[MissingHint]:
    missing = []
    _validate_attributes(clazz, missing)
    _validate_method_annotations(clazz, missing)
    return missing


def validate_class_type_hints(clazz: Type[T]) -> None:
    """
    Args:
        clazz:

    Raises:

        MissingTypeHintsError

    """
    missing = get_missing_class_type_hints(clazz)
    if len(missing) > 0:
        raise MissingTypeHintsError(
            "{} has missing type hints.".format(clazz),
            missing
        )
