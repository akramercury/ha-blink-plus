"""End-to-end test of immis.py against a fake Blink IMMIS server + real ffmpeg."""

import asyncio
import importlib.util
import json
import os
import ssl
import subprocess
import sys
import types

TEST_DIR = sys.argv[1]
IMMIS_PY = sys.argv[2]
MODE = sys.argv[3] if len(sys.argv) > 3 else "token_ok"  # token_ok | null_only

calls = []
state = {"session_open": False, "headers": [], "port": None}

# ---- stub blinkpy.api ------------------------------------------------------
api = types.ModuleType("blinkpy.api")


async def http_post(blink, url, data=None, **kw):
    calls.append(("POST", url, json.loads(data) if data else None))
    if url.endswith("/liveview"):
        state["session_open"] = True
        n = sum(1 for c in calls if c[0] == "POST" and c[1].endswith("/liveview"))
        return {
            "command_id": 1000 + n,
            "network_id": 42,
            "server": f"immis://127.0.0.1:{state['port']}/CONNID{n:04d}__IMDS_G8T1ABCDEF?client_id=777",
            "polling_interval": 2,
            "duration": 30,
            "continue_interval": 30,
            "type": "lv" if n == 1 else "elv",
            "liveview_token": "TESTTOKEN_abc123",
        }
    return {}


async def request_command_status(blink, network, command_id):
    calls.append(("STATUS", command_id))
    cond = "running" if state["session_open"] else "done"
    return {"status_code": 908, "commands": [{"id": command_id, "state_condition": cond}]}


async def request_command_done(blink, network, command_id):
    calls.append(("DONE", command_id))
    return {}


api.http_post = http_post
api.request_command_status = request_command_status
api.request_command_done = request_command_done
pkg = types.ModuleType("blinkpy")
pkg.api = api
sys.modules["blinkpy"] = pkg
sys.modules["blinkpy.api"] = api

spec = importlib.util.spec_from_file_location("immis", IMMIS_PY)
immis = importlib.util.module_from_spec(spec)
sys.modules["immis"] = immis
spec.loader.exec_module(immis)


# ---- fake IMMIS server -----------------------------------------------------
async def immis_handler(reader, writer):
    header = await reader.readexactly(122)
    state["headers"].append(header)
    token_field = header[30:98]
    has_token = token_field[4:].strip(b"\x00") != b""
    if MODE == "null_only" and has_token:
        # Pretend the server ignores bad auth: keep socket open, send nothing.
        writer.close()  # relay hangs up on a bad token
        return
    data = open(os.path.join(TEST_DIR, "sample.ts"), "rb").read()
    seq = 0
    chunk = 188 * 7
    for off in range(0, len(data), chunk):
        payload = data[off : off + chunk]
        seq += 1
        writer.write(bytes([0]) + seq.to_bytes(4, "big") + len(payload).to_bytes(4, "big") + payload)
        if seq % 20 == 0:  # some non-video frame
            writer.write(bytes([0x12]) + seq.to_bytes(4, "big") + (4).to_bytes(4, "big") + b"abcd")
        await writer.drain()
        await asyncio.sleep(0.05)
    state["session_open"] = False
    writer.close()


class FakeCam:
    name = "Front Door"
    serial = "G8T1ABCDEF"
    network_id = "42"
    camera_id = "99"
    camera_type = "doorbell"


class FakeUrls:
    base_url = "https://rest-u1.immedia-semi.com"


class FakeBlink:
    account_id = 555
    urls = FakeUrls()


async def main():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(os.path.join(TEST_DIR, "cert.pem"), os.path.join(TEST_DIR, "key.pem"))
    srv = await asyncio.start_server(immis_handler, "127.0.0.1", 0, ssl=ctx)
    state["port"] = srv.sockets[0].getsockname()[1]
    immis.FIRST_DATA_TIMEOUT = 25

    live = immis.BlinkLiveViewServer(FakeBlink(), FakeCam(), linger=2, max_minutes=10)
    await live.async_start()
    out = os.path.join(TEST_DIR, f"out_{MODE}.ts")
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-loglevel", "error", "-y", "-i", live.url, "-t", "10", "-c", "copy", out,
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    import time as _t; t0 = _t.monotonic()
    _, err = await asyncio.wait_for(proc.communicate(), 90)
    print("ffmpeg wall time %.1fs, url %s" % (_t.monotonic() - t0, live.url))
    print("ffmpeg rc", proc.returncode, err.decode()[-300:])
    await asyncio.sleep(4)  # linger -> session should end
    print("state after viewers left:", live.stats.as_dict())
    await live.async_stop()
    srv.close()

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
         "-show_entries", "stream=codec_name,width,height,nb_read_frames", "-of", "json", out],
        capture_output=True, text=True,
    )
    print("ffprobe:", probe.stdout.replace("\n", " "))
    frames = int(json.loads(probe.stdout)["streams"][0]["nb_read_frames"])
    stats = live.stats.as_dict()
    assert proc.returncode == 0, "ffmpeg failed"
    assert frames > 100, f"only {frames} frames decoded"
    assert stats["live_view_sessions"] == 2, "extended_liveview hand-off did not happen"
    assert stats["live_view_state"] == "idle", "session did not end after viewer left"
    assert stats["live_view_token_used"] is (MODE == "token_ok")
    lv = [c for c in calls if c[0] == "POST" and c[1].endswith("/liveview")]
    print("liveview requests:", [(c[1].split("/api/")[1], c[2]["intent"]) for c in lv])
    print("done calls:", [c for c in calls if c[0] == "DONE"])
    for h in state["headers"]:
        tok = h[34:98].rstrip(b"\x00")
        print("auth header len", len(h), "magic", h[:4].hex(), "serial", h[8:24].rstrip(b"\x00"),
              "client_id", int.from_bytes(h[24:28], "big"), "token", tok or None,
              "conn", h[102:118].rstrip(b"\x00"), "trailer", h[118:].hex())


asyncio.run(main())
print("PASS", MODE)
