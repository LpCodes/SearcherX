# Importing necessary modules
import wikipedia
from flask import Flask, render_template, request

# Creating an instance of the Flask class
app = Flask(__name__)

# Registering the 'zip' function as a Jinja2 filter
app.jinja_env.filters["zip"] = zip

# Setting the cache-control header to disable caching of static files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# A function to search Wikipedia for the given keyword
def finder_x(keyword):
    results = wikipedia.search(keyword, results=8)  # Search Wikipedia for given keyword and limit results to 8
    print(f"Total Results fetched {len(results)}")
    tp = []  # A list to store the page titles
    linksforpage = []  # A list to store the links of the pages
    pageinfoforhtml = []  # A list to store the summaries of the pages
    for x in results:  # Iterate through the search results
        try:
            tp.append(x)
            # Get the URL of the page
            getlink = wikipedia.page(x, auto_suggest=False, redirect=False).url
            linksforpage.append(getlink)
            # Get the summary of the page
            page_summary = wikipedia.summary(
                x, sentences=1, auto_suggest=False, redirect=False
            )
            pageinfoforhtml.append(page_summary)

        except wikipedia.exceptions.PageError as e:
            print(f"wikipedia.page({x}).url not found.")
        except wikipedia.exceptions.DisambiguationError as e:
            pass
    return tp, linksforpage, pageinfoforhtml


# The default route of the Flask application
@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method != "POST":  # If the request method is GET, render the HTML template
        return render_template("index.html")
    userinput = request.form.get("pswd")  # Get the user's input from the form
    heading, links, info = finder_x(f"{userinput}")  # Call the finder_x function to get search results
    userinput = userinput.capitalize()  # Capitalize the user's input

    # Render the HTML template with the search results and user's input
    return render_template(
        "index.html",
        si=userinput,
        lol=zip(heading, links, info),
        sz=list(zip(heading, links, info)),
    )


# The main driver function of the Flask application
if __name__ == "__main__":
    app.run()  # Start the Flask application
