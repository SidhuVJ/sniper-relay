from fastapi import FastAPI, Request
import httpx, os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

app = FastAPI()

@app.post("/tv")
async def tv_alert(request: Request):
    data = await request.json()
    symbol = data.get("symbol")
    flowconv = float(data.get("flowconv", 0))
    atr1 = float(data.get("atr1", 0))
    atr14 = float(data.get("atr14", 1))
    qualifies = atr1 >= 1.2 * atr14 and flowconv >= 3
    color = 0x00FF7F if qualifies else 0xCC3333
    embed = {
        "title": f"{'A+' if flowconv>=5 else 'A'} Setup — {symbol}",
        "description": "Auto-check via Aladdin v18.1",
        "color": color,
        "fields": [
            {"name":"ATR Gate","value":str(atr1>=1.2*atr14)},
            {"name":"FlowConv","value":str(flowconv)}
        ]
    }
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK, json={"embeds":[embed]})
    return {"ok": True}

# --- add this to bottom of main.py ---
import os
from fastapi.middleware.cors import CORSMiddleware

# Optional CORS (lets TradingView post from its domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))   # Render gives this dynamically
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
from fastapi import FastAPI, Request, HTTPException
import httpx, os

app = FastAPI()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
TV_SECRET = os.getenv("TV_SECRET")  # optional shared secret

@app.get("/healthz")
async def health():
    return {"status": "ok"}

@app.post("/tv")
async def tv_alert(request: Request):
    payload = await request.json()
    # optional guard
    if TV_SECRET and payload.get("secret") != TV_SECRET:
        raise HTTPException(status_code=403, detail="invalid secret")

    symbol = payload.get("symbol")
    flowconv = float(payload.get("flowconv", 0))
    atr1 = float(payload.get("atr1", 0))
    atr14 = float(payload.get("atr14", 1))

    qualifies = (atr1 >= 1.2 * atr14) and (flowconv >= 3)
    color = 0x00FF7F if (qualifies and flowconv >= 5) else 0xFFA500 if qualifies else 0xCC3333
    embed = {
        "title": f"{'A+' if flowconv>=5 else 'A'} Setup — {symbol}",
        "description": "Auto-check via Aladdin v18.1",
        "color": color,
        "fields": [
            {"name": "ATR Gate", "value": str(atr1 >= 1.2*atr14)},
            {"name": "FlowConv", "value": str(flowconv)}
        ]
    }
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(https://sniper-relay-l7x5.onrender.com/, json={"embeds": [embed]})
    return {"ok": True}

# keep existing __main__ uvicorn run block you added


