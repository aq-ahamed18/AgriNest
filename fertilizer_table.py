import json
import os
import streamlit as st

FERTILIZER_FILE = "fertilizers.json"

def load_fertilizers():
    if os.path.exists(FERTILIZER_FILE) and os.path.getsize(FERTILIZER_FILE) > 0:
        with open(FERTILIZER_FILE, "r") as f:
            return json.load(f)
    return []

def save_fertilizers(fertilizers):
    with open(FERTILIZER_FILE, "w") as f:
        json.dump(fertilizers, f, indent=4)

def fertilizer_table():
    st.subheader("💧 Manage Fertilizers")

    fertilizers = load_fertilizers()

    # ---------- Add Fertilizer ----------
    st.markdown("### ➕ Add a New Fertilizer")
    fertilizer_id = st.text_input("Enter Fertilizer ID", key="add_fertilizer_id")
    fertilizer_name = st.text_input("Enter Fertilizer Name", key="add_fertilizer_name")
    diseases_input = st.text_area("Enter Diseases Treated (comma-separated)", key="add_diseases_input")

    if st.button("Add Fertilizer"):
        if not fertilizer_id or not fertilizer_name:
            st.warning("Please fill both Fertilizer ID and Name.")
        elif any(f['FertilizerID'].lower() == fertilizer_id.lower() for f in fertilizers):
            st.warning("⚠️ This Fertilizer ID already exists.")
        elif any(f['FertilizerName'].lower() == fertilizer_name.lower() for f in fertilizers):
            st.warning("⚠️ This Fertilizer Name already exists.")
        else:
            diseases_list = [d.strip().capitalize() for d in diseases_input.split(",") if d.strip()]
            new_fertilizer = {
                "FertilizerID": fertilizer_id,
                "FertilizerName": fertilizer_name,
                "Diseases Treated": diseases_list
            }
            fertilizers.append(new_fertilizer)
            save_fertilizers(fertilizers)
            st.success("✅ Fertilizer added successfully!")

    # ---------- Delete Fertilizer ----------
    st.markdown("### ➖ Delete a Fertilizer")
    if fertilizers:
        fertilizer_to_delete = st.selectbox("Select a Fertilizer to Delete", [f["FertilizerName"] for f in fertilizers])
        if st.button("Delete Fertilizer"):
            fertilizers = [f for f in fertilizers if f["FertilizerName"] != fertilizer_to_delete]
            save_fertilizers(fertilizers)
            st.success(f"✅ Fertilizer '{fertilizer_to_delete}' deleted successfully!")
    else:
        st.info("No fertilizers available to delete.")

    # ---------- Display Current Fertilizers (Sorted by ID) ----------
    st.markdown("### 📋 Existing Fertilizers")
    if fertilizers:
        fertilizers_sorted = sorted(fertilizers, key=lambda x: x["FertilizerID"])
        display_data = []
        for f in fertilizers_sorted:
            display_data.append({
                "Fertilizer ID": f["FertilizerID"],
                "Fertilizer Name": f["FertilizerName"],
                "Diseases Treated": ", ".join(f["Diseases Treated"])
            })
        st.table(display_data)
    else:
        st.info("No fertilizers found yet.")
