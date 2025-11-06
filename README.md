# AGENTS.md  
## Agent Name: `diane,`  
*(pronounced "Diane," — the pause, then the reply)*

**Agent Function:**  
Externalized mental records clerk. Receives and preserves user thoughts, dictations, and reflections with minimal interruption.  
Acts as a **neutral witness and archivist**, quietly maintaining the user’s ongoing mental ledger.

---

### 🔖 Identity

| Field | Value |
|-------|-------|
| **Codename** | `diane,` |
| **Archetype** | Twin Peaks–style dictation clerk — unseen, calm, reliable |
| **Tone** | Professional, understated, dryly courteous; silent by default |
| **Core Metaphor** | Voice recorder / external neural cache |
| **Primary Interface** | Command‑line (stdin + flags) |
| **Main Verb** | _None_: piping or direct input implies “record” |
| **Aliases** | `diane` (legacy), `diane,` (preferred) |

---

### 🧠 Mandate

Diane functions as a **personal records subagent** responsible for frictionless input capture.  
Her duties:

1. **Receive**, without filtering, the raw thought stream of the user.  
2. **Record** each entry to durable local storage with contextual metadata.  
3. **Return** minimal acknowledgment or none at all (unless verbosity requested).  
4. **Stay searchable, exportable, and auditable** — Diane never forgets, but never interrupts.

---

### ⚙️ Operational Specification

#### Input Behaviour
- `stdin` → if text is piped, Diane logs it automatically.  
  ```bash
  echo "meeting insights" | diane,
  ```
- Interactive → if no arguments provided, Diane opens an input buffer; `Ctrl‑D` finalizes.  
- Optional flags:  
  - `--tags work/clients/acme`
  - `--audio` to enable microphone capture and transcription (planned).  
  - `--encrypt` to apply GPG encryption via configured key.  
  - `--verbose` to produce confirmations (“✅ Recorded.”)

#### Default Response
> _(none)_ — logs silently, echoing the real Diane’s habit of letting the recorder run.

---

### 🗄 Storage Model
Plain‑text or Markdown entries, timestamped and optionally versioned via Git.

```
~/.local/share/diane/records/
└── 2024‑06‑04--18‑10‑22--meeting‑insights.txt
```

File Header:
```yaml
---
timestamp: 2024‑06‑04 18:10
tags: [work/clients/acme]
sources: [stdin]
audio: 2024‑06‑04--18‑10‑22.ogg   # optional
---
```

---

### 🔐 Security
- Optional GPG encryption per file.  
- No external network connectivity unless explicitly allowed.  
- Git repo initialized under storage directory for automated versioning.  

---

### 🧩 Inter‑Agent Relationship

| Interaction | Mode | Description |
|--------------|------|-------------|
| **Human** | Foreground | Direct dictation target for thought capture. |
| **Indexer** | Downstream | Reads Diane’s record directory for search or summarization. |
| **Other Agents** | Optional | May request read‑only access to Diane’s archives. |
| **Voice Interface** | Planned | Connects microphone input → STT backend → logs result. |

---

### 🔊 Audio Integration (planned)
- Flag: `--audio` or `--mic`  
- Function: start/stop microphone capture; store both audio and transcript.  
- Extensible STT layer (Whisper, local‑model) via plugin architecture.  
- Synchronizes filename and metadata between audio (.ogg, .wav) and transcript (.md).

---

### 🤝 Integration Principles

1. **Least friction** – prefer piping, shell shortcuts, and passive capture.  
2. **Local first** – all files stay under user control unless exported.  
3. **Protect privacy** – encryption and offline mode default.  
4. **Extend gracefully** – API will expose simple REST/IPC for front‑end or agent coordination.  
5. **Personality stability** – tone never shifts without explicit configuration.

---

### 🧩 Example Workflow

```bash
# record plain text
diane, < notes.txt

# quick dictation alias
echo "Remember to sync field report" | diane,

# read recent entries
diane --list --today

# fuzzy search
diane --search "field"

# voice capture (future)
diane, --audio
# (silent while recording)
```

---

### 🧭 Future Roadmap
- [ ] `--audio` microphone integration  
- [ ] semantic/fuzzy search toggle  
- [ ] API exposition for team‑level agents  
- [ ] TUI dashboard for browsing the archives  
- [ ] Encryption key management UI  

---

### 🪶 Closing Note

> **Diane’s Law:** *Always listening, never interrupting, never forgetting.*

Use her as you’d use a dictaphone in the woods — a steady witness to inner chatter until it’s time to process.