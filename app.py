import streamlit as st
import pickle
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --gold:   #F5A623;
    --gold2:  #FFD166;
    --blue:   #0A1628;
    --mid:    #0F2040;
    --card:   #132847;
    --border: rgba(245,166,35,0.25);
    --text:   #E8EDF5;
    --muted:  #7A8BA8;
    --win:    #06D6A0;
    --lose:   #EF476F;
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--blue) !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero banner ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(135deg, #0F2040 0%, #1a3a6e 50%, #0F2040 100%);
    border-radius: 20px;
    border: 1px solid var(--border);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(245,166,35,0.15) 0%, transparent 65%);
}
.hero-badge {
    display: inline-block;
    background: var(--gold);
    color: var(--blue);
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.25rem 0.85rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.8rem, 8vw, 4.5rem);
    letter-spacing: 0.04em;
    line-height: 1;
    background: linear-gradient(135deg, #ffffff 30%, var(--gold2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem;
}
.hero p {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* ── Section label ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold);
    margin: 1.8rem 0 0.6rem;
}

/* ── Card wrapper ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

/* ── VS divider ── */
.vs-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 0.6rem 0;
}
.vs-pill {
    background: var(--gold);
    color: var(--blue);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    border-radius: 50px;
    padding: 0.1rem 0.9rem;
    flex-shrink: 0;
}
.vs-line { flex: 1; height: 1px; background: var(--border); }

/* ── Stat cards ── */
.stats-row {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1 1 100px;
    background: var(--mid);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.stat-card .num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.9rem;
    color: var(--gold2);
    line-height: 1;
}
.stat-card .lbl {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.25rem;
}

/* ── Selectbox / number-input overrides ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: var(--mid) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}

/* ── Predict button ── */
[data-testid="stButton"] > button {
    width: 100%;
    padding: 0.85rem 2rem;
    background: linear-gradient(135deg, var(--gold) 0%, #e8941a 100%);
    color: var(--blue) !important;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.35rem;
    letter-spacing: 0.12em;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 24px rgba(245,166,35,0.35);
    margin-top: 0.5rem;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(245,166,35,0.5);
}

/* ── Result panel ── */
.result-panel {
    background: linear-gradient(135deg, #0d2240 0%, #132847 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem 1.6rem;
    text-align: center;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-panel::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% -20%, rgba(245,166,35,0.12), transparent 60%);
    pointer-events: none;
}
.result-panel h4 {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold);
    margin: 0 0 1.4rem;
}
.result-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.2rem;
}
.result-team {
    flex: 1;
    text-align: center;
}
.result-team .pct {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    line-height: 1;
}
.result-team .name {
    font-size: 0.8rem;
    color: var(--muted);
    font-weight: 500;
    margin-top: 0.3rem;
    line-height: 1.3;
}
.win-color  { color: var(--win); }
.lose-color { color: var(--lose); }

/* ── Progress bar container ── */
.prob-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 50px;
    height: 10px;
    overflow: hidden;
    margin: 0.4rem 0 1rem;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, var(--win), #06a880);
    transition: width 0.8s ease;
}

/* ── Divider ── */
.result-divider {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--gold);
    padding: 0 0.5rem;
    flex-shrink: 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.75rem;
    margin-top: 2.5rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]
cities = [
    'Mumbai', 'Chandigarh', 'Kolkata', 'Hyderabad', 'Chennai', 'Jaipur',
    'Bengaluru', 'Pune', 'Delhi', 'Indore', 'Visakhapatnam', 'Abu Dhabi',
    'Unknown', 'Ahmedabad', 'Dubai', 'Sharjah', 'Navi Mumbai', 'Guwahati'
]

pipe = pickle.load(open('pipe.pkl', 'rb'))

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🏏 Cricket Analytics</div>
    <h1>IPL WIN PREDICTOR</h1>
    <p>Real-time win probability powered by machine learning</p>
</div>
""", unsafe_allow_html=True)

# ── Match Setup ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">⚔️ Match Setup</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('🏏 Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('🎯 Bowling Team', sorted(teams))

selected_city = st.selectbox('📍 Host City', sorted(cities))

st.markdown('<div class="section-label">🎯 Target</div>', unsafe_allow_html=True)
target = st.number_input('Runs Target', min_value=0, step=1)

# ── Live Scorecard ────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">📊 Current Scorecard</div>', unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Current Score', min_value=0, step=1)
with col4:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")
with col5:
    wickets_out = st.number_input('Wickets Fallen', min_value=0, max_value=10, step=1)

# ── Derived quick-stats preview ───────────────────────────────────────────────
if overs > 0 and target > 0:
    runs_left   = int(target - score)
    balls_left  = int(120 - overs * 6)
    crr_val     = round(score / overs)
    rrr_val     = round((runs_left * 6) / balls_left)

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card">
            <div class="num">{runs_left}</div>
            <div class="lbl">Runs Needed</div>
        </div>
        <div class="stat-card">
            <div class="num">{balls_left}</div>
            <div class="lbl">Balls Left</div>
        </div>
        <div class="stat-card">
            <div class="num">{crr_val}</div>
            <div class="lbl">CRR</div>
        </div>
        <div class="stat-card">
            <div class="num">{rrr_val}</div>
            <div class="lbl">RRR</div>
        </div>
        <div class="stat-card">
            <div class="num">{10 - wickets_out}</div>
            <div class="lbl">Wickets Left</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
predict_clicked = st.button('⚡ Predict Win Probability')

if predict_clicked:
    if batting_team == bowling_team:
        st.warning("⚠️ Batting and bowling teams cannot be the same!")
    elif overs == 0:
        st.warning("⚠️ Overs completed must be greater than 0.")
    else:
        runs_left_f  = target - score
        balls_left_f = 120 - (overs * 6)
        wickets_f    = 10 - wickets_out
        crr_f        = score / overs
        rrr_f        = (runs_left_f * 6) / balls_left_f 

        input_df = pd.DataFrame({
            'batting_team':  [batting_team],
            'bowling_team':  [bowling_team],
            'city':          [selected_city],
            'runs_left':     [runs_left_f],
            'balls_left':    [balls_left_f],
            'team_wicket':   [wickets_f],
            'runs_target':   [target],
            'crr':           [crr_f],
            'rrr':           [rrr_f],
        })

        if rrr_f > 36:  # Physically impossible — max 6 sixes in 6 balls
            st.error("⚠️ This scenario is statistically impossible. "
                    "50 runs cannot be scored in 6 balls.")
        elif runs_left_f <= 0:
            st.success("🏆 Batting team has already won!")
        elif balls_left_f <= 0:
            st.error("⛔ No balls remaining — bowling team wins!")
        else:
            result = pipe.predict_proba(input_df)
    # ... show result
        loss = round(result[0][0] * 100)
        win  = round(result[0][1] * 100)

        # Result panel
        st.markdown(f"""
        <div class="result-panel">
            <h4>🔮 Win Probability Analysis</h4>
            <div class="result-row">
                <div class="result-team">
                    <div class="pct win-color">{win}%</div>
                    <div class="name">{batting_team}</div>
                </div>
                <div class="result-divider">VS</div>
                <div class="result-team">
                    <div class="pct lose-color">{loss}%</div>
                    <div class="name">{bowling_team}</div>
                </div>
            </div>
            <div class="prob-bar-wrap">
                <div class="prob-bar-fill" style="width:{win}%"></div>
            </div>
            <p style="color:var(--muted);font-size:0.78rem;margin:0;">
                {"🏆 " + batting_team + " are heavy favourites!" if win >= 70 
                 else "⚖️ It's neck and neck — anyone's game!" if 40 <= win <= 60
                 else "⚠️ " + bowling_team + " are in control!"}
            </p>
        </div>
        """, unsafe_allow_html=True)
