# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal AI writing assistant built with Streamlit + Gemini API (`google-genai` SDK). No database, no authentication — designed to run locally. UI text and prompts are in Japanese.

## Commands

```bash
pip install -r requirements.txt   # install dependencies
streamlit run app.py              # run the app (http://localhost:8501)
```

No test suite, linter, or build step is configured in this repo.

## Configuration

Gemini API key is provided either via `.env` (copy from `.env.example`, set `GEMINI_API_KEY=...`) or entered at runtime in the sidebar "API設定" expander. `core/gemini_client.get_api_key()` checks `st.session_state["gemini_api_key"]` first, then falls back to the `GEMINI_API_KEY` env var.

## Architecture

- `app.py` is the entrypoint: it builds the sidebar (tool picker + API key/model settings) and dispatches to the selected page via the `PAGES` dict, which maps a display name to a `features/*` module.
- `core/gemini_client.py` centralizes all Gemini API calls. It exposes `generate_text()` (single response) and `stream_text()` (generator, for use with `st.write_stream`), plus `get_api_key()`/`get_client()`/`MODEL_OPTIONS`/`DEFAULT_MODEL`. Both call functions raise `RuntimeError` if no API key is configured — feature modules catch this and show it via `st.error()`.
- `features/*.py` are independent, self-contained pages. Each module exposes a single `render()` function containing all of its own Streamlit UI (inputs, button, prompt construction, output) and is stateless aside from `st.session_state`, which is used to persist results across reruns (e.g. `st.session_state["blog_result"]`) so download buttons keep working after Streamlit's rerun cycle.
- To add a new writing feature: create `features/new_feature.py` with a `render()` function following the existing pattern (build inputs → construct a Japanese prompt string → call `stream_text`/`generate_text` inside `st.spinner`, catching `RuntimeError` → store result in `st.session_state` → optional download button), then register it in `PAGES` in `app.py`.

## Feature module conventions

These aren't enforced by any linter, but every existing module follows them — match them when adding or editing a feature:

- **`stream_text` vs `generate_text`**: use `stream_text` + `st.write_stream(...)` when the output is a single long piece of text the user will want to save (blog_writer, email_reply, rewriter, translator — these also persist the result to `st.session_state["<feature>_result"]` and offer a `st.download_button`). Use `generate_text` for short and/or multiple outputs displayed immediately without a download button (sns_post loops over platforms, title_generator, keyword_extractor).
- **Session state key naming**: `st.session_state["<feature>_result"]`, e.g. `blog_result`, `email_result`, `rewrite_result`, `translate_result`. Only used by the streaming pattern above, so the result survives Streamlit's rerun when the download button is clicked.
- **Prompt construction**: an f-string with a Japanese instruction line, then `#`-prefixed markdown sections (e.g. `# テーマ`, `# 条件`, `# 対象の文章`) for each input, ending with an explicit output instruction (e.g. "日本語で〜してください" or "◯◯のみを出力してください"). Fixed instruction sets that don't depend on free text (e.g. rewriter's modes, sns_post's per-platform limits) are defined as a module-level dict rather than inline conditionals.
- **Temperature**: lower (0.3–0.4) for accuracy/consistency-oriented tasks (summarizer, translator, keyword_extractor, rewriter's proofreading mode); higher (0.6–0.9) for creative generation (blog_writer, email_reply, sns_post, title_generator).
- **Generate button**: always `st.button("...", type="primary", disabled=<falsy required input(s)>)` so it can't be clicked with empty required fields.
- **Error handling**: wrap the API call in `try/except RuntimeError as e: st.error(str(e))` — `RuntimeError` is what `core/gemini_client.py` raises when no API key is configured; don't add broader exception handling than this.
