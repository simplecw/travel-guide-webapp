from fastapi import Header, HTTPException


def require_editor(role: str = Header(default="viewer")):
    if role != "editor":
        raise HTTPException(403, "需要编辑权限")


def require_viewer(role: str = Header(default="viewer")):
    return True