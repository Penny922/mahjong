import streamlit as st

# =========================
# Basic tile setting
# =========================
suits = ["m", "p", "s"]

ALL_CARDS = []
for suit in suits:
    for num in range(1, 10):
        ALL_CARDS.append(f"{num}{suit}")

ALL_CARDS += ["東", "南", "西", "北", "中", "發", "白"]
types = len(ALL_CARDS)

DISPLAY_NAME = {}

for num in range(1, 10):
    DISPLAY_NAME[f"{num}m"] = f"{num}萬"
    DISPLAY_NAME[f"{num}p"] = f"{num}筒"
    DISPLAY_NAME[f"{num}s"] = f"{num}條"

for honor in ["東", "南", "西", "北", "中", "發", "白"]:
    DISPLAY_NAME[honor] = honor


# =========================
# Mahjong logic
# =========================
def win(counts):
    # 台灣麻將：16 張手牌 + 摸進 1 張 = 17 張胡牌
    if sum(counts) != 17:
        return False

    for idx in range(types):
        if counts[idx] >= 2:
            temp_counts = list(counts)
            temp_counts[idx] -= 2

            if is_valid(temp_counts):
                return True

    return False


def is_valid(number):
    if sum(number) == 0:
        return True

    first = 0
    while first < types and number[first] == 0:
        first += 1

    if first >= types:
        return True

    # Check triplet
    if number[first] >= 3:
        number[first] -= 3

        if is_valid(number):
            number[first] += 3
            return True

        number[first] += 3

    # Check sequence
    if first < 27 and (first % 9) <= 6:
        if number[first + 1] > 0 and number[first + 2] > 0:
            number[first] -= 1
            number[first + 1] -= 1
            number[first + 2] -= 1

            if is_valid(number):
                number[first] += 1
                number[first + 1] += 1
                number[first + 2] += 1
                return True

            number[first] += 1
            number[first + 1] += 1
            number[first + 2] += 1

    return False


def check_tenpai(hand_counts):
    waiting_tiles = []

    for i in range(types):
        if hand_counts[i] < 4:
            hand_counts[i] += 1

            if win(hand_counts):
                waiting_tiles.append(ALL_CARDS[i])

            hand_counts[i] -= 1

    return waiting_tiles


# =========================
# Streamlit page setting
# =========================
st.set_page_config(
    page_title="台灣麻將聽牌判斷器",
    page_icon="🀄",
    layout="wide"
)

# =========================
# CSS style
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b5c3b;
        color: white;
    }

    h1, h2, h3, p, div {
        font-family: "Microsoft JhengHei", sans-serif;
    }

    .title-box {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #116b45, #083d29);
        border-radius: 20px;
        margin-bottom: 20px;
        border: 3px solid #d6b46a;
    }

    .title-box h1 {
        color: #ffd56b;
        font-size: 42px;
        margin-bottom: 5px;
    }

    .title-box p {
        color: white;
        font-size: 18px;
    }

    .hand-box {
        background-color: #063d29;
        padding: 20px;
        border-radius: 18px;
        border: 2px solid #d6b46a;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .tile {
        display: inline-block;
        background-color: #fff8e7;
        color: #111111;
        border: 2px solid #c9b27c;
        border-radius: 10px;
        padding: 10px 8px;
        margin: 5px;
        min-width: 45px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 2px 3px 4px rgba(0,0,0,0.35);
    }

    .result-box {
        background-color: #fff8e7;
        color: #111111;
        padding: 20px;
        border-radius: 18px;
        border: 3px solid #d6b46a;
        margin-top: 20px;
        text-align: center;
    }

    div.stButton > button {
        background-color: #fff8e7;
        color: #111111;
        border: 2px solid #d6b46a;
        border-radius: 12px;
        height: 55px;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 2px 3px 4px rgba(0,0,0,0.25);
    }

    div.stButton > button:hover {
        background-color: #ffd56b;
        color: #111111;
        border: 2px solid white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Session state
# =========================
if "hand_counts" not in st.session_state:
    st.session_state.hand_counts = [0] * types

if "result" not in st.session_state:
    st.session_state.result = None


# =========================
# Helper functions
# =========================
def add_tile(tile):
    idx = ALL_CARDS.index(tile)

    if sum(st.session_state.hand_counts) >= 16:
        st.warning("已經選滿 16 張牌。")
        return

    if st.session_state.hand_counts[idx] >= 4:
        st.warning(f"{DISPLAY_NAME[tile]} 最多只能有 4 張。")
        return

    st.session_state.hand_counts[idx] += 1


def remove_tile(tile):
    idx = ALL_CARDS.index(tile)

    if st.session_state.hand_counts[idx] > 0:
        st.session_state.hand_counts[idx] -= 1


def clear_hand():
    st.session_state.hand_counts = [0] * types
    st.session_state.result = None


def render_hand():
    html = ""

    for idx, count in enumerate(st.session_state.hand_counts):
        for _ in range(count):
            html += f'<span class="tile">{DISPLAY_NAME[ALL_CARDS[idx]]}</span>'

    if html == "":
        html = "<p>尚未選牌</p>"

    st.markdown(
        f"""
        <div class="hand-box">
            <h3>目前手牌</h3>
            {html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_waiting_tiles(waiting_tiles):
    html = ""

    for tile in waiting_tiles:
        html += f'<span class="tile">{DISPLAY_NAME[tile]}</span>'

    st.markdown(
        f"""
        <div class="result-box">
            <h2>有聽牌！</h2>
            <p>你聽的牌是：</p>
            {html}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# UI
# =========================
st.markdown(
    """
    <div class="title-box">
        <h1>🀄 台灣麻將聽牌判斷器</h1>
        <p>點選麻將牌加入手牌，選滿 16 張後判斷是否聽牌</p>
    </div>
    """,
    unsafe_allow_html=True
)

total_tiles = sum(st.session_state.hand_counts)

col_a, col_b, col_c = st.columns([1, 1, 1])

with col_a:
    st.metric("目前張數", f"{total_tiles} / 16")

with col_b:
    if st.button("清空手牌"):
        clear_hand()
        st.rerun()

with col_c:
    if st.button("判斷聽牌"):
        if total_tiles != 16:
            st.session_state.result = "invalid"
        else:
            st.session_state.result = check_tenpai(st.session_state.hand_counts)

render_hand()

st.divider()

# =========================
# Tile buttons
# =========================
st.subheader("萬子")
cols = st.columns(9)
for i in range(9):
    tile = f"{i + 1}m"
    with cols[i]:
        if st.button(DISPLAY_NAME[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()

st.subheader("筒子")
cols = st.columns(9)
for i in range(9):
    tile = f"{i + 1}p"
    with cols[i]:
        if st.button(DISPLAY_NAME[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()

st.subheader("條子")
cols = st.columns(9)
for i in range(9):
    tile = f"{i + 1}s"
    with cols[i]:
        if st.button(DISPLAY_NAME[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()

st.subheader("字牌")
cols = st.columns(7)
honors = ["東", "南", "西", "北", "中", "發", "白"]

for i, tile in enumerate(honors):
    with cols[i]:
        if st.button(DISPLAY_NAME[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()

st.divider()

# =========================
# Remove tile section
# =========================
st.subheader("移除手牌")

selected_tiles = []
for idx, count in enumerate(st.session_state.hand_counts):
    if count > 0:
        selected_tiles.append(ALL_CARDS[idx])

if selected_tiles:
    cols = st.columns(min(len(selected_tiles), 8))

    for i, tile in enumerate(selected_tiles):
        with cols[i % len(cols)]:
            if st.button(f"移除 {DISPLAY_NAME[tile]}", key=f"remove_{tile}"):
                remove_tile(tile)
                st.rerun()
else:
    st.write("目前沒有可移除的牌。")

# =========================
# Result
# =========================
if st.session_state.result == "invalid":
    st.error("請選剛好 16 張手牌。")

elif isinstance(st.session_state.result, list):
    if len(st.session_state.result) > 0:
        render_waiting_tiles(st.session_state.result)
    else:
        st.markdown(
            """
            <div class="result-box">
                <h2>沒聽牌</h2>
                <p>目前這副牌還沒有形成聽牌狀態。</p>
            </div>
            """,
            unsafe_allow_html=True
        )
