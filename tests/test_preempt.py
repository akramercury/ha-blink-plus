import asyncio, importlib.util, json, os, ssl, sys, types, time
TEST_DIR, IMMIS_PY = sys.argv[1], sys.argv[2]
state = {"port": None, "open": {}, "max_concurrent": 0, "stops": []}
api = types.ModuleType("blinkpy.api"); n = {"i": 0}
async def http_post(blink, url, data=None, **kw):
    n["i"] += 1
    cam = url.split("/")[-2]
    return {"command_id": 2000 + n["i"], "network_id": 42, "polling_interval": 2,
            "server": f"immis://127.0.0.1:{state['port']}/C{n['i']:03d}{cam}__IMDS_SER{cam}?client_id=1"}
async def request_command_status(b, net, cid):
    return {"status_code": 908, "commands": [{"id": cid, "state_condition": "running"}]}
async def request_command_done(b, net, cid): return {}
api.http_post, api.request_command_status, api.request_command_done = http_post, request_command_status, request_command_done
pkg = types.ModuleType("blinkpy"); pkg.api = api; sys.modules["blinkpy"] = pkg; sys.modules["blinkpy.api"] = api
spec = importlib.util.spec_from_file_location("immis", IMMIS_PY); immis = importlib.util.module_from_spec(spec); sys.modules["immis"] = immis; spec.loader.exec_module(immis)
data = open(os.path.join(TEST_DIR, "sample.ts"), "rb").read()

async def relay(reader, writer):
    h = await reader.readexactly(122); serial = h[8:24].rstrip(b"\0").decode()
    state["open"][serial] = state["open"].get(serial, 0) + 1
    state["max_concurrent"] = max(state["max_concurrent"], sum(state["open"].values()))
    async def read_client():
        try:
            while True:
                h2 = await reader.readexactly(9)
                ln = int.from_bytes(h2[5:9], "big")
                if ln: await reader.readexactly(ln)
                if h2[0] == 7:
                    state["stops"].append((serial, h2.hex()))
        except Exception:
            pass
    rt = asyncio.create_task(read_client())
    try:
        seq = 0
        while True:
            for off in range(0, len(data), 1316):
                p = data[off:off+1316]; seq += 1
                writer.write(bytes([0]) + seq.to_bytes(4, "big") + len(p).to_bytes(4, "big") + p)
                await writer.drain(); await asyncio.sleep(0.04)
    except (ConnectionError, OSError): pass
    finally:
        state["open"][serial] -= 1

class Cam:
    def __init__(s, name, cid): s.name, s.serial, s.network_id, s.camera_id, s.camera_type = name, None, "42", cid, ""
class U: base_url = "https://x"
class B: account_id = 1; urls = U()

async def viewer(url, secs):
    host, port = url.split("//")[1].split("/")[0].split(":")
    r, w = await asyncio.open_connection(host, int(port))
    w.write(b"GET /stream.ts HTTP/1.1\r\nHost: x\r\n\r\n"); await w.drain()
    got = 0; t0 = time.monotonic()
    try:
        while time.monotonic() - t0 < secs:
            chunk = await asyncio.wait_for(r.read(65536), secs)
            if not chunk: break
            got += len(chunk)
    except (TimeoutError, ConnectionError): pass
    w.close(); return got, round(time.monotonic() - t0, 1)

async def main():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH); ctx.load_cert_chain(f"{TEST_DIR}/cert.pem", f"{TEST_DIR}/key.pem")
    srv = await asyncio.start_server(relay, "127.0.0.1", 0, ssl=ctx); state["port"] = srv.sockets[0].getsockname()[1]
    preempted = []
    a = immis.BlinkLiveViewServer(B(), Cam("Front", "11"), linger=2); b = immis.BlinkLiveViewServer(B(), Cam("Backyard", "22"), linger=2)
    a.on_preempt = lambda: preempted.append("Front")
    await a.async_start(); await b.async_start()
    va = asyncio.create_task(viewer(a.url, 20))
    await asyncio.sleep(5)
    vb = asyncio.create_task(viewer(b.url, 8))
    ra = await va; rb = await vb
    print("Front viewer:", ra, "(should end ~5-7s, cut off by Backyard)")
    print("Backyard viewer:", rb, "bytes>0:", rb[0] > 0)
    print("preempted:", preempted, "max concurrent relay sessions:", state["max_concurrent"])
    r2 = await viewer(a.url, 3)
    print("Front reconnect within cooldown:", r2, "(should be 0 bytes)")
    await asyncio.sleep(4)
    print("active after viewers left:", a.active, b.active)
    print("STOP frames received by relay:", state["stops"])
    assert preempted == ["Front"], preempted
    assert state["max_concurrent"] == 1, "two live views ran on one sync module"
    assert rb[0] > 0, "second camera got no video"
    assert r2[0] < 200, "preempted camera restarted during cool-down"
    assert len(state["stops"]) == 2 and all(s[1] == "070000000100000000" for s in state["stops"])
    assert not a.active and not b.active
    await a.async_stop(); await b.async_stop(); srv.close()
asyncio.run(main())
print("PASS preempt")
