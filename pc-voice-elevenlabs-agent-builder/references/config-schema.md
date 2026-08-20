# Agent Configuration Schema (API-direct)

Complete reference for the JSON object you `POST`/`PATCH` to `/v1/convai/agents`. Everything
here is sent as raw JSON over HTTP — no SDK or CLI. Read this when SKILL.md doesn't cover a
specific field.

## Top-level object

```json
{
  "name": "My Agent",
  "tags": ["production"],
  "conversation_config": {
    "agent":        { "first_message": "...", "language": "es", "prompt": { "...": "..." } },
    "tts":          { "...": "..." },
    "asr":          { "...": "..." },
    "turn":         { "...": "..." },
    "conversation": { "...": "..." },
    "vad":          { "...": "..." },
    "language_presets": { "...": "..." }
  },
  "platform_settings": { "...": "..." },
  "workflow": { "...": "..." }
}
```

| Top-level field | Purpose |
|-----------------|---------|
| `name` | Display name. |
| `tags` | Classification labels for filtering (e.g. `["production"]`, `["test"]`). |
| `conversation_config` | Real-time conversation behavior (the agent itself). |
| `platform_settings` | Security, limits, guardrails, privacy, analysis language. |
| `workflow` | Optional multi-step conversation flow with branching (advanced). |

---

## conversation_config.agent

```json
{
  "first_message": "¡Hola! ¿En qué te ayudo?",
  "language": "es",
  "disable_first_message_interruptions": false,
  "prompt": { "...": "..." }
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `first_message` | string | `""` | Spoken greeting when the conversation starts. Keep it short and in the agent's language. |
| `language` | string | `"en"` | ISO 639-1 code. Use `"es"` for Spanish. |
| `disable_first_message_interruptions` | bool | `false` | Prevent the user from interrupting the first message. |
| `max_conversation_duration_message` | string | – | Message sent when `conversation.max_duration_seconds` is reached. |
| `dynamic_variables` | object | – | `dynamic_variable_placeholders` with key-value pairs injected at runtime. |
| `prompt` | object | – | LLM + system prompt + tools + knowledge base (below). |

## conversation_config.agent.prompt

The brain of the agent.

```json
{
  "prompt": "<system prompt, in English per the skill's default>",
  "llm": "gemini-2.5-flash",
  "temperature": 0.3,
  "max_tokens": 250,
  "tools": [],
  "built_in_tools": {},
  "knowledge_base": [],
  "rag": {}
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `prompt` | string | `""` | System prompt. Use the six-block structure (Personality/Environment/Tone/Goal/Guardrails/Tools). |
| `llm` | string | – | Model ID (see [LLM providers](#llm-providers)). |
| `temperature` | float | `0` | 0-1; higher = more creative. Voice agents: 0.1-0.4 typical. |
| `max_tokens` | int | `-1` | Max response tokens (`-1` = unlimited). Cap at ~150-250 for voice brevity. |
| `reasoning_effort` | string | – | `none`,`minimal`,`low`,`medium`,`high`,`xhigh` (model-dependent). |
| `thinking_budget` | int | – | Max thinking tokens for reasoning models. |
| `tools` | array | – | Server-side `webhook` tool definitions (see below). |
| `built_in_tools` | object | – | Platform system tools (see below). |
| `tool_ids` | array | – | References to standalone tools created via `POST /v1/convai/tools` (reusable across agents, or platform integration tools). Like `tools`, this is a full-array replace — GET, append, PATCH. See SKILL.md → "Inline tools vs. standalone (referenced) tools". |
| `knowledge_base` | array | – | Documents for RAG (see [Knowledge base](#knowledge-base--rag)). |
| `rag` | object | – | RAG retrieval config. |
| `timezone` | string | – | IANA timezone (e.g. `America/Mexico_City`) for time-aware behavior. |
| `backup_llm_config` | object | – | Fallback LLM configuration. |
| `cascade_timeout_seconds` | number | `8` | Seconds before cascading to the backup LLM (2-15). |
| `ignore_default_personality` | bool | – | Skip ElevenLabs' default personality instructions. |

### Server (webhook) tools — `prompt.tools[]`

The only tool type in scope for this skill. Runs server-side; the agent calls your HTTPS API.

```json
{
  "type": "webhook",
  "name": "get_order",
  "description": "Fetch an order by its ID. Call this before stating any order detail.",
  "api_schema": {
    "url": "https://api.example.com/orders",
    "method": "POST",
    "request_headers": [
      { "name": "Authorization", "secret": { "env_var_label": "orders_api_key" } }
    ],
    "request_body_schema": {
      "type": "object",
      "properties": { "order_id": { "type": "string", "description": "The order ID" } },
      "required": ["order_id"]
    }
  }
}
```

- `description` (tool-level) tells the LLM **when** to call it; property `description`s tell it **how** to fill arguments.
- URLs must be HTTPS. Reference secrets via `env_var_label`; never inline tokens.
- `api_schema` also supports `query_params_schema` and `path_params_schema` for GET-style tools, and `response_timeout_secs`.

### Built-in system tools — `prompt.built_in_tools`

`{}` enables defaults; provide a `description` to customize; omit to disable.

| Tool | Enable for |
|------|------------|
| `end_call` | All agents (lets the agent hang up when done). |
| `language_detection` | Agents whose callers may switch languages. |
| `skip_turn` | Tutoring/coaching (agent stays silent and listens). |
| `transfer_to_agent` | Multi-agent handoff within a workflow. |

> `transfer_to_number` (escalation to a human phone line) and `voicemail_detection` /
> `play_keypad_touch_tone` are telephony features tied to outbound/phone plumbing — out of scope
> for this skill's agent-configuration focus.

---

## conversation_config.tts

```json
{
  "voice_id": "EXAVITQu4vr4xnSDxMaL",
  "model_id": "eleven_flash_v2_5",
  "stability": 0.5,
  "similarity_boost": 0.8,
  "speed": 1.0,
  "optimize_streaming_latency": 3
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `voice_id` | string | – | Voice to use. Must natively support the target language. |
| `model_id` | string | – | TTS model (see table below). |
| `stability` | float | `0.5` | 0-1; lower = more expressive, higher = more consistent. |
| `similarity_boost` | float | `0.8` | 0-1; higher = closer to the original voice. |
| `speed` | float | `1.0` | 0.7-1.2 speech-speed multiplier. |
| `optimize_streaming_latency` | int | – | 0-4; higher = faster, slightly lower quality. |
| `expressive_mode` | bool | `true` | Enable expressive generation. |
| `pronunciation_dictionary_locators` | array | – | Pronunciation overrides for tricky terms/brands. |
| `agent_output_audio_format` | string | – | Output audio codec. |

**TTS models for agents:**

| Model ID | Languages | Latency |
|----------|-----------|---------|
| `eleven_flash_v2_5` | 32 (incl. Spanish) | ~75 ms — **recommended for real-time** |
| `eleven_flash_v2` | English | ~75 ms |
| `eleven_turbo_v2_5` | 32 | ~250-300 ms |
| `eleven_turbo_v2` | English | ~250-300 ms |
| `eleven_multilingual_v2` | 29 | Standard (high fidelity) |
| `eleven_v3_conversational` | 70+ | Standard (most expressive) |

Discover Spanish voices: `GET /v1/shared-voices?language=es` or inspect `labels` from `GET /v1/voices`.

---

## conversation_config.asr

```json
{ "quality": "high", "provider": "elevenlabs", "keywords": ["Aurora Telecom", "fibra"], "user_input_audio_format": "pcm_16000" }
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `quality` | string | `"high"` | Transcription quality level. |
| `provider` | string | `"elevenlabs"` | `elevenlabs` or `scribe_realtime`. |
| `keywords` | array | – | Words/brands to boost recognition accuracy. Add domain terms here. |
| `user_input_audio_format` | string | – | e.g. `pcm_16000`, `ulaw_8000`. |

---

## conversation_config.turn

```json
{ "turn_timeout": 7, "turn_eagerness": "normal", "silence_end_call_timeout": -1 }
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `turn_timeout` | number | `7` | Seconds to wait before re-engaging a silent user. |
| `turn_eagerness` | string | `"normal"` | `patient`, `normal`, or `eager`. |
| `silence_end_call_timeout` | number | `-1` | Seconds of silence before ending the call (`-1` = disabled). |
| `initial_wait_time` | number | – | Seconds to wait for the user to start speaking. |
| `spelling_patience` | string | `"auto"` | Entity-detection patience: `auto` or `off`. |
| `speculative_turn` | bool | `false` | Enable speculative turn detection. |
| `soft_timeout_config` | object | – | Message if the user goes silent (below). |

**soft_timeout_config:** `timeout_seconds` (number, `-1` = off), `message` (string), `use_llm_generated_message` (bool).

---

## conversation_config.conversation

```json
{ "max_duration_seconds": 900, "text_only": false, "monitoring_enabled": false }
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_duration_seconds` | int | `600` | Max conversation duration. |
| `text_only` | bool | `false` | Text-only mode (avoids audio pricing). |
| `file_input` | object | – | Allow image/PDF uploads for multimodal LLMs (`enabled`, `max_files_per_conversation`). |
| `monitoring_enabled` | bool | `false` | Real-time monitoring. |
| `client_events` / `monitoring_events` | array | – | Events forwarded to connected/monitoring apps. |
| `source_attribution` | bool | `false` | Make the agent report which knowledge-base sources it used. |

## conversation_config.vad

Voice Activity Detection — governs how readily user speech is detected and how barge-in
(interruption) is handled. Confirm the exact sub-fields against the live API reference before
fine-tuning; in most cases tuning `turn_eagerness` + `turn_timeout` is sufficient.

---

## platform_settings

```json
{
  "summary_language": "es",
  "auth": { "enable_auth": true, "allowlist": [{ "hostname": "example.com" }] },
  "call_limits": { "agent_concurrency_limit": 10, "daily_limit": 1000, "bursting_enabled": true },
  "guardrails": { "...": "..." },
  "privacy": { "...": "..." },
  "trust_context": "low"
}
```

| Field | Description |
|-------|-------------|
| `summary_language` | Language for analysis outputs (summaries, titles, eval rationales). Set `"es"`. |
| `auth` | `enable_auth` (require signed URLs/tokens), `allowlist` (allowed origins). |
| `call_limits` | `agent_concurrency_limit` (default -1 = unlimited), `daily_limit` (default 100000), `bursting_enabled`. |
| `guardrails` | Independent safety controls (below). |
| `privacy` | Recording, retention, redaction (below). |
| `trust_context` | `unknown`, `low`, or `high`. |

### platform_settings.guardrails

Runs independently of the LLM. Use `"version": "1"`.

| Field | Description |
|-------|-------------|
| `focus` | `{ "is_enabled": bool }` — keeps the agent on-topic. |
| `prompt_injection` | `{ "is_enabled": bool }` — detects manipulation / instruction-override. |
| `content` | Category moderation. `execution_mode`: `streaming` or `blocking`. `config.<category>`: `{ "is_enabled": bool, "threshold": 0.0-1.0 | "low"|"medium"|"high" }`. Categories: `sexual`, `violence`, `harassment`, `self_harm`, `profanity`, `religion_or_politics`, `medical_and_legal_information`. |
| `custom` | LLM-evaluated domain rules: `config.configs[]` each `{ "is_enabled", "name", "prompt", "execution_mode": "blocking", "trigger_action": { "type": "retry"|"end", "feedback": "..." } }`. |

`trigger_action` `retry` removes the blocked reply, injects your `feedback` as a system message,
and regenerates up to 3 times before ending the session. Feedback templates support
`{{trigger_reason}}` and `{{agent_message}}`.

**Per vertical:** healthcare/finance/legal → enable `medical_and_legal_information`;
education/youth → `sexual`/`violence`/`self_harm`/`profanity`; support/sales →
`harassment`/`profanity`. All agents benefit from `focus` + `prompt_injection` + 2-4 custom rules.

### platform_settings.privacy

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `conversation_history_redaction` | object | – | Redact entity types from stored transcripts/audio/analysis. |
| `conversation_history_redaction.enabled` | bool | `false` | Toggle redaction. |
| `conversation_history_redaction.entities` | array | – | e.g. `name`, `name.name_given`, `email_address`, `contact_number`, `dob`, `age`. |

---

## Knowledge base / RAG

Configured inside `conversation_config.agent.prompt` — server-side retrieval, fully in scope.

```json
{
  "knowledge_base": [
    { "type": "file", "id": "doc-id", "name": "Manual de Producto", "usage_mode": "auto" }
  ],
  "rag": {
    "enabled": true,
    "embedding_model": "qwen3_embedding_4b",
    "max_documents_length": 50000,
    "max_retrieved_rag_chunks_count": 20
  }
}
```

`embedding_model`: `e5_mistral_7b_instruct`, `multilingual_e5_large_instruct` (good for Spanish),
or `qwen3_embedding_4b`. Set `conversation.source_attribution: true` to have the agent cite sources.

---

## LLM providers

Confirm the live catalog (including deprecations and capability flags) with `GET /v1/convai/llm/list`.

| Provider | Model IDs |
|----------|-----------|
| OpenAI | `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` |
| Anthropic | `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-sonnet-4-5`, `claude-sonnet-4`, `claude-haiku-4-5`, `claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-haiku` |
| Google | `gemini-3.1-pro-preview`, `gemini-3-flash-preview`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.0-flash`, `gemini-2.0-flash-lite` |
| ElevenLabs (hosted, ultra-low latency) | `glm-45-air-fp8`, `qwen3-30b-a3b`, `gpt-oss-120b`, and other `qwen*` variants |
| Custom | `custom-llm` (requires a `custom_llm` config block with `url`, `model_id`, `api_key.secret_id`, `api_type`) |

For real-time Spanish voice, default to a fast Gemini/`*-mini`/`haiku`/ElevenLabs-hosted model
and set a `backup_llm_config`. Reserve large reasoning models for genuinely complex flows.

---

## Updatable fields (PATCH)

Send only the slice you're changing. **Arrays (`tools`, `knowledge_base`, `built_in_tools`,
guardrail configs) replace wholesale — `GET` first, modify, then `PATCH` the full array.**

| Section | Fields |
|---------|--------|
| Root | `name`, `tags` |
| `conversation_config.agent` | `first_message`, `language`, `disable_first_message_interruptions`, `dynamic_variables` |
| `conversation_config.agent.prompt` | `prompt`, `llm`, `temperature`, `max_tokens`, `reasoning_effort`, `tools`, `built_in_tools`, `knowledge_base`, `rag`, `timezone`, `backup_llm_config` |
| `conversation_config.tts` | `voice_id`, `model_id`, `stability`, `similarity_boost`, `speed`, `optimize_streaming_latency`, `expressive_mode` |
| `conversation_config.asr` | `quality`, `provider`, `keywords`, `user_input_audio_format` |
| `conversation_config.turn` | `turn_timeout`, `turn_eagerness`, `silence_end_call_timeout`, `soft_timeout_config` |
| `conversation_config.conversation` | `max_duration_seconds`, `text_only`, `monitoring_enabled` |
| `platform_settings` | `summary_language`, `guardrails`, `privacy`, `auth`, `call_limits` |

---

## Out of scope (intentionally omitted)

This skill deliberately excludes: client-side tools, outbound/Twilio calls, the web widget
embed (`<elevenlabs-convai>` and `platform_settings.widget` styling), the ElevenLabs CLI, and
language SDKs. If a task requires those, tell the user they're outside this skill's focus.
