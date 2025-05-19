from flask import Blueprint
from app.agent.agent import AIAgent
from app.agent.schemas import QuestionRequest, AnswerResponse, HealthResponse
from app.utils.error_handlers import handle_errors

bp = Blueprint('api', __name__)

# Initialize agent when blueprint is accessed
agent = None

def get_agent():
    global agent
    if agent is None:
        agent = AIAgent()
    return agent

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test agent availability without processing a question
        return HealthResponse(
            status="healthy",
            message="AI Agent is ready"
        ).dict()
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=str(e)
        ).dict(), 500

@bp.route('/ask', methods=['POST'])
@handle_errors
def ask_question():
    """Endpoint to ask questions to the AI agent"""
    from flask import request  # Local import to avoid circular imports
    data = request.get_json()
    question_request = QuestionRequest(**data)
    
    answer = get_agent().ask(question_request.question)
    
    return AnswerResponse(
        question=question_request.question,
        answer=answer
    ).dict()