# 🏏 IPL Win Predictor

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55+-FF4B4B?style=for-the-badge&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Model-F7931E?style=for-the-badge&logo=scikit-learn)

> **Real-time IPL win probability predictor powered by Machine Learning** — enter live match conditions and get instant win probabilities for both teams.

🔗 **Live Demo:** [ipl-win-predictor-18.streamlit.app](https://ipl-win-predictor-18.streamlit.app)

---

## ✨ Features

- ⚡ **Real-time predictions** — instant win probability as match conditions change
- 📊 **Live scorecard stats** — runs needed, balls left, CRR, RRR, wickets in hand
- 🎯 **Visual probability bar** — animated win/loss split between both teams
- 🏟️ **Venue-aware** — supports 18 IPL host cities
- 🛡️ **Edge case handling** — detects impossible scenarios and already-won matches
- 🎨 **Premium dark UI** — custom-designed cricket analytics aesthetic

---

## 🧠 How It Works

The predictor uses a **Logistic Regression pipeline** trained on historical IPL match data. Given live match conditions, it outputs the probability of the batting team winning.

**Input features used by the model:**

| Feature | Description |
|---|---|
| `batting_team` | Team currently batting |
| `bowling_team` | Team currently bowling |
| `city` | Match venue city |
| `runs_left` | Runs still needed to win |
| `balls_left` | Balls remaining in the innings |
| `team_wicket` | Wickets in hand |
| `runs_target` | Total target set by first innings |
| `crr` | Current Run Rate |
| `rrr` | Required Run Rate |

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/abishekak18/IPL-Win-Predictor.git
cd IPL-Win-Predictor
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
IPL-Win-Predictor/
├── app.py                        # Streamlit web application
├── pipe.pkl                      # Trained ML pipeline (model + preprocessor)
├── requirements.txt              # Python dependencies
├── IPL_Winner_Prediction.ipynb   # Model training notebook (local only)
└── .gitignore
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + Custom CSS |
| ML Model | Scikit-learn (Logistic Regression) |
| Data Processing | Pandas, NumPy |
| Deployment | Streamlit Community Cloud |

---

## 📦 Dependencies

```
streamlit
pandas
numpy
scikit-learn
```

---

## 🏟️ Supported Teams

| Team |
|---|
| Chennai Super Kings |
| Mumbai Indians |
| Royal Challengers Bangalore |
| Kolkata Knight Riders |
| Sunrisers Hyderabad |
| Rajasthan Royals |
| Delhi Capitals |
| Kings XI Punjab |

---

## 📊 Model Training

The model was trained on IPL match data (`IPL.csv`) using a Scikit-learn pipeline:
- **Preprocessing:** One-Hot Encoding for categorical features (team, city)
- **Model:** Logistic Regression
- **Output:** Win probability for batting team (0–100%)

The trained pipeline is serialized as `pipe.pkl` and loaded at runtime.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

