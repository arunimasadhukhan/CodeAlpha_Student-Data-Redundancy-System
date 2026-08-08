# Student Data Redundancy System

A secure and reliable Python application featuring localized database redundancy and an interactive web dashboard. This project was developed as part of the **CodeAlpha Software Engineering Internship**.

## 🚀 Features
* **Interactive UI:** Built entirely with Streamlit for a smooth and dynamic user experience.
* **Database Redundancy:** Automatically syncs data across a primary database (`student_records.directory.db`) and a secondary backup database (`system_directory.db`) to ensure zero data loss.
* **Full CRUD Operations:** Seamlessly add, view, update, and delete student records.
* **Configuration Integrity:** Uses environment variable handling via `.env` configuration files for secure application deployment.

## 🛠️ Tech Stack
* **Frontend UI:** Streamlit
* **Database Backend:** SQLite3
* **Language:** Python 3.x

## 📁 Project Structure
* `app.py`: Main application code containing the Streamlit UI and user workflow.
* `database.py`: Core logic for managing SQLite database connections and synchronization routines.
* `config.py`: System wide environmental and app configurations.
* `requirements.txt`: Python package dependencies required to run the application.

## 💻 Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd CodeAlpha_Student-Data-Redundancy-System
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   * Rename `.env.example` to `.env`
   * Configure any required application environment keys inside `.env`

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## ⚖️ License
This project is built for educational and internship assessment purposes under CodeAlpha.
