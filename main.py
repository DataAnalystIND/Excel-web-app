from fastapi import FastAPI, UploadFile, File
import pandas as pd
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

# ✅ Fix CORS Issue (Frontend can now communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Route to Upload and Process Excel File
@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)  # Read uploaded Excel file
        df["Row Number"] = range(1, len(df) + 1)  # Add Row Numbers in Column B

        output_file = "processed_file.xlsx"
        df.to_excel(output_file, index=False)  # Save updated file
        
        return FileResponse(output_file, filename="updated_excel.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# ✅ Test API Endpoint
@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

# ✅ Run the App (For Local Testing)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
