import pytest

from cats.signals.types import Message


@pytest.fixture
def sample_messages():
    return [
        Message(timestamp="2026-01-01T08:00:00+00:00", text="Il governo italiano annuncia nuovo piano economico."),
        Message(timestamp="2026-01-01T09:00:00+00:00", text="Protesta dei lavoratori in piazza a Roma."),
        Message(timestamp="2026-01-01T10:00:00+00:00", text="Il parlamento discute la legge di bilancio del governo."),
    ]


@pytest.fixture
def single_message():
    return [
        Message(timestamp="2026-01-01T08:00:00+00:00", text="Messaggio singolo di prova."),
    ]


@pytest.fixture
def many_messages():
    return [
        Message(
            timestamp=f"2026-01-{i+1:02d}T08:00:00+00:00",
            text=f"Messaggio numero {i+1} con contenuto variabile sulla politica italiana.",
        )
        for i in range(20)
    ]
