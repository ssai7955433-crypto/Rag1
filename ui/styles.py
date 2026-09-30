from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
          --ink: #172521;
          --muted: #697873;
          --paper: #f3f6f2;
          --line: #dce4dc;
          --accent: #16765a;
        }
        [data-testid="stAppViewContainer"] { background: var(--paper); color: var(--ink); }
        .block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 4rem; }
        [data-testid="stSidebar"] { background: #eaf0e9; border-right: 1px solid var(--line); }
        .app-header { display:flex; justify-content:space-between; align-items:center; gap:2rem; padding:1rem 0 1.5rem; border-bottom:1px solid var(--line); margin-bottom:1.5rem; }
        .app-header h1 { margin:0.2rem 0; font-size:2rem; color:var(--ink); }
        .app-header p { margin:0; color:var(--muted); }
        .eyebrow { color:var(--accent); font-size:0.72rem; font-weight:800; letter-spacing:0.12em; }
        .runtime-status { display:flex; align-items:center; gap:0.65rem; padding:0.7rem 0.85rem; background:#fff; border:1px solid var(--line); border-radius:6px; min-width:215px; }
        .runtime-status small { display:block; color:var(--muted); margin-top:0.2rem; }
        .status-dot { width:10px; height:10px; border-radius:50%; flex:0 0 10px; }
        .status-dot.online { background:#198754; box-shadow:0 0 0 4px #dff1e6; }
        .status-dot.offline { background:#c24b3b; box-shadow:0 0 0 4px #f8e6e2; }
        .welcome-panel { display:flex; gap:1rem; align-items:center; padding:1.5rem 0; border-top:1px solid var(--line); border-bottom:1px solid var(--line); margin:1.5rem 0; }
        .welcome-mark { display:grid; place-items:center; width:48px; height:48px; flex:0 0 48px; background:var(--accent); color:white; font-weight:800; font-size:1.25rem; border-radius:8px; }
        .welcome-panel h2 { margin:0 0 0.3rem; font-size:1.35rem; }
        .welcome-panel p { margin:0; color:var(--muted); }
        [data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:6px; padding:0.8rem 1rem; }
        [data-testid="stChatMessage"] { border:1px solid var(--line); border-radius:8px; }
        div[data-testid="stFileUploader"] { background:#fff; border:1px solid var(--line); border-radius:6px; padding:0.5rem; }
        @media (max-width: 700px) {
          .app-header { align-items:flex-start; flex-direction:column; gap:1rem; }
          .app-header h1 { font-size:1.65rem; }
          .runtime-status { width:100%; box-sizing:border-box; }
          .welcome-panel { align-items:flex-start; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
