import json
import os
import streamlit as st

PLANT_FILE = "plants.json"

def load_plants():
    if os.path.exists(PLANT_FILE) and os.path.getsize(PLANT_FILE) > 0:
        with open(PLANT_FILE, "r") as f:
            return json.load(f)
    return []

def save_plants(plants):
    with open(PLANT_FILE, "w") as f:
        json.dump(plants, f, indent=4)

def get_plants():
    st.subheader("🌿 Manage Plants")

    plants = load_plants()

    # ---------- Add Plant ----------
    st.markdown("### ➕ Add a New Plant")
    plant_id = st.text_input("Enter Plant ID", key="add_plant_id")
    plant_name = st.text_input("Enter Plant Name", key="add_plant_name")

    if st.button("Add Plant"):
        if not plant_id or not plant_name:
            st.warning("Please fill both ID and Name.")
        elif any(p['ID'].lower() == plant_id.lower() for p in plants):
            st.warning("⚠️ This Plant ID already exists.")
        elif any(p['Plant Name'].lower() == plant_name.lower() for p in plants):
            st.warning("⚠️ This Plant Name already exists.")
        else:
            plants.append({"ID": plant_id, "Plant Name": plant_name})
            save_plants(plants)
            st.success("✅ Plant added successfully!")

    # ---------- Delete Plant ----------
    st.markdown("### ➖ Delete a Plant")
    if plants:
        plant_to_delete = st.selectbox("Select a Plant to Delete", [p["Plant Name"] for p in plants])
        if st.button("Delete Plant"):
            plants = [p for p in plants if p["Plant Name"] != plant_to_delete]
            save_plants(plants)
            st.success(f"✅ Plant '{plant_to_delete}' deleted successfully!")
    else:
        st.info("No plants available to delete.")

    # ---------- Display Current Plants (Sorted by ID) ----------
    st.markdown("### 📋 Current Plants")
    plants_sorted = sorted(plants, key=lambda x: x["ID"])
    st.table(plants_sorted)
