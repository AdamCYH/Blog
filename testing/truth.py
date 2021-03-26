import json
from unittest import TestCase


def assert_that(test_case, actual, expected, ignore_order=False):
    """
    Asserts http response with expected json string.
    """
    actual = actual.data
    expected = expected

    TestCase.assertEqual(test_case, first=len(actual), second=len(expected))
    TestCase.assertEqual(test_case,
                         first=json.dumps(actual, sort_keys=ignore_order),
                         second=json.dumps(expected, sort_keys=ignore_order))


def assert_that_ignore_fields(test_case, actual, expected, ignored_fields=None, ignore_order=False):
    """
    Asserts http response with expected json string with ignored fields
    """
    if ignored_fields is None:
        ignored_fields = []

    actual = actual.data
    expected = expected

    _deep_remove_fields(actual, ignored_fields)
    _deep_remove_fields(expected, ignored_fields)

    TestCase.assertEqual(test_case, first=len(actual), second=len(expected))
    TestCase.assertEqual(test_case,
                         first=json.dumps(actual, sort_keys=ignore_order),
                         second=json.dumps(expected, sort_keys=ignore_order))


def _deep_remove_fields(source, ignored_fields):
    stack = [source]
    while stack:
        curr = stack.pop()
        if isinstance(curr, dict):
            for ignored_field in ignored_fields:
                if ignored_field in curr:
                    del curr[ignored_field]

            for value in curr.values():
                if isinstance(value, list):
                    for item in curr:
                        stack.append(item)

        if isinstance(curr, list):
            for item in curr:
                stack.append(item)
