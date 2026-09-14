"""Gemini API との通信をまとめたモジュール。"""
from __future__ import annotations

import os
from typing import Iterator, Optional

import streamlit as st
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-3.6-flash"

MODEL_OPTIONS = {
    "Gemini 3.6 Flash（高速・バランス型）": "gemini-3.6-flash",
    "Gemini 3.6 Pro（高精度）": "gemini-3.6-pro",
    "Gemini 3.6 Flash-Lite（軽量・低コスト）": "gemini-3.6-flash-lite",
}


def get_api_key() -> Optional[str]:
    return st.session_state.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")


def get_client() -> Optional[genai.Client]:
    api_key = get_api_key()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def _resolve_model(model: Optional[str]) -> str:
    return model or st.session_state.get("gemini_model", DEFAULT_MODEL)


def generate_text(
    prompt: str,
    *,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    model: Optional[str] = None,
) -> str:
    """プロンプトを送信し、生成結果を1つの文字列として返す。"""
    client = get_client()
    if client is None:
        raise RuntimeError("Gemini APIキーが設定されていません。サイドバーから入力してください。")

    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    response = client.models.generate_content(
        model=_resolve_model(model),
        contents=prompt,
        config=config,
    )
    return response.text or ""


def stream_text(
    prompt: str,
    *,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    model: Optional[str] = None,
) -> Iterator[str]:
    """プロンプトを送信し、生成結果をストリーミングで返す（st.write_stream用）。"""
    client = get_client()
    if client is None:
        raise RuntimeError("Gemini APIキーが設定されていません。サイドバーから入力してください。")

    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    for chunk in client.models.generate_content_stream(
        model=_resolve_model(model),
        contents=prompt,
        config=config,
    ):
        if chunk.text:
            yield chunk.text
