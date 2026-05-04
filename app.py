import streamlit as st
import json
import os
import uuid

# Configuration
st.set_page_config(
    page_title="Quantum Chromodynamics (QCD)",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a better look
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #8b5cf6;
        font-weight: 800;
    }
    h2, h3 {
        color: #a78bfa;
    }
    .experiment-card {
        background-color: #1e1e2f;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #8b5cf6;
        margin-bottom: 1rem;
    }
    .experiment-title {
        font-size: 1.25rem;
        font-weight: bold;
        color: white;
        margin-bottom: 0.25rem;
    }
    .experiment-date {
        color: #9ca3af;
        font-size: 0.875rem;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def dashboard():
    st.title("Quantum Chromodynamics")
    st.write("The theory of the strong interaction between quarks and gluons, the fundamental particles that make up composite hadrons such as the proton, neutron and pion.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("The QCD Lagrangian")
        st.write("The dynamics of the quarks and gluons are governed by the quantum chromodynamics Lagrangian. It describes a non-abelian gauge theory based on the SU(3) gauge group.")
        
        st.latex(r"""
        \mathcal{L}_{QCD} = \bar{\psi}_i \left( i \gamma^\mu (D_\mu)_{ij} - m \delta_{ij} \right) \psi_j - \frac{1}{4} G_{\mu\nu}^a G_a^{\mu\nu}
        """)
        
        st.caption(r"Where $\psi_i(x)$ is the quark field, $G_{\mu\nu}^a$ is the gluon field strength tensor, and $D_\mu$ is the gauge covariant derivative.")
        
        st.header("Key Properties")
        st.subheader("Color Confinement")
        st.write("Quarks and gluons cannot be isolated; they are always confined into colorless hadrons.")
        
        st.subheader("Asymptotic Freedom")
        st.write("At very high energies (or short distances), the strong interaction becomes remarkably weak.")

    with col2:
        st.header("Experimental Evidence")
        st.caption("Real-time data fetched from local database")
        
        experiments = load_data()
        
        if not experiments:
            st.info("No experiments found in the database. Add some from the sidebar!")
        else:
            for exp in reversed(experiments): # Show newest first
                st.markdown(f"""
                <div class="experiment-card">
                    <div class="experiment-title">{exp['title']}</div>
                    <div class="experiment-date">{exp['date']}</div>
                    <div><strong>Description:</strong> {exp['description']}</div>
                    <div style="margin-top: 0.5rem;"><strong>Significance:</strong> {exp['significance']}</div>
                </div>
                """, unsafe_allow_html=True)

def add_experiment():
    st.title("Add New Experiment")
    st.write("Contribute to the database of Quantum Chromodynamics research.")
    
    with st.form("experiment_form"):
        title = st.text_input("Experiment Title", placeholder="e.g. Discovery of the Gluon")
        date = st.text_input("Date / Year", placeholder="e.g. 1979")
        description = st.text_area("Description", placeholder="Briefly describe the experiment methodology...")
        significance = st.text_area("Significance / Result", placeholder="What did this prove regarding QCD?")
        
        submitted = st.form_submit_button("Submit to Database")
        
        if submitted:
            if title and date and description and significance:
                data = load_data()
                new_exp = {
                    "id": f"exp_{uuid.uuid4().hex[:8]}",
                    "title": title,
                    "date": date,
                    "description": description,
                    "significance": significance
                }
                data.append(new_exp)
                save_data(data)
                st.success("Experiment added successfully!")
            else:
                st.error("Please fill in all fields.")

def main():
    st.sidebar.title("QCD Explorer")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Add Experiment"])
    
    if page == "Dashboard":
        dashboard()
    elif page == "Add Experiment":
        add_experiment()

    st.sidebar.markdown("---")
    st.sidebar.info("Built with [Streamlit](https://streamlit.io/) for easy public hosting.")

if __name__ == "__main__":
    main()
