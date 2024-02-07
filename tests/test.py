from typing import Any
import unittest
import os
import subprocess


class WikipediaPlagiariserTests(unittest.TestCase):
    _ran_times: dict[str, int] = (
        {}
    )  # multiple tests dont work, add counter for each name

    def _get_current_test_name(self) -> str:
        return self.id().split(".")[-1]

    def _get_cwd(self) -> str:
        return __file__.removesuffix(os.path.basename(__file__))

    def _get_snapshot_path(self) -> str:
        return os.path.join(
            self._get_cwd(),
            "./snapshots",
            self._get_current_test_name()
            + f"_step_{self._ran_times.get(self._get_current_test_name(), 0)}",
        )

    def get_snapshot(self) -> bytes | None:
        case_name = self._get_current_test_name()
        path = self._get_snapshot_path()

        if self._ran_times.get(case_name) is None:
            self._ran_times[case_name] = 0

        self._ran_times[case_name] += 1

        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()

        return None

    def run_program_with_arguments(self, *args: str) -> tuple[str]:
        result = subprocess.run(
            executable="python", args=["python", "main.py", *args], capture_output=True
        )
        return result.stdout, result.stderr

    def _check_ouput(self, output: Any) -> None:
        if not os.path.exists(self._get_snapshot_path()):
            with open(self._get_snapshot_path(), "wb") as f:
                f.write(output)

        self.assertEqual(output, self.get_snapshot())

    def test_no_colour(self):
        output, error = self.run_program_with_arguments("201")
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments("201", "--no-colour")
        self._check_ouput(output)
        self.assertEqual(error, b"")

    def test_json(self):
        output, error = self.run_program_with_arguments("418")
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "201", "--no-colour", "--output-as-json"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

    def test_json_indent(self):
        output, error = self.run_program_with_arguments("418")
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "201", "--no-colour", "--output-as-json", "--indent-size", "1"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "201", "--no-colour", "--output-as-json", "--indent-size", "10"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

    def test_no_pretty(self):
        output, error = self.run_program_with_arguments("418")
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "201", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

    def test_wildcard(self):
        output, error = self.run_program_with_arguments(
            "x", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

    def test_partial_wildcards(self):
        output, error = self.run_program_with_arguments(
            "xxx", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "2x0", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "4xx", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "xx0", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

    def test_text_search(self):
        output, error = self.run_program_with_arguments(
            "legal", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "invalid", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "hello", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")

        output, error = self.run_program_with_arguments(
            "server", "--no-colour", "--output-as-json", "--no-pretty"
        )
        self._check_ouput(output)
        self.assertEqual(error, b"")


if __name__ == "__main__":
    unittest.main()
