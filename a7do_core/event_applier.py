from .gating import allow_event

def apply_event(a7do, event):
    if not allow_event(event["intensity"]):
        a7do.log.add("event gated (overload)")
        return

    a7do.perceived.update_place(event["place"])
    a7do.body.apply_intensity(event["intensity"])
    a7do.familiarity.reinforce(event["pattern"])
    a7do.log.add(
        f"experienced pattern={event['pattern']} place={event['place']}"
    )