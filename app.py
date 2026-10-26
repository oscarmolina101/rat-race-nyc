import html
import json
import math
import random

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# RAT RACE NYC - VERSION 5
# Automatic 12-month simulation
# Rats run RIGHT TO LEFT
# ============================================================

st.set_page_config(
    page_title="Rat Race NYC",
    page_icon="🐀",
    layout="wide"
)

BUDGET = 100_000
INITIAL = 450

OPTIONS = {
    "A": (
        "Deploy rat traps",
        10_000,
        "Quick removal, limited lasting effect."
    ),
    "B": (
        "Hire exterminators",
        25_000,
        "Strong initial removal, weaker long-term effect."
    ),
    "C": (
        "Increase garbage collection",
        30_000,
        "Reduces the food supply that supports rat growth."
    ),
    "D": (
        "Seal building entry points",
        20_000,
        "Reduces shelter and access to nesting sites."
    ),
    "E": (
        "Organizational Restructuring Initiative",
        15_000,
        "Replace the entire rat control team."
    ),
    "F": (
        "Strategic Advisory Partnership",
        40_000,
        "Commission a prestigious consulting report."
    ),
    "G": (
        "Public Awareness and Engagement Campaign",
        20_000,
        "Launch a citywide anti-rat publicity campaign."
    ),
    "H": (
        "Interagency Rodent Coordination Task Force",
        15_000,
        "Create a new committee to coordinate the response."
    ),
    "I": (
        "Executive Leadership Enhancement",
        25_000,
        "Appoint a Chief Rat Officer."
    ),
}


# ============================================================
# VISUAL DESIGN
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f7f5ef;
    }

    .block-container {
        padding-top: 1.5rem;
    }

    h1, h2, h3 {
        color: #173329;
    }

    .hero {
        background: linear-gradient(115deg, #153d32, #296951);
        color: white;
        padding: 24px 28px;
        border-radius: 18px;
        margin-bottom: 18px;
    }

    .hero h1 {
        color: white;
        font-size: 3.1rem;
        margin: 0;
    }

    .hero p {
        color: #f2f7ee;
        margin: 5px 0 0;
    }

    .badge {
        display: inline-block;
        background: #e3f0da;
        color: #20402d;
        border-radius: 20px;
        padding: 4px 12px;
        font-weight: 700;
        margin-top: 12px;
    }

    .event {
        background: #fff1d8;
        border-left: 6px solid #e8a03d;
        padding: 14px;
        border-radius: 8px;
        margin: 8px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GAME HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🐀 RAT RACE NYC</h1>
        <p>
        A Race to Justice Simulation of Government Spending,
        Political Decisions, and Unintended Consequences
        </p>
        <span class="badge">Available Budget: $100,000</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "A fictional, satirical systems-science game. "
    "All intervention costs, population dynamics, and political "
    "effects are invented for gameplay."
)


# ============================================================
# PLAYER SETUP
# ============================================================

with st.sidebar:

    st.header("🎮 Player setup")

    player = st.text_input(
        "Your name",
        value="Guest",
        max_chars=32
    ).strip() or "Guest"

    seed = st.number_input(
        "Simulation seed",
        min_value=1,
        max_value=999999,
        value=2026,
        step=1
    )

    st.caption(
        "Results are saved to this browser session only. "
        "A shared multiplayer leaderboard requires a database."
    )


# ============================================================
# INTERVENTION SELECTION
# ============================================================

st.subheader("Select up to three interventions")

st.write(
    "Politically attractive proposals may not address "
    "the causes of rat population growth. Choose carefully."
)

cols = st.columns(3)

selected = []

for i, (key, (label, cost, desc)) in enumerate(OPTIONS.items()):

    with cols[i % 3]:

        checked = st.checkbox(
            f"{key}. {label}",
            key=f"option_{key}"
        )

        st.caption(f"${cost:,} · {desc}")

        if checked:
            selected.append(key)


spent = sum(OPTIONS[k][1] for k in selected)

remaining = BUDGET - spent

m1, m2, m3 = st.columns(3)

m1.metric(
    "Selected interventions",
    f"{len(selected)} / 3"
)

m2.metric(
    "Planned spending",
    f"${spent:,}"
)

m3.metric(
    "Remaining budget",
    f"${remaining:,}"
)

valid = (
    1 <= len(selected) <= 3
    and spent <= BUDGET
)

if len(selected) > 3:
    st.error("You can choose at most three interventions.")

if spent > BUDGET:
    st.error("Your plan exceeds the $100,000 budget.")


# ============================================================
# POPULATION SIMULATION
# ============================================================

def simulate(keys, seed_value):

    rng = random.Random(seed_value)

    n = float(INITIAL)

    results = [
        {"Month": 0, "Rats": round(n)}
    ]

    events = []

    for month in range(1, 13):

        growth = 0.30
        capacity = 1150.0

        # Structural interventions

        if "C" in keys:
            growth -= 0.095
            capacity -= 260

        if "D" in keys:
            growth -= 0.075
            capacity -= 180

        # Political and administrative interventions

        if "E" in keys:
            growth += 0.070

        if "F" in keys:
            growth += 0.035

        if "G" in keys:
            growth += 0.018

        if "H" in keys:
            growth += 0.025

        if "I" in keys:
            growth += 0.030

        # Removal interventions

        removal = 0.0

        if "A" in keys:
            removal += (
                0.14 * math.exp(-0.34 * (month - 1))
            )

        if "B" in keys:
            removal += (
                0.31 * math.exp(-0.27 * (month - 1))
            )

        noise = rng.uniform(-0.022, 0.022)

        n += (
            growth * n * (1 - n / capacity)
            - removal * n
            + noise * n
        )

        n = max(10.0, min(n, 1800.0))

        results.append({
            "Month": month,
            "Rats": round(n)
        })

        if month == 5 and "F" in keys:
            events.append(
                '📊 Consultant report delivered: '
                '“New York City has rats.”'
            )

        if month == 3 and "E" in keys:
            events.append(
                "📣 The replacement rat-control team is "
                "still onboarding. The rats are not."
            )

        if month == 7 and "H" in keys:
            events.append(
                "📋 Task force convenes its seventh meeting. "
                "Attendance exceeds trap deployment."
            )

    return pd.DataFrame(results), events


# ============================================================
# START GAME
# ============================================================

if st.button(
    "🚀 DEPLOY THE PROGRAM",
    type="primary",
    disabled=not valid,
    use_container_width=True
):

    data, events = simulate(
        tuple(selected),
        int(seed)
    )

    st.session_state["run"] = {
        "name": player,
        "keys": list(selected),
        "seed": int(seed),
        "spent": spent,
        "data": data,
        "events": events
    }

    st.session_state["show_reveal"] = False


# ============================================================
# ANIMATED CITY
# ============================================================

if "run" in st.session_state:

    run = st.session_state["run"]

    data = run["data"]

    st.divider()

    st.subheader(
        "🏙️ Watch the rat population change"
    )

    st.caption(
        "The simulation automatically advances from Month 0 "
        "to Month 12. Rats run from RIGHT to LEFT, and their "
        "numbers change with the modeled population."
    )

    monthly_counts = [
        int(v)
        for v in data["Rats"].tolist()
    ]

    scene = r"""
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">

    <style>

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        font-family: system-ui, sans-serif;
        background: transparent;
    }

    .scene {
        height: 325px;
        position: relative;
        overflow: hidden;
        border-radius: 18px;

        background: linear-gradient(
            #bde5f5 0 45%,
            #98bd7c 45% 72%,
            #858e85 72%
        );

        border: 3px solid #476d56;
    }

    .building {
        position: absolute;
        bottom: 28%;
        height: 125px;
        width: 100px;
        background: #e2a679;
        border: 4px solid #9d6246;
        border-radius: 5px;
        text-align: center;
        font-size: 44px;
        line-height: 90px;
    }

    .b1 {
        left: 5%;
    }

    .b2 {
        left: 40%;
        background: #d5d0b0;
    }

    .b3 {
        right: 5%;
        background: #b2c8d9;
    }

    .street {
        position: absolute;
        bottom: 12%;
        width: 100%;
        height: 8%;
        background: #626d67;
        border-top: 3px dashed #e9e3a4;
    }

    /* =========================================
       RATS RUN FROM RIGHT TO LEFT
       ========================================= */

    .rat {
        position: absolute;
        font-size: 25px;
        display: block;

        /* Begin outside the RIGHT edge */
        left: 100%;

        animation-name: scurry;
        animation-timing-function: linear;
        animation-iteration-count: infinite;

        filter: drop-shadow(1px 2px 1px #3337);

        will-change: transform;
        pointer-events: none;
    }

    @keyframes scurry {

        0% {
            transform: translateX(30px);
        }

        100% {
            transform: translateX(
                calc(-1 * var(--travel-distance))
            );
        }
    }

    .label {
        position: absolute;
        z-index: 4;
        top: 12px;
        left: 14px;
        background: #fffffff0;
        border-radius: 8px;
        padding: 8px 12px;
        font-weight: 800;
        color: #1c4032;
    }

    .controls {
        position: absolute;
        z-index: 5;
        right: 12px;
        top: 12px;
        display: flex;
        gap: 6px;
    }

    button {
        border: 0;
        border-radius: 8px;
        background: #194d3c;
        color: white;
        font-size: 13px;
        font-weight: 700;
        padding: 9px 12px;
        cursor: pointer;
    }

    button:hover {
        background: #2c7358;
    }

    .bar {
        position: absolute;
        z-index: 5;
        bottom: 4px;
        left: 0;
        height: 5px;
        background: #f3d46c;
        width: 0;
        transition: width .3s;
    }

    </style>
    </head>

    <body>

    <div class="scene" id="scene">

        <div class="building b1">🏠</div>
        <div class="building b2">🏢</div>
        <div class="building b3">🏪</div>

        <div class="street"></div>

        <div class="label" id="status">
            MONTH 0 · 450 RATS
        </div>

        <div class="controls">

            <button id="pause">
                ⏸ Pause
            </button>

            <button id="replay">
                ↻ Replay
            </button>

        </div>

        <div class="bar" id="progress"></div>

    </div>

    <script>

    const counts = __COUNTS__;

    const scene = document.getElementById("scene");
    const status = document.getElementById("status");
    const progress = document.getElementById("progress");

    const pause = document.getElementById("pause");
    const replay = document.getElementById("replay");

    const pool = [];

    let month = 0;
    let playing = true;

    const maxIcons = Math.min(
        95,
        Math.max(
            1,
            Math.round(Math.max(...counts) / 12)
        )
    );

    function updateTravelDistance() {

        const distance = scene.clientWidth + 90;

        scene.style.setProperty(
            "--travel-distance",
            distance + "px"
        );
    }

    updateTravelDistance();

    window.addEventListener(
        "resize",
        updateTravelDistance
    );

    // Create the animated rats

    for (let i = 0; i < maxIcons; i++) {

        const el = document.createElement("span");

        el.className = "rat";
        el.textContent = "🐀";

        el.style.top = (
            30 + Math.random() * 52
        ) + "%";

        // Different rats have different speeds

        const duration = 7 + Math.random() * 9;

        el.style.animationDuration = (
            duration + "s"
        );

        // Stagger the rats across the scene

        el.style.animationDelay = (
            -Math.random() * duration + "s"
        );

        el.style.zIndex = "2";

        scene.appendChild(el);

        pool.push(el);
    }

    // Update population each month

    function showMonth() {

        const count = counts[month];

        const visible = Math.min(
            pool.length,
            Math.max(
                1,
                Math.round(count / 12)
            )
        );

        pool.forEach((el, i) => {

            el.style.display = (
                i < visible ? "block" : "none"
            );

        });

        status.textContent =
            `MONTH ${month} · ${count.toLocaleString()} RATS`;

        progress.style.width = (
            month / 12 * 100
        ) + "%";
    }

    // Pause or resume

    function setPlaying(value) {

        playing = value;

        pause.textContent = (
            value ? "⏸ Pause" : "▶ Play"
        );

        pool.forEach(el => {

            el.style.animationPlayState = (
                value ? "running" : "paused"
            );

        });
    }

    pause.onclick = () => {

        if (month === 12 && !playing) {
            month = 0;
            showMonth();
        }

        setPlaying(!playing);
    };

    // Replay the simulation

    replay.onclick = () => {

        month = 0;

        showMonth();

        setPlaying(true);
    };

    showMonth();

    // Advance one month every 1.5 seconds

    setInterval(() => {

        if (!playing) {
            return;
        }

        if (month < 12) {

            month++;

            showMonth();

        } else {

            setPlaying(false);

            pause.textContent = "▶ Play again";
        }

    }, 1500);

    </script>

    </body>
    </html>
    """

    scene = scene.replace(
        "__COUNTS__",
        json.dumps(monthly_counts)
    )

    components.html(
        scene,
        height=340
    )


    # ========================================================
    # SIMULATION RESULTS
    # ========================================================

    c1, c2, c3 = st.columns(3)

    initial = int(data["Rats"].iloc[0])

    final = int(data["Rats"].iloc[-1])

    c1.metric(
        "Initial population",
        f"{initial:,}"
    )

    c2.metric(
        "Population at month 12",
        f"{final:,}",
        delta=f"{final-initial:+,}",
        delta_color="inverse"
    )

    c3.metric(
        "Budget spent",
        f'${run["spent"]:,}'
    )

    chart = px.line(
        data,
        x="Month",
        y="Rats",
        markers=True,
        title="Rat population across 12 months"
    )

    chart.update_layout(
        yaxis_range=[
            0,
            max(
                600,
                int(data["Rats"].max() * 1.12)
            )
        ]
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    for event in run["events"]:

        st.markdown(
            f'<div class="event">'
            f'{html.escape(event)}'
            f'</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # END GAME
    # ========================================================

    if st.button(
        "🏆 FINISH GAME & REVEAL RESULTS",
        use_container_width=True
    ):

        st.session_state["show_reveal"] = True

        if "scores" not in st.session_state:
            st.session_state["scores"] = []

        signature = (
            run["name"],
            tuple(run["keys"]),
            run["seed"],
            final
        )

        if not any(
            x["signature"] == signature
            for x in st.session_state["scores"]
        ):

            st.session_state["scores"].append({
                "name": run["name"],
                "rats": final,
                "signature": signature
            })


    # ========================================================
    # HALL OF RAT FAME
    # ========================================================

    if st.session_state.get("show_reveal"):

        st.warning(
            "🚨 THE RATS ARE BACK! "
            "Short-term removal can be undone when food, "
            "shelter, and growth conditions remain."
        )

        st.success(
            f'**{html.escape(run["name"])} finished '
            f'with {final:,} rats.** '
            f'Lower sustained populations rank higher.'
        )

        st.markdown(
            "### 🏆 Hall of Rat Fame"
        )

        titles = [
            (
                "🥇",
                "The Ratfather 🐀",
                "The undisputed ruler of NYC's rat population"
            ),
            (
                "🥈",
                "Ratscal",
                "Almost defeated the rats, but not quite"
            ),
            (
                "🥉",
                "Chief Rat Enabler",
                "Somehow made the rats feel welcome"
            )
        ]

        scores = sorted(
            st.session_state.get("scores", []),
            key=lambda s: s["rats"]
        )[:3]

        table = []

        for i, entry in enumerate(scores):

            medal, title, meaning = titles[i]

            table.append({
                "Rank": medal,
                "Award": title,
                "Player": entry["name"],
                "Rats remaining": entry["rats"],
                "Meaning": meaning
            })

        st.dataframe(
            pd.DataFrame(table),
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "**Systems-science lesson:** "
            "Optimizing one part of a system doesn't "
            "necessarily improve the whole system.\n\n"
            "**Better approach:** Coordinate removal "
            "with lasting reductions in food sources, "
            "shelter, and conditions that sustain "
            "population growth."
        )

        st.caption(
            "Leaderboard is session-only and not shared "
            "across devices. Rat dynamics are illustrative, "
            "not a validated NYC forecasting model."
        )

else:

    st.info(
        "Choose up to three interventions, stay within "
        "budget, and deploy to see what happens over 12 months."
    )