import pytest


def test_support_create_ticket_and_status_flow(api_client):
    create = api_client.post(
        "/support/ticket",
        json={"subject": "Order delay", "message": "Please check where my order is."},
    )
    assert create.status_code in (200, 201)
    data = create.json()
    ticket_id = data.get("ticket_id")
    assert ticket_id is not None
    assert data.get("status") == "OPEN"

    list_res = api_client.get("/support/tickets")
    assert list_res.status_code == 200

    to_progress = api_client.put(f"/support/tickets/{ticket_id}", json={"status": "IN_PROGRESS"})
    assert to_progress.status_code == 200

    to_closed = api_client.put(f"/support/tickets/{ticket_id}", json={"status": "CLOSED"})
    assert to_closed.status_code == 200


def test_support_reject_subject_too_short(api_client):
    res = api_client.post(
        "/support/ticket",
        json={"subject": "abcd", "message": "valid"},
    )
    assert res.status_code == 400


def test_support_reject_message_too_long(api_client):
    msg = "b" * 501
    res = api_client.post(
        "/support/ticket",
        json={"subject": "Valid Subject", "message": msg},
    )
    assert res.status_code == 400


@pytest.mark.xfail(reason="Bug: OPEN ticket can be moved directly to CLOSED")
def test_support_invalid_status_transition_rejected(api_client):
    create = api_client.post(
        "/support/ticket",
        json={"subject": "Bad transition", "message": "Trying invalid transition path."},
    )
    assert create.status_code in (200, 201)
    ticket_id = create.json().get("ticket_id")
    assert ticket_id is not None

    bad = api_client.put(f"/support/tickets/{ticket_id}", json={"status": "CLOSED"})
    assert bad.status_code == 400


@pytest.mark.xfail(reason="Bug: CLOSED ticket can be moved back to IN_PROGRESS")
def test_support_reject_closed_to_in_progress(api_client):
    create = api_client.post(
        "/support/ticket",
        json={"subject": "Flow Test", "message": "state flow"},
    )
    assert create.status_code in (200, 201)
    ticket_id = create.json().get("ticket_id")
    assert ticket_id is not None

    p = api_client.put(f"/support/tickets/{ticket_id}", json={"status": "IN_PROGRESS"})
    c = api_client.put(f"/support/tickets/{ticket_id}", json={"status": "CLOSED"})
    assert p.status_code == 200
    assert c.status_code == 200

    back = api_client.put(f"/support/tickets/{ticket_id}", json={"status": "IN_PROGRESS"})
    assert back.status_code == 400


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"subject": "Valid Subject"},
        {"message": "Valid message for support"},
        {"subject": 12345, "message": "Valid message for support"},
        {"subject": "Valid Subject", "message": 12345},
        {"subject": " ", "message": " "},
    ],
)
def test_support_create_ticket_payload_variants_validation(api_client, payload):
    res = api_client.post("/support/ticket", json=payload)
    assert res.status_code == 400
