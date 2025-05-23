import streamlit as st

st.title("24-Hour Pre-operative IV Fluid Recommendation")

# Sidebar inputs
st.sidebar.header("Patient Data")
age = st.sidebar.number_input("Age (years)", min_value=0, value=30)
weight = st.sidebar.number_input("Weight (kg)", min_value=0.0, value=70.0)
npo_duration = st.sidebar.number_input("NPO duration (hours)", min_value=0, value=12)
serum_na = st.sidebar.number_input("Serum Na (mEq/L)", value=140.0)
serum_k = st.sidebar.number_input("Serum K (mEq/L)", value=4.0)
serum_cl = st.sidebar.number_input("Serum Cl (mEq/L)", value=100.0)
serum_hco3 = st.sidebar.number_input("Serum HCO₃ (mEq/L)", value=24.0)
blood_glucose = st.sidebar.number_input("Blood glucose (mg/dL)", value=100.0)
creatinine = st.sidebar.number_input("Creatinine (mg/dL)", value=1.0)
bun = st.sidebar.number_input("BUN (mg/dL)", value=15.0)
pediatric = st.sidebar.checkbox("Pediatric patient", value=False)
insulin_infusion = st.sidebar.checkbox("On insulin infusion", value=False)
malnourished = st.sidebar.checkbox("Malnourished/catabolic", value=False)

if st.button("Generate Recommendation"):
    # Maintenance calculation
    m1 = min(weight, 10) * 4
    m2 = min(max(weight - 10, 0), 10) * 2
    m3 = max(weight - 20, 0) * 1
    rate_ml_h = m1 + m2 + m3
    total_volume = rate_ml_h * 24

    # Fluid type logic
    if pediatric:
        fluid_type = "D5LR" if npo_duration >= 24 else "D5W"
    else:
        if npo_duration > 24:
            fluid_type = "Lactated Ringer’s + 5% dextrose"
        else:
            fluid_type = "Lactated Ringer’s"

    # Override for severe hyponatremia
    if serum_na < 125:
        fluid_type = "0.9% NaCl"

    # Potassium supplement logic
    if serum_k < 3.5:
        potassium_note = "Add KCl 20 mEq per liter"
    else:
        potassium_note = "No additional KCl"

    # Dextrose logic
    if npo_duration > 24 or pediatric or insulin_infusion or malnourished:
        dextrose_note = "Include dextrose per fluid choice"
    else:
        dextrose_note = "No dextrose needed"

    # Display recommendation
    st.subheader("Recommended IV Fluid Order")
    st.write(f"**Fluid:** {fluid_type}")
    st.write(f"**Total volume (24 h):** {total_volume:.0f} mL")
    st.write(f"**Infusion rate:** {rate_ml_h:.0f} mL/h")
    st.write(f"**Potassium supplement:** {potassium_note}")
    st.write(f"**Dextrose:** {dextrose_note}")
