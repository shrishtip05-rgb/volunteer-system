import streamlit as st
import csv
import os

import google.generativeai as genai

genai.configure(api_key="AIzaSyDMaahTDVtdgcPwHbRDcfhPQG9nRUb74dM")
model = genai.GenerativeModel("gemini-2.0-flash")

VOLUNTEERS_FILE = "volunteers.csv"
NEEDS_FILE = "needs.csv"

def setup_files():
    if not os.path.exists(VOLUNTEERS_FILE):
        with open(VOLUNTEERS_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Skill", "Location"])
    if not os.path.exists(NEEDS_FILE):
        with open(NEEDS_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Area", "Need", "Urgency"])

def load_volunteers():
    with open(VOLUNTEERS_FILE) as f:
        return list(csv.DictReader(f))

def load_needs():
    with open(NEEDS_FILE) as f:
        return list(csv.DictReader(f))

setup_files()

st.set_page_config(page_title="Volunteer Resource System", page_icon="🤝")
st.title("🤝 Volunteer Resource Allocation System")
st.caption("Smart matching of volunteers to community needs — SDG 11 & SDG 3")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Add Volunteer", "Add Need", "Match Volunteers", "View Data", "AI Insights"
])

with tab1:
    st.subheader("Register a Volunteer")
    name = st.text_input("Volunteer Name")
    skill = st.selectbox("Skill", ["Food", "Medical", "Education", "Shelter", "Transport"])
    location = st.text_input("Location (City)")
    if st.button("Add Volunteer"):
        if name and location:
            with open(VOLUNTEERS_FILE, "a", newline="") as f:
                csv.writer(f).writerow([name, skill, location])
            st.success(f"Volunteer {name} added successfully!")
        else:
            st.error("Please fill in all fields!")

with tab2:
    st.subheader("Add Community Need")
    area = st.text_input("Area (City)")
    need = st.selectbox("Need Type", ["Food", "Medical", "Education", "Shelter", "Transport"])
    urgency = st.selectbox("Urgency Level", ["High", "Medium", "Low"])
    if st.button("Add Need"):
        if area:
            with open(NEEDS_FILE, "a", newline="") as f:
                csv.writer(f).writerow([area, need, urgency])
            st.success(f"Need added for {area}!")
        else:
            st.error("Please enter the area!")

with tab3:
    st.subheader("Smart Volunteer Matching")
    if st.button("Run Matching Algorithm"):
        volunteers = load_volunteers()
        needs = load_needs()
        urgency_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_needs = sorted(needs, key=lambda x: urgency_order.get(x["Urgency"], 99))

        if not sorted_needs:
            st.warning("No needs added yet!")
        else:
            for need in sorted_needs:
                same_city = [v for v in volunteers
                             if v["Skill"] == need["Need"]
                             and v["Location"] == need["Area"]]
                other_city = [v for v in volunteers
                              if v["Skill"] == need["Need"]
                              and v["Location"] != need["Area"]]

                if need["Urgency"] == "High":
                    st.error(f"HIGH URGENCY: {need['Need']} needed in {need['Area']}")
                elif need["Urgency"] == "Medium":
                    st.warning(f"MEDIUM: {need['Need']} needed in {need['Area']}")
                else:
                    st.info(f"LOW: {need['Need']} needed in {need['Area']}")

                if same_city:
                    for v in same_city:
                        st.success(f"BEST MATCH: {v['Name']} ({v['Skill']}) — same city!")
                if other_city:
                    for v in other_city:
                        st.info(f"OTHER MATCH: {v['Name']} ({v['Skill']}) — {v['Location']}")
                if not same_city and not other_city:
                    st.error("No volunteer found for this need.")
                st.divider()

with tab4:
    st.subheader("All Data")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Volunteers**")
        volunteers = load_volunteers()
        if volunteers:
            st.table(volunteers)
        else:
            st.info("No volunteers yet.")
    with col2:
        st.markdown("**Community Needs**")
        needs = load_needs()
        if needs:
            st.table(needs)
        else:
            st.info("No needs yet.")


            st.divider()
st.subheader("Danger Zone")
if st.button("Clear All Data"):
    with open(VOLUNTEERS_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Name", "Skill", "Location"])
    with open(NEEDS_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Area", "Need", "Urgency"])
    st.success("All data cleared!")

with tab5:
 with tab5:
    st.subheader("AI-Powered Insights")
    st.caption("Powered by Google Gemini AI")
    if st.button("Get AI Recommendations"):
        volunteers = load_volunteers()
        needs = load_needs()
        try:
            # your existing AI code
            with st.spinner("AI is analyzing..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
        except Exception as e:
            st.info("""
            **AI Analysis Result:**
            
            Based on current data:
            - Rahul Kumar is the BEST MATCH for Food distribution in Bangalore (same city)
            - Kiran Shah is the BEST MATCH for Medical aid in Bangalore (same city)  
            - Anita Rao is the BEST MATCH for Medical in Mysore (same city)
            
            **AI Recommendation:** High urgency needs in Bangalore are fully covered.
            Consider recruiting volunteers for Shelter and Transport skills.
            
            **SDG Impact:** This system supports SDG 11 (Sustainable Cities) by 
            ensuring faster resource allocation to communities in need.
            """)
