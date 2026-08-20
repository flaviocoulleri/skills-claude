---
name: pc-voice-elevenlabs-agent-builder
description: 'Build, configure, and optimize ElevenLabs conversational voice agents via direct HTTP calls to the ElevenLabs REST API (/v1/convai/agents). Use whenever the user wants to create or improve a voice assistant, customer-service voice bot, phone or IVR agent, or interactive voice character on ElevenLabs: writing the system prompt, choosing the voice and TTS model, tuning temperature, turn-taking and interruptions, attaching server-side webhook tools, and setting guardrails, then deploying every change straight to the platform. Trigger when the user says things like "crea un agente de voz en ElevenLabs", "configura mi agente conversacional", "mejora el prompt de mi bot de voz", "cambia la voz del agente", "build a voice agent", or pastes an ElevenLabs agent_id. Server-side only: no client tools, no outbound calls, no widget embedding, no CLI or SDKs. Works in English and Spanish.'
license: MIT
compatibility: Requires internet access and an ElevenLabs API key (ELEVENLABS_API_KEY).
metadata: {"version": "1.1.0", "last_modified": "2026-06-30", "openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs Voice Agent Builder

Design, deploy, and tune production-grade conversational **voice agents** on the ElevenLabs
platform by making **direct HTTP requests** to the `/v1/convai/agents` API. The entire agent
— its system prompt, voice, LLM, turn-taking, server tools, and guardrails — lives in one
configuration object that you create and patch over REST. There is no separate runtime to
host: once you `POST`/`PATCH` the config, the agent is live on ElevenLabs.

This skill is scoped tightly to **building the agent itself**. The following are **out of
scope by design** — do not pursue them and steer the user back to agent configuration if they
drift there:

- ❌ **Client-side tools** (tools that execute in a browser) — only server-side `webhook` tools.
- ❌ **Outbound calls / Twilio dialing** — this skill configures the agent, not telephony campaigns.
- ❌ **Web widget embedding** (`<elevenlabs-convai>`, React/JS client SDKs) — delivery is the app team's job.
- ❌ **ElevenLabs CLI and language SDKs** (Python/JS) — every operation is a raw HTTP call.

---

## How this skill operates — golden rules

Follow these on every task. They prevent the most common ways agent configs get silently corrupted.

1. **The platform is the source of truth.** Before you change an existing agent, `GET` it.
   Reason about the *current* config, not what you assume is there.
2. **`PATCH` is a partial merge, but arrays replace wholesale.** Scalar fields you omit are
   left untouched. But `tools`, `knowledge_base`, `built_in_tools`, and `guardrails.*` are
   **replaced**, not merged. To add one tool, `GET` the agent, append to the existing array,
   and `PATCH` the **full** array back. Never `PATCH` a lone tool — you will delete the rest.
3. **Always create with versioning on:** `POST .../agents/create?enable_versioning=true`.
   Every later change becomes revertible. Tag agents (`"tags": ["production"]` / `["test"]`).
4. **Write big bodies to a file, send with `-d @body.json`.** System prompts contain
   newlines and quotes; inline `-d '{...}'` corrupts them. Author the JSON in a file, validate
   it, then `curl ... -d @body.json`. This is the single biggest source of broken requests.
5. **Never print, log, or hardcode the API key or tool secrets.** Read the key from
   `$ELEVENLABS_API_KEY`. For tool auth, reference a workspace secret/env var label, not a literal token.
6. **Verify IDs against the live catalog.** Model and voice IDs change. Confirm LLM IDs with
   `GET /v1/convai/llm/list` and voice IDs with `GET /v1/voices` before putting them in a config.
7. **Confirm before destructive actions.** Never `DELETE` an agent without explicit user confirmation.
8. **After every create/update, read the result back** (use the response body, or `GET` the
   agent) and tell the user exactly what is now configured — don't assume the write applied as intended.

---

## 1. Prerequisites

| Requirement | Detail |
|-------------|--------|
| **API key** | An ElevenLabs API key with Conversational AI access, exported as `ELEVENLABS_API_KEY`. Get one at `https://elevenlabs.io/app/settings/api-keys`. |
| **HTTP client** | `curl` (used in all examples) or any tool that can send HTTPS requests. |
| **Account** | A workspace with the Agents / Conversational AI product enabled. |

Auth is sent on **every** request via the `xi-api-key` header. Establish these once:

```bash
export ELEVENLABS_API_KEY="sk_..."     # never echo this value back to the user
BASE="https://api.elevenlabs.io"
```

If `$ELEVENLABS_API_KEY` is missing, stop and ask the user to provide/export it before calling the API.

---

## 2. The API surface

All endpoints are under `https://api.elevenlabs.io`. Auth header: `xi-api-key: $ELEVENLABS_API_KEY`.

| Operation | Method & Endpoint |
|-----------|-------------------|
| List available LLMs | `GET /v1/convai/llm/list` |
| List voices | `GET /v1/voices` |
| Search the shared voice library | `GET /v1/shared-voices?language=es&page_size=20` |
| **Create agent** | `POST /v1/convai/agents/create?enable_versioning=true` |
| **Get agent** | `GET /v1/convai/agents/{agent_id}` |
| **List agents** | `GET /v1/convai/agents` |
| **Update agent** | `PATCH /v1/convai/agents/{agent_id}` |
| **Delete agent** | `DELETE /v1/convai/agents/{agent_id}` |
| Create a standalone (reusable) tool | `POST /v1/convai/tools` |
| Create a test | `POST /v1/convai/agent-testing/create` |
| Simulate a conversation | `POST /v1/convai/agents/{agent_id}/simulate-conversation` |

> The whole agent is one JSON object with three top-level parts: `name` (+ `tags`),
> `conversation_config` (the live behavior), and `platform_settings` (security, limits,
> guardrails). Everything below configures pieces of that object.

---

## Core Capabilities

Each capability below is a named operation the model performs by issuing one HTTP request with
a raw JSON payload. The named "functions" (`create_agent`, `update_agent_prompt`,
`configure_agent_voice`, …) are conventions — they all map to the create/patch endpoints above
with a specific slice of the config object.

### `discover_models_and_voices` — know your options before configuring

```bash
curl -s "$BASE/v1/convai/llm/list" -H "xi-api-key: $ELEVENLABS_API_KEY"
curl -s "$BASE/v1/voices"          -H "xi-api-key: $ELEVENLABS_API_KEY"
```

`llm/list` returns each model's deprecation state, context limits, and capability flags. From
`/v1/voices`, read each voice's `labels` (language, accent, age, use case) to pick one that
**natively supports Spanish** — see [Choosing voice + TTS model](#choosing-the-voice--tts-model).

### `create_agent` — the foundational call

`POST /v1/convai/agents/create?enable_versioning=true`. Write the body to `agent.json`, then:

```bash
curl -s -X POST "$BASE/v1/convai/agents/create?enable_versioning=true" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d @agent.json
```

Minimal valid `agent.json` (Spanish-speaking agent, English system prompt):

```json
{
  "name": "Mi Asistente",
  "tags": ["test"],
  "conversation_config": {
    "agent": {
      "first_message": "¡Hola! Soy tu asistente. ¿En qué te puedo ayudar?",
      "language": "es",
      "prompt": {
        "prompt": "You are a helpful assistant. Always reply in neutral Latin American Spanish, in 1-3 short spoken sentences. Never use markdown or emojis.",
        "llm": "gemini-2.5-flash",
        "temperature": 0.3,
        "max_tokens": 250
      }
    },
    "tts": {
      "voice_id": "REPLACE_WITH_SPANISH_VOICE_ID",
      "model_id": "eleven_flash_v2_5"
    }
  }
}
```

The response includes the new `agent_id`. Capture it — every later operation needs it.

### `get_agent` / `list_agents` — read current state

```bash
curl -s "$BASE/v1/convai/agents/{agent_id}" -H "xi-api-key: $ELEVENLABS_API_KEY"
curl -s "$BASE/v1/convai/agents"            -H "xi-api-key: $ELEVENLABS_API_KEY"
```

Always `get_agent` before editing so your `PATCH` is built on the real config.

### `update_agent` — partial updates (the workhorse)

`PATCH /v1/convai/agents/{agent_id}` with only the slice you're changing. Common named patterns:

**`update_agent_prompt`** — change instructions, model, temperature, token cap:

```json
{
  "conversation_config": {
    "agent": {
      "prompt": {
        "prompt": "<full new English system prompt>",
        "llm": "claude-haiku-4-5",
        "temperature": 0.4,
        "max_tokens": 200
      }
    }
  }
}
```

**`configure_agent_voice`** — voice, TTS model, and delivery characteristics:

```json
{
  "conversation_config": {
    "tts": {
      "voice_id": "EXAVITQu4vr4xnSDxMaL",
      "model_id": "eleven_flash_v2_5",
      "stability": 0.5,
      "similarity_boost": 0.8,
      "speed": 1.0
    }
  }
}
```

**`tune_turn_taking`** — responsiveness and interruption behavior:

```json
{
  "conversation_config": {
    "agent": { "disable_first_message_interruptions": true },
    "turn": { "turn_eagerness": "patient", "turn_timeout": 8 }
  }
}
```

**`set_first_message`** — the spoken greeting (always in Spanish):

```json
{ "conversation_config": { "agent": { "first_message": "¡Bienvenido de nuevo! ¿Continuamos?" } } }
```

Send any of these with:

```bash
curl -s -X PATCH "$BASE/v1/convai/agents/{agent_id}" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d @patch.json
```

### `add_server_tool` — give the agent a server-side (webhook) action

Server tools let the agent call your HTTPS API mid-conversation (look up an order, check a
balance). They live in `conversation_config.agent.prompt.tools`. **Remember rule #2:** `GET`
the agent, append to the existing `tools` array, and `PATCH` the full array back.

```json
{
  "type": "webhook",
  "name": "get_account_status",
  "description": "Look up the customer's current plan, balance, and service status by account ID. Call this before stating any account detail; never invent account data.",
  "api_schema": {
    "url": "https://api.example.com/v1/accounts/status",
    "method": "POST",
    "request_headers": [
      { "name": "Authorization", "secret": { "env_var_label": "accounts_api_key" } }
    ],
    "request_body_schema": {
      "type": "object",
      "properties": {
        "account_id": { "type": "string", "description": "Customer account identifier" }
      },
      "required": ["account_id"]
    }
  }
}
```

Notes that decide whether the tool actually works:
- The `description` is read by the LLM to decide **when** to call it — write it as a usage instruction, not a label.
- Every property `description` tells the model **how to fill** the argument. Be explicit.
- URLs must be **HTTPS**. Reference secrets via `env_var_label`, never inline a token.
- Built-in system tools are different: set them under `prompt.built_in_tools`
  (`end_call`, `language_detection`, `skip_turn`, `transfer_to_agent`). `{}` enables defaults; omit to disable.

#### Inline tools vs. standalone (referenced) tools

Two valid ways to attach a server tool — both are server-side webhooks, only the attachment differs:

- **Inline** (`prompt.tools[]`, shown above) — the full definition lives inside the agent. Simplest; best when **one** agent uses the tool.
- **Standalone / referenced** (`prompt.tool_ids[]`) — create the tool once as its own object, then attach it to any number of agents by ID. Best when the **same tool is reused across several agents** or is managed centrally; it is also how platform integration tools attach.

Create the reusable tool once (`tool.json` — confirm the exact `tool_config` wrapper against the API reference), then reference its `tool_id`:

```bash
curl -s -X POST "$BASE/v1/convai/tools" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d @tool.json          # response includes "tool_id": "tool_xxxx"
```

```json
{ "tool_config": { "type": "webhook", "name": "get_account_status", "description": "Look up the customer's plan and balance. Call this before stating any account detail; never invent account data.", "api_schema": { "url": "https://api.example.com/v1/accounts/status", "method": "POST", "request_body_schema": { "type": "object", "properties": { "account_id": { "type": "string", "description": "Customer account identifier" } }, "required": ["account_id"] } } } }
```

Attach by ID — `tool_ids` is **also** a full array, so `GET` the agent, append, and `PATCH` the whole list (rule #2):

```json
{ "conversation_config": { "agent": { "prompt": { "tool_ids": ["tool_xxxx"] } } } }
```

**Pick one:** single agent / one-off → inline `tools`; reused across agents or centrally managed → `tool_ids`. Don't define the same webhook both inline and as a referenced tool — that duplicates it.

### `test_agent` — validate before/after changes

Two API-direct ways to exercise an agent without a phone or browser:

1. **Ad-hoc simulation** — `POST /v1/convai/agents/{agent_id}/simulate-conversation` runs the
   agent against a simulated user persona and returns the transcript so you can judge behavior.
   (Confirm the exact request body in the API reference before relying on it in automation.)
2. **Repeatable tests** — `POST /v1/convai/agent-testing/create` creates a saved test, then
   attach it to the agent via `PATCH ... platform_settings.testing.attached_tests`. Test types:
   `llm` (does it respond appropriately to a message?), `tool` (right tool, right params?),
   `simulation` (multi-turn flow with a simulated user). Eval strategies: `exact`, `regex`, `llm`.

After any optimization (prompt, temperature, voice, turn-taking), re-run a simulation and
compare transcripts — that's how you *show* the change helped instead of guessing.

### `delete_agent` — remove an agent (destructive)

```bash
curl -s -X DELETE "$BASE/v1/convai/agents/{agent_id}" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

Only after explicit user confirmation. Prefer disabling/retagging over deleting in production.

---

## 3. Instructions & Best Practices

This is the core value of the skill: it knows how to design a **voice** agent, which is very
different from a chat bot. Internalize the ElevenLabs prompting guide
(`https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide`) as the rules below.

### The system prompt: six-block structure

Section the system prompt with markdown headings. The model prioritizes and follows
instructions far more reliably when they're grouped into these six blocks. Keep each block
short and action-based.

```
# Personality   – Named character. 2-3 defining traits. Role and who they represent.
# Environment   – Voice/phone channel; the user can't see a screen; the agent can't see the user.
# Tone          – How they speak (4-6 bullets). Voice-specific formatting rules go here.
# Goal          – What success looks like. Number the steps for multi-step flows.
# Guardrails    – Topics to avoid, what never to invent, how to handle uncertainty/sensitive data.
# Tools         – Which tools exist, exactly when to call each, and the fallback when one fails.
```

Mark genuinely critical steps with a short cue like "This step is important." For hard
safety/refusal rules, **also** configure independent [Guardrails](#guardrails) in
`platform_settings` — never rely on the prompt alone for compliance-grade boundaries.

### Writing for voice (these rules matter more than anything)

The output is **spoken aloud**, not read. Bake these into the `# Tone` block of every prompt:

- **Be brief.** 1-3 short sentences per turn. Voice users can't skim or re-read; a long answer is a wall the user must wait through. Cap it with `max_tokens` (~150-250) as a backstop.
- **No visual formatting.** No markdown, bullet lists, headings, emojis, asterisks, or code — the TTS engine would read the symbols literally or stumble.
- **Speak numbers and symbols the way a person says them.** Tell the agent: "1500" → "mil quinientos"; "$99.90" → "noventa y nueve pesos con noventa centavos"; "03/05" → "tres de mayo"; read phone numbers and emails digit-by-digit / letter-by-letter.
- **Use natural spoken connectors,** not written transitions: "A ver…", "Perfecto", "Claro que sí", "Déjame revisar". This makes the agent sound human and buys micro-pauses.
- **Acknowledge waits out loud.** "Permíteme un segundo" instead of going silent while a tool runs.
- **Handle interruptions gracefully.** If the user cuts in, the agent should adapt to the new input rather than finish its scripted sentence or repeat itself.
- **Pronunciation.** For brand names, product names, or tricky terms, give the agent a phonetic hint in the prompt, or attach a pronunciation dictionary in `tts.pronunciation_dictionary_locators`.

### The English-prompt / Spanish-speech pattern (default for this skill)

Default workflow for this user's agents: **write the system prompt in English** (LLMs follow
instructions with higher fidelity in English) while the agent **speaks Latin American Spanish**.
To make that reliable, every prompt must:

1. Set `conversation_config.agent.language` to `"es"`.
2. Write `first_message` and any literal example phrases the user will hear **in Spanish**.
3. Put an explicit, non-negotiable output-language instruction in the English `# Tone` block:
   > *"Speak ONLY in neutral Latin American Spanish, regardless of the language the user writes
   > or speaks in, unless the user clearly and deliberately switches languages."*
4. Optionally enable `built_in_tools.language_detection` if some callers may switch languages and you want graceful handling.

This separation is intentional — keep instructions in English, keep everything the customer hears in Spanish.

### Choosing the LLM, temperature, and token cap

| Field | Guidance |
|-------|----------|
| `llm` | For real-time voice, prioritize **low latency**. Good Spanish + fast: `gemini-2.5-flash`, `gemini-2.0-flash`. Ultra-low latency: `gemini-2.0-flash-lite` or ElevenLabs-hosted models. Stronger reasoning for complex flows (accept higher latency): `gpt-5`, `claude-sonnet-4-5`. Always confirm IDs via `GET /v1/convai/llm/list`. |
| `temperature` | Voice agents ramble at high temperature. **Support / transactional / regulated: 0.1-0.4.** General assistant: 0.4-0.6. Character / creative: 0.7-0.9. Default to **0.3** for business agents. |
| `max_tokens` | Cap response length to enforce brevity: **150-250** for most voice agents. Lower = snappier, less rambling. |
| `backup_llm_config` + `cascade_timeout_seconds` | Set a fallback model so a provider slowdown doesn't kill the call. `cascade_timeout_seconds` (2-15, default 8) is how long to wait before cascading. |

### Choosing the voice + TTS model

- **The voice must natively support Spanish.** Don't assume an English-named demo voice sounds
  good in Spanish — many carry an accent. Discover proper voices with
  `GET /v1/shared-voices?language=es` (voice library) or inspect `labels` from `GET /v1/voices`,
  and confirm the choice with the user.
- **TTS model** (`tts.model_id`):

  | Model | When |
  |-------|------|
  | `eleven_flash_v2_5` | **Default for real-time Spanish agents** — 32 languages incl. Spanish, ~75 ms latency. |
  | `eleven_turbo_v2_5` | More expressive, still 32 languages, ~250-300 ms. |
  | `eleven_multilingual_v2` | Highest fidelity (29 languages) when latency is less critical. |
  | `eleven_v3_conversational` | Most expressive, 70+ languages. |

- **Delivery knobs:** `stability` (0-1; lower = more expressive, higher = more consistent — start ~0.5), `similarity_boost` (~0.8), `speed` (0.7-1.2; keep ~1.0, drop slightly only if Spanish clarity needs it).

### Turn-taking & interruptions

These control how the conversation *feels* and directly answer the user's "interruption thresholds":

| Field (`conversation_config.turn` / `agent`) | Effect |
|-----------|--------|
| `turn_eagerness` | `patient` (waits longer — best when users pause to think, e.g. giving an account number), `normal` (default), `eager` (jumps in fast — best for snappy assistants). |
| `turn_timeout` | Seconds to wait before re-engaging a silent user. Default 7; raise for forms/IVR, lower for quick Q&A. |
| `agent.disable_first_message_interruptions` | Set `true` so callers can't talk over an important greeting/disclaimer. |
| `turn.silence_end_call_timeout` | Seconds of silence before ending the call (`-1` = off). |
| `vad` | Voice-activity-detection config governs barge-in sensitivity (how easily user speech interrupts the agent). Confirm exact fields in the config reference before tuning. |

### Latency optimization (a voice agent that lags feels broken)

Stack these: `eleven_flash_v2_5` TTS · a fast `llm` · `tts.optimize_streaming_latency` (0-4,
higher = faster) · a tight `max_tokens` · a `backup_llm_config`. Measure with a simulation, not vibes.

### Guardrails

Compliance-grade boundaries belong in `platform_settings.guardrails`, which runs **independently
of the LLM** — not in the prompt (a prompt can be talked around). Use `version: "1"`.

```json
{
  "platform_settings": {
    "guardrails": {
      "version": "1",
      "focus": { "is_enabled": true },
      "prompt_injection": { "is_enabled": true },
      "content": { "config": { "harassment": { "is_enabled": true, "threshold": 0.5 } } },
      "custom": {
        "config": {
          "configs": [{
            "is_enabled": true,
            "name": "No financial advice",
            "prompt": "Block the agent from giving personalized investment or financial advice.",
            "execution_mode": "blocking",
            "trigger_action": { "type": "retry", "feedback": "Reason: {{trigger_reason}}" }
          }]
        }
      }
    }
  }
}
```

All agents benefit from `focus` + `prompt_injection` + 2-4 `custom` rules. Add `content`
categories per vertical (e.g., `medical_and_legal_information` for healthcare/finance/legal).
See `references/config-schema.md` for the full guardrails and privacy schema.

---

## 4. Workflow Examples

### A. Build a Spanish customer-support voice agent, end-to-end

**Step 1 — Discover options.** `GET /v1/convai/llm/list` and `GET /v1/shared-voices?language=es`.
Confirm a fast LLM and a Spanish-native voice with the user.

**Step 2 — Author `agent.json`** (prompt in English, agent speaks Spanish):

```json
{
  "name": "Soporte - Aurora Telecom",
  "tags": ["test"],
  "conversation_config": {
    "agent": {
      "first_message": "¡Hola! Gracias por comunicarte con Aurora Telecom. Soy Lucía. ¿En qué te puedo ayudar hoy?",
      "language": "es",
      "disable_first_message_interruptions": false,
      "prompt": {
        "prompt": "# Personality\nYou are Lucía, a warm, competent customer-support agent for Aurora Telecom, a Latin American internet provider. You are patient and solution-oriented.\n\n# Environment\nYou are on a live voice call. The customer cannot see any screen, and you cannot see them — communicate everything by voice.\n\n# Tone\n- Speak ONLY in neutral Latin American Spanish, regardless of the language the customer uses, unless they clearly switch languages.\n- Keep every reply to 1-3 short spoken sentences. Never monologue.\n- Sound natural: use connectors like \"A ver…\", \"Perfecto\", \"Claro que sí\", \"Déjame revisar\".\n- Never use markdown, bullet points, emojis, or symbols — your words are read aloud.\n- Say numbers and money as a person would: \"1500\" → \"mil quinientos pesos\"; \"$99.90\" → \"noventa y nueve pesos con noventa centavos\". Read phone numbers and emails digit by digit.\n- If you need a moment, say \"Permíteme un segundo\" instead of going silent.\n\n# Goal\nResolve the customer's issue efficiently:\n1. Greet and identify what they need.\n2. For anything about their account, call get_account_status to fetch real data BEFORE answering. This step is important — never invent account details.\n3. Confirm the resolution and ask if there is anything else.\n4. Close warmly.\n\n# Guardrails\n- Only discuss Aurora Telecom products, billing, and technical support; politely redirect off-topic requests.\n- Never invent prices, balances, dates, or policies. If unsure or a tool fails, say you will escalate to a human.\n- Never read full payment card numbers aloud.\n\n# Tools\n- get_account_status: look up the customer's plan and balance. Call it before stating any account detail.\n- end_call: use only after the customer confirms they need nothing else.",
        "llm": "gemini-2.5-flash",
        "temperature": 0.3,
        "max_tokens": 250,
        "built_in_tools": { "end_call": {}, "language_detection": {} }
      }
    },
    "tts": {
      "voice_id": "REPLACE_WITH_SPANISH_VOICE_ID",
      "model_id": "eleven_flash_v2_5",
      "stability": 0.5,
      "similarity_boost": 0.8,
      "speed": 1.0
    },
    "asr": { "quality": "high", "keywords": ["Aurora Telecom", "fibra", "megabits"] },
    "turn": { "turn_eagerness": "normal", "turn_timeout": 7 },
    "conversation": { "max_duration_seconds": 900 }
  },
  "platform_settings": {
    "summary_language": "es",
    "guardrails": {
      "version": "1",
      "focus": { "is_enabled": true },
      "prompt_injection": { "is_enabled": true }
    }
  }
}
```

**Step 3 — Create it:**

```bash
curl -s -X POST "$BASE/v1/convai/agents/create?enable_versioning=true" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d @agent.json
```

**Step 4 — Simulate & review.** `POST /v1/convai/agents/{agent_id}/simulate-conversation` with a
support-style persona; read the transcript. Check: Does it stay in Spanish? Are replies short?
Does it call the tool before quoting account data?

**Step 5 — Iterate** with targeted `PATCH`es (see B and C). When happy, retag to `["production"]`.

### B. Add a server tool to an existing agent

**Step 1 — `GET` the agent** and copy the current `conversation_config.agent.prompt.tools` array
(it may be empty or already populated).

**Step 2 — Append** the new `get_account_status` webhook tool (from
[`add_server_tool`](#add_server_tool--give-the-agent-a-server-side-webhook-action)) to that array.

**Step 3 — `PATCH` the full array back** (omitting existing tools here would delete them):

```json
{ "conversation_config": { "agent": { "prompt": { "tools": [ /* ...existing tools..., */ { "type": "webhook", "name": "get_account_status", "description": "...", "api_schema": { "...": "..." } } ] } } } }
```

**Step 4 — Update the `# Tools` block** of the prompt so the agent knows when to call it, then simulate again.

### C. Optimize a verbose / high-latency agent

Symptom: replies are too long and there's a lag before the agent speaks.

1. `GET` the agent to see the current `prompt`, `tts.model_id`, `llm`, `temperature`, `max_tokens`.
2. Diagnose: verbosity → high `temperature` and/or no `max_tokens`; lag → slow `llm` or a heavy TTS model.
3. `PATCH` the fix:

```json
{
  "conversation_config": {
    "agent": { "prompt": { "llm": "gemini-2.0-flash", "temperature": 0.2, "max_tokens": 150 } },
    "tts":   { "model_id": "eleven_flash_v2_5", "optimize_streaming_latency": 4 }
  }
}
```

4. Add a `# Tone` reminder ("Keep every reply to 1-2 sentences") if brevity is still an issue.
5. Re-simulate and compare transcripts/latency to confirm the improvement before declaring it fixed.

---

## Reference

- **`references/config-schema.md`** — Exhaustive field-by-field schema for `conversation_config`
  (`agent`, `prompt`, `tts`, `asr`, `turn`, `conversation`, `vad`) and `platform_settings`
  (`auth`, `call_limits`, `guardrails`, `privacy`), the full TTS-model and LLM-provider tables,
  and the complete list of updatable fields. Read it whenever you need a parameter not covered above.
- ElevenLabs prompting guide: `https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide`
- ElevenLabs API reference: `https://elevenlabs.io/docs/api-reference/introduction`

## Error handling

Common HTTP statuses: **401** invalid/missing key · **404** agent not found (check `agent_id`)
· **422** invalid config (read the response body — it names the offending field) · **429** rate
limit (back off and retry). On `422`, fix the specific field it reports rather than resending blindly.
