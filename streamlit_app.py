import streamlit as st
import pandas as pd
import requests
import re
from html import escape

st.set_page_config(
    page_title="Periodicalc",
    page_icon="⚛️",
    layout="wide"
)

# ==========================
# GLOBAL CUSTOM STYLES — Tema pastel pink aplikasi
# ==========================
st.markdown("""<style>
/* ========== Tema Pastel Pink Global ========== */

:root, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    --primary-color: rgb(219, 112, 147) !important;
    --primary-color-hover: rgb(255, 182, 213) !important;
}

/* Background halaman — pink sangat muda */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, rgba(255, 228, 240, 0.65), rgba(255, 240, 246, 0.75), rgba(255, 255, 255, 0.85)) !important;
}

/* Sidebar — nuansa pastel pink */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255, 214, 232, 0.55), rgba(252, 228, 236, 0.45)) !important;
}

/* Modern Pink Sidebar Navigation Styling */
div[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
    font-size: 0.9em !important;
    font-weight: 700 !important;
    color: var(--text-color) !important;
    margin-bottom: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    opacity: 0.7 !important;
}
div[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
    background: transparent !important;
}
div[data-testid="stSidebar"] label[data-baseweb="radio"] {
    background: rgba(255,214,232,0.15) !important;
    border: 1px solid rgba(219,112,147,0.15) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 0px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
}
/* Hide standard radio circle selector */
div[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-of-type {
    display: none !important;
}
/* Align item text */
div[data-testid="stSidebar"] label[data-baseweb="radio"] > div:last-child {
    color: var(--text-color) !important;
    font-size: 0.95em !important;
    font-weight: 500 !important;
    font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif !important;
}
/* Active Sidebar Button — pink soft highlight */
div[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
    background: rgba(248, 187, 208, 0.45) !important;
    border-color: rgba(219, 112, 147, 0.45) !important;
    box-shadow: 0 4px 12px rgba(219,112,147,0.1) !important;
    transform: translateX(4px) !important;
}
div[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) > div:last-child {
    font-weight: 600 !important;
}
/* Hover State — pink muda */
div[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
    background: rgba(255, 214, 232, 0.55) !important;
    border-color: rgba(219, 112, 147, 0.25) !important;
    transform: translateX(2px) !important;
}

/* ========== Tombol / Button — rose pastel ========== */
[data-testid="stAppViewContainer"] button,
[data-testid="stSidebar"] button {
    background: rgba(248, 187, 208, 0.38) !important;
    border: 1px solid rgba(219, 112, 147, 0.42) !important;
    border-radius: 10px !important;
    color: var(--text-color) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stAppViewContainer"] button:hover,
[data-testid="stSidebar"] button:hover {
    background: rgba(244, 167, 193, 0.5) !important;
    border-color: rgba(219,112,147,0.5) !important;
    box-shadow: 0 3px 10px rgba(219,112,147,0.12) !important;
}
[data-testid="stAppViewContainer"] button:active,
[data-testid="stSidebar"] button:active {
    background: rgba(244, 167, 193, 0.6) !important;
    transform: scale(0.98) !important;
}

/* ========== Tabel hasil — header pink muda ========== */
[data-testid="stAppViewContainer"] table thead th {
    background: rgba(255,214,232,0.3) !important;
    border-bottom: 2px solid rgba(219,112,147,0.2) !important;
    color: var(--text-color) !important;
}
[data-testid="stAppViewContainer"] table {
    border: 1px solid rgba(219,112,147,0.15) !important;
    border-radius: 8px !important;
    background-color: rgba(255, 255, 255, 0.3) !important;
}
[data-testid="stAppViewContainer"] table tbody tr {
    transition: background-color 0.15s ease !important;
}
[data-testid="stAppViewContainer"] table tbody tr:hover {
    background-color: rgba(255, 214, 232, 0.15) !important;
}
[data-testid="stAppViewContainer"] table td {
    color: var(--text-color) !important;
    border-bottom: 1px solid rgba(219, 112, 147, 0.1) !important;
}

/* ========== Expander Custom Pink Styling ========== */
div[data-testid="stExpander"] {
    background-color: rgba(252, 228, 236, 0.45) !important;
    border: 1.5px solid rgba(219, 112, 147, 0.28) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(219, 112, 147, 0.03) !important;
}
div[data-testid="stExpander"] details summary {
    background-color: rgba(248, 187, 208, 0.35) !important;
    color: var(--text-color) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    border-bottom: none !important;
}
div[data-testid="stExpander"] details summary:hover {
    background-color: rgba(248, 187, 208, 0.45) !important;
}
div[data-testid="stExpander"] details summary svg {
    color: rgba(219, 112, 147, 0.8) !important;
    fill: rgba(219, 112, 147, 0.8) !important;
}
div[data-testid="stExpander"] details[open] summary {
    border-radius: 12px 12px 0 0 !important;
    border-bottom: 1.5px solid rgba(219, 112, 147, 0.15) !important;
}

/* ========== Tabs — pink accent ========== */
[data-testid="stAppViewContainer"] .stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid rgba(219, 112, 147, 0.15) !important;
}
[data-testid="stAppViewContainer"] button[data-baseweb="tab"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    color: var(--text-color) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stAppViewContainer"] button[data-baseweb="tab"]:hover {
    color: rgb(219, 112, 147) !important;
    background-color: rgba(255, 214, 232, 0.15) !important;
}
[data-testid="stAppViewContainer"] button[data-baseweb="tab"][aria-selected="true"] {
    color: rgb(219, 112, 147) !important;
    font-weight: 700 !important;
}
[data-testid="stAppViewContainer"] div[data-baseweb="tab-highlight"] {
    background-color: rgb(219, 112, 147) !important;
}

/* ========== Input & Widget Borders and Focus ========== */
[data-testid="stAppViewContainer"] div[data-baseweb="input"],
[data-testid="stAppViewContainer"] div[data-baseweb="select"],
[data-testid="stAppViewContainer"] div[data-baseweb="textarea"] {
    border: 1.5px solid rgba(219, 112, 147, 0.18) !important;
    border-radius: 8px !important;
    background-color: rgba(255, 255, 255, 0.65) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stAppViewContainer"] div[data-baseweb="input"]:hover,
[data-testid="stAppViewContainer"] div[data-baseweb="select"]:hover,
[data-testid="stAppViewContainer"] div[data-baseweb="textarea"]:hover {
    border-color: rgba(219, 112, 147, 0.35) !important;
}
[data-testid="stAppViewContainer"] div[data-baseweb="input"]:focus-within,
[data-testid="stAppViewContainer"] div[data-baseweb="select"]:focus-within,
[data-testid="stAppViewContainer"] div[data-baseweb="textarea"]:focus-within {
    border-color: rgba(219, 112, 147, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(255, 182, 213, 0.2) !important;
}
[data-testid="stAppViewContainer"] input,
[data-testid="stAppViewContainer"] textarea {
    border: none !important;
    background-color: transparent !important;
    color: var(--text-color) !important;
}

[data-testid="stNumberInput"] button {
    border-color: rgba(219, 112, 147, 0.2) !important;
    background-color: rgba(255, 182, 213, 0.1) !important;
    color: rgb(219, 112, 147) !important;
}
[data-testid="stNumberInput"] button:hover {
    background-color: rgba(255, 182, 213, 0.25) !important;
    border-color: rgba(219, 112, 147, 0.4) !important;
}

/* ========== Alert Boxes Custom Pink Theme ========== */
div[data-testid="stAlert"] {
    background-color: rgba(255, 235, 243, 0.55) !important;
    color: var(--text-color) !important;
    border: 1px solid rgba(219, 112, 147, 0.25) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(219, 112, 147, 0.03) !important;
}
div[data-testid="stAlert"] p, div[data-testid="stAlert"] li, div[data-testid="stAlert"] span {
    color: var(--text-color) !important;
}
div[data-testid="stAlert"]:has(div[aria-label="Success"]) {
    background-color: rgba(255, 235, 243, 0.65) !important;
    border-color: rgba(219, 112, 147, 0.4) !important;
}
div[data-testid="stAlert"]:has(div[aria-label="Info"]) {
    background-color: rgba(243, 235, 255, 0.6) !important; /* lavender-pink */
    border-color: rgba(159, 122, 234, 0.35) !important;
}
div[data-testid="stAlert"]:has(div[aria-label="Warning"]) {
    background-color: rgba(255, 240, 230, 0.6) !important; /* peach-pink */
    border-color: rgba(255, 177, 66, 0.35) !important;
}
div[data-testid="stAlert"]:has(div[aria-label="Error"]) {
    background-color: rgba(255, 220, 220, 0.6) !important; /* light reddish-pink */
    border-color: rgba(255, 107, 107, 0.35) !important;
}

/* Title, Header Accents and Dividers */
h1, h2, h3 {
    color: #4a1525 !important;
}
h1 {
    border-bottom: 2px solid rgba(219, 112, 147, 0.2) !important;
    padding-bottom: 8px !important;
}
h2 {
    border-left: 4px solid rgba(219, 112, 147, 0.5) !important;
    padding-left: 10px !important;
}
hr {
    border-color: rgba(219, 112, 147, 0.2) !important;
}

/* Global Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(219, 112, 147, 0.25);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(219, 112, 147, 0.45);
}

/* ========== Tabel Periodik layout ========== */
.pt-container{background:transparent;padding:5px 0px;margin-bottom:20px;overflow-x:auto;-webkit-overflow-scrolling:touch;width:100%}
.pt-table-grid{min-width:800px;padding:12px 14px 14px;box-sizing:border-box}
.pt-title{color:var(--text-color);font-size:1.6rem;font-weight:700;margin-bottom:6px;font-family:'Segoe UI',sans-serif}
.pt-helper{color:color-mix(in srgb,var(--text-color) 62%,transparent);font-size:0.82rem;margin-bottom:16px;font-family:'Segoe UI',sans-serif}
.pt-row{display:grid;grid-template-columns:26px repeat(18,minmax(36px,1fr));gap:3px;margin-bottom:3px;align-items:center}
.pt-group-row{margin-bottom:6px}
.pt-axis-label{height:100%;min-height:18px;display:flex;align-items:center;justify-content:center;color:color-mix(in srgb,var(--text-color) 58%,transparent);font-size:0.62em;font-weight:700;font-family:'Segoe UI',sans-serif}
.pt-period-label{font-size:0.68em;color:color-mix(in srgb,var(--text-color) 62%,transparent)}
.pt-series-label{justify-content:flex-end;padding-right:6px;text-align:right;line-height:1.1}
.pt-spacer-row{height:10px;margin-bottom:0}
.pt-spacer-row .pt-cell,.pt-spacer-row a.pt-link{background:transparent!important;border:none!important;box-shadow:none!important;pointer-events:none}

/* Grid elements with pink-tinted borders */
a.pt-link{text-decoration:none;aspect-ratio:1;border:1.5px solid rgba(219,112,147,0.28);border-radius:5px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:transform 0.16s ease,border-color 0.16s ease,box-shadow 0.16s ease;position:relative;min-width:0;box-shadow:0 2px 5px rgba(219,112,147,0.12)}
a.pt-link:hover{transform:scale(1.14);z-index:10;border-color:rgba(219,112,147,0.5);box-shadow:0 0 12px rgba(255,182,213,0.3),0 5px 12px rgba(219,112,147,0.12)}
.pt-cell{aspect-ratio:1;border:1.5px solid transparent;border-radius:5px;display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:0;background:transparent!important;box-shadow:none!important}
.pt-num{font-size:0.5em;color:rgba(255,255,255,0.92);line-height:1;font-family:'Segoe UI',sans-serif;text-shadow:0 1px 2px rgba(0,0,0,0.5)}
.pt-sym{font-size:0.85em;font-weight:800;color:#fff;line-height:1.2;text-shadow:0 1px 3px rgba(0,0,0,0.55);font-family:'Segoe UI',sans-serif}

/* Legend section — pink border */
.pt-legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px;padding-top:14px;border-top:1px solid rgba(219,112,147,0.15)}
.pt-legend-item{display:flex;align-items:center;gap:6px;font-size:0.72em;color:color-mix(in srgb, var(--text-color) 75%, transparent);font-family:'Segoe UI',sans-serif}
.pt-legend-dot{width:10px;height:10px;border-radius:3px;flex-shrink:0}

/* Popup Styles — pink-tinted glassmorphism */
.pt-popup{display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(80,20,50,0.4);backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);z-index:999999;justify-content:center;align-items:center}
.pt-popup:target{display:flex}

.pt-popup-content{background:rgba(40,16,24,0.92);border:2px solid rgba(244,167,193,0.45);border-radius:24px;padding:28px;width:90%;max-width:630px;max-height:80vh;overflow-y:auto;position:relative;box-shadow:0 24px 60px rgba(80,20,50,0.45),0 4px 16px rgba(0,0,0,0.3),inset 0 1px 0 rgba(255,214,232,0.2);color:#ffffff !important;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;animation:pt-scaleup 0.26s cubic-bezier(0.16,1,0.3,1)}
@keyframes pt-scaleup{from{opacity:0;transform:scale(0.93)}to{opacity:1;transform:scale(1)}}

/* Circle Close Button — pink accent */
a.pt-popup-close{position:absolute;top:20px;right:20px;width:32px;height:32px;border-radius:50%;background:rgba(255,182,213,0.1);border:1px solid rgba(255,182,213,0.2);display:flex;align-items:center;justify-content:center;color:rgba(255,214,232,0.65) !important;text-decoration:none !important;transition:all 0.2s ease;cursor:pointer}
a.pt-popup-close:hover{background:rgba(255,182,213,0.22);color:#ffffff !important;transform:scale(1.05)}

/* Detail panel card items */
.pt-detail-header{display:flex;align-items:center;gap:20px;margin-bottom:16px}
.pt-detail-symbol{border:1.5px solid rgba(255,182,213,0.3);border-radius:14px;width:85px;height:85px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(80,20,50,0.2);flex-shrink:0}
.pt-detail-name{font-size:1.6em;font-weight:700;color:#ffffff !important;line-height:1.2}
.pt-detail-sub{font-size:0.9em;color:rgba(255,214,232,0.65);margin-top:4px}
.pt-detail-divider{height:1.5px;background:rgba(255,182,213,0.18);margin:18px 0 20px 0}
.pt-detail-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}

.pt-detail-card{background:rgba(244,167,193,0.1);border:1px solid rgba(244,167,193,0.22);border-radius:10px;padding:12px 14px;transition:background-color 0.2s}
.pt-detail-card:hover{background:rgba(244,167,193,0.18)}
.pt-detail-label{font-size:0.72em;color:rgba(255,214,232,0.5);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;font-weight:500}
.pt-detail-value{font-size:0.95em;color:#ffffff !important;font-weight:600}
.pt-detail-summary{margin-top:18px;padding:16px;background:rgba(244,167,193,0.08);border-radius:10px;border:1px solid rgba(244,167,193,0.2);font-size:0.88em;line-height:1.6;color:rgba(255,240,245,0.9)}

/* Elegant Thin Scrollbar for Popup Content */
.pt-popup-content::-webkit-scrollbar{width:6px}
.pt-popup-content::-webkit-scrollbar-track{background:transparent}
.pt-popup-content::-webkit-scrollbar-thumb{background:rgba(255,182,213,0.3);border-radius:3px}
.pt-popup-content::-webkit-scrollbar-thumb:hover{background:rgba(255,182,213,0.5)}

/* Search Result Panel — pink soft */
.pt-search-results{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin-top:12px;max-width:980px}
.pt-search-result-box{display:flex;align-items:center;justify-content:space-between;gap:14px;background:rgba(252,228,236,0.45);border:1px solid rgba(219,112,147,0.28);border-radius:12px;padding:12px 14px;font-family:'Segoe UI',sans-serif;color:var(--text-color);box-sizing:border-box;min-width:0}
.pt-search-info{display:flex;align-items:center;gap:14px;font-size:0.92em;flex-grow:1}
.pt-search-badge{width:36px;height:36px;border-radius:8px;display:inline-flex;align-items:center;justify-content:center;font-weight:800;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.2);flex-shrink:0}
.pt-search-details{display:flex;flex-direction:column;min-width:0}
.pt-search-title{font-weight:700;font-size:1.05em;color:var(--text-color)}
.pt-search-subtitle{font-size:0.8em;color:color-mix(in srgb, var(--text-color) 60%, transparent);margin-top:2px;line-height:1.35}
a.pt-search-button{text-decoration:none!important;color:var(--text-color)!important;background:rgba(248, 187, 208, 0.38);border:1px solid rgba(219, 112, 147, 0.42);padding:8px 16px;border-radius:10px;font-size:0.82em;font-weight:600;transition:all 0.2s ease;flex-shrink:0;box-shadow:0 2px 5px rgba(219,112,147,0.08)}
a.pt-search-button:hover{background:rgba(244, 167, 193, 0.5);border-color:rgba(219,112,147,0.5);transform:translateY(-1px);box-shadow:0 4px 10px rgba(219,112,147,0.12)}

.pt-mobile-list{display:none}
.pt-mobile-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:10px;margin-top:12px}
.pt-mobile-card{display:flex;align-items:center;gap:10px;text-decoration:none!important;color:var(--text-color)!important;background:rgba(255,214,232,0.1);border:1px solid rgba(219,112,147,0.12);border-radius:10px;padding:10px;min-width:0}
.pt-mobile-badge{width:42px;height:42px;border-radius:9px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;flex-shrink:0;border:1px solid rgba(255,255,255,0.22);text-shadow:0 1px 3px rgba(0,0,0,0.5)}
.pt-mobile-num{font-size:0.58em;line-height:1}
.pt-mobile-sym{font-size:1em;font-weight:800;line-height:1.05}
.pt-mobile-name{font-weight:700;font-size:0.92em;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pt-mobile-cat{font-size:0.74em;color:color-mix(in srgb,var(--text-color) 58%,transparent);line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

@media (max-width: 760px){
    .pt-container{overflow-x:visible}
    .pt-table-grid{display:none}
    .pt-mobile-list{display:block}
    .pt-title{font-size:1.35rem;margin-bottom:4px}
    .pt-helper{font-size:0.8rem;margin-bottom:10px}
    .pt-popup{align-items:center; justify-content:center}
    .pt-popup-content{width:92%; max-width:440px; max-height:82vh; border-radius:18px; padding:18px 16px; box-sizing:border-box}
    a.pt-popup-close{top:14px; right:14px; width:28px; height:28px}
    .pt-detail-header{gap:12px; margin-bottom:12px}
    .pt-detail-symbol{width:52px; height:52px; border-radius:10px}
    .pt-detail-symbol > span:first-child{font-size:0.62em !important}
    .pt-detail-symbol > span:last-child{font-size:1.4em !important}
    .pt-detail-name{font-size:1.25em !important}
    .pt-detail-sub{font-size:0.8em !important}
    .pt-detail-divider{margin:10px 0 12px 0 !important}
    .pt-detail-grid{grid-template-columns:repeat(2, 1fr) !important; gap:6px !important}
    .pt-detail-card{padding:6px 8px !important; border-radius:6px !important}
    .pt-detail-label{font-size:0.62em !important; margin-bottom:2px !important}
    .pt-detail-value{font-size:0.8em !important}
    .pt-detail-summary{margin-top:10px !important; padding:10px !important; font-size:0.8em !important; line-height:1.4 !important; border-radius:6px !important}
    .pt-search-result-box{align-items:flex-start;flex-direction:column}
    a.pt-search-button{width:100%;text-align:center;box-sizing:border-box}
}
</style>""", unsafe_allow_html=True)

# ==========================
# DATABASE SENYAWA UMUM
# ==========================
COMPOUNDS_DB = {
    "NaCl": "Natrium Klorida",
    "NaOH": "Natrium Hidroksida",
    "KOH": "Kalium Hidroksida",
    "HCl": "Asam Klorida",
    "H2SO4": "Asam Sulfat",
    "HNO3": "Asam Nitrat",
    "CH3COOH": "Asam Asetat",
    "KMnO4": "Kalium Permanganat",
    "Ca(OH)2": "Kalsium Hidroksida",
    "Al2(SO4)3": "Aluminium Sulfat",
    "CuSO4": "Tembaga(II) Sulfat",
    "AgNO3": "Perak Nitrat",
    "BaCl2": "Barium Klorida",
    "MgCl2": "Magnesium Klorida",
    "K2Cr2O7": "Kalium Dikromat",
    "FeCl3": "Besi(III) Klorida",
}

# ==========================
# DATA UNSUR LOKAL (FALLBACK)
# ==========================
LOCAL_ELEMENTS = [
    {"number":1,"symbol":"H","name":"Hydrogen","category":"diatomic nonmetal","atomic_mass":1.008,"phase":"Gas","density":0.00008988,"melt":13.99,"boil":20.271,"electron_configuration":"1s1","electronegativity":2.20,"discovered_by":"Henry Cavendish","appearance":"colorless gas","summary":"Hydrogen is a chemical element with chemical symbol H and atomic number 1.","xpos":1,"ypos":1},
    {"number":6,"symbol":"C","name":"Carbon","category":"polyatomic nonmetal","atomic_mass":12.011,"phase":"Solid","density":2.267,"melt":3823,"boil":4098,"electron_configuration":"[He] 2s2 2p2","electronegativity":2.55,"discovered_by":"Ancient Egypt","appearance":"","summary":"Carbon is a chemical element with symbol C and atomic number 6.","xpos":14,"ypos":2},
    {"number":7,"symbol":"N","name":"Nitrogen","category":"diatomic nonmetal","atomic_mass":14.007,"phase":"Gas","density":0.0012506,"melt":63.15,"boil":77.36,"electron_configuration":"[He] 2s2 2p3","electronegativity":3.04,"discovered_by":"Daniel Rutherford","appearance":"colorless gas","summary":"Nitrogen is a chemical element with symbol N and atomic number 7.","xpos":15,"ypos":2},
    {"number":8,"symbol":"O","name":"Oxygen","category":"diatomic nonmetal","atomic_mass":15.999,"phase":"Gas","density":0.001429,"melt":54.36,"boil":90.20,"electron_configuration":"[He] 2s2 2p4","electronegativity":3.44,"discovered_by":"Carl Wilhelm Scheele","appearance":"","summary":"Oxygen is a chemical element with symbol O and atomic number 8.","xpos":16,"ypos":2},
    {"number":11,"symbol":"Na","name":"Sodium","category":"alkali metal","atomic_mass":22.990,"phase":"Solid","density":0.971,"melt":370.87,"boil":1156,"electron_configuration":"[Ne] 3s1","electronegativity":0.93,"discovered_by":"Humphry Davy","appearance":"silvery white metallic","summary":"Sodium is a chemical element with symbol Na and atomic number 11.","xpos":1,"ypos":3},
    {"number":12,"symbol":"Mg","name":"Magnesium","category":"alkaline earth metal","atomic_mass":24.305,"phase":"Solid","density":1.738,"melt":923,"boil":1363,"electron_configuration":"[Ne] 3s2","electronegativity":1.31,"discovered_by":"Joseph Black","appearance":"shiny grey solid","summary":"Magnesium is a chemical element with symbol Mg and atomic number 12.","xpos":2,"ypos":3},
    {"number":13,"symbol":"Al","name":"Aluminium","category":"post-transition metal","atomic_mass":26.982,"phase":"Solid","density":2.698,"melt":933.47,"boil":2792,"electron_configuration":"[Ne] 3s2 3p1","electronegativity":1.61,"discovered_by":"","appearance":"silvery gray metallic","summary":"Aluminium is a chemical element with symbol Al and atomic number 13.","xpos":13,"ypos":3},
    {"number":16,"symbol":"S","name":"Sulfur","category":"polyatomic nonmetal","atomic_mass":32.06,"phase":"Solid","density":2.067,"melt":388.36,"boil":717.87,"electron_configuration":"[Ne] 3s2 3p4","electronegativity":2.58,"discovered_by":"Ancient china","appearance":"lemon yellow sintered microcrystals","summary":"Sulfur is a chemical element with symbol S and atomic number 16.","xpos":16,"ypos":3},
    {"number":17,"symbol":"Cl","name":"Chlorine","category":"halogen","atomic_mass":35.45,"phase":"Gas","density":0.003214,"melt":171.6,"boil":239.11,"electron_configuration":"[Ne] 3s2 3p5","electronegativity":3.16,"discovered_by":"Carl Wilhelm Scheele","appearance":"pale yellow-green gas","summary":"Chlorine is a chemical element with symbol Cl and atomic number 17.","xpos":17,"ypos":3},
    {"number":19,"symbol":"K","name":"Potassium","category":"alkali metal","atomic_mass":39.098,"phase":"Solid","density":0.862,"melt":336.53,"boil":1032,"electron_configuration":"[Ar] 4s1","electronegativity":0.82,"discovered_by":"Humphry Davy","appearance":"silvery gray","summary":"Potassium is a chemical element with symbol K and atomic number 19.","xpos":1,"ypos":4},
    {"number":20,"symbol":"Ca","name":"Calcium","category":"alkaline earth metal","atomic_mass":40.078,"phase":"Solid","density":1.55,"melt":1115,"boil":1757,"electron_configuration":"[Ar] 4s2","electronegativity":1.00,"discovered_by":"Humphry Davy","appearance":"","summary":"Calcium is a chemical element with symbol Ca and atomic number 20.","xpos":2,"ypos":4},
    {"number":24,"symbol":"Cr","name":"Chromium","category":"transition metal","atomic_mass":51.996,"phase":"Solid","density":7.15,"melt":2180,"boil":2944,"electron_configuration":"[Ar] 3d5 4s1","electronegativity":1.66,"discovered_by":"Louis Nicolas Vauquelin","appearance":"silvery metallic","summary":"Chromium is a chemical element with symbol Cr and atomic number 24.","xpos":6,"ypos":4},
    {"number":25,"symbol":"Mn","name":"Manganese","category":"transition metal","atomic_mass":54.938,"phase":"Solid","density":7.44,"melt":1519,"boil":2334,"electron_configuration":"[Ar] 3d5 4s2","electronegativity":1.55,"discovered_by":"Torbern Olof Bergman","appearance":"silvery metallic","summary":"Manganese is a chemical element with symbol Mn and atomic number 25.","xpos":7,"ypos":4},
    {"number":26,"symbol":"Fe","name":"Iron","category":"transition metal","atomic_mass":55.845,"phase":"Solid","density":7.874,"melt":1811,"boil":3134,"electron_configuration":"[Ar] 3d6 4s2","electronegativity":1.83,"discovered_by":"5000 BC","appearance":"lustrous metallic with a grayish tinge","summary":"Iron is a chemical element with symbol Fe and atomic number 26.","xpos":8,"ypos":4},
    {"number":29,"symbol":"Cu","name":"Copper","category":"transition metal","atomic_mass":63.546,"phase":"Solid","density":8.96,"melt":1357.77,"boil":2835,"electron_configuration":"[Ar] 3d10 4s1","electronegativity":1.90,"discovered_by":"Middle East","appearance":"red-orange metallic luster","summary":"Copper is a chemical element with symbol Cu and atomic number 29.","xpos":11,"ypos":4},
    {"number":30,"symbol":"Zn","name":"Zinc","category":"transition metal","atomic_mass":65.38,"phase":"Solid","density":7.134,"melt":692.68,"boil":1180,"electron_configuration":"[Ar] 3d10 4s2","electronegativity":1.65,"discovered_by":"India","appearance":"silver-gray","summary":"Zinc is a chemical element with symbol Zn and atomic number 30.","xpos":12,"ypos":4},
    {"number":47,"symbol":"Ag","name":"Silver","category":"transition metal","atomic_mass":107.868,"phase":"Solid","density":10.501,"melt":1234.93,"boil":2435,"electron_configuration":"[Kr] 4d10 5s1","electronegativity":1.93,"discovered_by":"unknown","appearance":"lustrous white metal","summary":"Silver is a chemical element with symbol Ag and atomic number 47.","xpos":11,"ypos":5},
    {"number":56,"symbol":"Ba","name":"Barium","category":"alkaline earth metal","atomic_mass":137.327,"phase":"Solid","density":3.594,"melt":1000,"boil":2170,"electron_configuration":"[Xe] 6s2","electronegativity":0.89,"discovered_by":"Carl Wilhelm Scheele","appearance":"","summary":"Barium is a chemical element with symbol Ba and atomic number 56.","xpos":2,"ypos":6},
    {"number":53,"symbol":"I","name":"Iodine","category":"halogen","atomic_mass":126.904,"phase":"Solid","density":4.93,"melt":386.85,"boil":457.4,"electron_configuration":"[Kr] 4d10 5s2 5p5","electronegativity":2.66,"discovered_by":"Bernard Courtois","appearance":"lustrous metallic gray, violet as a gas","summary":"Iodine is a chemical element with symbol I and atomic number 53.","xpos":17,"ypos":5},
]

# ==========================
# LOAD DATA PERIODIK
# ==========================
@st.cache_data
def load_elements():
    url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json"
    use_local = False
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()["elements"]
    except (requests.RequestException, KeyError, ValueError):
        data = None
        use_local = True

    if data is not None:
        elements = []
        for e in data:
            if int(e.get("number", 0)) > 118:
                continue
            elements.append({
                "number": e["number"],
                "symbol": e["symbol"],
                "name": e["name"],
                "category": e.get("category", ""),
                "atomic_mass": e.get("atomic_mass", ""),
                "phase": e.get("phase", ""),
                "density": e.get("density", ""),
                "melt": e.get("melt", ""),
                "boil": e.get("boil", ""),
                "electron_configuration": e.get("electron_configuration_semantic", ""),
                "electronegativity": e.get("electronegativity_pauling", ""),
                "discovered_by": e.get("discovered_by", ""),
                "appearance": e.get("appearance", ""),
                "summary": e.get("summary", ""),
                "xpos": e["xpos"],
                "ypos": e["ypos"]
            })
        return pd.DataFrame(elements).sort_values("number").reset_index(drop=True), use_local
    else:
        return pd.DataFrame(LOCAL_ELEMENTS).sort_values("number").reset_index(drop=True), use_local


def parse_formula(formula):
    formula = formula.strip()
    if not formula:
        raise ValueError("Rumus molekul tidak boleh kosong.")

    stack = [{}]
    index = 0

    while index < len(formula):
        char = formula[index]

        if char == "(":
            stack.append({})
            index += 1
            continue

        if char == ")":
            if len(stack) == 1:
                raise ValueError("Tanda kurung penutup tidak memiliki pasangan.")

            group_counts = stack.pop()
            if not group_counts:
                raise ValueError("Tanda kurung tidak boleh kosong.")
            index += 1
            multiplier_match = re.match(r"\d+", formula[index:])
            multiplier = int(multiplier_match.group()) if multiplier_match else 1
            if multiplier <= 0:
                raise ValueError("Jumlah atom setelah kurung harus lebih dari 0.")
            if multiplier_match:
                index += len(multiplier_match.group())

            for symbol, count in group_counts.items():
                stack[-1][symbol] = stack[-1].get(symbol, 0) + count * multiplier
            continue

        if char.isupper():
            symbol = char
            index += 1

            if index < len(formula) and formula[index].islower():
                symbol += formula[index]
                index += 1

            number_match = re.match(r"\d+", formula[index:])
            count = int(number_match.group()) if number_match else 1
            if count <= 0:
                raise ValueError("Jumlah atom harus lebih dari 0.")
            if number_match:
                index += len(number_match.group())

            stack[-1][symbol] = stack[-1].get(symbol, 0) + count
            continue

        if char.isdigit():
            raise ValueError("Angka harus ditulis setelah simbol unsur atau tanda kurung.")

        raise ValueError(f"Karakter '{char}' tidak valid dalam rumus molekul.")

    if len(stack) != 1:
        raise ValueError("Tanda kurung buka belum ditutup.")

    if not stack[0]:
        raise ValueError("Rumus molekul tidak valid.")

    return stack[0]


def calculate_mr(formula, elements_data):
    composition = parse_formula(formula)
    atomic_masses = {
        str(row["symbol"]): float(row["atomic_mass"])
        for _, row in elements_data.iterrows()
    }

    details = []
    total_mr = 0.0

    for symbol, count in composition.items():
        if symbol not in atomic_masses:
            raise ValueError(f"Unsur '{symbol}' tidak ditemukan di data tabel periodik.")

        atomic_mass = atomic_masses[symbol]
        subtotal = count * atomic_mass
        details.append({
            "Unsur": symbol,
            "Jumlah Atom": count,
            "Ar": atomic_mass,
            "Subtotal": subtotal
        })
        total_mr += subtotal

    return total_mr, details


def calculate_mass_molarity(molarity, mr, volume_ml):
    return molarity * mr * volume_ml / 1000


def calculate_mass_normality(normality, mr, valence, volume_ml):
    return normality * mr * valence * volume_ml / 1000


def format_decimal(value, decimals=2):
    return f"{value:.{decimals}f}".replace(".", ",")


def make_result_table(rows):
    return pd.DataFrame(rows, columns=["Parameter", "Hasil"])


def make_mr_detail_table(details):
    return pd.DataFrame([
        {
            "Unsur": item["Unsur"],
            "Perhitungan": (
                f'{item["Jumlah Atom"]} x {format_decimal(item["Ar"], 2)} = '
                f'{format_decimal(item["Subtotal"], 2)}'
            )
        }
        for item in details
    ])

# ==========================
# SIDEBAR
# ==========================
menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Beranda",
        "⚛️ Tabel Periodik",
        "🧪 Pembuatan Larutan",
        "💧 Pengenceran"
    ]
)

# ==========================
# BERANDA
# ==========================
if menu == "🏠 Beranda":

    # --- Beranda CSS — Tema pastel pink -----
    st.markdown("""<style>
    .beranda-hero{background:linear-gradient(135deg, rgba(248, 187, 208, 0.55), rgba(255, 240, 246, 0.85), rgba(241, 230, 255, 0.45));border:1.5px solid rgba(219, 112, 147, 0.28);border-radius:18px;padding:38px 34px 30px;margin-bottom:24px;position:relative;overflow:hidden}
    .beranda-hero::before{content:'⚛️';position:absolute;right:-18px;top:-18px;font-size:8rem;opacity:0.06;pointer-events:none}
    .beranda-hero-title{font-size:2.4rem;font-weight:800;color:var(--text-color);margin:0 0 4px;font-family:'Segoe UI',sans-serif;line-height:1.15}
    .beranda-hero-sub{font-size:1.05rem;font-weight:600;color:color-mix(in srgb,var(--text-color) 68%,transparent);margin:0 0 14px;font-family:'Segoe UI',sans-serif}
    .beranda-hero-desc{font-size:0.92rem;color:color-mix(in srgb,var(--text-color) 72%,transparent);line-height:1.65;margin:0 0 18px;max-width:680px;font-family:'Segoe UI',sans-serif}
    .beranda-badge{display:inline-block;background:rgba(255,182,213,0.25);border:1px solid rgba(219,112,147,0.3);border-radius:20px;padding:5px 14px;font-size:0.78rem;font-weight:600;color:color-mix(in srgb,var(--text-color) 65%,transparent);letter-spacing:0.3px;font-family:'Segoe UI',sans-serif}
    .beranda-card{background:rgba(252, 228, 236, 0.45);border:1.5px solid rgba(219, 112, 147, 0.22);border-radius:14px;padding:22px 20px;height:100%;box-sizing:border-box;transition:all 0.2s}
    .beranda-card:hover{background:rgba(248, 187, 208, 0.38);border-color:rgba(219, 112, 147, 0.45);transform:translateY(-2px);box-shadow:0 6px 18px rgba(219, 112, 147, 0.14)}
    .beranda-card-icon{font-size:1.6rem;margin-bottom:8px}
    .beranda-card-title{font-size:1rem;font-weight:700;color:var(--text-color);margin-bottom:6px;font-family:'Segoe UI',sans-serif}
    .beranda-card-text{font-size:0.85rem;color:color-mix(in srgb,var(--text-color) 65%,transparent);line-height:1.55;font-family:'Segoe UI',sans-serif}
    .beranda-section-title{font-size:1.1rem;font-weight:700;color:var(--text-color);margin:20px 0 6px;font-family:'Segoe UI',sans-serif}
    .beranda-member{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(219,112,147,0.1);font-family:'Segoe UI',sans-serif}
    .beranda-member:last-child{border-bottom:none}
    .beranda-member-num{width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,rgba(255,182,213,0.35),rgba(232,222,255,0.35));display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;color:var(--text-color);flex-shrink:0}
    .beranda-member-name{font-size:0.88rem;color:var(--text-color);font-weight:500}
    .beranda-member-nim{font-size:0.78rem;color:color-mix(in srgb,var(--text-color) 50%,transparent);margin-left:4px}
    </style>""", unsafe_allow_html=True)

    # --- 1. Hero Card ---
    st.markdown("""
    <div class="beranda-hero">
        <div class="beranda-hero-title">Periodicalc</div>
        <div class="beranda-hero-sub">Tabel Periodik, Pembuatan Larutan, dan Pengenceran Larutan</div>
        <div class="beranda-hero-desc">
            Aplikasi berbasis Python dan Streamlit untuk membantu pengguna memahami tabel periodik
            serta melakukan perhitungan pembuatan larutan dan pengenceran larutan.
        </div>
        <div class="beranda-badge">Kelompok 5 • LPK 2026</div>
    </div>
    """, unsafe_allow_html=True)

    # --- 2. Tentang Aplikasi & Kelompok 5 ---
    with st.expander("🌸 Tentang Aplikasi & Kelompok 5", expanded=False):
        st.markdown("""
**Selamat Datang di Periodicalc!**

Periodicalc adalah aplikasi yang dirancang sebagai alat bantu interaktif untuk mempermudah pengguna
dalam memahami tabel periodik, menghitung pembuatan larutan, dan menghitung pengenceran larutan.

---

**Tujuan & Kegunaan:**
- Mengetahui bobot molekul suatu senyawa beserta karakteristiknya dalam tabel periodik.
- Mengetahui suatu massa yang diperlukan untuk membuat suatu larutan serta cara pembuatan larutan.
- Mengetahui konsentrasi atau volume yang diinginkan dalam pengenceran suatu larutan.

---

**Sumber Data:**

Data unsur pada tabel periodik diambil dari sumber data online, lalu aplikasi juga memiliki data lokal
sebagai cadangan jika data online gagal dimuat.

---

**Fitur Utama:**

1. **Tabel Periodik** — Menampilkan data unsur kimia, detail unsur, kategori unsur, dan fitur pencarian unsur.
2. **Pembuatan Larutan** — Menghitung Mr dari rumus molekul, lalu menghitung massa zat yang harus ditimbang berdasarkan molaritas atau normalitas.
3. **Pengenceran** — Menghitung V₁ atau M₁ menggunakan rumus M₁V₁ = M₂V₂.
        """)

        st.markdown("---")
        st.markdown("**Dikembangkan oleh Kelompok 5:**")

        members = [
            ("Fani Aulia Nurfauziah", "2560626"),
            ("Fanny Arrahmah Khaerunnisa", "2560627"),
            ("Mawaddah Dwita Pebyana", "2560668"),
            ("Naila Syafitri Ramadhani", "2560703"),
            ("Najma Faiza Khairiah", "2560706"),
        ]
        members_html = ""
        for i, (nama, nim) in enumerate(members, 1):
            members_html += (
                f'<div class="beranda-member">'
                f'<div class="beranda-member-num">{i}</div>'
                f'<span class="beranda-member-name">{nama}</span>'
                f'<span class="beranda-member-nim">({nim})</span>'
                f'</div>'
            )
        st.markdown(members_html, unsafe_allow_html=True)

    # --- 3. Feature Cards ---
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="beranda-card">
            <div class="beranda-card-icon">⚛️</div>
            <div class="beranda-card-title">Tabel Periodik</div>
            <div class="beranda-card-text">Melihat informasi unsur dan mencari unsur berdasarkan simbol, nama, kategori, atau nomor atom.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="beranda-card">
            <div class="beranda-card-icon">🧪</div>
            <div class="beranda-card-title">Pembuatan Larutan</div>
            <div class="beranda-card-text">Menghitung Mr dan massa zat yang harus ditimbang berdasarkan konsentrasi dan volume larutan.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="beranda-card">
            <div class="beranda-card-icon">💧</div>
            <div class="beranda-card-title">Pengenceran</div>
            <div class="beranda-card-text">Menghitung volume atau konsentrasi larutan awal menggunakan rumus pengenceran.</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================
# TABEL PERIODIK
# ==========================
elif menu == "⚛️ Tabel Periodik":

    df, _local_mode = load_elements()
    if _local_mode:
        st.warning("⚠️ Data online gagal dimuat, aplikasi memakai data unsur lokal.")

    # Category colors
    cat_colors = {
        "alkali metal": "rgba(255,107,107,0.85)",
        "alkaline earth metal": "rgba(255,177,66,0.85)",
        "transition metal": "rgba(99,179,237,0.8)",
        "post-transition metal": "rgba(130,201,30,0.8)",
        "metalloid": "rgba(255,212,59,0.85)",
        "nonmetal": "rgba(56,178,172,0.85)",
        "diatomic nonmetal": "rgba(56,178,172,0.85)",
        "polyatomic nonmetal": "rgba(56,178,172,0.85)",
        "halogen": "rgba(159,122,234,0.85)",
        "noble gas": "rgba(237,100,166,0.85)",
        "lanthanide": "rgba(246,135,179,0.8)",
        "actinide": "rgba(183,148,244,0.8)",
        "unknown, probably transition metal": "rgba(99,179,237,0.5)",
        "unknown, probably post-transition metal": "rgba(130,201,30,0.5)",
        "unknown, probably metalloid": "rgba(255,212,59,0.5)",
        "unknown, predicted to be noble gas": "rgba(237,100,166,0.5)",
    }

    # Build cells lookup
    cells = {}
    for _, row in df.iterrows():
        cells[(int(row["ypos"]), int(row["xpos"]))] = row

    # --- Build HTML grid (NO indentation to avoid markdown code block interpretation) ---
    def clean_text(value):
        if value == "" or value is None or (isinstance(value, float) and pd.isna(value)):
            return ""
        return escape(str(value), quote=True)

    def fmt(val, unit=""):
        if val == "" or val is None or (isinstance(val, float) and pd.isna(val)):
            return "&mdash;"
        return escape(f"{val} {unit}".strip(), quote=True)

    # Terjemahan kategori ke Bahasa Indonesia
    category_id = {
        "alkali metal": "Logam Alkali",
        "alkaline earth metal": "Logam Alkali Tanah",
        "transition metal": "Logam Transisi",
        "post-transition metal": "Logam Pasca-Transisi",
        "metalloid": "Metaloid",
        "nonmetal": "Nonlogam",
        "diatomic nonmetal": "Nonlogam Diatomik",
        "polyatomic nonmetal": "Nonlogam Poliatomik",
        "halogen": "Halogen",
        "noble gas": "Gas Mulia",
        "lanthanide": "Lantanida",
        "actinide": "Aktinida",
        "unknown, probably transition metal": "Belum Diketahui (kemungkinan Logam Transisi)",
        "unknown, probably post-transition metal": "Belum Diketahui (kemungkinan Logam Pasca-Transisi)",
        "unknown, probably metalloid": "Belum Diketahui (kemungkinan Metaloid)",
        "unknown, predicted to be noble gas": "Belum Diketahui (prediksi Gas Mulia)",
    }

    # Terjemahan fase ke Bahasa Indonesia
    phase_id = {
        "solid": "Padat",
        "liquid": "Cair",
        "gas": "Gas",
    }

    def category_title(value):
        if not value or (isinstance(value, float) and pd.isna(value)):
            return "&mdash;"
        key = str(value).lower().strip()
        translated = category_id.get(key)
        if translated:
            return escape(translated, quote=True)
        return clean_text(str(value).title())

    def fmt_phase(val):
        if val == "" or val is None or (isinstance(val, float) and pd.isna(val)):
            return "&mdash;"
        key = str(val).lower().strip()
        translated = phase_id.get(key)
        if translated:
            return escape(translated, quote=True)
        return escape(str(val), quote=True)

    def make_cell(el):
        cat = str(el["category"]).lower()
        bg = cat_colors.get(cat, "rgba(100,200,255,0.6)")
        sym = clean_text(el["symbol"])
        name = clean_text(el["name"])
        num = int(el["number"])
        return (
            f'<a class="pt-link" style="background:{bg}" '
            f'href="#detail-{sym}" title="{name} ({num})">'
            f'<span class="pt-num">{num}</span>'
            f'<span class="pt-sym">{sym}</span></a>'
        )

    empty_cell = '<div class="pt-cell"></div>'
    blank_axis = '<div class="pt-axis-label"></div>'

    def make_grid_row(label, ypos, label_class="pt-period-label"):
        r = [f'<div class="pt-axis-label {label_class}">{label}</div>']
        for group in range(1, 19):
            key = (ypos, group)
            r.append(make_cell(cells[key]) if key in cells else empty_cell)
        return '<div class="pt-row">' + ''.join(r) + '</div>'

    rows = []
    group_labels = [blank_axis] + [
        f'<div class="pt-axis-label">{group}</div>'
        for group in range(1, 19)
    ]
    rows.append('<div class="pt-row pt-group-row">' + ''.join(group_labels) + '</div>')

    # Periods 1-7
    for period in range(1, 8):
        rows.append(make_grid_row(period, period))

    # Spacer
    rows.append('<div class="pt-row pt-spacer-row">' + blank_axis + (empty_cell * 18) + '</div>')

    # Lanthanides and actinides follow the source dataset's f-block rows.
    rows.append(make_grid_row("La-Lu", 9, "pt-series-label"))
    rows.append(make_grid_row("Ac-Lr", 10, "pt-series-label"))

    grid_html = ''.join(rows)

    # Legend items
    legend = (
        '<div class="pt-legend">'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(56,178,172,0.85)"></div>Nonlogam</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(255,107,107,0.85)"></div>Logam Alkali</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(255,177,66,0.85)"></div>Logam Alkali Tanah</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(99,179,237,0.8)"></div>Logam Transisi</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(130,201,30,0.8)"></div>Logam Pasca-Transisi</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(255,212,59,0.85)"></div>Metaloid</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(237,100,166,0.85)"></div>Gas Mulia</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(246,135,179,0.8)"></div>Lantanida</div>'
        '<div class="pt-legend-item"><div class="pt-legend-dot" style="background:rgba(183,148,244,0.8)"></div>Aktinida</div>'
        '</div>'
    )

    # --- Generate Popups for all 118 elements ---
    popups = []
    for _, el in df.iterrows():
        sym = clean_text(el["symbol"])
        name = clean_text(el["name"])
        num = int(el["number"])
        cat = str(el["category"]).lower()
        bg = cat_colors.get(cat, "rgba(100,200,255,0.6)")

        detail_cards = (
            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Massa Atom</div>'
            f'<div class="pt-detail-value">{fmt(el["atomic_mass"], "u")}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Kategori</div>'
            f'<div class="pt-detail-value">{category_title(el["category"])}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Fase (STP)</div>'
            f'<div class="pt-detail-value">{fmt_phase(el["phase"])}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Densitas</div>'
            f'<div class="pt-detail-value">{fmt(el["density"], "g/cm3")}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Titik Leleh</div>'
            f'<div class="pt-detail-value">{fmt(el["melt"], "K")}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Titik Didih</div>'
            f'<div class="pt-detail-value">{fmt(el["boil"], "K")}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Konfigurasi Elektron</div>'
            f'<div class="pt-detail-value" style="font-size:0.82em">{fmt(el["electron_configuration"])}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Elektronegativitas (Pauling)</div>'
            f'<div class="pt-detail-value">{fmt(el["electronegativity"])}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Penampilan</div>'
            f'<div class="pt-detail-value" style="font-size:0.82em;text-transform:capitalize">{fmt(el["appearance"])}</div></div>'

            '<div class="pt-detail-card">'
            '<div class="pt-detail-label">Ditemukan Oleh</div>'
            f'<div class="pt-detail-value" style="font-size:0.82em">{fmt(el["discovered_by"])}</div></div>'
        )

        # Buat ringkasan berbahasa Indonesia dari data unsur
        phase_text = fmt_phase(el["phase"]).replace("&mdash;", "").strip()
        cat_text = category_title(el["category"]).replace("&mdash;", "").strip()
        mass_text = fmt(el["atomic_mass"], "u").replace("&mdash;", "").strip()

        ringkasan_parts = [f"{name} adalah unsur kimia dengan simbol {sym} dan nomor atom {num}."]
        if mass_text:
            ringkasan_parts.append(f"Massa atomnya adalah {mass_text}.")
        if cat_text:
            ringkasan_parts.append(f"Unsur ini termasuk dalam kategori {cat_text}.")
        if phase_text:
            ringkasan_parts.append(f"Pada kondisi standar (STP), unsur ini berfase {phase_text}.")

        ringkasan = " ".join(ringkasan_parts)

        summary_html = (
            '<div class="pt-detail-summary">'
            '<strong style="color:rgba(255,255,255,0.65);font-size:0.85em">Ringkasan:</strong><br>'
            f'{escape(ringkasan, quote=True)}'
            '</div>'
        )

        popup_html = (
            f'<div id="detail-{sym}" class="pt-popup">'
            f'<div class="pt-popup-content">'
            f'<a href="#" class="pt-popup-close">'
            f'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:block">'
            f'<line x1="18" y1="6" x2="6" y2="18"></line>'
            f'<line x1="6" y1="6" x2="18" y2="18"></line>'
            f'</svg>'
            f'</a>'
            f'<div class="pt-detail-header">'
            f'<div class="pt-detail-symbol" style="background:{bg}">'
            f'<span style="font-size:0.75em;color:rgba(255,255,255,0.85)">{num}</span>'
            f'<span style="font-size:2em;font-weight:800;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,0.3)">{sym}</span>'
            f'</div>'
            f'<div>'
            f'<div class="pt-detail-name">{name}</div>'
            f'<div class="pt-detail-sub">Nomor Atom {num} &middot; {category_title(el["category"])}</div>'
            f'</div></div>'
            f'<div class="pt-detail-divider"></div>'
            f'<div class="pt-detail-grid">{detail_cards}</div>'
            f'{summary_html}'
            f'</div></div>'
        )
        popups.append(popup_html)

    all_popups_html = ''.join(popups)

    mobile_cards = []
    for _, el in df.iterrows():
        cat = str(el["category"]).lower()
        bg = cat_colors.get(cat, "rgba(100,200,255,0.6)")
        sym = clean_text(el["symbol"])
        name = clean_text(el["name"])
        num = int(el["number"])
        mobile_cards.append(
            f'<a class="pt-mobile-card" href="#detail-{sym}" title="{name} ({num})">'
            f'<div class="pt-mobile-badge" style="background:{bg}">'
            f'<span class="pt-mobile-num">{num}</span>'
            f'<span class="pt-mobile-sym">{sym}</span>'
            f'</div>'
            f'<div style="min-width:0">'
            f'<div class="pt-mobile-name">{name}</div>'
            f'<div class="pt-mobile-cat">{category_title(el["category"])}</div>'
            f'</div>'
            f'</a>'
        )
    mobile_html = (
        '<div class="pt-mobile-list">'
        '<div class="pt-helper">118 unsur resmi, disusun untuk layar kecil.</div>'
        '<div class="pt-mobile-grid">' + ''.join(mobile_cards) + '</div>'
        '</div>'
    )

    # --- Search section (above the table) ---
    st.subheader("🔍 Cari Unsur")

    cari = st.text_input("Masukkan nama atau simbol unsur")

    query = cari.strip()
    if query:
        query_lower = query.lower()
        searchable = (
            df["symbol"].astype(str).str.lower().str.contains(query_lower, regex=False) |
            df["name"].astype(str).str.lower().str.contains(query_lower, regex=False) |
            df["category"].astype(str).str.lower().str.contains(query_lower, regex=False) |
            df["number"].astype(str).str.contains(query_lower, regex=False)
        )
        hasil = df[searchable].copy()

        if not hasil.empty:
            hasil["rank"] = 2
            hasil.loc[hasil["name"].str.lower().str.startswith(query_lower), "rank"] = 1
            hasil.loc[hasil["symbol"].str.lower().str.startswith(query_lower), "rank"] = 1
            hasil.loc[hasil["name"].str.lower() == query_lower, "rank"] = 0
            hasil.loc[hasil["symbol"].str.lower() == query_lower, "rank"] = 0
            hasil = hasil.sort_values(["rank", "number"]).head(8)

            result_cards = []
            for _, unsur in hasil.iterrows():
                cat = str(unsur["category"]).lower()
                bg = cat_colors.get(cat, "rgba(100,200,255,0.6)")
                sym = clean_text(unsur["symbol"])
                name = clean_text(unsur["name"])
                result_cards.append(
                    '<div class="pt-search-result-box">'
                    '<div class="pt-search-info">'
                    f'<div class="pt-search-badge" style="background:{bg}">{sym}</div>'
                    '<div class="pt-search-details">'
                    f'<span class="pt-search-title">{name}</span>'
                    f'<span class="pt-search-subtitle">Nomor Atom: {int(unsur["number"])} &middot; Massa: {fmt(unsur["atomic_mass"], "u")} &middot; Kategori: {category_title(unsur["category"])}</span>'
                    '</div>'
                    '</div>'
                    f'<a href="#detail-{sym}" class="pt-search-button">Buka Detail</a>'
                    '</div>'
                )
            search_html = '<div class="pt-search-results">' + ''.join(result_cards) + '</div>'
            st.markdown(search_html, unsafe_allow_html=True)
        else:
            st.warning("Unsur tidak ditemukan.")

    st.divider()

    # Render periodic table layout with wrapper to prevent cutoff
    table_html = (
        '<div class="pt-container">'
        '<div class="pt-title">Tabel Periodik</div>'
        '<div class="pt-helper">118 unsur resmi dengan kategori, nomor grup, dan periode.</div>'
        '<div class="pt-table-grid">' + grid_html + legend + '</div>'
        f'{mobile_html}'
        '</div>' + all_popups_html
    )
    st.markdown(table_html, unsafe_allow_html=True)



# ==========================
# PEMBUATAN LARUTAN
# ==========================
elif menu == "🧪 Pembuatan Larutan":

    st.title("🧪 Pembuatan Larutan")

    elements_df, _local_mode = load_elements()
    if _local_mode:
        st.warning("⚠️ Data online gagal dimuat, aplikasi memakai data unsur lokal.")

    tab1, tab2 = st.tabs([
        "Molaritas",
        "Normalitas"
    ])

    # MOLARITAS
    with tab1:

        st.subheader("Pembuatan Larutan Molaritas")
        st.write("Fitur ini membantu menghitung massa zat yang diperlukan untuk membuat larutan dengan konsentrasi dan volume tertentu. Cukup masukkan rumus senyawa, molaritas, dan volume larutan, kemudian sistem akan menghitung massa zat yang harus ditimbang secara otomatis.")

        st.latex(
            r"M=\frac{m}{Mr}\times\frac{1000}{V}"
        )
        st.latex(
            r"m=\frac{M\times Mr\times V}{1000}"
        )

        if "formula_mol_val" not in st.session_state:
            st.session_state.formula_mol_val = ""

        # Apply pending selection before widget renders
        if "_mol_selected" in st.session_state:
            st.session_state.formula_mol_val = st.session_state._mol_selected
            st.session_state["formula_mol_input"] = st.session_state._mol_selected
            del st.session_state._mol_selected

        formula = st.text_input(
            "🧪 Rumus molekul / senyawa",
            value=st.session_state.formula_mol_val,
            placeholder="Ketik rumus: NaCl, H2SO4, Ca(OH)2, MgCl2, ...",
            key="formula_mol_input"
        )

        if formula != st.session_state.formula_mol_val:
            st.session_state.formula_mol_val = formula

        query_mol = formula.strip()
        if query_mol:
            # Show recommendations if not an exact match
            if query_mol not in COMPOUNDS_DB:
                matches_mol = {
                    f: n for f, n in COMPOUNDS_DB.items()
                    if query_mol.lower() in f.lower() or query_mol.lower() in n.lower()
                }
                if matches_mol:
                    st.caption("💡 Rekomendasi senyawa:")
                    for f_key, f_name in matches_mol.items():
                        if st.button(f"{f_key} — {f_name}", key=f"rec_mol_{f_key}"):
                            st.session_state._mol_selected = f_key
                            st.rerun()

        M = st.number_input(
            "Molaritas / Konsentrasi (M)",
            min_value=0.0,
            step=0.01,
            format="%.4f",
            key="molarity_value"
        )

        V = st.number_input(
            "Volume (mL)",
            min_value=0.0,
            step=1.0,
            format="%.2f",
            key="molarity_volume"
        )

        if st.button(
            "Hitung Massa",
            key="calculate_molarity"
        ):
            if not formula.strip():
                st.error("Rumus molekul tidak boleh kosong.")
            elif M <= 0:
                st.error("Konsentrasi harus lebih dari 0.")
            elif V <= 0:
                st.error("Volume harus lebih dari 0.")
            else:
                try:
                    mr, mr_details = calculate_mr(formula, elements_df)
                    massa = calculate_mass_molarity(M, mr, V)
                    compound = formula.strip()

                    st.success(f"Massa yang ditimbang: {format_decimal(massa, 3)} g")
                    st.table(make_result_table([
                        ["Senyawa", compound],
                        ["Mr", f"{format_decimal(mr, 2)} g/mol"],
                        ["Konsentrasi", f"{format_decimal(M, 4).rstrip('0').rstrip(',')} M"],
                        ["Volume", f"{format_decimal(V, 2).rstrip('0').rstrip(',')} mL"],
                        ["Massa yang ditimbang", f"{format_decimal(massa, 3)} g"],
                    ]))

                    st.subheader("Rincian Perhitungan Mr")
                    st.table(make_mr_detail_table(mr_details))
                    st.write(f"Mr {compound} = {format_decimal(mr, 2)} g/mol")

                    st.subheader("Langkah Pembuatan Larutan")
                    st.markdown(
                        "\n".join([
                            f"1. Timbang {format_decimal(massa, 3)} gram {compound}.",
                            "2. Masukkan zat ke dalam gelas kimia atau labu ukur.",
                            "3. Tambahkan aquadest secukupnya untuk melarutkan zat.",
                            f"4. Tambahkan aquadest hingga tanda tera atau hingga volume {format_decimal(V, 2).rstrip('0').rstrip(',')} mL.",
                            "5. Homogenkan larutan."
                        ])
                    )
                except ValueError as exc:
                    st.error(str(exc))

    # NORMALITAS
    with tab2:

        st.subheader("Pembuatan Larutan Normalitas")
        st.write("Fitur ini membantu menghitung massa zat yang diperlukan untuk membuat larutan dengan konsentrasi dan volume tertentu. Cukup masukkan rumus senyawa, normalitas, valensi, dan volume larutan, kemudian sistem akan menghitung massa zat yang harus ditimbang secara otomatis.")

        st.latex(
            r"N=\frac{m}{Mr\times valensi}\times\frac{1000}{V}"
        )
        st.latex(
            r"m=\frac{N\times Mr\times valensi\times V}{1000}"
        )

        if "formula_norm_val" not in st.session_state:
            st.session_state.formula_norm_val = ""

        # Apply pending selection before widget renders
        if "_norm_selected" in st.session_state:
            st.session_state.formula_norm_val = st.session_state._norm_selected
            st.session_state["formula_norm_input"] = st.session_state._norm_selected
            del st.session_state._norm_selected

        formula_normality = st.text_input(
            "🧪 Rumus molekul / senyawa",
            value=st.session_state.formula_norm_val,
            placeholder="Ketik rumus: H2SO4, KMnO4, Ca(OH)2, FeCl3, ...",
            key="formula_norm_input"
        )

        if formula_normality != st.session_state.formula_norm_val:
            st.session_state.formula_norm_val = formula_normality

        query_norm = formula_normality.strip()
        if query_norm:
            # Show recommendations if not an exact match
            if query_norm not in COMPOUNDS_DB:
                matches_norm = {
                    f: n for f, n in COMPOUNDS_DB.items()
                    if query_norm.lower() in f.lower() or query_norm.lower() in n.lower()
                }
                if matches_norm:
                    st.caption("💡 Rekomendasi senyawa:")
                    for f_key, f_name in matches_norm.items():
                        if st.button(f"{f_key} — {f_name}", key=f"rec_norm_{f_key}"):
                            st.session_state._norm_selected = f_key
                            st.rerun()

        N = st.number_input(
            "Normalitas (N)",
            min_value=0.0,
            step=0.01,
            format="%.4f",
            key="normality_value"
        )

        valensi = st.number_input(
            "Valensi",
            min_value=1,
            step=1,
            key="normality_valence"
        )
        st.caption(
            "ℹ️ Valensi bergantung pada jenis reaksi atau senyawa yang digunakan. "
        )

        V2 = st.number_input(
            "Volume Larutan (mL)",
            min_value=0.0,
            step=1.0,
            format="%.2f",
            key="normality_volume"
        )

        if st.button(
            "Hitung Massa Normalitas",
            key="calculate_normality"
        ):
            if not formula_normality.strip():
                st.error("Rumus molekul tidak boleh kosong.")
            elif N <= 0:
                st.error("Normalitas harus lebih dari 0.")
            elif valensi <= 0:
                st.error("Valensi harus lebih dari 0.")
            elif V2 <= 0:
                st.error("Volume harus lebih dari 0.")
            else:
                try:
                    mr, mr_details = calculate_mr(formula_normality, elements_df)
                    massa = calculate_mass_normality(N, mr, valensi, V2)
                    compound = formula_normality.strip()

                    st.success(f"Massa yang ditimbang: {format_decimal(massa, 3)} g")
                    st.table(make_result_table([
                        ["Senyawa", compound],
                        ["Mr", f"{format_decimal(mr, 2)} g/mol"],
                        ["Normalitas", f"{format_decimal(N, 4).rstrip('0').rstrip(',')} N"],
                        ["Valensi", str(valensi)],
                        ["Volume", f"{format_decimal(V2, 2).rstrip('0').rstrip(',')} mL"],
                        ["Massa yang ditimbang", f"{format_decimal(massa, 3)} g"],
                    ]))

                    st.subheader("Rincian Perhitungan Mr")
                    st.table(make_mr_detail_table(mr_details))
                    st.write(f"Mr {compound} = {format_decimal(mr, 2)} g/mol")

                    st.subheader("Langkah Pembuatan Larutan")
                    st.markdown(
                        "\n".join([
                            f"1. Timbang {format_decimal(massa, 3)} gram {compound}.",
                            "2. Masukkan zat ke dalam gelas kimia atau labu ukur.",
                            "3. Tambahkan aquadest secukupnya untuk melarutkan zat.",
                            f"4. Tambahkan aquadest hingga tanda tera atau hingga volume {format_decimal(V2, 2).rstrip('0').rstrip(',')} mL.",
                            "5. Homogenkan larutan."
                        ])
                    )
                except ValueError as exc:
                    st.error(str(exc))

# ==========================
# PENGENCERAN
# ==========================
elif menu == "💧 Pengenceran":

    st.title("💧 Pengenceran Larutan")

    st.latex(
        r"M_1V_1=M_2V_2"
    )

    # Menggunakan Streamlit tabs
    tab1, tab2 = st.tabs(["Hitung V1", "Hitung M1"])

    # --- TAB 1: HITUNG V1 ---
    with tab1:
        st.subheader("Pengenceran V1")
        st.write("Fitur ini membantu menghitung volume yang diperlukan dalam proses pengenceran larutan. Masukkan data yang diketahui, kemudian sistem akan menghitung volume yang diperlukan berdasarkan persamaan pengenceran M₁V₁ = M₂V₂.")
        st.subheader("Hitung Volume Awal (V1)")
        M1 = st.number_input(
            "Konsentrasi Awal (M1)",
            min_value=0.0,
            key="dilution_m1",
            format="%.4f"
        )
        M2 = st.number_input(
            "Konsentrasi Akhir (M2)",
            min_value=0.0,
            key="dilution_m2_v1",
            format="%.4f"
        )
        V2 = st.number_input(
            "Volume Akhir (V2) (mL)",
            min_value=0.0,
            key="dilution_v2_v1",
            format="%.2f"
        )

        if st.button("Hitung V1", key="btn_calc_v1"):
            if M1 <= 0:
                st.error("M1 (konsentrasi awal) harus lebih besar dari 0.")
            elif M2 <= 0:
                st.error("M2 (konsentrasi akhir) harus lebih besar dari 0.")
            elif V2 <= 0:
                st.error("V2 (volume akhir) harus lebih besar dari 0.")
            else:
                V1 = (M2 * V2) / M1
                
                # Cek warning tetapi tetap lakukan perhitungan
                if M2 > M1:
                    st.warning("Konsentrasi akhir lebih besar dari konsentrasi awal. Ini bukan proses pengenceran.")
                
                st.success(f"V1 = {format_decimal(V1, 2)} mL")
                
                # Output hasil dalam tabel sederhana
                st.table(make_result_table([
                    ["Konsentrasi Awal (M1)", f"{format_decimal(M1, 4)} M"],
                    ["Konsentrasi Akhir (M2)", f"{format_decimal(M2, 4)} M"],
                    ["Volume Akhir (V2)", f"{format_decimal(V2, 2)} mL"],
                    ["Volume Dipipet (V1)", f"{format_decimal(V1, 2)} mL"],
                ]))
                
                st.info(f"Diambil {format_decimal(V1, 2)} mL larutan, kemudian tambahkan pelarut hingga volume akhir {format_decimal(V2, 2)} mL.")

    # --- TAB 2: HITUNG M1 ---
    with tab2:
        st.subheader("Pengenceran M1")
        st.write("Fitur ini membantu menghitung konsentrasi yang diperlukan dalam proses pengenceran larutan. Masukkan data yang diketahui, kemudian sistem akan menghitung konsentrasi yang diperlukan berdasarkan persamaan pengenceran M₁V₁ = M₂V₂.")
        st.subheader("Hitung Konsentrasi Awal (M1)")
        V1_m1 = st.number_input(
            "Volume Awal (V1) (mL)",
            min_value=0.0,
            key="dilution_v1_m1",
            format="%.2f"
        )
        M2_m1 = st.number_input(
            "Konsentrasi Akhir (M2)",
            min_value=0.0,
            key="dilution_m2_m1",
            format="%.4f"
        )
        V2_m1 = st.number_input(
            "Volume Akhir (V2) (mL)",
            min_value=0.0,
            key="dilution_v2_m1",
            format="%.2f"
        )

        if st.button("Hitung M1", key="btn_calc_m1"):
            if V1_m1 <= 0:
                st.error("V1 (volume awal) harus lebih besar dari 0.")
            elif M2_m1 <= 0:
                st.error("M2 (konsentrasi akhir) harus lebih besar dari 0.")
            elif V2_m1 <= 0:
                st.error("V2 (volume akhir) harus lebih besar dari 0.")
            else:
                M1_calc = (M2_m1 * V2_m1) / V1_m1
                
                # Cek warning tetapi tetap lakukan perhitungan
                if V1_m1 > V2_m1:
                    st.warning("V1 lebih besar dari V2. Pada pengenceran, volume larutan biasanya tidak lebih besar dari volume akhir.")
                
                if M1_calc < M2_m1:
                    st.warning("M1 lebih kecil dari M2. Ini tidak sesuai konsep pengenceran karena larutan awal seharusnya lebih pekat.")
                
                st.success(f"M1 = {format_decimal(M1_calc, 4)} M")
                
                # Output hasil dalam tabel sederhana
                st.table(make_result_table([
                    ["Volume Awal  (V1)", f"{format_decimal(V1_m1, 2)} mL"],
                    ["Konsentrasi Akhir (M2)", f"{format_decimal(M2_m1, 4)} M"],
                    ["Volume Akhir (V2)", f"{format_decimal(V2_m1, 2)} mL"],
                    ["Konsentrasi (M1)", f"{format_decimal(M1_calc, 4)} M"],
                ]))
                
                st.info(f"Dibutuhkan larutan dengan konsentrasi {format_decimal(M1_calc, 4)} M. Diambil {format_decimal(V1_m1, 2)} mL larutan, kemudian encerkan hingga volume akhir {format_decimal(V2_m1, 2)} mL.")
                
