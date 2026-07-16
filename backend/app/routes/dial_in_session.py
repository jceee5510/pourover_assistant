from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.dial_in_session import DialInSession
from app.schemas.dial_in_session import (
    DialInSessionCreate,
    DialInSessionUpdate,
    DialInSessionResponse,
    DialInSessionDetailResponse
)


router = APIRouter(
    prefix="/dial-in-sessions",
    tags=["dial-in-sessions"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DialInSessionResponse)
def create_session(
    session: DialInSessionCreate,
    db: Session = Depends(get_db)
):

    new_session = DialInSession(
        coffee_bean_id=session.coffee_bean_id,
        status="ACTIVE",
        goal_type=session.goal_type,
        desired_notes=session.desired_notes,
        preferred_profile=session.preferred_profile
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


@router.get("/", response_model=list[DialInSessionResponse])
def get_sessions(
    db: Session = Depends(get_db)
):

    return db.query(DialInSession).all()


@router.get("/{session_id}", response_model=DialInSessionResponse)
def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
        db.query(DialInSession)
        .filter(DialInSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Dial-in session not found"
        )

    return session


@router.put("/{session_id}", response_model=DialInSessionResponse)
def update_session(
    session_id: int,
    update: DialInSessionUpdate,
    db: Session = Depends(get_db)
):

    session = (
        db.query(DialInSession)
        .filter(DialInSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Dial-in session not found"
        )

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(session, field, value)

    db.commit()
    db.refresh(session)

    return session


@router.delete("/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
        db.query(DialInSession)
        .filter(DialInSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Dial-in session not found"
        )

    db.delete(session)
    db.commit()

    return {
        "message": "Dial-in session deleted"
    }

@router.get(
    "/{session_id}/details",
    response_model=DialInSessionDetailResponse
)
def get_session_details(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
        db.query(DialInSession)
        .filter(DialInSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Dial-in session not found"
        )

    return session