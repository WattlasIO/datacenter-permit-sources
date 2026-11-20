import unittest
import urllib.parse

import lookup


class TestDatacenterPermitSources(unittest.TestCase):
    def test_sources_schema_and_urls(self) -> None:
        sources = lookup.load_sources()
        self.assertGreaterEqual(len(sources), 8)
        ids = set()
        for s in sources:
            for k in ("id", "name", "jurisdiction", "category", "url", "proves", "does_not_prove"):
                self.assertTrue(s.get(k), f"Missing {k} in {s}")
            self.assertNotIn(s["id"], ids)
            ids.add(s["id"])
            p = urllib.parse.urlparse(s["url"])
            self.assertEqual(p.scheme, "https")
            self.assertTrue(p.netloc)

    def test_filters(self) -> None:
        sources = lookup.load_sources()
        tx = lookup.filter_sources(sources, jurisdiction="texas")
        self.assertEqual([s["id"] for s in tx], ["tx-tdlr-tabs"])
        env = lookup.filter_sources(sources, category="environmental-permit")
        self.assertEqual(len(env), 2)

    def test_validate_record(self) -> None:
        valid = {
            "project_name": "Sample Campus Phase 1",
            "state": "TX",
            "stage": "permitted",
            "source_id": "tx-tdlr-tabs",
            "filing_url": "https://www.tdlr.texas.gov/TABS/Search/Project/TABS2026000001",
            "observed_date": "2026-11-19",
        }
        ids = {s["id"] for s in lookup.load_sources()}
        self.assertEqual(lookup.validate_record(valid, ids), [])

        bad = {"project_name": "Press Release Only", "stage": "rumored", "filing_url": "not-a-url"}
        errs = lookup.validate_record(bad, ids)
        self.assertGreaterEqual(len(errs), 3)


if __name__ == "__main__":
    unittest.main()
