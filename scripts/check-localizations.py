#!/usr/bin/env python3
"""Static contract checks for the first OpenZCine Chinese localization pass."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ANDROID_RES = ROOT / "Apps/Android/app/src/main/res"
IOS = ROOT / "ios/Runner"
LOCALES = ("zh-Hans", "zh-Hant")
ANDROID_QUALIFIER = {"zh-Hans": "values-b+zh+Hans", "zh-Hant": "values-b+zh+Hant"}
FORMAT_SPEC = re.compile(r"%(?:\d+\$)?[#+\- 0,(]*\d*(?:\.\d+)?[a-zA-Z%]")
APPLE_ROW = re.compile(r'^"((?:\\.|[^"\\])*)"\s*=\s*"((?:\\.|[^"\\])*)";$')


def android_strings(filename: Path) -> dict[str, str]:
    root = ET.parse(filename).getroot()
    assert root.tag == "resources", filename
    names = [node.attrib["name"] for node in root.findall("string")]
    assert len(names) == len(set(names)), f"Duplicate Android resource in {filename}"
    return {node.attrib["name"]: "".join(node.itertext()) for node in root.findall("string")}


def apple_strings(filename: Path) -> dict[str, str]:
    lines = filename.read_text(encoding="utf-8").splitlines()
    data: dict[str, str] = {}
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("/*") or line.startswith("//"):
            continue
        found = APPLE_ROW.fullmatch(line)
        assert found is not None, f"Invalid Apple .strings line {filename}:{number}: {line}"
        key, value = found.groups()
        assert key not in data, f"Duplicate Apple key {key} in {filename}"
        data[key] = value
    return data


def main() -> None:
    base = android_strings(ANDROID_RES / "values/strings.xml")
    required = {
        "app_language_title", "app_language_system", "app_language_english",
        "app_language_simplified", "app_language_traditional",
        "settings_title", "settings_tab_system", "pairing_step_choose_path",
    }
    assert required <= base.keys()
    report = []
    for locale in LOCALES:
        translated = android_strings(ANDROID_RES / ANDROID_QUALIFIER[locale] / "strings.xml")
        assert required <= translated.keys()
        assert translated.keys() <= base.keys(), f"Unknown {locale} Android string keys"
        for name, content in translated.items():
            original = Counter(FORMAT_SPEC.findall(base[name]))
            translated_formats = Counter(FORMAT_SPEC.findall(content))
            assert original == translated_formats, (
                f"{locale}:{name} changed format placeholders: "
                f"{original} -> {translated_formats}"
            )
        local = apple_strings(IOS / (locale + ".lproj") / "Localizable.strings")
        info = apple_strings(IOS / (locale + ".lproj") / "InfoPlist.strings")
        assert {"Language", "Follow System", "Operator Setup", "Settings"} <= local.keys()
        assert {"NSCameraUsageDescription", "NSLocalNetworkUsageDescription",
                "NSLocationWhenInUseUsageDescription"} <= info.keys()
        report.append(f"{locale}: {len(translated)} Android, {len(local)} Apple UI, "
                      f"{len(info)} Apple permission strings")

    project = (ROOT / "ios/Runner.xcodeproj/project.pbxproj").read_text()
    for value in ("Localizable.strings in Resources", "InfoPlist.strings in Resources",
                  '"zh-Hans"', '"zh-Hant"'):
        assert value in project, f"Xcode project missing {value}"

    print("Localization resource validation passed.")
    print("\n".join(report))


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, ET.ParseError) as error:
        print(f"Localization check failed: {error}", file=sys.stderr)
        sys.exit(1)
