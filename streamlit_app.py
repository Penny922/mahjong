import streamlit as st

# =========================
# Tile data
# =========================

suits = ["m", "p", "s"]  # m = 萬, p = 筒, s = 條

ALL_CARDS = []

for suit in suits:
    for num in range(1, 10):
        ALL_CARDS.append(f"{num}{suit}")

ALL_CARDS += ["東", "南", "西", "北", "中", "發", "白"]

types = len(ALL_CARDS)


# =========================
# Basic conversion
# =========================

chinese_numbers = {
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九"
}


# =========================
# Display functions
# =========================

def tile_name(tile):
    """
    Normal display name.
    Used in warning messages.
    """

    if tile.endswith("m"):
        return chinese_numbers[tile[0]] + "萬"
    elif tile.endswith("p"):
        return chinese_numbers[tile[0]] + "筒"
    elif tile.endswith("s"):
        return chinese_numbers[tile[0]] + "條"
    else:
        return tile


def tile_button_name(tile):
    """
    Button display name.
    Tiles are shown vertically by using newline.
    """

    if tile.endswith("m"):
        return chinese_numbers[tile[0]] + "\n萬"
    elif tile.endswith("p"):
        return chinese_numbers[tile[0]] + "\n筒"
    elif tile.endswith("s"):
        return chinese_numbers[tile[0]] + "\n條"
    else:
        return tile


def format_tile(tile):
    """
    Format listening result tile with HTML color.
    Rules:
    萬：數字紅色，萬黑色
    筒、條：黑色
    中：紅色
    發：綠色
    其他字牌：黑色
    """

    if tile.endswith("m"):
        num = chinese_numbers[tile[0]]
        return f"""
        <span class="tile">
            <span style="color:red; font-weight:900;">{num}</span>
            <span style="color:black; font-weight:900;">萬</span>
        </span>
        """

    elif tile.endswith("p"):
        num = chinese_numbers[tile[0]]
        return f"""
        <span class="tile">
            <span style="color:black; font-weight:900;">{num}</span>
            <span style="color:black; font-weight:900;">筒</span>
        </span>
        """

    elif tile.endswith("s"):
        num = chinese_numbers[tile[0]]
        return f"""
        <span class="tile">
            <span style="color:black; font-weight:900;">{num}</span>
            <span style="color:black; font-weight:900;">條</span>
        </span>
        """

    elif tile == "中":
        return """
        <span class="tile">
            <span style="color:red; font-weight:900;">中</span>
        </span>
        """

    elif tile == "發":
        return """
        <span class="tile">
            <span style="color:green; font-weight:900;">發</span>
        </span>
        """

    else:
        return f"""
        <span class="tile">
            <span style="color:black; font-weight:900;">{tile}</span>
        </span>
        """


# =========================
# Mahjong winning logic
# =========================

def win(counts):
    """
    Check whether 17 tiles form a legal winning hand.
    Structure:
    1 pair + 5 groups
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
    Check whether the remaining tiles can be divided into valid groups.
    Valid groups:
    1. Triplet
    2. Sequence
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
    # Only suited tiles can form sequences.
    # Honors cannot form sequences.
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


# =========================
# Streamlit page setting
# =========================

st.set_page_config(
    page_title="麻將聽牌判斷器",
    page_icon="🀄",
    layout="centered"
)


# =========================
# CSS style
# =========================

st.markdown("""
<style>

/* =========================
   Tile buttons: secondary buttons
   選牌區與目前手牌的牌按鈕
   ========================= */

div.stButton > button[kind="secondary"] {
    width: 52px !important;
    height: 78px !important;
    min-width: 52px !important;
    min-height: 78px !important;

    background-color: #fff8e7 !important;
    color: black !important;

    border: 2px solid #333 !important;
    border-radius: 8px !important;

    padding: 0px !important;
    margin: 2px !important;

    box-shadow: 2px 2px 4px rgba(0,0,0,0.25) !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Tile button text */
div.stButton > button[kind="secondary"] p {
    margin: 0 !important;
    color: black !important;
    font-weight: 900 !important;
    font-size: 24px !important;
    line-height: 1.05 !important;
    white-space: pre-line !important;
    text-align: center !important;
}

/* Tile button hover */
div.stButton > button[kind="secondary"]:hover {
    background-color: #f3e2c7 !important;
    color: black !important;
    border: 2px solid #111 !important;
}

/* Tile button active */
div.stButton > button[kind="secondary"]:active {
    background-color: #ead2ad !important;
    color: black !important;
}


/* =========================
   Control buttons: primary buttons
   清空、刪除、判斷按鈕
   ========================= */

div.stButton > button[kind="primary"] {
    width: 120px !important;
    height: 42px !important;
    min-width: 120px !important;
    min-height: 42px !important;

    background-color: #eeeeee !important;
    color: black !important;

    border: 2px solid #333 !important;
    border-radius: 8px !important;

    padding: 0px 12px !important;
    margin: 2px !important;

    box-shadow: 1px 1px 3px rgba(0,0,0,0.2) !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Control button text */
div.stButton > button[kind="primary"] p {
    margin: 0 !important;
    color: black !important;
    font-weight: 900 !important;
    font-size: 20px !important;
    line-height: 1.0 !important;
    white-space: nowrap !important;
    text-align: center !important;
}

/* Control button hover */
div.stButton > button[kind="primary"]:hover {
    background-color: #dddddd !important;
    color: black !important;
    border: 2px solid #111 !important;
}

/* Control button active */
div.stButton > button[kind="primary"]:active {
    background-color: #cccccc !important;
    color: black !important;
}


/* =========================
   Tile style for listening result
   聽牌結果牌面
   ========================= */

.tile {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    width: 52px;
    height: 78px;

    text-align: center;
    margin: 4px;

    border: 2px solid #333;
    border-radius: 8px;

    background-color: #fff8e7;

    font-size: 24px;
    font-weight: 900;

    box-shadow: 2px 2px 4px rgba(0,0,0,0.25);

    vertical-align: middle;
    line-height: 1.1;
}

</style>
""", unsafe_allow_html=True)


# =========================
# Title
# =========================

st.title("麻將聽牌判斷器")
st.write("請選擇你的 16 張手牌，系統會判斷目前聽哪些牌。")


# =========================
# Session state
# =========================

if "my_hand" not in st.session_state:
    st.session_state.my_hand = []


# =========================
# Add tile function
# =========================

def add_tile(tile):
    """
    Add one tile to hand.
    Maximum:
    16 tiles in hand
    4 identical tiles
    """

    if len(st.session_state.my_hand) >= 16:
        st.warning("最多只能選 16 張牌")
        return

    if st.session_state.my_hand.count(tile) >= 4:
        st.warning(f"{tile_name(tile)} 最多只能有 4 張")
        return

    st.session_state.my_hand.append(tile)


# =========================
# Tile selection area
# =========================

st.subheader("選牌區")

tile_rows = [
    ("萬子", [f"{i}m" for i in range(1, 10)]),
    ("筒子", [f"{i}p" for i in range(1, 10)]),
    ("條子", [f"{i}s" for i in range(1, 10)]),
    ("字牌", ["東", "南", "西", "北", "中", "發", "白"])
]

for row_title, row_tiles in tile_rows:
    st.markdown(f"### {row_title}")

    cols = st.columns(len(row_tiles))

    for i, tile in enumerate(row_tiles):
        with cols[i]:
            if st.button(
                tile_button_name(tile),
                key=f"add_{tile}",
                type="secondary"
            ):
                add_tile(tile)
                st.rerun()


# =========================
# Current hand area
# =========================

st.subheader("目前手牌")
st.write(f"目前已選：{len(st.session_state.my_hand)} / 16 張")

if len(st.session_state.my_hand) > 0:
    st.write("點選下方手牌即可移除該張牌")

    cards_per_row = 8

    for row_start in range(0, len(st.session_state.my_hand), cards_per_row):
        row_tiles = st.session_state.my_hand[row_start:row_start + cards_per_row]

        cols = st.columns(cards_per_row)

        for i, tile in enumerate(row_tiles):
            hand_index = row_start + i

            with cols[i]:
                if st.button(
                    tile_button_name(tile),
                    key=f"remove_{hand_index}_{tile}",
                    type="secondary"
                ):
                    st.session_state.my_hand.pop(hand_index)
                    st.rerun()
else:
    st.write("尚未選牌")


# =========================
# Control buttons
# =========================

st.subheader("操作")

control_col1, control_col2 = st.columns(2)

with control_col1:
    if st.button("清空", type="primary"):
        st.session_state.my_hand = []
        st.rerun()

with control_col2:
    if st.button("刪除", type="primary"):
        if len(st.session_state.my_hand) > 0:
            st.session_state.my_hand.pop()
            st.rerun()


# =========================
# Listening tile calculation
# =========================

st.subheader("聽牌結果")

if st.button("判斷", type="primary"):
    my_hand = st.session_state.my_hand

    if len(my_hand) != 16:
        st.error("請先選滿 16 張手牌")

    else:
        hand_counts = [0] * types

        for tile in my_hand:
            idx = ALL_CARDS.index(tile)
            hand_counts[idx] += 1

        waiting_tiles = []

        for i in range(types):
            if hand_counts[i] < 4:
                hand_counts[i] += 1

                if win(hand_counts):
                    waiting_tiles.append(ALL_CARDS[i])

                hand_counts[i] -= 1

        if len(waiting_tiles) > 0:
            st.success("有聽牌！")

            result_html = ""

            for tile in waiting_tiles:
                result_html += format_tile(tile)

            st.markdown(result_html, unsafe_allow_html=True)

        else:
            st.error("沒聽牌")
