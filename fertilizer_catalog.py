import streamlit as st
import json
import os

FILENAME = "fertilizer_catalogue.json"
PLACEHOLDER_IMAGE = "https://via.placeholder.com/200"

# ------------------- Load / Save -------------------
def load_fertilizer_catalogue():
    if os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0:
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

def save_fertilizer_catalogue(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

# ------------------- Generate ID -------------------
def generate_fertilizer_id(fertilizers):
    if not fertilizers:
        return "F001"
    last_id = fertilizers[-1]["FertilizerID"]
    num = int(last_id[1:]) + 1
    return f"F{num:03d}"

# ------------------- Admin Catalog Management -------------------
def manage_fertilizer_catalog():
    st.subheader("🌱 Fertilizer Catalog")
    fertilizers = load_fertilizer_catalogue()
    new_id = generate_fertilizer_id(fertilizers)

    with st.form("fertilizer_form"):
        st.text_input("Fertilizer ID", value=new_id, disabled=True)
        fertilizer_name = st.text_input("Fertilizer Name")
        description = st.text_area("Description")
        image_url = st.text_input("Image URL (Google Drive link)")
        price = st.number_input("Price", min_value=0.0, step=1.0)

        submitted = st.form_submit_button("Add Fertilizer")
        if submitted:
            if not fertilizer_name or not description:
                st.error("Please fill in all the fields except Image URL (optional)!")
            else:
                if not image_url:
                    image_url = PLACEHOLDER_IMAGE
                new_fertilizer = {
                    "FertilizerID": new_id,
                    "FertilizerName": fertilizer_name,
                    "Description": description,
                    "ImageURL": image_url,
                    "Price": price
                }
                fertilizers.append(new_fertilizer)
                save_fertilizer_catalogue(fertilizers)
                st.success(f"Fertilizer '{fertilizer_name}' added successfully!")

    st.subheader("📋 Existing Fertilizers")
    if fertilizers:
        fertilizers_sorted = sorted(fertilizers, key=lambda x: x["FertilizerID"])
        for f in fertilizers_sorted:
            image_url = f.get('ImageURL') if f.get('ImageURL') else PLACEHOLDER_IMAGE
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**ID:** {f['FertilizerID']}")
                st.markdown(f"**Name:** {f['FertilizerName']}")
                st.markdown(f"**Description:** {f['Description']}")
                st.markdown(f"**Price:** Rs. {f.get('Price',0)}")
            with col2:
                st.image(image_url, width=150)
            st.markdown("---")

# ------------------- Premium User Display Only -------------------
def display_fertilizer_catalog(cart=None):
    fertilizers = load_fertilizer_catalogue()
    if fertilizers:
        fertilizers_sorted = sorted(fertilizers, key=lambda x: x["FertilizerID"])
        for f in fertilizers_sorted:
            image_url = f.get('ImageURL') if f.get('ImageURL') else PLACEHOLDER_IMAGE
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**ID:** {f['FertilizerID']}")
                st.markdown(f"**Name:** {f['FertilizerName']}")
                st.markdown(f"**Description:** {f['Description']}")
                st.markdown(f"**Price:** Rs. {f.get('Price',0)}")
                if cart is not None:
                    if st.button(f"Add '{f['FertilizerName']}' to Cart", key=f"cart_{f['FertilizerID']}"):
                        cart.append(f)
                        st.success(f"✅ '{f['FertilizerName']}' added to cart!")
            with col2:
                st.image(image_url, width=150)
            st.markdown("---")
    else:
        st.info("No fertilizers added yet.")
