from __future__ import annotations

import os
import tempfile


runtime_dir = os.path.join(tempfile.gettempdir(), "handtrackerai-runtime")
os.makedirs(runtime_dir, exist_ok=True)

# MediaPipe solutions import matplotlib even if plotting is not used.
# Point caches to a writable temp directory and force a non-GUI backend.
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(runtime_dir, "mpl"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(runtime_dir, "xdg-cache"))

