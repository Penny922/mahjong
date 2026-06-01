import streamlit as st

# =========================
# Basic tile setting
# =========================
suits = ["m", "p", "s"]  # 萬 (m)、筒 (p)、條 (s)

ALL_CARDS = []

for suit in suits:
    for num in range(1, 10):
        ALL_CARDS.append(f"{num}{suit}")

ALL_CARDS += ["東", "南", "西", "北", "中", "發", "白"]

types = len(ALL_CARDS)

# 中文名稱
DISPLAY_NAME = {}

for num in range(1, 10):
    DISPLAY_NAME[f"{num}m"] = f"{num}萬"
    DISPLAY_NAME[f"{num}p"] = f"{num}筒"
    DISPLAY_NAME[f"{num}s"] = f"{num}條"

for honor in ["東", "南", "西", "北", "中", "發", "白"]:
    DISPLAY_NAME[honor] = honor

# 麻將 Unicode 圖案
TILE_ICON = {
    # 萬子
    "1m": "🀇",
    "2m": "🀈",
    "3m": "🀉",
    "4m": "🀊",
    "5m": "🀋",
    "6m": "🀌",
    "7m": "🀍",
    "8m": "🀎",
    "9m": "🀏",

    # 條子
    "1s": "🀐",
    "2s": "🀑",
    "3s": "🀒",
    "4s": "🀓",
    "5s": "🀔",
    "6s": "🀕",
    "7s": "🀖",
    "8s": "🀗",
    "9s": "🀘",

    # 筒子
    "1p": "🀙",
    "2p": "🀚",
    "3p": "🀛",
    "4p": "🀜",
    "5p": "🀝",
    "6p": "🀞",
    "7p": "🀟",
    "8p": "🀠",
    "9p": "🀡",

    # 字牌
    "東": "🀀",
    "南": "🀁",
    "西": "🀂",
    "北": "🀃",
    "中": "🀄",
    "發": "🀅",
    "白": "🀆",
}


# =========================
# Mahjong winning logic
# =========================
def win(counts):
    """
    台灣麻將：
    16 張手牌 + 摸進 1 張 = 17 張胡牌
    胡牌結構：5 組面子 + 1 組雀頭
    """

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
    """
    判斷扣掉雀頭後，剩下的牌能不能全部組成：
    1. 刻子：三張一樣
    2. 順子：連續三張同花色數牌
    """

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
    # Only numbered tiles can form sequence
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
    """
    判斷目前 16 張手牌聽哪些牌。
    方法：
    每一種牌都試著摸進 1 張，
    如果加進去後可以胡牌，就代表聽那張。
    """

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
        background: radial-gradient(circle at top, #157347 0%, #063d29 55%, #032217 100%);
        color: white;
    }

    h1, h2, h3, p, div {
        font-family: "Microsoft JhengHei", "Noto Sans TC", sans-serif;
    }

    .title-box {
        text-align: center;
        padding: 24px;
        background: linear-gradient(135deg, #126b46, #052d1f);
        border-radius: 22px;
        margin-bottom: 22px;
        border: 3px solid #d6b46a;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
    }

    .title-box h1 {
        color: #ffd56b;
        font-size: 44px;
        margin-bottom: 8px;
    }

    .title-box p {
        color: white;
        font-size: 18px;
    }

    .hand-box {
        background-color: rgba(3, 45, 31, 0.92);
        padding: 20px;
        border-radius: 18px;
        border: 2px solid #d6b46a;
        margin-top: 15px;
        margin-bottom: 15px;
        min-height: 135px;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.3);
    }

    .tile {
        display: inline-block;
        background-color: #fff8e7;
        color: #111111;
        border: 2px solid #c9b27c;
        border-radius: 13px;
        padding: 6px 8px;
        margin: 6px;
        min-width: 58px;
        min-height: 78px;
        text-align: center;
        font-size: 46px;
        line-height: 78px;
        box-shadow: 3px 5px 8px rgba(0,0,0,0.40);
    }

    .tile-label {
        display: inline-block;
        color: white;
        font-size: 14px;
        margin-left: 8px;
    }

    .result-box {
        background-color: #fff8e7;
        color: #111111;
        padding: 22px;
        border-radius: 18px;
        border: 3px solid #d6b46a;
        margin-top: 24px;
        text-align: center;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
    }

    .result-box h2 {
        color: #0b5c3b;
        font-size: 34px;
        margin-bottom: 10px;
    }

    .result-box p {
        color: #111111;
        font-size: 18px;
    }

    div.stButton > button {
        background-color: #fff8e7;
        color: #111111;
        border: 2px solid #d6b46a;
        border-radius: 14px;
        height: 86px;
        width: 100%;
        font-size: 42px;
        font-weight: bold;
        box-shadow: 3px 5px 8px rgba(0,0,0,0.30);
    }

    div.stButton > button:hover {
        background-color: #ffd56b;
        color: #111111;
        border: 2px solid white;
        transform: translateY(-2px);
    }

    div[data-testid="stMetric"] {
        background-color: rgba(255, 248, 231, 0.95);
        padding: 16px;
        border-radius: 16px;
        border: 2px solid #d6b46a;
        color: black;
    }

    div[data-testid="stMetric"] label {
        color: #0b5c3b;
        font-weight: bold;
    }

    div[data-testid="stMetricValue"] {
        color: #111111;
    }

    .section-title {
        background-color: rgba(255, 248, 231, 0.15);
        padding: 10px 16px;
        border-left: 6px solid #ffd56b;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 10px;
        font-size: 24px;
        font-weight: bold;
        color: #ffd56b;
    }

    .small-note {
        color: #f5f5f5;
        font-size: 15px;
        margin-top: 4px;
        margin-bottom: 12px;
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
    st.session_state.result = None


def remove_tile(tile):
    idx = ALL_CARDS.index(tile)

    if st.session_state.hand_counts[idx] > 0:
        st.session_state.hand_counts[idx] -= 1
        st.session_state.result = None


def clear_hand():
    st.session_state.hand_counts = [0] * types
    st.session_state.result = None


def render_hand():
    html = ""

    for idx, count in enumerate(st.session_state.hand_counts):
        for _ in range(count):
            tile = ALL_CARDS[idx]
            html += f'<span class="tile">{TILE_ICON[tile]}</span>'

    if html == "":
        html = "<p>尚未選牌，請從下方點選麻將牌。</p>"

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
        html += f'<span class="tile">{TILE_ICON[tile]}</span>'

    name_text = "、".join([DISPLAY_NAME[tile] for tile in waiting_tiles])

    st.markdown(
        f"""
        <div class="result-box">
            <h2>有聽牌！</h2>
            <p>你聽的牌是：{name_text}</p>
            {html}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# UI title
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


# =========================
# Top control area
# =========================
total_tiles = sum(st.session_state.hand_counts)

col_a, col_b, col_c = st.columns([1, 1, 1])

with col_a:
    st.metric("目前張數", f"{total_tiles} / 16")

with col_b:
    if st.button("清空"):
        clear_hand()
        st.rerun()

with col_c:
    if st.button("判斷"):
        if total_tiles != 16:
            st.session_state.result = "invalid"
        else:
            st.session_state.result = check_tenpai(st.session_state.hand_counts)

render_hand()


# =========================
# Tile selection area
# =========================
st.markdown('<div class="section-title">萬子</div>', unsafe_allow_html=True)
st.markdown('<div class="small-note">點牌即可加入手牌，最多 4 張。</div>', unsafe_allow_html=True)

cols = st.columns(9)

for i in range(9):
    tile = f"{i + 1}m"

    with cols[i]:
        if st.button(TILE_ICON[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()
        st.caption(DISPLAY_NAME[tile])


st.markdown('<div class="section-title">筒子</div>', unsafe_allow_html=True)

cols = st.columns(9)

for i in range(9):
    tile = f"{i + 1}p"

    with cols[i]:
        if st.button(TILE_ICON[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()
        st.caption(DISPLAY_NAME[tile])


st.markdown('<div class="section-title">條子</div>', unsafe_allow_html=True)

cols = st.columns(9)

for i in range(9):
    tile = f"{i + 1}s"

    with cols[i]:
        if st.button(TILE_ICON[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()
        st.caption(DISPLAY_NAME[tile])


st.markdown('<div class="section-title">字牌</div>', unsafe_allow_html=True)

cols = st.columns(7)

honors = ["東", "南", "西", "北", "中", "發", "白"]

for i, tile in enumerate(honors):
    with cols[i]:
        if st.button(TILE_ICON[tile], key=f"add_{tile}"):
            add_tile(tile)
            st.rerun()
        st.caption(DISPLAY_NAME[tile])


# =========================
# Remove tile area
# =========================
st.markdown('<div class="section-title">移除手牌</div>', unsafe_allow_html=True)
st.markdown('<div class="small-note">點下方按鈕可以移除已選的牌。</div>', unsafe_allow_html=True)

selected_tiles = []

for idx, count in enumerate(st.session_state.hand_counts):
    if count > 0:
        selected_tiles.append(ALL_CARDS[idx])

if selected_tiles:
    cols = st.columns(8)

    for i, tile in enumerate(selected_tiles):
        with cols[i % 8]:
            button_text = f"{TILE_ICON[tile]} -1"
            if st.button(button_text, key=f"remove_{tile}"):
                remove_tile(tile)
                st.rerun()
else:
    st.write("目前沒有可移除的牌。")


# =========================
# Result area
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
