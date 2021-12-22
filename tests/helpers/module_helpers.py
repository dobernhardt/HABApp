import importlib
import inspect
import sys
from typing import Iterable, Optional

if sys.version_info >= (3, 10):
    get_annotations = inspect.get_annotations
else:
    get_annotations = lambda x: getattr(x, '__annotations__')


def get_module_classes(module_name: str, exclude: Optional[Iterable[str]] = None, skip_imports=True):
    if exclude is None:
        exclude = set()

    importlib.import_module(module_name)
    return dict(inspect.getmembers(
        sys.modules[module_name],
        lambda x: inspect.isclass(x) and (skip_imports or x.__module__ == module_name) and x.__name__ not in exclude
    ))


def check_class_annotations(module_name: str, exclude: Optional[Iterable[str]] = None, skip_imports=True):
    """Ensure that the annotations match with the actual variables"""

    classes = get_module_classes(module_name, exclude=exclude)
    for name, cls in classes.items():
        c = cls()
        args = dict(filter(
            lambda x: not x[0].startswith('__'),
            dict(inspect.getmembers(c, lambda x: not inspect.ismethod(x))).items())
        )

        annotations = get_annotations(c)

        # Check that all vars are in __annotations__
        for arg_name in args:
            assert arg_name in annotations, f'"{arg_name}" is missing in annotations!"\n' \
                                                  f'members    : {", ".join(sorted(args))}\n' \
                                                  f'annotations: {", ".join(sorted(annotations))}'

        for arg_name in annotations:
            assert arg_name in args, f'"{arg_name}" is missing in args!"\n' \
                                     f'members    : {", ".join(sorted(args))}\n' \
                                     f'annotations: {", ".join(sorted(annotations))}'
