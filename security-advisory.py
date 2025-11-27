#!/usr/bin/python3

import argparse, json, sys
from typing import List, Dict
import requests

UBUNTU_NOTICES_URL = "https://ubuntu.com/security/notices.json"
NVD_CVES_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_ubuntu_kernel_usns(release: str) -> List[Dict]:
    try:
        r = requests.get(UBUNTU_NOTICES_URL)
        r.raise_for_status()
        data = r.json()
        unicorn_python = data['notices'][0]['release_packages']['noble']

        for x in range(0,len(str(unicorn_python))):
            a_fusion = data['notices'][0]['release_packages']['noble'][x]
            print(a_fusion)

    except IndexError:
        pass


def fetch_nvd(keyword: str, results_per_page: int = 100) -> List[Dict]:
    try:
        r = requests.get(NVD_CVES_URL, params={"keywordSearch": keyword, "resultsPerPage": results_per_page}, timeout=30)
        r.raise_for_status()
        data = r.json()
        out = []
        for v in data.get("vulnerabilities", []):
            cve = v.get("cve", {})
            # Try CVSS v3.1, fallback to v3.0, else unknown
            sev = "unknown"
            m = cve.get("metrics", {})
            v31 = (m.get("cvssMetricV31") or [{}])[0].get("cvssData") if m.get("cvssMetricV31") else None
            v30 = (m.get("cvssMetricV30") or [{}])[0].get("cvssData") if m.get("cvssMetricV30") else None
            if v31 and v31.get("baseSeverity"):
                sev = v31["baseSeverity"].lower()
            elif v30 and v30.get("baseSeverity"):
                sev = v30["baseSeverity"].lower()

            out.append({
                "cve_id": cve.get("id"),
                "description": (cve.get("descriptions") or [{}])[0].get("value"),
                "severity": sev,
                "published": cve.get("published"),
                "modified": cve.get("lastModified"),
            })
        return out
    except Exception as e:
        print(f"nvd fetch error: {e}", file=sys.stderr)
        return []

def categorize(items: List[Dict], key: str = "severity") -> Dict[str, List[Dict]]:
    buckets = {"critical": [], "important": [], "moderate": [], "low": [], "unknown": []}
    for it in items:
        sev = (it.get(key) or "unknown").lower()
        if "critical" in sev:
            buckets["critical"].append(it)
        elif "high" in sev or "important" in sev:
            buckets["important"].append(it)
        elif "medium" in sev or "moderate" in sev:
            buckets["moderate"].append(it)
        elif "low" in sev:
            buckets["low"].append(it)
        else:
            buckets["unknown"].append(it)
    return buckets

def main():
    p = argparse.ArgumentParser(description="Barebones security advisory fetcher")
    p.add_argument("--ubuntu", metavar="RELEASE", help="Ubuntu codename (e.g., focal, jammy, noble). Can repeat.", action="append")
    p.add_argument("--nvd", metavar="KEYWORD", help='NVD keyword search (e.g., "linux kernel")')
    p.add_argument("--out", metavar="FILE", help="Write JSON to file (optional)")
    args = p.parse_args()

    result = {}

    if args.ubuntu:
        for rel in args.ubuntu:
            usns = fetch_ubuntu_kernel_usns(rel)
            result[f"ubuntu_{rel}"] = categorize(usns, key="severity")

    # if args.nvd:
    #     nvd_items = fetch_nvd(args.nvd)
    #     result["nvd"] = categorize(nvd_items, key="severity")

    # If nothing requested, show quick help
    if not result:
        print("Nothing to do. Example:\n  ./minimal_sec.py --ubuntu jammy --nvd 'linux kernel'")
        sys.exit(0)

    j = json.dumps(result, indent=2, ensure_ascii=False)
    print(j)

    if args.out:
        with open(args.out, "w") as f:
            f.write(j)

if __name__ == "__main__":
    fetch_ubuntu_kernel_usns("ubuntu")
    
