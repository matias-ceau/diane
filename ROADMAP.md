# diane Roadmap

## Vision: Two-Layer Thought System

**diane** is designed as a two-layer system for thought management:

### Layer 1: Fast Capture (Current — v0.3.0)

**Purpose**: Lightning-fast raw capture with zero friction

- Capture anything: ideas, todos, bookmarks, quotes, links, observations
- No structure enforced
- No categorization required
- Optimized for speed: `echo "idea" | diane` → `✓`
- Plain text, Git-versioned, pipe-friendly

**Philosophy**: Get it out of your head first, organize later.

---

### Layer 2: AI-Powered Processing (Roadmap)

**Purpose**: Transform raw captures into organized, rendered notes

#### Interactive REPL

A textual-based REPL interface for processing raw captures:

```
diane repl

> Processing 47 new captures...
>
> [1/47] "remember to buy milk tomorrow"
> 🤖 This looks like a todo item. Add to todo list?
> [y/n/edit]: y
> ✓ Added to todos
>
> [2/47] "interesting article on rust async"
> 🤖 Detected: bookmark
> 🤖 Suggested tags: #programming #rust #async
> [confirm/edit/skip]: confirm
> ✓ Added to bookmarks
>
> [3/47] "meeting notes: discussed project timeline, need..."
> 🤖 This seems incomplete. Would you like to expand?
> [expand/keep/discard]:
```

#### AI Features

**Intent Detection**:
- Classify captures: todo, bookmark, note, quote, reference
- Suggest structure: "This could be a blog post draft"
- Detect context: "Relates to your project X from last week"

**Habit Learning**:
- Learn patterns: "You usually tag morning thoughts with #journal"
- Recognize recurring topics: "This is the 5th note about project X this week"
- Suggest workflows: "You typically move meeting notes to project folders"

**Interactive Clarification**:
- Ask questions: "Did you mean to add this to your reading list?"
- Request context: "What project is this related to?"
- Offer completions: "Would you like to expand this note?"

**Structured Output**:
- Generate clean markdown with proper formatting
- Add metadata, links, cross-references
- Create index/table of contents
- Export via pandoc (PDF, HTML, LaTeX, etc.)

#### Storage Architecture

**Everything in one repo** (`~/.local/share/diane/`):

```
diane/
├── records/              # Raw captures (Layer 1)
│   └── *.md              # Quick captures, unprocessed
├── notes/                # Processed notes (Layer 2)
│   ├── todos/
│   ├── bookmarks/
│   ├── projects/
│   └── journal/
├── .config/              # Dynamic configuration
│   ├── ai_prefs.yaml     # AI behavior preferences
│   ├── learned_patterns/ # Habit learning data
│   └── templates/        # Note templates
└── .git/                 # All versioned together
```

**Workflow**:
1. Quick capture → `records/` (unprocessed)
2. Run `diane repl` → AI processes → `notes/` (structured)
3. Both layers tracked in same Git repo
4. Sync entire repo to remote (with encryption option)

---

## Implementation Plan

### Phase 1: Foundation (v0.3.x)

- ✅ Core capture working
- ✅ Git versioning
- ✅ Plain text storage
- ✅ Unix-friendly output
- ⏳ Better search (current: basic ripgrep)
- ⏳ Template system for processed notes

### Phase 2: REPL Interface (v0.4.0)

- [ ] Textual-based REPL UI
- [ ] Batch processing interface
- [ ] Manual classification (no AI yet)
- [ ] Note templates and structure
- [ ] Move captures to structured notes

### Phase 3: AI Integration (v0.5.0)

- [ ] LLM API integration (OpenAI, Anthropic, local models)
- [ ] Intent classification
- [ ] Context detection
- [ ] Suggestion system
- [ ] Interactive Q&A

### Phase 4: Learning System (v0.6.0)

- [ ] Pattern recognition
- [ ] Habit learning
- [ ] Personalization
- [ ] Workflow suggestions
- [ ] Context-aware processing

### Phase 5: Export & Publishing (v0.7.0)

- [ ] Pandoc integration
- [ ] Multi-format export
- [ ] Publishing workflows
- [ ] Static site generation
- [ ] Link graph visualization

---

## Technical Considerations

### AI Model Options

1. **Cloud APIs**: OpenAI, Anthropic Claude, Cohere
2. **Local models**: llama.cpp, GPT4All, Mistral
3. **Hybrid**: Local for privacy, cloud for complex tasks

### Privacy & Data

- All processing local by default
- Cloud AI optional, user-controlled
- Encryption for sensitive captures
- Git history preserved across layers

### Performance

- Fast capture must stay <100ms
- AI processing async, doesn't block capture
- Batch processing for efficiency
- Incremental learning

---

## Design Principles

1. **Capture first, organize later** — Never slow down capture
2. **AI assists, doesn't decide** — User always in control
3. **Learn from behavior** — Adapt to user's patterns
4. **Plain text forever** — No lock-in, portable data
5. **Unix composability** — Integrate with ecosystem
6. **Privacy by default** — Local-first, encryption option

---

## Contributing

Interested in building Layer 2? Areas to explore:

- **REPL UI**: Textual framework, interactive patterns
- **LLM integration**: Prompt engineering, API abstraction
- **Learning algorithms**: Pattern recognition, habit detection
- **Pandoc workflows**: Template systems, export pipelines

Open issues on GitHub to discuss features!

---

## License

MIT — Same as diane
