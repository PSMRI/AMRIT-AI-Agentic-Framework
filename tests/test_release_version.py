from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION_SCRIPT = REPOSITORY_ROOT / "scripts" / "next-release-version.py"


def load_script(module_name: str, filename: str) -> ModuleType:
    script_path = REPOSITORY_ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release_version = load_script("test_next_release_version", "next-release-version.py")


class ReleaseLineTests(unittest.TestCase):
    def test_accepts_major_minor_release_lines(self) -> None:
        for release_line, expected in (
            ("1.0", (1, 0)),
            ("2.4", (2, 4)),
            ("10.12", (10, 12)),
            ("0.1", (0, 1)),
            ("1.0\n", (1, 0)),
            ("  1.2  \n", (1, 2)),
        ):
            with self.subTest(release_line=release_line):
                self.assertEqual(
                    release_version.parse_release_line(release_line), expected
                )

    def test_rejects_malformed_release_lines(self) -> None:
        for release_line in (
            "v1.2",
            "1",
            "1.2.3",
            "1.x",
            "1.2-beta",
            "1.",
            ".2",
            "01.2",
            "1.02",
            "1,2",
            "1.2 3.4",
            "1.2\n1.3\n",
            "",
            "   ",
            "\n",
        ):
            with self.subTest(release_line=release_line):
                with self.assertRaises(release_version.ReleaseVersionError):
                    release_version.parse_release_line(release_line)

    def test_empty_release_line_names_the_file(self) -> None:
        with self.assertRaisesRegex(
            release_version.ReleaseVersionError, r"\.release-version is empty"
        ):
            release_version.parse_release_line("\n")

    def test_reads_the_release_line_from_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            release_version_file = Path(temporary) / ".release-version"
            release_version_file.write_text("3.7\n", encoding="utf-8")

            self.assertEqual(
                release_version.read_release_line(release_version_file), (3, 7)
            )

    def test_missing_release_version_file_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / ".release-version"

            with self.assertRaisesRegex(
                release_version.ReleaseVersionError, "Could not read"
            ):
                release_version.read_release_line(missing)


class NextTagTests(unittest.TestCase):
    def assert_next_tag(
        self, release_line: str, tags: list[str], expected: str
    ) -> None:
        self.assertEqual(
            release_version.calculate_next_tag(release_line, tags), expected
        )

    def test_first_release_on_a_release_line(self) -> None:
        self.assert_next_tag("1.2", [], "v1.2.0")

    def test_normal_increment(self) -> None:
        self.assert_next_tag("1.2", ["v1.2.0", "v1.2.1"], "v1.2.2")

    def test_patches_are_compared_numerically_not_lexicographically(self) -> None:
        self.assert_next_tag("1.2", ["v1.2.9", "v1.2.10"], "v1.2.11")

    def test_gaps_do_not_reuse_missing_patches(self) -> None:
        self.assert_next_tag("1.2", ["v1.2.1", "v1.2.7"], "v1.2.8")

    def test_ignores_other_release_lines(self) -> None:
        self.assert_next_tag(
            "1.2",
            ["v1.1.99", "v1.2.4", "v1.3.30", "v2.0.0"],
            "v1.2.5",
        )

    def test_ignores_prerelease_like_and_unrelated_tags(self) -> None:
        self.assert_next_tag(
            "1.2",
            ["v1.2.3-beta", "foo-v1.2.100", "v1.2.4"],
            "v1.2.5",
        )

    def test_ignores_further_malformed_matching_tags(self) -> None:
        self.assert_next_tag(
            "1.2",
            [
                "1.2.50",
                "V1.2.60",
                "v1.2.007",
                "v1.2.",
                "v1.2.4.1",
                "v1.2.4+build",
                "release/v1.2.70",
                "v1.20.80",
                "v11.2.90",
                "v1.2.4",
            ],
            "v1.2.5",
        )

    def test_new_minor_line_starts_at_patch_zero(self) -> None:
        self.assert_next_tag("1.3", ["v1.2.11", "v1.2.12"], "v1.3.0")

    def test_new_major_line_starts_at_patch_zero(self) -> None:
        self.assert_next_tag("2.0", ["v1.9.4", "v1.9.5"], "v2.0.0")

    def test_unordered_and_duplicated_tags_are_handled(self) -> None:
        self.assert_next_tag(
            "1.2",
            ["v1.2.10", "v1.2.2", "v1.2.10", "v1.2.9"],
            "v1.2.11",
        )

    def test_surrounding_whitespace_on_tags_is_tolerated(self) -> None:
        self.assert_next_tag("1.2", ["  v1.2.4  ", "\tv1.2.5\t"], "v1.2.6")

    def test_selects_the_released_patch_numbers(self) -> None:
        self.assertEqual(
            release_version.select_release_patches(
                1, 2, ["v1.2.3", "v1.2.10", "v1.3.0", "v1.2.3"]
            ),
            [3, 10],
        )

    def test_a_malformed_release_line_never_produces_a_tag(self) -> None:
        with self.assertRaises(release_version.ReleaseVersionError):
            release_version.calculate_next_tag("1.2.3", ["v1.2.0"])


class TagInputTests(unittest.TestCase):
    def test_splits_tag_listings_and_drops_blank_lines(self) -> None:
        self.assertEqual(
            release_version.split_tags("v1.2.0\n\n  v1.2.1  \n\n"),
            ["v1.2.0", "v1.2.1"],
        )

    def test_reads_tags_from_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tags_file = Path(temporary) / "tags.txt"
            tags_file.write_text("v1.2.0\nv1.2.1\n", encoding="utf-8")

            self.assertEqual(
                release_version.read_tags_from_file(tags_file),
                ["v1.2.0", "v1.2.1"],
            )

    def test_missing_tags_file_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(
                release_version.ReleaseVersionError, "Could not read"
            ):
                release_version.read_tags_from_file(Path(temporary) / "absent.txt")


class CommandLineTests(unittest.TestCase):
    """Exercise the interface the release workflow actually calls."""

    def run_script(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(RELEASE_VERSION_SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def write_inputs(self, temporary: str, release_line: str, tags: str) -> tuple[Path, Path]:
        release_version_file = Path(temporary) / ".release-version"
        release_version_file.write_text(release_line, encoding="utf-8")
        tags_file = Path(temporary) / "tags.txt"
        tags_file.write_text(tags, encoding="utf-8")
        return release_version_file, tags_file

    def test_prints_only_the_next_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            release_version_file, tags_file = self.write_inputs(
                temporary, "1.2\n", "v1.2.9\nv1.2.10\nv2.0.0\n"
            )

            result = self.run_script(
                "--release-version-file",
                str(release_version_file),
                "--tags-file",
                str(tags_file),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "v1.2.11")

    def test_first_release_on_a_new_minor_line(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            release_version_file, tags_file = self.write_inputs(
                temporary, "1.3\n", "v1.2.14\nv1.2.15\n"
            )

            result = self.run_script(
                "--release-version-file",
                str(release_version_file),
                "--tags-file",
                str(tags_file),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "v1.3.0")

    def test_malformed_release_line_fails_without_printing_a_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            release_version_file, tags_file = self.write_inputs(
                temporary, "1.2.3\n", "v1.2.0\n"
            )

            result = self.run_script(
                "--release-version-file",
                str(release_version_file),
                "--tags-file",
                str(tags_file),
            )

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout.strip(), "")
            self.assertIn("Release version calculation failed", result.stderr)

    def test_reads_tags_from_standard_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            release_version_file, _ = self.write_inputs(temporary, "1.2\n", "")

            result = subprocess.run(
                [
                    sys.executable,
                    str(RELEASE_VERSION_SCRIPT),
                    "--release-version-file",
                    str(release_version_file),
                    "--tags-file",
                    "-",
                ],
                input="v1.2.1\nv1.2.7\n",
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "v1.2.8")


class CommittedReleaseVersionTests(unittest.TestCase):
    def test_committed_release_version_file_is_a_valid_release_line(self) -> None:
        release_version_file = REPOSITORY_ROOT / ".release-version"
        self.assertTrue(
            release_version_file.is_file(),
            f"Expected a committed release line at {release_version_file}",
        )

        major, minor = release_version.read_release_line(release_version_file)

        self.assertGreaterEqual(major, 0)
        self.assertGreaterEqual(minor, 0)

    def test_committed_release_version_file_has_no_patch_component(self) -> None:
        contents = (REPOSITORY_ROOT / ".release-version").read_text(encoding="utf-8")

        self.assertNotIn(".", contents.strip().replace(".", "", 1))


if __name__ == "__main__":
    unittest.main()
