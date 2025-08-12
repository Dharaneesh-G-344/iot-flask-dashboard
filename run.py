# from app import Create_app

# app = Create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0",port=5000 ,debug=True)


# run.py  (paste in project root)
import os
from app import create_app   # if your app/__init__.py has a factory called create_app
# OR if app/__init__.py already creates `app`, use: from app import app

try:
    app = create_app()      # try factory mode
except Exception:
    # fallback: import app directly if create_app doesn't exist
    from app import app     # type: ignore

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
