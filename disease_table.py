import json
import os
import streamlit as st

DISEASE_FILE = "diseases.json"

def load_diseases():
    if os.path.exists(DISEASE_FILE) and os.path.getsize(DISEASE_FILE) > 0:
        with open(DISEASE_FILE, "r") as f:
            return json.load(f)
    return []

def save_diseases(diseases):
    with open(DISEASE_FILE, "w") as f:
        json.dump(diseases, f, indent=4)

def disease_table():
    diseases = load_diseases()
    st.subheader("🌿 Manage Diseases")

    # ---------- Add Disease ----------
    st.markdown("### ➕ Add a New Disease")
    disease_id = st.text_input("Enter Disease ID", key="add_disease_id")
    disease_name = st.text_input("Enter Disease Name", key="add_disease_name")
    affected_plants = st.text_input("Enter Affected Plants (comma-separated)", key="add_affected_plants")

    if st.button("Add Disease"):
        if any(d["ID"] == disease_id for d in diseases):
            st.error("❌ Disease ID already exists!")
        elif any(d["Disease Name"].lower() == disease_name.lower() for d in diseases):
            st.error("❌ Disease Name already exists!")
        else:
            new_disease = {
                "ID": disease_id,
                "Disease Name": disease_name.capitalize(),
                "Plants Affected": [p.strip().capitalize() for p in affected_plants.split(",") if p.strip()]
            }
            diseases.append(new_disease)
            save_diseases(diseases)
            st.success("✅ Disease added successfully!")

    # ---------- Delete Disease ----------
    st.markdown("### ➖ Delete a Disease")
    if diseases:
        disease_to_delete = st.selectbox("Select a Disease to Delete", [d["Disease Name"] for d in diseases])
        if st.button("Delete Disease"):
            diseases = [d for d in diseases if d["Disease Name"] != disease_to_delete]
            save_diseases(diseases)
            st.success(f"✅ Disease '{disease_to_delete}' deleted successfully!")
    else:
        st.info("No diseases available to delete.")

    # ---------- Display Current Diseases (Sorted by ID) ----------
    st.markdown("### 📋 Existing Diseases")
    diseases_sorted = sorted(diseases, key=lambda x: x["ID"])
    st.dataframe(diseases_sorted)
