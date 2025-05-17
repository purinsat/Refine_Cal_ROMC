import streamlit as st
import random
import time
import copy

# -------------------------------
# SAFE REFINE CALCULATOR SECTION
# -------------------------------
def cal_safe_refine(default, targetRefine, EE, E, CheapestPrice):
    Elu = [5,10,15,25,50,80,135,225,375,600,900]
    EQ = [1,2,3,4,6,10,22,30,45,69,98,290]
    Zeny = [0.1,0.22,0.47,0.91,1.63,2.74,5.25,9,14.5,24.5,42]
    Elu_Total = 0
    EQ_Total = 0
    ZenyTotal = 0
    Elu_owned = E + (EE * 5)
    for i in range(default, targetRefine):
        Elu_Total += Elu[i - 4]
        EQ_Total += EQ[i - 4]
        ZenyTotal += Zeny[i - 4]

    Elu_Cost = (Elu_Total - Elu_owned) * 0.025
    if Elu_Cost < 0: Elu_Cost = 0
    EQ_Cost = EQ_Total * CheapestPrice
    TotalCost = ZenyTotal + Elu_Cost + EQ_Cost
    return (Elu_Total, Elu_owned, Elu_Cost, EQ_Total, EQ_Cost, ZenyTotal, TotalCost)

# -------------------------------
# NORMAL REFINE SIMULATION SECTION
# -------------------------------
def cal_oneclick(refinelv):
    zenycost = [9500,19000,28500,38000,47500,57000,66500,76000,85500,95000,95000,95000,95000,95000]
    elu_price = 25000 if refinelv < 10 else 125000
    return zenycost[refinelv - 1] + elu_price

def cal_result(state, price, refinelv):
    cost = cal_oneclick(refinelv)
    outcome = random.choices(['success', 'fail', 'break'], weights=[40, 45, 15])[0]

    if state == 'damaged':
        return 'damaged', refinelv, 0

    if outcome == 'success':
        return 'normal', refinelv + 1, cost
    elif outcome == 'fail':
        return 'normal', max(4, refinelv - 1), cost
    elif outcome == 'break':
        return 'damaged', max(4, refinelv - 1), cost

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="Ragnarok Refine Tools", layout="centered")
st.title("🔧 Ragnarok Mobile Refine Tools by PonderingTH")

tab1, tab2 = st.tabs(["🛡️ Safe Refine Calculator", "🎲 Normal Refine Simulator"])

# -------------------------------
# TAB 1: Safe Refine
# -------------------------------
with tab1:
    st.subheader("Safe Refine Cost Calculator")
    default = st.number_input("From +", min_value=4, max_value=14, value=4)
    target = st.number_input("To +", min_value=5, max_value=15, value=5)
    EE = st.number_input("Extra Elunium (EE)", min_value=0, value=0)
    E = st.number_input("Elunium Owned", min_value=0, value=0)
    CheapestPrice = st.number_input("Cheapest EQ Price (million Zeny)", min_value=0.0, value=0.3, step=0.01)

    if st.button("💰 Calculate Safe Refine Cost"):
        result = cal_safe_refine(default, target, EE, E, CheapestPrice)
        st.markdown(f"""
        ### 🧾 Cost Breakdown
        - **Elunium Needed**: `{result[0]}` (Owned: `{result[1]}`, Cost: `{result[2]:.2f}m`)
        - **EQ Needed**: `{result[3]}` (Cost: `{result[4]:.2f}m`)
        - **NPC Zeny Cost**: `{result[5]:.2f}m`
        - 💰 **Total Cost: `{result[6]:.2f}m`**
        """)

# -------------------------------
# TAB 2: Normal Refine Simulation
# -------------------------------
with tab2:
    st.subheader("Normal Refine Simulation (2 Items)")

    if "items" not in st.session_state:
        st.session_state["items"] = [
            {"refine": 4, "state": "normal", "cost": 0, "price": 30000},
            {"refine": 4, "state": "normal", "cost": 0, "price": 30000}
        ]

    # Display items side-by-side
    col1, col2 = st.columns(2)
    for i, col in enumerate([col1, col2]):
        with col:
            item = st.session_state["items"][i]
            st.markdown(f"### 🧪 Item {i+1}")
            st.number_input(
                f"🔧 Equipment Price (Item {i+1})", 
                key=f"price_input_{i}", 
                value=item["price"], 
                step=1000
            )
            # Update price
            st.session_state["items"][i]["price"] = st.session_state[f"price_input_{i}"]

            st.text(f"Refine Level: +{item['refine']}")
            st.text(f"State: {item['state'].capitalize()}")
            st.text(f"Total Cost: {item['cost']:,} Zeny")

    # Buttons in same row
    button_col1, button_col2 = st.columns(2)

    for i, col in enumerate([button_col1, button_col2]):
        with col:
            item = copy.deepcopy(st.session_state["items"][i])
            label = f"🛠 Repair Item {i+1}" if item["state"] == "damaged" else f"🔨 Refine Item {i+1}"

            if st.button(label, key=f"refine_btn_{i}"):
                with st.spinner("Refining..."):
                    time.sleep(1.2)

                if item["state"] == "damaged":
                    item["cost"] += item["price"]
                    item["state"] = "normal"
                else:
                    state, new_lv, add_cost = cal_result(item["state"], item["price"], item["refine"])
                    item["refine"] = new_lv
                    item["state"] = state
                    item["cost"] += add_cost

                updated_items = copy.deepcopy(st.session_state["items"])
                updated_items[i] = item
                st.session_state["items"] = updated_items
                st.rerun()  # ✅ Streamlit v1.30+ replacement

    st.markdown("---")
    if st.button("🔄 Reset All"):
        st.session_state["items"] = [
            {"refine": 4, "state": "normal", "cost": 0, "price": 30000},
            {"refine": 4, "state": "normal", "cost": 0, "price": 30000}
        ]
        st.rerun()

st.subheader("Please subscribe on my channel PonderingTH on Youtube to support me. Thanks!")