import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="OneRep Weightlifting Meet Manager",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# OneRep-Inspired Styling
# -----------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --onerep-black: #050505;
            --onerep-cream: #fff8ee;
            --onerep-white: #ffffff;
            --onerep-teal: #76f7ff;
            --onerep-teal-dark: #22b8c7;
            --onerep-pink: #f6c7c7;
            --onerep-mint: #bff4df;
            --onerep-yellow: #ffd166;
            --onerep-gray: #f2eee7;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: var(--onerep-black);
            color: var(--onerep-white);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        .onerep-hero {
            background: var(--onerep-white);
            border: 4px solid var(--onerep-black);
            border-radius: 28px;
            padding: 2rem 2.25rem;
            margin-bottom: 1.5rem;
            box-shadow: 10px 10px 0px var(--onerep-teal);
        }

        .onerep-kicker {
            color: var(--onerep-teal-dark);
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-weight: 800;
            font-size: 0.8rem;
            margin-bottom: 0.35rem;
        }

        .onerep-title {
            font-family: 'Fredoka', sans-serif;
            color: #000000 !important;
            font-size: clamp(2.4rem, 6vw, 5rem);
            line-height: 0.95;
            margin: 0;
            text-shadow: 3px 3px 0px var(--onerep-teal);
        }

        .onerep-subtitle {
            color: var(--onerep-black);
            font-size: 1.05rem;
            max-width: 760px;
            margin-top: 1rem;
        }

        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Fredoka', sans-serif;
            color: var(--onerep-white);
        }

        [data-testid="stForm"], [data-testid="stExpander"], .stDataFrame {
            background: rgba(255, 255, 255, 0.95);
            border: 3px solid var(--onerep-black);
            border-radius: 22px;
            box-shadow: 7px 7px 0px var(--onerep-teal);
            padding: 1rem;
            color: var(--onerep-black);
        }

        [data-testid="stForm"] h1,
        [data-testid="stForm"] h2,
        [data-testid="stForm"] h3,
        [data-testid="stExpander"] h1,
        [data-testid="stExpander"] h2,
        [data-testid="stExpander"] h3 {
            color: var(--onerep-black);
        }

        .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
            background: var(--onerep-pink);
            color: var(--onerep-black);
            border: 3px solid var(--onerep-black);
            border-radius: 999px;
            font-family: 'Futura PT', 'Inter', sans-serif;
            font-weight: 800;
            letter-spacing: 0.02em;
            box-shadow: 4px 4px 0px var(--onerep-black);
            transition: all 0.08s ease-in-out;
        }

        .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
            background: var(--onerep-teal);
            color: var(--onerep-black);
            border: 3px solid var(--onerep-black);
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px var(--onerep-black);
        }

        label, [data-testid="stWidgetLabel"] {
            font-weight: 800;
            color: var(--onerep-black);
        }

        input, textarea, select {
            border-radius: 14px !important;
        }

        [data-testid="stMetric"] {
            background: var(--onerep-mint);
            border: 3px solid var(--onerep-black);
            border-radius: 22px;
            padding: 1rem;
            box-shadow: 5px 5px 0px var(--onerep-black);
            color: var(--onerep-black);
        }

        [data-testid="stMetric"] label,
        [data-testid="stMetric"] div {
            color: var(--onerep-black) !important;
        }

        .onerep-pill-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }

        .onerep-pill {
            background: var(--onerep-pink);
            border: 2px solid var(--onerep-black);
            border-radius: 999px;
            padding: 0.35rem 0.75rem;
            font-weight: 800;
            color: var(--onerep-black);
        }

        .display-card {
            background: var(--onerep-white);
            color: var(--onerep-black);
            border: 5px solid var(--onerep-black);
            border-radius: 32px;
            padding: 2.5rem;
            box-shadow: 12px 12px 0px var(--onerep-teal);
            text-align: center;
        }

        .display-label {
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--onerep-teal-dark);
            font-weight: 900;
            font-size: 1rem;
        }

        .display-name {
            font-family: 'Fredoka', sans-serif;
            font-size: clamp(3rem, 8vw, 7rem);
            line-height: 0.95;
            margin: 0.5rem 0;
            text-shadow: 4px 4px 0px var(--onerep-teal);
        }

        .display-weight {
            font-family: 'Fredoka', sans-serif;
            font-size: clamp(4rem, 12vw, 10rem);
            line-height: 1;
            margin: 0.5rem 0;
        }

        .display-detail-row {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }

        .display-detail {
            background: var(--onerep-pink);
            border: 3px solid var(--onerep-black);
            border-radius: 999px;
            padding: 0.65rem 1.1rem;
            font-weight: 900;
            font-size: 1.1rem;
        }

        .timer-box {
            background: var(--onerep-black);
            color: var(--onerep-white);
            border-radius: 26px;
            padding: 1rem 2rem;
            margin: 1.5rem auto 0;
            max-width: 420px;
            font-family: 'Fredoka', sans-serif;
            font-size: clamp(3rem, 9vw, 7rem);
            line-height: 1;
            box-shadow: 7px 7px 0px var(--onerep-pink);
        }

        .plate-card, .results-card {
            background: rgba(255, 255, 255, 0.95);
            color: var(--onerep-black);
            border: 3px solid var(--onerep-black);
            border-radius: 22px;
            box-shadow: 7px 7px 0px var(--onerep-mint);
            padding: 1rem;
            margin-top: 1.25rem;
        }

        .plate-line {
            font-size: 1.15rem;
            font-weight: 800;
            margin: 0.35rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Session State Setup
# -----------------------------
if "competitors" not in st.session_state:
    st.session_state.competitors = []

if "current_lifter_index" not in st.session_state:
    st.session_state.current_lifter_index = 0

if "current_lift" not in st.session_state:
    st.session_state.current_lift = "Snatch"

if "current_attempt" not in st.session_state:
    st.session_state.current_attempt = 1

if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 60

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_start_time" not in st.session_state:
    st.session_state.timer_start_time = None

if "meet_results" not in st.session_state:
    st.session_state.meet_results = []

# -----------------------------
# Helper Functions
# -----------------------------
def get_current_attempt_weight(competitor, lift, attempt):
    if not competitor:
        return 0

    if lift == "Snatch":
        return competitor.get(f"Snatch {attempt}", 0) or 0
    else:
        return competitor.get(f"Clean & Jerk {attempt}", 0) or 0


def get_timer_display():
    if st.session_state.timer_running and st.session_state.timer_start_time is not None:
        elapsed = int(time.time() - st.session_state.timer_start_time)
        remaining = max(st.session_state.timer_seconds - elapsed, 0)

        if remaining == 0:
            st.session_state.timer_running = False
    else:
        remaining = st.session_state.timer_seconds

    minutes = remaining // 60
    seconds = remaining % 60
    return f"{minutes}:{seconds:02d}"


def record_lift_result(result):
    if not st.session_state.competitors:
        return

    competitor = st.session_state.competitors[st.session_state.current_lifter_index]
    weight = get_current_attempt_weight(
        competitor,
        st.session_state.current_lift,
        st.session_state.current_attempt
    )

    lift_key = f"{st.session_state.current_lift} {st.session_state.current_attempt} Result"
    competitor[lift_key] = result

    result_record = {
        "Competitor": competitor["Name"],
        "Lift": st.session_state.current_lift,
        "Attempt": st.session_state.current_attempt,
        "Weight (kg)": weight,
        "Result": result,
    }

    st.session_state.meet_results.append(result_record)


def calculate_plates(total_weight, bar_weight_text):
    try:
        bar_weight = float(bar_weight_text.replace(" kg", ""))
    except Exception:
        bar_weight = 20

    remaining = total_weight - bar_weight

    if remaining <= 0:
        return []

    per_side = remaining / 2
    plate_options = [25, 20, 15, 10, 5, 2.5, 2, 1.5, 1, 0.5]
    plate_icons = {
        25: "🔴",
        20: "🔵",
        15: "🟡",
        10: "🟢",
        5: "⚪",
        2.5: "🔴",
        2: "🔵",
        1.5: "🟡",
        1: "🟢",
        0.5: "⚪",
    }

    plates = []

    for plate in plate_options:
        count = int(per_side // plate)
        if count > 0:
            plates.append({
                "plate": plate,
                "count": count,
                "icon": plate_icons[plate]
            })
            per_side = round(per_side - (count * plate), 2)

    return plates


def render_plate_calculator(total_weight, bar_weight_text):
    plates = calculate_plates(total_weight, bar_weight_text)

    if total_weight <= 0:
        return "<div class='plate-card'><h3>Plate Calculator</h3><p>No attempt weight selected yet.</p></div>"

    if not plates:
        return f"<div class='plate-card'><h3>Plate Calculator</h3><p>Use the empty {bar_weight_text} bar.</p></div>"

    rows = ""
    for plate in plates:
        size_label = "big" if plate["plate"] >= 5 else "little"
        rows += f"<div class='plate-line'>{plate['icon']} {plate['count']} x {plate['plate']} kg {size_label} plate per side</div>"

    return f"""
    <div class='plate-card'>
        <h3>Plate Calculator</h3>
        <p><strong>Total:</strong> {total_weight} kg | <strong>Bar:</strong> {bar_weight_text}</p>
        {rows}
    </div>
    """

# -----------------------------
# View Navigation
# -----------------------------
view = st.sidebar.radio(
    "View",
    ["Admin Control Desk", "Public Display", "Meet Results"]
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="onerep-hero">
        <div class="onerep-kicker">Meet Day Control Desk</div>
        <h1 class="onerep-title">ONE REP<br>Meet Manager</h1>
        <div class="onerep-subtitle">
            A simple, joyful meet-day tool for tracking athletes, bar weight, openers, attempts, and the platform clock.
        </div>
        <div class="onerep-pill-row">
            <span class="onerep-pill">Snatch</span>
            <span class="onerep-pill">Clean & Jerk</span>
            <span class="onerep-pill">15 kg / 20 kg Bar</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Admin Control Desk
# -----------------------------
if view == "Admin Control Desk":
    with st.form("competitor_form", clear_on_submit=True):
        st.markdown("### Enter Competitor Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input("Competitor Name")

        with col2:
            body_weight = st.number_input("Body Weight (kg)", min_value=0.0, step=0.1)

        with col3:
            bar_weight = st.selectbox("Bar Weight", ["15 kg", "20 kg"])

        st.markdown("### Opening Attempts")

        col4, col5 = st.columns(2)

        with col4:
            snatch_opener = st.number_input("Snatch Opener (kg)", min_value=0, step=1)

        with col5:
            clean_jerk_opener = st.number_input("Clean & Jerk Opener (kg)", min_value=0, step=1)

        submitted = st.form_submit_button("Add Competitor")

        if submitted:
            if not name:
                st.error("Please enter a competitor name.")
            else:
                competitor = {
                    "Name": name,
                    "Body Weight (kg)": body_weight,
                    "Bar Weight": bar_weight,
                    "Snatch 1": snatch_opener,
                    "Snatch 2": None,
                    "Snatch 3": None,
                    "Clean & Jerk 1": clean_jerk_opener,
                    "Clean & Jerk 2": None,
                    "Clean & Jerk 3": None,
                    "Best Snatch": None,
                    "Best Clean & Jerk": None,
                    "Total": None,
                }

                st.session_state.competitors.append(competitor)
                st.success(f"Added {name} to the meet.")

    st.divider()
    st.subheader("Platform Attempt Control")

    if st.session_state.competitors:
        names = [c["Name"] for c in st.session_state.competitors]

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            selected_name = st.selectbox(
                "Current Competitor",
                names,
                index=min(st.session_state.current_lifter_index, len(names) - 1)
            )
            st.session_state.current_lifter_index = names.index(selected_name)

        with col_b:
            st.session_state.current_lift = st.selectbox(
                "Current Lift",
                ["Snatch", "Clean & Jerk"],
                index=0 if st.session_state.current_lift == "Snatch" else 1
            )

        with col_c:
            st.session_state.current_attempt = st.selectbox(
                "Attempt",
                [1, 2, 3],
                index=st.session_state.current_attempt - 1
            )

        current_competitor = st.session_state.competitors[st.session_state.current_lifter_index]
        weight = get_current_attempt_weight(
            current_competitor,
            st.session_state.current_lift,
            st.session_state.current_attempt
        )

        st.metric("Current Attempt Weight", f"{weight} kg")
        st.markdown("### Attempt Weight Editor")

edit_col1, edit_col2 = st.columns(2)

with edit_col1:
    st.markdown("#### Snatch Attempts")

    current_competitor["Snatch 2"] = st.number_input(
        "Snatch 2 (kg)",
        min_value=0,
        step=1,
        value=int(current_competitor["Snatch 2"] or 0),
        key=f"sn2_{current_competitor['Name']}"
    )

    current_competitor["Snatch 3"] = st.number_input(
        "Snatch 3 (kg)",
        min_value=0,
        step=1,
        value=int(current_competitor["Snatch 3"] or 0),
        key=f"sn3_{current_competitor['Name']}"
    )

with edit_col2:
    st.markdown("#### Clean & Jerk Attempts")

    current_competitor["Clean & Jerk 2"] = st.number_input(
        "Clean & Jerk 2 (kg)",
        min_value=0,
        step=1,
        value=int(current_competitor["Clean & Jerk 2"] or 0),
        key=f"cj2_{current_competitor['Name']}"
    )

    current_competitor["Clean & Jerk 3"] = st.number_input(
        "Clean & Jerk 3 (kg)",
        min_value=0,
        step=1,
        value=int(current_competitor["Clean & Jerk 3"] or 0),
        key=f"cj3_{current_competitor['Name']}"
    )

        st.markdown("### Judge Decision")
        judge_col1, judge_col2 = st.columns(2)

        with judge_col1:
            if st.button("✅ Pass / Good Lift"):
                record_lift_result("Pass")
                st.success("Lift marked as Pass.")
                st.rerun()

        with judge_col2:
            if st.button("❌ Fail / No Lift"):
                record_lift_result("Fail")
                st.error("Lift marked as Fail.")
                st.rerun()

        st.markdown("### Timer Controls")
        t1, t2, t3, t4 = st.columns(4)

        with t1:
            st.session_state.timer_seconds = st.number_input(
                "Clock Seconds",
                min_value=15,
                max_value=120,
                value=st.session_state.timer_seconds,
                step=15
            )

        with t2:
            if st.button("Start Timer"):
                st.session_state.timer_start_time = time.time()
                st.session_state.timer_running = True
                st.rerun()

        with t3:
            if st.button("Stop Timer"):
                st.session_state.timer_running = False
                st.rerun()

        with t4:
            if st.button("Reset Timer"):
                st.session_state.timer_running = False
                st.session_state.timer_start_time = None
                st.rerun()

        st.markdown(f"### Current Clock: `{get_timer_display()}`")

    else:
        st.info("Add competitors first, then you can control the current platform attempt.")

    st.divider()
    st.subheader("Competitor List")

    if st.session_state.competitors:
        df = pd.DataFrame(st.session_state.competitors)
        df.index = df.index + 1
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Competitor List as CSV",
            data=csv,
            file_name="onerep_competitor_list.csv",
            mime="text/csv"
        )
    else:
        st.info("No competitors added yet.")

    with st.expander("Admin Controls"):
        st.caption("Use these controls carefully during meet setup.")

        if st.button("Clear All Competitors"):
            st.session_state.competitors = []
            st.session_state.current_lifter_index = 0
            st.session_state.timer_running = False
            st.session_state.timer_start_time = None
            st.warning("All competitors have been cleared.")
            st.rerun()

        if st.button("Clear Meet Results"):
            st.session_state.meet_results = []
            st.warning("Meet results have been cleared.")
            st.rerun()

# -----------------------------
# Public Display
# -----------------------------
if view == "Public Display":
    if st.session_state.competitors:
        current_competitor = st.session_state.competitors[st.session_state.current_lifter_index]
        weight = get_current_attempt_weight(
            current_competitor,
            st.session_state.current_lift,
            st.session_state.current_attempt
        )
        timer_display = get_timer_display()

        st.markdown(
            f"""
            <div class="display-card">
                <div class="display-label">Now Lifting</div>
                <div class="display-name">{current_competitor['Name']}</div>
                <div class="display-weight">{weight} kg</div>
                <div class="display-detail-row">
                    <div class="display-detail">{st.session_state.current_lift}</div>
                    <div class="display-detail">Attempt {st.session_state.current_attempt} of 3</div>
                    <div class="display-detail">{current_competitor['Bar Weight']} Bar</div>
                </div>
                <div class="timer-box">{timer_display}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            render_plate_calculator(weight, current_competitor["Bar Weight"]),
            unsafe_allow_html=True
        )

        if st.session_state.timer_running:
            time.sleep(1)
            st.rerun()

    else:
        st.info("No competitors added yet. Add competitors from the Admin Control Desk first.")

# -----------------------------
# Meet Results View
# -----------------------------
if view == "Meet Results":
    st.subheader("Live Meet Results")

    if st.session_state.meet_results:
        results_df = pd.DataFrame(st.session_state.meet_results)
        results_df.index = results_df.index + 1
        st.dataframe(results_df, use_container_width=True)

        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Meet Results as CSV",
            data=csv,
            file_name="onerep_meet_results.csv",
            mime="text/csv"
        )
    else:
        st.info("No lift results recorded yet. Use the Judge Decision buttons in the Admin Control Desk.")
