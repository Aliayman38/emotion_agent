import time
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.schemas import PredictRequest, PredictResponse
from app.graph import agent_graph
from app.state import AgentState
from app.logger import logger

app = FastAPI(
    title="Jordanian Arabic Emotion Classification Agent",
    version="1.0.0",
    description="Production-grade pipeline orchestrating multi-stage classification routines via LangGraph."
)

@app.middleware("http")
async def log_performance_middleware(request: Request, call_next):
    """Global request tracking middleware to measure performance and errors."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} | Execution Duration: {duration:.4f}s | Status: {response.status_code}")
    return response

@app.post(
    "/predict", 
    response_model=PredictResponse, 
    status_code=status.HTTP_200_OK,
    summary="Classify Emotion from Dialect Input"
)
async def predict_emotion(payload: PredictRequest):
    """
    Ingests raw Arabic textual parameters, triggers execution of the underlying 
    agent graph, and yields validated emotion classifications.
    """
    logger.info(f"Inbound routing payload received. Raw Payload: '{payload.text}'")
    
    # Initialize State Schema matching graph specification
    initial_state: AgentState = {
        "input_text": payload.text,
        "normalized_text": None,
        "predicted_emotion": None,
        "confidence_score": None,
        "retry_count": 0,
        "is_valid": False,
        "error_log": None
    }
    
    try:
        # Synchronous execution abstraction of compiled LangGraph
        final_state = agent_graph.invoke(initial_state)
        
        # Verify terminal structural validity execution state
        if not final_state.get("is_valid") and final_state.get("error_log"):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Upstream Model Processing Failure: {final_state.get('error_log')}"
            )
            
        if final_state.get("predicted_emotion") not in ["happy", "sad", "angry", "neutral"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="System was unable to resolve a reliable output matching classification validation types."
            )

        return PredictResponse(
            emotion=final_state["predicted_emotion"],
            confidence=final_state["confidence_score"]
        )
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.critical(f"Unchecked pipeline exception intercepted: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal agent execution exception occurred: {str(e)}"
        )

@app.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
async def health_check():
    """Simple verification probe mapping operational availability."""
    return {"status": "operational", "timestamp": time.time()}