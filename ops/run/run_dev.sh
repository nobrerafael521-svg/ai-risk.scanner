
set -e

# Run backend in dev mode (Linux / macOS)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../../backend"

cd "$BACKEND_DIR"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

export APP_ENV=development
export APP_HOST=127.0.0.1
export APP_PORT=8000

uvicorn app.main:app --host $APP_HOST --port $APP_PORT --reload
