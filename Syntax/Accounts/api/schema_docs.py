from drf_spectacular.utils import OpenApiResponse

register_view_schema = {
    "description": """
        This endpoint registers a new user and creates a related profile automatically.

        **Required Fields:**
        - `username`: Unique username for the user
        - `email`: Valid email address
        - `phone_number`: Valid phone number
        - `password`: Must be at least 8 characters

        On success, JWT tokens are returned in cookies.
    """,
    "responses": {
        201: OpenApiResponse(description="User registered successfully with JWT tokens."),
        400: OpenApiResponse(description="You are not authenticated."),
        401: OpenApiResponse(description="Authentication credentials were invalid."),
        403: OpenApiResponse(description="You do not have permission to perform this action."),
    }
}


logout_view_schema = {
    "description": """
        Logs out the current user by deleting JWT tokens stored in cookies.

        This endpoint works even if the user is not authenticated,
        but it will silently clear tokens if present.
    """,
    "responses": {
        201: OpenApiResponse(description="User registered successfully with JWT tokens."),
        400: OpenApiResponse(description="You are not authenticated."),
        401: OpenApiResponse(description="Authentication credentials were invalid."),
        403: OpenApiResponse(description="You do not have permission to perform this action."),
    }
}


user_profile_view_schema = {
    "description": """
        Retrieve a user's profile by username.

        - If the authenticated user requests **their own profile**, full private profile data is returned.
        - If the user requests **another user's profile**, only public profile information is returned.

        **Path Parameter:**
        - `username`: The username of the user whose profile you want to retrieve.
    """,
    "responses": {

        200: OpenApiResponse(
            description="""
                        Profile retrieved successfully. 
                        
                        **PrivateProfileSerializer fields:**
                        - `username`: Username of the user
                        
                        - `first_name`: First name of the user
                        - `last_name`: Last name of the user
                        - `bio`: User's bio
                        - `professional`: Boolean indicating if the user is professional
                        - `followings_count`: Number of users this user is following
                        - `followers_count`: Number of users following this user
                        - `posts_count`: Total number of user's posts
                        - `avatar`: URL or file path to user's avatar
                        
                        if user wanted to get his profile will see this field too
                        - `email`: Email address (read-only)
                        - `phone_number`: Phone number (read-only)
                    """
        ),
        403: OpenApiResponse(description="The user is not active."),
        404: OpenApiResponse(description="The user does not exist."),
    }
}