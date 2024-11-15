# app/api/voting_routes.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from db.models.user import User
from db.models.question import Question
from db.models.answer import Answer
from utils.dependencies import verify_in_company

router = APIRouter(tags=["Voting"])

# Upvote a Question
@router.post("/questions/{question_id}/upvote")
async def upvote_question(question_id: str, current_user: User = Depends(verify_in_company)):
    question = await Question.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.upvotes += 1
    await question.save()
    return {"message": "Question upvoted successfully"}

# Upvote an Answer
@router.post("/answers/{answer_id}/upvote")
async def upvote_answer(answer_id: str, current_user: User = Depends(verify_in_company)):
    answer = await Answer.get(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    answer.upvotes += 1
    await answer.save()
    return {"message": "Answer upvoted successfully"}

# Downvote a Question
@router.post("/questions/{question_id}/downvote")
async def downvote_question(question_id: str, current_user: User = Depends(verify_in_company)):
    question = await Question.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.upvotes -= 1
    await question.save()
    return {"message": "Question downvoted successfully"}

# Downvote an Answer
@router.post("/answers/{answer_id}/downvote")
async def downvote_answer(answer_id: str, current_user: User = Depends(verify_in_company)):
    answer = await Answer.get(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    answer.upvotes -= 1
    await answer.save()
    return {"message": "Answer downvoted successfully"}
