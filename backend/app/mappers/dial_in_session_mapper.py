from app.models.dial_in_session import DialInSession
from app.schemas.dial_in_session import (
    DialInSessionResponse
)


def session_to_response(
    session: DialInSession
) -> DialInSessionResponse:

    return DialInSessionResponse(
        id=session.id,
        coffee_bean_id=session.coffee_bean_id,
        status=session.status,
        goal_type=session.goal_type,
        desired_notes=session.desired_notes,
        preferred_profile=session.preferred_profile,
        started_at=session.started_at,
        completed_at=session.completed_at,
    )