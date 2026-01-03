import time
from experience_layer.sensory_drip import sensory_drip

# -----------------------------
# Continuous sensory drip loop
# -----------------------------

if a7do.is_awake:
    # Advance world time gently
    clock.advance(0.25)  # 15 minutes of world time

    # Apply background sensory exposure
    drip = sensory_drip(world, "hospital" if not a7do.birthed else "home")
    apply_event(a7do, drip)

    # Slow the UI loop (Streamlit-safe)
    time.sleep(0.5)