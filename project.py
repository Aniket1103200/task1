import json
import sys
import urllib.error
import urllib.request


def check_requirements(requirements_text):
    # Number of lines in the file
    lines = [line.strip() for line in requirements_text.strip().splitlines() if line.strip()]
    dependencies_checked = len(lines)

    packages_not_on_pypi = 0
    versions_not_on_pypi = 0
    valid_releases = []

    for line in lines:
        if "==" not in line:
            continue

        name, version = (part.strip() for part in line.split("==", 1))

        # 1. Check if the package exists on PyPI
        pkg_url = f"https://pypi.org/pypi/{name}/json"
        try:
            req = urllib.request.Request(pkg_url, headers={"User-Agent": "PyPIChecker/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                packages_not_on_pypi += 1
            continue
        except Exception:
            continue

        # 2. Check if the specific pinned version exists on PyPI
        ver_url = f"https://pypi.org/pypi/{name}/{version}/json"
        try:
            req = urllib.request.Request(ver_url, headers={"User-Agent": "PyPIChecker/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                ver_data = json.loads(response.read().decode())

            # Use the upload_time of the first file listed under urls
            urls = ver_data.get("urls", [])
            if urls and "upload_time" in urls[0]:
                upload_time = urls[0]["upload_time"]
                year = upload_time.split("-")[0]
                valid_releases.append((upload_time, name, version, year))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                versions_not_on_pypi += 1
            continue
        except Exception:
            continue

    # 4. Oldest pinned release among lines where package and version both exist
    oldest_release_str = "None"
    if valid_releases:
        valid_releases.sort(key=lambda x: x[0])
        oldest = valid_releases[0]
        oldest_release_str = f"{oldest[1]}=={oldest[2]} ({oldest[3]})"

    # Print results in required format
    print(f"Dependencies checked: {dependencies_checked}")
    print(f"Packages not on PyPI: {packages_not_on_pypi}")
    print(f"Versions not on PyPI: {versions_not_on_pypi}")
    print(f"Oldest pinned release: {oldest_release_str}")

    return {
        "dependencies_checked": dependencies_checked,
        "packages_not_on_pypi": packages_not_on_pypi,
        "versions_not_on_pypi": versions_not_on_pypi,
        "oldest_pinned_release": oldest_release_str,
    }


if __name__ == "__main__":
    # If a filename argument is passed, read from file; otherwise use the assigned input
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # Assigned task input
        content = """django==1.11
pandas==0.99.0
beautifulsoup4==4.6.0
langchain-agents-toolkit==0.2.1
scikit-learn==0.20.0
six==1.10.0
openai-function-caller==0.3.0
requests==2.31.0"""

    check_requirements(content)