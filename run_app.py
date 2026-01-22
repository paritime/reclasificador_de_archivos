import streamlit.web.cli as stcli
import os, sys, traceback

# Redirect output to a log file for debugging crashes
# In production, you might want to remove this or keep it for troubleshooting
sys.stdout = open("app.log", "a", buffering=1)
sys.stderr = sys.stdout

def log(msg):
    print(msg)
    sys.stdout.flush()

def resolve_path(path):
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(sys.executable)
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)

if __name__ == "__main__":
    try:
        log("Starting Launcher...")
        app_path = resolve_path("app.py")
        
        # Fallback for onedir mode if app.py is in _internal (common in recent PyInstaller)
        if not os.path.exists(app_path):
            fallback = os.path.join(os.path.dirname(sys.executable), "_internal", "app.py")
            if os.path.exists(fallback):
                app_path = fallback
        
        log(f"App path: {app_path}")
        
        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--global.developmentMode=false",
        ]
        
        log("Launching Streamlit...")
        stcli.main()
        
    except SystemExit as e:
        log(f"App exited: {e}")
    except Exception as e:
        log(f"CRITICAL ERROR: {e}")
        traceback.print_exc()
