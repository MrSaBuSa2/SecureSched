from fastapi import APIRouter, HTTPException
router = APIRouter()
@router.get("/schedules")
async def get_schedules():
    return [{"id": 1, "name": "Meeting with Bob"}, {"id": 2, "name": "Project deadline"}]     