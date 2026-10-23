"""Тесты для Github-Commit-Counter."""

import unittest
from datetime import datetime
from unittest.mock import patch

import requests

import main


class FakeResponse:
    """Минимальная заглушка ответа requests."""

    def __init__(self, payload: dict) -> None:
        self._payload: dict = payload

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return self._payload


def success_payload(total: int) -> dict:
    return {
        "data": {
            "user": {
                "contributionsCollection": {"totalCommitContributions": total}
            }
        }
    }


class ValidateUsernameTests(unittest.TestCase):
    def test_accepts_letters_digits_and_hyphen(self) -> None:
        self.assertTrue(main.validate_username("FelineFantasy"))
        self.assertTrue(main.validate_username("octo-cat-42"))

    def test_rejects_empty_and_invalid_characters(self) -> None:
        self.assertFalse(main.validate_username(""))
        self.assertFalse(main.validate_username("   "))
        self.assertFalse(main.validate_username("octo_cat"))
        self.assertFalse(main.validate_username("octo cat"))


class ValidateYearTests(unittest.TestCase):
    def test_accepts_boundaries(self) -> None:
        self.assertTrue(main.validate_year(2008))
        self.assertTrue(main.validate_year(datetime.now().year))

    def test_rejects_out_of_range(self) -> None:
        self.assertFalse(main.validate_year(2007))
        self.assertFalse(main.validate_year(datetime.now().year + 1))


class ParseArgsTests(unittest.TestCase):
    def test_defaults_are_none(self) -> None:
        args = main.parse_args([])
        self.assertIsNone(args.username)
        self.assertIsNone(args.year)
        self.assertFalse(args.json)

    def test_positional_arguments(self) -> None:
        args = main.parse_args(["octocat", "2024"])
        self.assertEqual(args.username, "octocat")
        self.assertEqual(args.year, 2024)

    def test_json_flag(self) -> None:
        self.assertTrue(main.parse_args(["--json"]).json)


class GetCommitsTests(unittest.TestCase):
    @patch("main.requests.post")
    def test_returns_commit_count(self, post_mock) -> None:
        post_mock.return_value = FakeResponse(success_payload(42))

        self.assertEqual(main.get_commits("octocat", 2024, "token"), 42)
        post_mock.assert_called_once()
        self.assertEqual(
            post_mock.call_args.kwargs["json"]["variables"]["from"],
            "2024-01-01T00:00:00Z",
        )
        self.assertEqual(
            post_mock.call_args.kwargs["json"]["variables"]["to"],
            "2024-12-31T23:59:59Z",
        )

    @patch("main.requests.post")
    def test_returns_none_on_api_error(self, post_mock) -> None:
        post_mock.return_value = FakeResponse({"errors": [{"message": "Bad token"}]})

        self.assertIsNone(main.get_commits("octocat", 2024, "token"))

    @patch("main.requests.post")
    def test_returns_none_when_user_is_missing(self, post_mock) -> None:
        post_mock.return_value = FakeResponse({"data": {"user": None}})

        self.assertIsNone(main.get_commits("nobody", 2024, "token"))

    @patch("main.requests.post")
    def test_returns_none_on_network_error(self, post_mock) -> None:
        post_mock.side_effect = requests.exceptions.ConnectionError("boom")

        self.assertIsNone(main.get_commits("octocat", 2024, "token"))


class MainTests(unittest.TestCase):
    def test_invalid_username_exits_with_error(self) -> None:
        with patch("builtins.print") as print_mock:
            code = main.main(["octo_cat", "2024"])

        self.assertEqual(code, 1)
        print_mock.assert_called_once()

    def test_invalid_year_exits_with_error(self) -> None:
        with patch("builtins.print") as print_mock:
            code = main.main(["octocat", "1999"])

        self.assertEqual(code, 1)
        print_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
