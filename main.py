import random
import string

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

shortened_urls = {}


def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    shorturl = "".join(random.choice(chars) for _ in range(length))
    return shorturl

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form["long_url"]
        custom_slug = request.form.get("custom_slug", "").strip()

        if custom_slug:
            # Check if the requested custom alias is already taken
            if custom_slug in shortened_urls:
                return "Error: That custom short URL is already taken!", 400
            short_url = custom_slug
        else:
            # Fall back to auto-generating a random code
            short_url = generate_short_url()
            while short_url in shortened_urls:
                short_url = generate_short_url()

        shortened_urls[short_url] = long_url
        return f"Shortened URL: {request.url_root}{short_url}"
        
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)