from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import joblib, tempfile, os, json
import pandas as pd
from analyze_metrics import analyze_python_file
from pydantic import BaseModel
from typing import Optional

# Init app
app = FastAPI()

# CORS untuk Vue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],  # Vue port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model pipeline
model = joblib.load("model/pca_rf_pipeline.pkl")

# Kolom sesuai dataset training
with open("model/feature_names.json") as f:
    feature_names = json.load(f)

@app.post("/predict")
async def predict_defect(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Ekstrak metrik
        metrics = analyze_python_file(tmp_path)

        print("📊 Extracted Metrics:")
        print(json.dumps(metrics, indent=2))
        print("🔢 Total Metrics:", len(metrics))

        # Buat DataFrame agar sesuai dengan pipeline yang dilatih
        row = [metrics[name] for name in feature_names]
        input_df = pd.DataFrame([row], columns=feature_names)

        # Prediksi & Probabilitas
        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0]

        print(f"🎯 Predict: {bool(pred)}")
        print(f"📈 Probability → Non-defect: {prob[0]:.4f}, Defect: {prob[1]:.4f}")
      
        return {
            "defect": bool(pred),
            "probability": {
                "non_defect": round(prob[0], 4),
                "defect": round(prob[1], 4)
            },
             "metrics": metrics 
        }


    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(tmp_path)


class MetricsInput(BaseModel):
    loc_total: float
    halstead_prog_time: float
    num_operands: float
    loc_code_and_comment: float
    num_operators: float
    loc_executable: float
    halstead_level: float
    branch_count: float
    design_complexity: float
    halstead_length: float
    essential_complexity: float
    loc_comments: float
    halstead_difficulty: float
    num_unique_operators: float
    halstead_error_est: float
    halstead_content: float
    num_unique_operands: float
    halstead_effort: float
    cyclomatic_complexity: float
    halstead_volume: float
    defective: Optional[int] = None  # ground truth, opsional

@app.post("/predict-metrics")
async def predict_from_metrics(data: MetricsInput):
    try:
        input_dict = data.dict()
        y_true = input_dict.pop("defective", None)

        row = [input_dict[name] for name in feature_names]
        input_df = pd.DataFrame([row], columns=feature_names)

        prob = model.predict_proba(input_df)[0]
        prediction = bool(prob[1] > 0.3)  # gunakan threshold 0.3

        result = {
            "defect": prediction,
            "probability": {
                "non_defect": round(prob[0], 4),
                "defect": round(prob[1], 4)
            }
        }

        if y_true is not None:
            result["ground_truth"] = bool(y_true)
            result["correct"] = prediction == bool(y_true)

        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
