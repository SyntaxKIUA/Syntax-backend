from drf_spectacular.utils import OpenApiResponse

search_user = {
    "description": """
        This endpoint allows users to search for other users based on their usernames.

        Users can provide a search query to find matching usernames.
        The search query must be at least 3 characters long.
        If the query is empty or too short, the system will return a validation error.
    """,
    "parameters": [
        {
            "name": "search",
            "in": "query",
            "description": "Search query to filter users by their usernames, firstname and lastname.",
            "required": True,
            "schema": {
                "type": "string",
                "example": "john"
            }
        }
    ],

    "responses": {
        200: OpenApiResponse(
            description="List of users matching the search query.",
            examples={
                "application/json": [
                    {
                        "username": "john_doe",
                        "full_name": "John",
                        "avatar": "media/kbduhdskbj/",
                    }
                ]
            }
        ),
        400: OpenApiResponse(description="The 'search' parameter is required."),
        404: OpenApiResponse(description="No users found matching the search query."),
        422: OpenApiResponse(description="The search query must be at least 3 characters long.")
    }
}
