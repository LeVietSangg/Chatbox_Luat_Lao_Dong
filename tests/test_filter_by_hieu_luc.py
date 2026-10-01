import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from retriever import LegalRetriever


class TestFilterByHieuLuc:
    """Kiểm thử tầng lọc hiệu lực văn bản (filter_by_hieu_luc)."""

    def test_filter_con_hieu_luc(self):
        sample_results = [
            {
                "provision_id": "45_2019_QH14__D113__K1",
                "content": {"hieu_luc": "con_hieu_luc", "van_ban": "Bộ luật Lao động 2019"},
                "score": 0.85
            },
            {
                "provision_id": "10_2012_QH13__D111__K1",
                "content": {"hieu_luc": "het_hieu_luc", "van_ban": "Bộ luật Lao động 2012"},
                "score": 0.90
            },
            {
                "provision_id": "145_2020_NDCP__D10__K1",
                "content": {"hieu_luc": "con_hieu_luc", "van_ban": "Nghị định 145/2020/NĐ-CP"},
                "score": 0.70
            }
        ]

        filtered = LegalRetriever.filter_by_hieu_luc(sample_results, "con_hieu_luc")
        assert len(filtered) == 2
        assert all(r["content"]["hieu_luc"] == "con_hieu_luc" for r in filtered)
        assert "10_2012_QH13__D111__K1" not in [r["provision_id"] for r in filtered]

    def test_filter_het_hieu_luc(self):
        sample_results = [
            {
                "provision_id": "45_2019_QH14__D113__K1",
                "content": {"hieu_luc": "con_hieu_luc"},
                "score": 0.85
            },
            {
                "provision_id": "10_2012_QH13__D111__K1",
                "content": {"hieu_luc": "het_hieu_luc"},
                "score": 0.90
            }
        ]

        filtered = LegalRetriever.filter_by_hieu_luc(sample_results, "het_hieu_luc")
        assert len(filtered) == 1
        assert filtered[0]["provision_id"] == "10_2012_QH13__D111__K1"

    def test_filter_empty_list(self):
        assert LegalRetriever.filter_by_hieu_luc([], "con_hieu_luc") == []
