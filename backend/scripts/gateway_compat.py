import json
import httpx

_original_json = httpx.Response.json


def _tolerant_json(self, **kwargs):
    try:
        return _original_json(self, **kwargs)
    except json.JSONDecodeError:
        text = self.text.lstrip("\ufeff \t\r\n")
        if text.startswith("data:"):
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("data:"):
                    payload = line[5:].strip()
                    if payload and payload != "[DONE]":
                        return json.loads(payload)
            raise
        value, _ = json.JSONDecoder().raw_decode(text)
        return value


httpx.Response.json = _tolerant_json