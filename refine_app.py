import streamlit as st

def CalRefine(default, targetRefine, EE, E, CheapestPrice):
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

st.title("🔧 Ragnarok Mobile Refinement Cost Calculator by PonderingTH ")

default = st.number_input("Start Refine Level", min_value=4, max_value=14, value=4)
target = st.number_input("Target Refine Level", min_value=5, max_value=15, value=5)
EE = st.number_input("Enriched Elu (EE)", min_value=0, value=0)
E = st.number_input("Elunium Owned", min_value=0, value=0)
price = st.number_input("Cheapest EQ Price (million Zeny)", min_value=0.0, value=0.3, step=0.01)

if st.button("Calculate"):
    result = CalRefine(default, target, EE, E, price)
    st.markdown(f"""
    ### 🧾 Result
    - Elunium Needed: `{result[0]}` (Owned: `{result[1]}`, Cost: `{result[2]:.2f}m`)
    - EQ Needed: `{result[3]} ea` (Cost: `{result[4]:.2f}m`)
    - Zeny Cost: `{result[5]:.2f}m`
    - 💰 **Total Cost: `{result[6]:.2f}m`**
    """)


st.title("🔧 Please subscribe my channel at PonderingTH (Youtube) Thanks! ")