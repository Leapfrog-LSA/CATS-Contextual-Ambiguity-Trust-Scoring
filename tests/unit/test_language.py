from cats.pipeline.language import ITALIAN_MARKERS, detect_language
from cats.signals.types import Message


def _msgs(*texts):
    return [Message(timestamp=f"2026-01-{i + 1:02d}T08:00:00+00:00", text=t) for i, t in enumerate(texts)]


class TestDetectLanguage:
    def test_italian_prose(self):
        a = detect_language(
            _msgs(
                "Il governo ha annunciato che la riforma della giustizia sarà discussa in parlamento.",
                "I sindacati non sono d'accordo con il piano economico del ministero.",
                "La commissione ha approvato il bilancio per la città dopo una lunga discussione.",
            )
        )
        assert a.detected == "italian"
        assert a.marker_ratio >= 0.12
        assert a.confidence > 0

    def test_english_prose(self):
        a = detect_language(
            _msgs(
                "The government announced that the justice reform will be debated in parliament.",
                "Trade unions disagree with the treasury's new economic plan.",
                "The committee approved the city budget after a long discussion.",
            )
        )
        assert a.detected == "other"
        assert a.marker_ratio < 0.06

    def test_french_prose_is_other(self):
        # Romance neighbour: the marker set excludes shared articles/pronouns
        # (la/le/lo/si/del/una), so French does not accumulate marker hits.
        a = detect_language(
            _msgs(
                "Le gouvernement a annoncé que la réforme de la justice sera discutée au parlement.",
                "Les syndicats ne sont pas d'accord avec le plan économique du ministère.",
                "La commission a approuvé le budget de la ville après une longue discussion.",
            )
        )
        assert a.detected == "other"

    def test_spanish_prose_is_other(self):
        a = detect_language(
            _msgs(
                "El gobierno ha anunciado que la reforma de la justicia será discutida en el parlamento.",
                "Los sindicatos no están de acuerdo con el plan económico del ministerio.",
                "La comisión aprobó el presupuesto de la ciudad tras una larga discusión.",
            )
        )
        assert a.detected == "other"

    def test_non_latin_script(self):
        a = detect_language(
            _msgs(
                "Правительство объявило новый экономический план сегодня утром.",
                "Профсоюзы ответили угрозой всеобщей забастовки в стране.",
            )
        )
        assert a.detected == "other"
        assert a.metadata.get("reason") == "non_latin_script"
        assert a.latin_script_ratio < 0.5

    def test_insufficient_text_is_unknown(self):
        a = detect_language(_msgs("Ciao."))
        assert a.detected == "unknown"
        assert a.confidence == 0.0
        assert a.metadata.get("reason") == "insufficient_text"

    def test_as_dict_shape(self):
        flagged = detect_language(_msgs("Ciao.")).as_dict()
        assert set(flagged) == {"detected", "confidence", "marker_ratio", "latin_script_ratio", "reason"}
        clean = detect_language(
            _msgs("Il governo ha annunciato che la riforma della giustizia sarà discussa in parlamento oggi.")
        ).as_dict()
        assert set(clean) == {"detected", "confidence", "marker_ratio", "latin_script_ratio"}

    def test_marker_list_avoids_cross_language_collisions(self):
        # One-letter tokens and shared English/Romance function words must stay
        # out of the marker set, or foreign text accumulates spurious hits.
        assert not ITALIAN_MARKERS & {"come", "in", "a", "e", "i", "o", "la", "le", "lo", "si", "del", "una"}
