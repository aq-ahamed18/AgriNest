import streamlit as st
import plant_table
import disease_table
import fertilizer_table
import functions
import fertilizer_catalog

def after_login():
    if "loggeduser" not in st.session_state or not st.session_state.loggeduser:
        st.write(" ")
        return

    user = st.session_state.loggeduser
    st.markdown(f"### 👋 Welcome, {user['username']}!")
    st.info(f"Logged in as **{user['userType']} ({user.get('accountType','N/A')})**")

    # ------------------- Payment Success Page -------------------
    if st.session_state.get("payment_success"):
        st.success("✅ Payment Successful!")
        
        st.markdown("---")
        st.subheader("Thank You for Your Purchase")
        
        # Payment summary
        if st.session_state.get("payment_details"):
            details = st.session_state.payment_details
            st.info(f"""
            **Payment Summary:**
            - Amount: Rs. {details.get('amount', 0)}
            - Method: {details.get('method', 'N/A')}
            - Status: Approved
            - Transaction ID: {details.get('transaction_id', 'N/A')}
            - Date: {details.get('date', 'N/A')}
            """)
        
        st.markdown("---")
        st.write("Your order has been processed successfully. You will receive a confirmation email shortly.")
        
        if st.button("🏠 Return to Homepage", type="primary", use_container_width=True):
            st.session_state.payment_success = False
            st.session_state.payment_page = False
            if 'payment_details' in st.session_state:
                del st.session_state.payment_details
            st.rerun()
        
        return

    # ------------------- Payment Page -------------------
    if st.session_state.get("payment_page"):
        st.subheader("💳 Dummy Payment Page")
        st.write("You are about to pay for the following items:")

        if st.session_state.get("cart", []):
            total_amount = 0
            table_data = []
            for item in st.session_state.cart:
                table_data.append([item['FertilizerName'], f"Rs. {item['Price']}"])
                total_amount += item['Price']

            st.table(table_data)
            st.write(f"**Total Amount: Rs. {total_amount}**")
            
            st.markdown("---")
            
            # Payment Method Selection
            st.subheader("Payment Details")
            payment_method = st.radio(
                "Select Payment Method",
                ["Visa", "Mastercard", "Other"]
            )
            
            # Credit Card Details Form
            col1, col2 = st.columns(2)
            
            with col1:
                card_number = st.text_input("Credit Card Number", 
                                          placeholder="1234 5678 9012 3456",
                                          max_chars=19)
                
            with col2:
                card_holder = st.text_input("Card Holder Name",
                                          placeholder="John Doe")
            
            col3, col4, col5 = st.columns(3)
            
            with col3:
                expiry_date = st.text_input("Expiry Date (MM/YY)",
                                          placeholder="12/25",
                                          max_chars=5)
            
            with col4:
                cvc = st.text_input("CVC",
                                  placeholder="123",
                                  max_chars=3,
                                  type="password")
            
            with col5:
                st.write("")  # Spacer for alignment
                st.write("")  # Spacer for alignment
                # Show card type based on selection
                if payment_method == "Visa":
                    st.info("💳 Visa")
                elif payment_method == "Mastercard":
                    st.info("💳 Mastercard")
                else:
                    st.info("💳 Other Card")
            
            # Terms and conditions
            agree_terms = st.checkbox("I agree to the terms and conditions")
            
            st.markdown("---")
            
            # Payment buttons
            col6, col7, col8 = st.columns([1, 2, 1])
            
            with col7:
                if st.button("✅ Confirm Payment", type="primary", use_container_width=True):
                    # Store payment details for success page
                    import datetime
                    st.session_state.payment_details = {
                        'amount': total_amount,
                        'method': payment_method,
                        'transaction_id': f"TXN{user.get('username', 'USER').upper()}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Clear cart and show success page
                    st.session_state.cart.clear()
                    st.session_state.payment_page = False
                    st.session_state.payment_success = True
                    st.rerun()
                
                if st.button("🚫 Cancel Payment", use_container_width=True):
                    st.session_state.payment_page = False
                    st.rerun()

        else:
            st.info("Cart is empty.")
            st.session_state.payment_page = False
            st.rerun()
        
        # Add a back button in sidebar too
        st.sidebar.markdown("---")
        if st.sidebar.button("← Back to Shopping"):
            st.session_state.payment_page = False
            st.rerun()
        
        return  # Stop execution here when on payment page

    # ------------------- Admin Actions -------------------
    if user["userType"] == "Admin":
        admin_action = st.selectbox("Select Admin Action",
                                    ["Choose Options",
                                     "Manage Plants",
                                     "Manage Diseases",
                                     "Manage Fertilizers",
                                     "Manage Fertilizer Catalog"])
        if admin_action == "Manage Plants":
            plant_table.get_plants()
        elif admin_action == "Manage Diseases":
            disease_table.disease_table()
        elif admin_action == "Manage Fertilizers":
            fertilizer_table.fertilizer_table()
        elif admin_action == "Manage Fertilizer Catalog":
            fertilizer_catalog.manage_fertilizer_catalog()

    # ------------------- User Actions -------------------
    elif user["userType"] == "User":
        diseases = disease_table.load_diseases()
        fertilizers = fertilizer_table.load_fertilizers()
        is_premium = user.get("accountType") == "Premium"

        # ------------------- Show Upgrade Option for Free Users -------------------
        if not is_premium:
            st.markdown("---")
            functions.upgrade_to_premium(user)
            st.markdown("---")

        # ------------------- Premium Banner for User Action -------------------
        if is_premium:
            st.markdown(
                """
                <div style='padding: 15px; border-radius: 12px; background: linear-gradient(to right, #a8e063, #56ab2f);
                            color: white; text-align: center; font-size: 18px; font-weight: bold;'>
                    🌟 Advanced Search Panel 🌟
                </div>
                """, unsafe_allow_html=True
            )

        user_action = st.selectbox("Select User Action",
                                   ["Choose Option",
                                    "Find Diseases by Plant Name",
                                    "Find Plants by Disease Name",
                                    "Find Diseases by Fertilizer Name",
                                    "Find Fertilizers by Disease Name"])

        if user_action == "Find Diseases by Plant Name":
            plant_name = st.text_input("Enter Plant Name", key="plant_name")
            if st.button("Search Diseases for Plant", key="search_diseases_plant"):
                result = functions.find_diseases_by_plant(plant_name, diseases)
                st.success(f"Diseases affecting **{plant_name}**: {', '.join(result)}") if result else st.info(f"No diseases found for **{plant_name}**")
        elif user_action == "Find Plants by Disease Name":
            disease_name = st.text_input("Enter Disease Name", key="disease_name")
            if st.button("Search Plants for Disease", key="search_plants_disease"):
                result = functions.find_plants_by_disease(disease_name, diseases)
                st.success(f"Plants affected by **{disease_name}**: {', '.join(result)}") if result else st.info(f"No plants found for **{disease_name}**")
        elif user_action == "Find Diseases by Fertilizer Name":
            if is_premium:
                fertilizer_name = st.text_input("Enter Fertilizer Name", key="fertilizer_name")
                if st.button("Search Diseases treated by Fertilizer", key="search_diseases_fertilizer"):
                    result = functions.find_diseases_by_fertilizer(fertilizer_name, fertilizers)
                    st.success(f"Diseases treated by **{fertilizer_name}**: {', '.join(result)}") if result else st.info(f"No diseases found for **{fertilizer_name}**")
            else:
                st.warning("⚠️ Premium only feature.")
        elif user_action == "Find Fertilizers by Disease Name":
            if is_premium:
                disease_name = st.text_input("Enter Disease Name", key="disease_for_fertilizer")
                if st.button("Search Fertilizers for Disease", key="search_fertilizers_disease"):
                    result = functions.find_fertilizers_by_disease(disease_name, fertilizers)
                    st.success(f"Fertilizers used for **{disease_name}**: {', '.join(result)}") if result else st.info(f"No fertilizers found for **{disease_name}**")
            else:
                st.warning("⚠️ Premium only feature.")

        # ------------------- Premium Fertilizer Ordering Banner -------------------
        if is_premium:
            st.markdown(
                """
                <div style='padding: 15px; border-radius: 12px; background: linear-gradient(to right, #f7971e, #ffd200);
                            color: black; text-align: center; font-size: 18px; font-weight: bold; margin-top:20px;'>
                    🛒 Fertilizer Shopping Center 🛒
                </div>
                """, unsafe_allow_html=True
            )
            st.markdown("---")
            if "cart" not in st.session_state:
                st.session_state.cart = []
            fertilizer_catalog.display_fertilizer_catalog(st.session_state.cart)

    # ------------------- Sidebar Cart (moved outside user section) -------------------
    if user["userType"] == "User" and user.get("accountType") == "Premium":
        cart_sidebar = st.sidebar
        cart_sidebar.title("🛒 Your Cart")
        if st.session_state.get("cart", []):
            total = sum(item['Price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                cart_sidebar.write(f"{item['FertilizerName']} - Rs. {item['Price']}")
            cart_sidebar.write(f"**Total: Rs. {total}**")
            if cart_sidebar.button("Proceed to Pay", type="primary"):
                st.session_state.payment_page = True
                st.rerun()
            if cart_sidebar.button("Clear Cart"):
                st.session_state.cart.clear()
                st.rerun()
        else:
            cart_sidebar.write("Cart is empty.")
