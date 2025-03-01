import streamlit as st
import pandas as pd

# loading excel file
@st.cache_data
def load_data():
    file_path = "fee-publication-data-jan22-dec22-(for-download).xlsx"  # Update with your actual file path
    df = pd.read_excel(file_path, sheet_name="1_TOSP TOF and Bill data")  # Load the relevant sheet
    return df

# loading dataset
df = load_data()



#st.write("Columns in DataFrame:", df.columns.tolist())


# extracting relevant columns (adjust based on the file structure)
columns_needed = ["Procedure", "Hospital Setting", "Ward Type", "P50 Bill"]
df = df[columns_needed].dropna()  # Remove any empty rows

# Streamlit UI
st.title("💰 Out-of-Pocket Medical Cost Calculator")
st.markdown("Use this tool to estimate your medical expenses based on procedure and hospital setting.")

# ask user for selections
procedure = st.selectbox("🔹 Select Your Procedure:", df["Procedure"].unique())
hospital_setting = st.selectbox("🏥 Select Hospital Setting:", df["Hospital Setting"].unique())
ward_type = st.selectbox("🛏️ Select Ward Type:", df["Ward Type"].unique())

# filtering data based on what user selected
filtered_data = df[
    (df["Procedure"] == procedure) &
    (df["Hospital Setting"] == hospital_setting) &
    (df["Ward Type"] == ward_type)
]

# display results
if not filtered_data.empty:
    avg_bill = filtered_data["P50 Bill"].values[0]
    st.subheader(f"💲 Estimated Bill: **${avg_bill:,.2f}**")

    # Insurance and subsidy options
    insurance_coverage = st.slider("📄 Insurance Coverage (%)", 0, 100, 50)  # Default 50%
    gov_subsidy = st.slider("🏛️ Government Subsidy (%)", 0, 100, 30)  # Default 30%

    # Calculate out-of-pocket cost
    covered_by_insurance = avg_bill * (insurance_coverage / 100)
    covered_by_subsidy = avg_bill * (gov_subsidy / 100)
    out_of_pocket = avg_bill - (covered_by_insurance + covered_by_subsidy)

    st.subheader(f"🧾 Estimated Out-of-Pocket Cost: **${out_of_pocket:,.2f}**")

else:
    st.warning("No data found for the selected options. Please try different selections.")

st.subheader("📜 Grant & Subsidy Eligibility Check")

income_bracket = st.selectbox("💰 Select Your Income Bracket:", ["Below $2,000", "$2,000-$4,000", "$4,000-$6,000", "Above $6,000"])
citizenship = st.radio("🌏 Are you a Singapore Citizen?", ["Yes", "No"])
medical_condition = st.checkbox("🏥 Do you have a chronic medical condition?")

# logic for grant eligibility
if citizenship == "Yes" and income_bracket in ["Below $2,000", "$2,000-$4,000"]:
    st.success("✅ You may be eligible for government medical subsidies!")
else:
    st.warning("⚠️ You may not qualify for full subsidies, but partial assistance may be available.")

# estimating success rate of grant application
st.subheader("📊 Estimated Success Rate of Grant Application")

grant_type = st.selectbox("🎯 Select Grant Type:", ["Medifund", "CHAS", "Subsidized Ward Grants"])
success_rates = {"Medifund": 75, "CHAS": 85, "Subsidized Ward Grants": 65}  # Example data

st.write(f"🔹 Estimated Success Rate: **{success_rates[grant_type]}%**")

st.markdown("---")  
st.subheader("⏳ Reimbursement Timeframe Estimator")

# sample data for estimated reimbursement times (from insurance websites)
reimbursement_times = {
    "Medisave": 30,  # Days
    "Private Insurance (AIA, Prudential, etc.)": 45,
    "Employer Reimbursement": 60,
    "Government Subsidy": 90
}

# ask for user's insurance type
insurance_type = st.selectbox("🏥 Select Your Insurance or Reimbursement Type:", list(reimbursement_times.keys()) + ["Other"])

# get estimated reimbursement time
if insurance_type in reimbursement_times:
    estimated_days = reimbursement_times[insurance_type]
else:
    estimated_days = st.number_input("📅 Enter Estimated Reimbursement Time (days):", min_value=1, value=30)

# calculating payout date
import datetime
today = datetime.date.today()
payout_date = today + datetime.timedelta(days=estimated_days)

# display results
st.info(f"💰 **Estimated Reimbursement Date:** {payout_date.strftime('%d %B %Y')}")
st.caption("📌 Note: This is an estimate. Actual processing times may vary.")


st.markdown("---")  
st.subheader("🛡️ Are You Over or Under-Insured?")

# user inputs for current insurance
monthly_income = st.number_input("💵 Enter Your Monthly Income (SGD):", min_value=0, value=5000)
current_insurance = st.number_input("📜 Enter Your Current Insurance Coverage (SGD):", min_value=0, value=50000)

# calculate recommended range (5-10 times annual income)
recommended_min = monthly_income * 12 * 5
recommended_max = monthly_income * 12 * 10

# displaying results
if current_insurance < recommended_min:
    st.error(f"⚠️ You are **under-insured**! Recommended coverage: **${recommended_min:,.0f} - ${recommended_max:,.0f}**")
elif current_insurance > recommended_max:
    st.warning(f"🔸 You may be **over-insured**. Recommended coverage: **${recommended_min:,.0f} - ${recommended_max:,.0f}**")
else:
    st.success(f"✅ Your coverage is **just right!** ({recommended_min:,.0f} - {recommended_max:,.0f})")

st.caption("📌 Note: These are general recommendations. Consult a financial advisor for a personalized plan.")

# Footer
st.markdown("---")
st.caption("📌 Note: This is an estimation tool. Actual costs may vary.")

