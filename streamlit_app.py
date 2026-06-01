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

    # Triplet
    if number[first] >= 3:
        number[first] -= 3

        if is_valid(number):
            number[first] += 3
            return True

        number[first] += 3

    # Sequence
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
# Streamlit UI
# =========================
st.set_page_config(
    page_title="台灣麻將聽牌判斷器",
    page_icon="🀄",
    layout="wide"
)

st.title("🀄 台灣麻將聽牌判斷器")

st.write("請輸入每一張牌的數量。總共需要剛好 16 張手牌。")

st.divider()

hand_counts = [0] * types

st.subheader("萬子")
cols = st.columns(9)

for i in range(9):
    tile = f"{i + 1}m"
    idx = ALL_CARDS.index(tile)

    with cols[i]:
        hand_counts[idx] = st.number_input(
            DISPLAY_NAME[tile],
            min_value=0,
            max_value=4,
            value=0,
            step=1,
            key=tile
        )

st.subheader("筒子")
cols = st.columns(9)

for i in range(9):
    tile = f"{i + 1}p"
    idx = ALL_CARDS.index(tile)

    with cols[i]:
        hand_counts[idx] = st.number_input(
            DISPLAY_NAME[tile],
            min_value=0,
            max_value=4,
            value=0,
            step=1,
            key=tile
        )

st.subheader("條子")
cols = st.columns(9)

for i in range(9):
    tile = f"{i + 1}s"
    idx = ALL_CARDS.index(tile)

    with cols[i]:
        hand_counts[idx] = st.number_input(
            DISPLAY_NAME[tile],
            min_value=0,
            max_value=4,
            value=0,
            step=1,
            key=tile
        )

st.subheader("字牌")
cols = st.columns(7)

honors = ["東", "南", "西", "北", "中", "發", "白"]

for i, tile in enumerate(honors):
    idx = ALL_CARDS.index(tile)

    with cols[i]:
        hand_counts[idx] = st.number_input(
            DISPLAY_NAME[tile],
            min_value=0,
            max_value=4,
            value=0,
            step=1,
            key=tile
        )

st.divider()

total_tiles = sum(hand_counts)
st.write(f"目前手牌數量：{total_tiles} 張")

selected_tiles = []

for idx, count in enumerate(hand_counts):
    for _ in range(count):
        selected_tiles.append(DISPLAY_NAME[ALL_CARDS[idx]])

if selected_tiles:
    st.write("你的手牌：")
    st.write("、".join(selected_tiles))

st.divider()

if st.button("判斷是否聽牌"):
    if total_tiles != 16:
        st.error("請輸入剛好 16 張手牌。")
    else:
        waiting_tiles = check_tenpai(hand_counts)

        if waiting_tiles:
            st.success("有聽牌！")

            result = "、".join([DISPLAY_NAME[tile] for tile in waiting_tiles])
            st.subheader(f"聽牌：{result}")
        else:
            st.warning("沒聽牌")
