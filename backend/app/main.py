from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from app.farm_agent.langgraph_app import app as langgraph_app
from app.api.utils import save_audio_local, save_image_local
from dotenv import load_dotenv
from app.api import routes as api_routes

load_dotenv()

app = FastAPI(title="FarmAssist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_routes.router, prefix="/api")

@app.post('/api/upload_audio')
async def upload_audio(
    file: UploadFile = File(...), 
    user_id: str = Form(...), 
    lat: float = Form(None), 
    lon: float = Form(None),
    image: UploadFile = File(None)
):
    """
    Save uploaded audio file (and optional image), invoke the LangGraph flow, and return the resulting state.
    """
    audio_path = await save_audio_local(file)
    image_path = None
    if image:
        image_path = await save_image_local(image)
    
    initial_state = {
        "audio_path": audio_path,
        "user_id": user_id,
        "gps": {"lat": lat, "lon": lon},
        "image_path": image_path,
        "messages": []
    }
    try:
        # Use ainvoke for async nodes (respond_node is async)
        result = await langgraph_app.ainvoke(initial_state)
        # Ensure we always have a reply_text
        if not result.get("reply_text"):
            result["reply_text"] = "I processed your audio but couldn't generate a response. Please try again."
        
        # Clean up non-serializable objects for JSON response
        clean_result = {
            "transcript": result.get("transcript", ""),
            "reply_text": result.get("reply_text", ""),
            "crop": result.get("crop"),
            "language": result.get("language"),
            "vision_result": result.get("vision_result"),
            "weather_forecast": result.get("weather_forecast"),
            "tts_path": result.get("tts_path"),
            "user_id": result.get("user_id", user_id),
            "gps": result.get("gps", {"lat": lat, "lon": lon})
        }
        return JSONResponse(clean_result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Return a helpful error response instead of crashing
        return JSONResponse({
            "error": str(e),
            "reply_text": "I apologize, but I'm experiencing technical difficulties processing your audio. Please try again in a moment.",
            "user_id": user_id
        }, status_code=500)

@app.post('/api/upload_image')
async def upload_image(
    image: UploadFile = File(...),
    user_id: str = Form(...),
    lat: float = Form(None),
    lon: float = Form(None),
    question: str = Form("")
):
    """
    Upload image for analysis. Can include optional text question.
    """
    image_path = await save_image_local(image)
    
    initial_state = {
        "audio_path": None,
        "user_id": user_id,
        "gps": {"lat": lat, "lon": lon},
        "image_path": image_path,
        "transcript": question,  # Use question as transcript if provided
        "messages": []
    }
    try:
        # Skip STT if no audio, go directly to intent/vision
        # We'll modify the flow to handle image-only queries
        result = await langgraph_app.ainvoke(initial_state)
        # Ensure we always have a reply_text
        if not result.get("reply_text"):
            result["reply_text"] = "I analyzed your image but couldn't generate a detailed response. Please try again."
        
        # Clean up non-serializable objects for JSON response
        clean_result = {
            "transcript": result.get("transcript", question),
            "reply_text": result.get("reply_text", ""),
            "crop": result.get("crop"),
            "language": result.get("language"),
            "vision_result": result.get("vision_result"),
            "weather_forecast": result.get("weather_forecast"),
            "tts_path": result.get("tts_path"),
            "user_id": result.get("user_id", user_id),
            "gps": result.get("gps", {"lat": lat, "lon": lon})
        }
        return JSONResponse(clean_result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Return a helpful error response instead of crashing
        return JSONResponse({
            "error": str(e),
            "reply_text": "I apologize, but I'm experiencing technical difficulties processing your image. Please try again in a moment.",
            "transcript": question,
            "user_id": user_id
        }, status_code=500)

@app.post('/api/chat')
async def chat(
    message: str = Form(...),
    user_id: str = Form(...),
    lat: float = Form(None),
    lon: float = Form(None),
    image: UploadFile = File(None)
):
    """
    Text-based chatbot endpoint. Can include optional image.
    """
    image_path = None
    if image:
        image_path = await save_image_local(image)
    
    initial_state = {
        "audio_path": None,
        "user_id": user_id,
        "gps": {"lat": lat, "lon": lon},
        "image_path": image_path,
        "transcript": message,  # Use message as transcript
        "messages": [{"role": "user", "content": message}]
    }
    try:
        # For text-only chat, skip STT and go to reasoning
        result = await langgraph_app.ainvoke(initial_state)
        # Ensure we always have a reply_text
        if not result.get("reply_text"):
            result["reply_text"] = "I received your message but couldn't generate a response. Please try again."
        
        # Clean up non-serializable objects for JSON response
        clean_result = {
            "transcript": result.get("transcript", ""),
            "reply_text": result.get("reply_text", ""),
            "crop": result.get("crop"),
            "language": result.get("language"),
            "vision_result": result.get("vision_result"),
            "weather_forecast": result.get("weather_forecast"),
            "tts_path": result.get("tts_path"),
            "user_id": result.get("user_id", user_id),
            "gps": result.get("gps", {"lat": lat, "lon": lon})
        }
        return JSONResponse(clean_result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Return a helpful error response instead of crashing
        error_msg = str(e)
        return JSONResponse({
            "error": error_msg,
            "reply_text": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
            "transcript": message,
            "user_id": user_id
        }, status_code=500)


@app.get('/api/get_tts')
async def get_tts(path: str):
    """
    Return a generated tts mp3 by local path.
    """
    if os.path.exists(path):
        return FileResponse(path, media_type='audio/mpeg', filename=os.path.basename(path))
    return JSONResponse({"error": "file not found"}, status_code=404)
