# Import the necessary modules and functions
from modules import DB_POSTS_ROOT, Blueprint, BytesIO, Log, request, send_file, sqlite3

# Create a blueprint for the return post banner route
returnPostBannerBlueprint = Blueprint("returnPostBanner", __name__)


@returnPostBannerBlueprint.route("/postImage/<int:postID>")
def returnPostBanner(postID):
    """
    This function returns the banner image for a given post ID.

    Args:
        postID (int): The ID of the post for which the banner image is requested.

    Returns:
        The banner image for the given post ID as a Flask Response object.

    """
    Log.database(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Connect to the SQLite database that stores the posts information
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    # Execute a SQL query to select the banner column from the posts table where the id matches the given post ID
    cursor.execute(
        """select banner from posts where id = ? """,
        [(postID)],
    )
    # Fetch the first row of the query result as a tuple and get the first element of the tuple as a bytes object
    image = BytesIO(cursor.fetchone()[0])

    # Log the image data
    Log.info(f"Post: {postID} | Image: {request.base_url} loaded")

    # Send the image as a Flask Response object with the mimetype set to image/png
    return send_file(image, mimetype="image/png")
