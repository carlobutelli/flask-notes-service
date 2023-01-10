#!/usr/bin/env python3
def test_ping(client):
    rv = client.get("/admin/ping")
    assert 200 == rv.status_code
    assert b"pong" in rv.data
