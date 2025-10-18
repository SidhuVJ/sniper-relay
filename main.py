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
