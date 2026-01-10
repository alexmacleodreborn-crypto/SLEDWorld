class ManagerBot:
    """
    Applies Sandy-gating to ledger patterns.
    Approves new symbols only when evidence is stable.
    """

    def __init__(self):
        self.approvals = []
        self.known_symbols = set()

        # thresholds
        self.min_repeats_for_symbol = 6

    def review(self, ledger, world=None):
        if not ledger.events:
            return

        # Example: unlock TV_ON / TV_OFF as stable symbols
        tv_on = 0
        tv_off = 0
        for e in ledger.events[-200:]:
            if e.get("source") in ("observer", "walker"):
                seen = e.get("seen_objects", {})
                tv_state = seen.get("tv_is_on")
                if tv_state is True:
                    tv_on += 1
                if tv_state is False:
                    tv_off += 1

        self._maybe_approve_symbol("TV_ON", tv_on)
        self._maybe_approve_symbol("TV_OFF", tv_off)

        # Example: unlock LIGHT_SIGNATURE if we see light > 0 often enough
        light_hits = 0
        for e in ledger.events[-200:]:
            if e.get("source") == "observer":
                if (e.get("heard", {}).get("sound_level", 0.0) > 0.05) or (e.get("seen", {}).get("light_level", 0.0) > 0.05):
                    light_hits += 1
        self._maybe_approve_symbol("SENSOR_SIGNATURE", light_hits)

    def _maybe_approve_symbol(self, name: str, count: int):
        if name in self.known_symbols:
            return
        if count >= self.min_repeats_for_symbol:
            self.known_symbols.add(name)
            self.approvals.append({
                "symbol": name,
                "count": count,
                "note": "Approved by Manager (stable repeats reached)."
            })

    def snapshot(self):
        return {
            "known_symbols": sorted(list(self.known_symbols)),
            "approvals_count": len(self.approvals),
            "min_repeats_for_symbol": self.min_repeats_for_symbol,
        }