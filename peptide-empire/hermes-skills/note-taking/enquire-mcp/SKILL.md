---
name: enquire-mcp
description: AI-powered local Obsidian vault search via enquire-mcp — zero cloud, hybrid retrieval (BM25 + TF-IDF + ML embeddings + BGE reranker), GraphRAG, .base query execution, 44 tools. Use when searching, querying, or analyzing an Obsidian vault with AI assistance.
version: 1.0
category: note-taking
tags: [obsidian, mcp, search, ai, rag, second-brain]
---

# enquire-mcp — AI-Powered Vault Intelligence

> *"The most advanced Obsidian MCP server. Period."* — MIT licensed, SLSA-3 verified, 664 tests

enquire-mcp is a standalone MCP (Model Context Protocol) server that gives AI agents deep, intelligent access to your Obsidian vault — **with zero cloud API calls**. Everything runs locally.

## When to Use

- Searching your vault with natural language queries
- Finding semantically related notes across the vault
- Executing `.base` queries without Obsidian running
- Building an AI-powered second brain
- Graph-based knowledge retrieval (wikilink communities)

## Prerequisites

```bash
# Node.js 18+
node --version

# Install globally
npm install -g @oomkapwn/enquire-mcp
```

## Setup

### One-Command Setup

```bash
# Downloads ML model, builds FTS5 index, creates embed database
enquire-mcp setup --vault "/path/to/vault"
```

### Health Check

```bash
enquire-mcp doctor --vault "/path/to/vault"
# Color-coded output: green = good, yellow = warn, red = fix needed
```

### Start the Server

```bash
# Tier 1: Basic (TF-IDF only, instant)
enquire-mcp serve --vault "/path/to/vault"

# Tier 4: Full hybrid search (recommended)
enquire-mcp serve --vault "/path/to/vault" --persistent-index --enable-reranker --use-hnsw

# Tier 7: Remote access (for mobile / web clients)
enquire-mcp serve-http --bearer-token "your-secret-token" --vault "/path/to/vault"
```

## Integration with Hermes Agent

Add to Hermes MCP config (`~/.hermes/config.yaml`):

```yaml
mcp_servers:
  obsidian:
    command: "npx"
    args:
      - "-y"
      - "@oomkapwn/enquire-mcp"
      - "serve"
      - "--vault"
      - "/path/to/vault"
      - "--persistent-index"
      - "--enable-reranker"
      - "--use-hnsw"
```

Then Hermes can use all 44 enquire-mcp tools to search and analyze the vault.

## Key Tools

### Search (7 tools)
| Tool | What It Does |
|------|-------------|
| `obsidian_search` | Hybrid search (BM25 + TF-IDF + embeddings + reranker) |
| `obsidian_hyde_search` | HyDE-augmented search (generates hypothetical doc then searches) |
| `obsidian_semantic_search` | Pure embedding-based semantic search |
| `obsidian_full_text_search` | BM25/FTS5 keyword search |
| `obsidian_find_similar` | Find notes similar to a given note |

### Graph & Wikilinks (8 tools)
| Tool | What It Does |
|------|-------------|
| `obsidian_get_backlinks` | All notes linking to a note |
| `obsidian_get_outbound_links` | All notes linked from a note |
| `obsidian_get_note_neighbors` | Graph neighbors of a note |
| `obsidian_find_path` | Shortest path between two notes |
| `obsidian_get_communities` | Louvain-detected wikilink communities |

### Bases (2 tools)
| Tool | What It Does |
|------|-------------|
| `obsidian_execute_base` | Execute a `.base` query without Obsidian running |
| `obsidian_list_bases` | List all `.base` files in the vault |

### Content (6 tools)
| Tool | What It Does |
|------|-------------|
| `obsidian_read_note` | Read full note content |
| `obsidian_get_frontmatter` | Extract frontmatter properties |
| `obsidian_list_notes` | List all notes in a folder |
| `obsidian_get_tags` | All tags with counts |

## Search Tiers

| Tier | Setup | Capability |
|------|-------|-----------|
| 1 | `serve --vault <path>` | TF-IDF cosine (zero setup, instant) |
| 2 | + `--persistent-index` | + BM25/FTS5 (sub-100ms top-10) |
| 3 | + `setup` | + Multilingual ML embeddings |
| 4 | + `--enable-reranker` | + BGE cross-encoder (+5-10 NDCG@10) |
| 5 | + `--use-hnsw` | + sub-10ms top-K at million-chunk scale |
| 6 | + `--include-pdfs` | + PDFs blended into search |
| 7 | `serve-http --bearer-token` | + Remote MCP access |

## Architecture

```
Query → [BM25 + TF-IDF + ML Embeddings]
          → RRF Fusion (k=60)
          → Graph Boost (α × in-degree)
          → BGE Cross-Encoder Reranker
          → Ranked Hits (per-signal observability per hit)
```

## Common Patterns

### Find everything about a topic
```
obsidian_search(query="second brain productivity system")
```

### Find notes similar to current note
```
obsidian_find_similar(note="Dashboard.md", limit=10)
```

### Discover knowledge graph communities
```
obsidian_get_communities()
```

### Execute a .base query programmatically
```
obsidian_execute_base(base="Project Board.base")
```

### Find the connection between two ideas
```
obsidian_find_path(from="PARA Method", to="Weekly Review")
```

## Pitfalls

| Issue | Solution |
|-------|----------|
| `enquire-mcp: command not found` | Run `npm install -g @oomkapwn/enquire-mcp` |
| Model download hangs | Run `enquire-mcp setup --vault <path>` separately |
| Search returns no results | Run `enquire-mcp doctor` — check index health |
| Large vault slow to index | Use `--use-hnsw` for million-chunk scale |
| Permission denied on vault | Ensure vault path is readable by the node process |

## References

- GitHub: https://github.com/oomkapwn/enquire-mcp
- npm: https://www.npmjs.com/package/@oomkapwn/enquire-mcp
- MIT License, SLSA-3 verified, semver-bound public API
