from fastapi import APIRouter, HTTPException, Query

from .schemas import TeamCreateRequest, TeamInviteOut, TeamInviteRequest, TeamMemberAddRequest, TeamOut
from .state import store

router = APIRouter(prefix="/teams", tags=["teams"])


def _team_to_out(team) -> TeamOut:
    return TeamOut(
        id=team.id,
        name=team.name,
        owner_user_id=team.owner_user_id,
        members=team.members,
        invites=[
            TeamInviteOut(
                id=invite.id,
                email=invite.email,
                invited_by=invite.invited_by,
                status=invite.status,
                created_at=invite.created_at.isoformat(),
            )
            for invite in team.invites
        ],
    )


@router.post("", response_model=TeamOut)
def create_team(body: TeamCreateRequest) -> TeamOut:
    team = store.create_team(name=body.name, owner_user_id=body.owner_user_id)
    return _team_to_out(team)


@router.get("", response_model=list[TeamOut])
def list_teams(user_id: str = Query(...)) -> list[TeamOut]:
    teams = store.list_teams_for_user(user_id)
    return [_team_to_out(team) for team in teams]


@router.post("/{team_id}/invite", response_model=TeamInviteOut)
def invite_member(team_id: str, body: TeamInviteRequest) -> TeamInviteOut:
    invite = store.invite_member(team_id=team_id, email=body.email, invited_by=body.invited_by)
    if not invite:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamInviteOut(
        id=invite.id,
        email=invite.email,
        invited_by=invite.invited_by,
        status=invite.status,
        created_at=invite.created_at.isoformat(),
    )


@router.post("/{team_id}/members", response_model=TeamOut)
def add_member(team_id: str, body: TeamMemberAddRequest) -> TeamOut:
    team = store.add_member(team_id=team_id, user_id=body.user_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return _team_to_out(team)
