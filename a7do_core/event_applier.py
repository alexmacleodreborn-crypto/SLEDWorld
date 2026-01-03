def apply_event(a7do, event):
    a7do.body.apply_intensity(event.get("intensity", 0.1))