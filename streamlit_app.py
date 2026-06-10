/* =========================
   Control buttons: primary buttons
   清空、刪除、判斷按鈕
   ========================= */

div.stButton > button[kind="primary"] {
    width: 120px !important;
    height: 42px !important;
    min-width: 120px !important;
    min-height: 42px !important;

    background-color: #00a67d !important;
    color: white !important;

    border: 2px solid #008f6b !important;
    border-radius: 8px !important;

    padding: 0px 12px !important;
    margin: 2px !important;

    box-shadow: 1px 1px 3px rgba(0,0,0,0.2) !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

div.stButton > button[kind="primary"] p {
    margin: 0 !important;
    color: white !important;
    font-weight: 900 !important;
    font-size: 20px !important;
    line-height: 1.0 !important;
    white-space: nowrap !important;
    text-align: center !important;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #008f6b !important;
    color: white !important;
    border: 2px solid #007a5c !important;
}

div.stButton > button[kind="primary"]:active {
    background-color: #007a5c !important;
    color: white !important;
}
