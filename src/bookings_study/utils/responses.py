from fastapi import Response


def build_protected_file_redirect_response(filepath: str):
    headers = {'X-Accel-Redirect': f"/internal_media/{filepath}"}
    response = Response(headers=headers)
    return response
