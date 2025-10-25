💾 Data Storage

This project uses JSON files for data storage instead of a traditional database system.
All information related to users, plants, diseases, and fertilizers is stored in individual .json files located within the project directory.

JSON was chosen to ensure simplicity, portability, and ease of setup, allowing the application to run without requiring external database configurations.

The application reads and writes data dynamically to these JSON files, demonstrating key database operations such as data retrieval, insertion, and persistence in a lightweight, file-based format.

📁 Project Structure
📦 Plant Disease and Fertilizer Information System
┣ 📜 app.py                  # Main Streamlit app file (frontend and logic)
┣ 📜 functions.py            # Contains helper functions (data handling, login logic, etc.)
┣ 📜 users.json              # Stores user account information
┣ 📜 plants.json             # Stores plant data
┣ 📜 diseases.json           # Stores disease details
┣ 📜 fertilizers.json        # Stores fertilizer data
┗ 📜 README.md               # Project documentation and setup instructions

🚀 How to Run

Install Streamlit using pip install streamlit

Run the application with the command:

streamlit run app.py


The web app will open automatically in your default browser.

🧠 Note

This project is developed for educational purposes to demonstrate the integration of Python, Streamlit, and JSON data handling.
It can be easily upgraded to use a real database (like SQLite or Firebase) in the future."# AgriNest" 
