import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="GenZ Career Survey Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for immersive styling
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading (Cached for performance)
@st.cache_data
def load_data():
    try:
        # AGAR AAPKI FILE KA NAAM ALAG HAI TO YAHA BADAL LEIN
        df = pd.read_csv("data.csv") 
        return df
    except FileNotFoundError:
        st.error("⚠️ 'data.csv' file nahi mili! Please check karein ki file sahi folder mein hai.")
        return None

df = load_data()

if df is not None:
    # 3. Sidebar Navigation
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3065/3065524.png", width=100)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:", 
        ["Overview & Dataset", "Demographics", "Career Aspirations", "Work Culture Preferences", "Key Insights"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Tip:** Charts par hover karke aap exact counts aur percentages dekh sakte hain.")

    # --- PAGE 1: OVERVIEW & DATASET ---
    if page == "Overview & Dataset":
        st.markdown('<div class="main-title">Employee Career Survey Analysis 📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Exploring GenZ career mindsets, aspirations, and workplace expectations</div>', unsafe_allow_html=True)
        
        # High-level metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Respondents", len(df))
        col2.metric("Total Countries", df['Your Current Country.'].nunique())
        col3.metric("Survey Questions Covered", len(df.columns) - 2)
        
        st.markdown("---")
        
        # Interactive Slider
        st.markdown("### 📋 Dataset Preview Settings")
        rows_to_show = st.slider("Select number of rows to display:", min_value=5, max_value=100, value=10, step=5)
        
        st.write(f"Showing top {rows_to_show} rows of the dataset:")
        st.dataframe(df.head(rows_to_show), use_container_width=True)

    # --- PAGE 2: DEMOGRAPHICS ---
    elif page == "Demographics":
        st.header("🌍 Respondent Demographics")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Breakdown")
            country_counts = df["Your Current Country."].value_counts()
            st.dataframe(country_counts)
            
        with col2:
            label = country_counts.index
            counts = country_counts.values
            colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
            
            fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
            fig.update_layout(title_text='Country-wise Distribution', margin=dict(t=50, b=0, l=0, r=0))
            fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=15,
                              marker=dict(colors=colors, line=dict(color='black', width=2)))
            st.plotly_chart(fig, use_container_width=True)

    # --- PAGE 3: CAREER ASPIRATIONS ---
    elif page == "Career Aspirations":
        st.header("🚀 Career Aspirations & Influences")
        
        tab1, tab2 = st.tabs(["Influencing Factors", "Higher Education Abroad"])
        
        with tab1:
            st.subheader("What influences GenZ career choices the most?")
            q1_data = df["Which of the below factors influence the most about your career aspirations ?"].value_counts()
            
            fig1 = go.Figure(data=[go.Pie(labels=q1_data.index, values=q1_data.values, marker=dict(colors=px.colors.qualitative.Plotly))])
            fig1.update_layout(title_text="Factors Influencing Career Aspirations")
            fig1.update_traces(hoverinfo="label+value", textinfo="percent", textfont_size=12,
                               marker=dict(line=dict(color="black", width=2)))
            st.plotly_chart(fig1, use_container_width=True)
            
        with tab2:
            st.subheader("Willingness to pursue Higher Education outside India (Self-Sponsored)")
            q2_col = "Would you definitely pursue a Higher Education / Post Graduation outside of India ? If only you have to self sponsor it."
            q2_data = df[q2_col].value_counts()
            
            fig2 = go.Figure(data=[go.Pie(labels=q2_data.index, values=q2_data.values, marker=dict(colors=['lightgreen', 'skyblue', 'coral']))])
            fig2.update_layout(title_text="Pursuing Higher Education Abroad")
            fig2.update_traces(hoverinfo="label+value", textinfo="percent", textfont_size=12,
                               marker=dict(line=dict(color='black', width=2)))
            st.plotly_chart(fig2, use_container_width=True)

    # --- PAGE 4: WORK CULTURE PREFERENCES ---
    elif page == "Work Culture Preferences":
        st.header("🏢 Workplace & Company Culture Preferences")
        
        st.subheader("1. How likely is it that you will work for one employer for 3 years or more?")
        q3_col = "How likely is that you will work for one employer for 3 years or more ?"
        q3_data = df[q3_col].value_counts()
        
        fig3 = go.Figure(data=[go.Pie(labels=q3_data.index, values=q3_data.values, marker=dict(colors=['aqua', 'green', 'orange']))])
        fig3.update_layout(title_text="Company Loyalty (3+ Years)")
        fig3.update_traces(hoverinfo="label+value", textinfo="percent", textfont_size=13,
                           marker=dict(line=dict(color="black", width=2)))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("2. What is the most preferred working environment?")
        q4_data = df["What is the most preferred working environment for you."].value_counts()
        
        fig4 = go.Figure(data=[go.Pie(labels=q4_data.index, values=q4_data.values, marker=dict(colors=px.colors.qualitative.Pastel))])
        fig4.update_layout(title_text="Preferred Working Environment")
        fig4.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=13,
                           marker=dict(line=dict(color='black', width=2)))
        st.plotly_chart(fig4, use_container_width=True)

    # --- PAGE 5: KEY INSIGHTS ---
    elif page == "Key Insights":
        st.header("📌 Project Conclusion & Key Insights")
        
        st.markdown("""
        ### Final Takeaways:
        * 🌍 **Global Representation:** Around **98%** of the survey participants are from **India**.
        * 👥 **Parental Guidance:** Data shows that approximately **33%** of GenZ's career aspirations are shaped directly by **Parental Influence**.
        * ✈️ **Global Ambitions:** Around **46-47%** of respondents are eager to pursue higher education or post-graduation abroad by earning and sponsoring themselves.
        * 🤝 **Company Loyalty:** While **59%** of GenZ find a strict 3-year tenure difficult, they are highly willing to stay longer if it's the **right company**.
        * 🏡 **Remote Work Trends:** GenZ's preference peaks at **21% for remote work with travel options**, while it drops to its lowest (**4%**) for fully remote setups with absolutely zero office access.
        """)
        
        st.balloons()
        st.success("🎉 Thank you for exploring the dashboard! Built as part of Data Analysis practice.")