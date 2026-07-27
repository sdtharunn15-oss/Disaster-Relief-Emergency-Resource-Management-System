from fastapi import Depends, HTTPException, status

from app.oauth2 import get_current_user


def admin_required(current_user=Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )
    return current_user


def coordinator_required(current_user=Depends(get_current_user)):
    if current_user.role not in ["Admin", "Relief Coordinator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin or Relief Coordinator can access this resource."
        )
    return current_user


def volunteer_required(current_user=Depends(get_current_user)):
    if current_user.role != "Volunteer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Volunteer access required."
        )
    return current_user