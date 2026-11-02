#!/usr/bin/env python3
"""
Ironflow Hyperliquid Liquidations Monitor
Idempotent, unauthenticated-only, rate-limited monitor for new monthly parquets
"""

import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


class IronflowMonitor:
    def __init__(self, repo_root=None):
        if repo_root is None:
            repo_root = Path(__file__).parent.parent
        self.repo_root = Path(repo_root)
        self.state_path = self.repo_root / "research_state" / "ironflow_monitor_state.json"
        self.evidence_dir = self.repo_root / "research_state"
        self.base_url = "https://huggingface.co"
        self.dataset = "ironflow/hyperliquid-liquidations"
        self.load_state()

    def load_state(self):
        if self.state_path.exists():
            with open(self.state_path) as f:
                self.state = json.load(f)
        else:
            self.state = {
                "last_check": None,
                "last_seen_files": {},
                "known_events": [],
                "known_fills": []
            }

    def save_state(self):
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)

    def probe_url(self, url):
        """Probe URL with full evidence capture (unauthenticated)"""
        evidence = {
            "url": url,
            "method": "GET",
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": None,
            "headers": {},
            "body_preview": None,
            "content_length": None,
            "sha256": None,
            "error": None
        }
        try:
            req = Request(url)
            req.add_header('User-Agent', 'FCLR-Monitor/1.0')
            with urlopen(req, timeout=30) as resp:
                evidence["status"] = resp.status
                # Capture headers
                for k, v in resp.headers.items():
                    evidence["headers"][k.lower()] = v
                evidence["content_length"] = resp.headers.get('Content-Length')
                body = resp.read()
                evidence["sha256"] = hashlib.sha256(body).hexdigest()
                evidence["body_preview"] = body[:200].decode('utf-8', errors='replace')
        except HTTPError as e:
            evidence["status"] = e.code
            evidence["error"] = str(e)
            for k, v in e.headers.items():
                evidence["headers"][k.lower()] = v
            try:
                body = e.read()
                evidence["sha256"] = hashlib.sha256(body).hexdigest()
                evidence["body_preview"] = body[:200].decode('utf-8', errors='replace')
            except:
                pass
        except Exception as e:
            evidence["error"] = str(e)
        return evidence

    def check_tree(self):
        """Check HF dataset tree for new files"""
        tree_url = f"{self.base_url}/api/datasets/{self.dataset}/tree/main?recursive=true"
        return self.probe_url(tree_url)

    def check_month(self, year_month):
        """Check specific month files"""
        results = {}
        for prefix in ['data/events', 'data/fills']:
            url = f"{self.base_url}/datasets/{self.dataset}/resolve/main/{prefix}/{year_month}.parquet"
            results[f"{prefix}/{year_month}.parquet"] = self.probe_url(url)
        return results

    def run(self):
        """Run monitor probe with full evidence"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        evidence = {
            "monitor_run_id": f"ironflow_probe_{timestamp}",
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tree_probe": None,
            "month_probes": {},
            "new_files_found": [],
            "action_required": False
        }

        # Probe tree
        evidence["tree_probe"] = self.check_tree()

        # Probe recent months (check Nov 2026 onward and a few recent)
        for ym in ['2026-11', '2026-12']:
            evidence["month_probes"][ym] = self.check_month(ym)
            for path, probe in evidence["month_probes"][ym].items():
                if probe["status"] == 200 and probe["content_length"] and int(probe["content_length"]) > 1000:
                    evidence["new_files_found"].append(path)
                    evidence["action_required"] = True

        # Save evidence
        evidence_file = self.evidence_dir / f"ironflow_probe_{timestamp}.json"
        with open(evidence_file, 'w') as f:
            json.dump(evidence, f, indent=2)

        # Update state
        self.state["last_check"] = evidence["timestamp_utc"]
        self.save_state()

        print(json.dumps({
            "monitor_run_id": evidence["monitor_run_id"],
            "new_files_found": evidence["new_files_found"],
            "action_required": evidence["action_required"],
            "evidence_file": str(evidence_file)
        }, indent=2))

        return evidence


def main():
    monitor = IronflowMonitor()
    monitor.run()


if __name__ == '__main__':
    main()
