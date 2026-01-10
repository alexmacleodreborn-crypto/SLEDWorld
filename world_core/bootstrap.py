def tick(self):
    self.frame += 1
    self.space.tick(self.frame)

    # --------------------------------------------------
    # 1. PHYSICAL REALITY & SENSING
    # --------------------------------------------------
    for agent in self.agents:
        if hasattr(agent, "tick"):
            agent.tick(self.clock)
        if hasattr(agent, "observe"):
            agent.observe(self)

    for scout in self.scouts:
        scout.observe(self)

    if self.surveyor:
        self.surveyor.observe(self)

    # --------------------------------------------------
    # 2. INVESTIGATION → LEDGER (RAW ONLY)
    # --------------------------------------------------
    snapshots = []

    for agent in self.agents:
        if hasattr(agent, "snapshot"):
            snapshots.append(agent.snapshot())

    for scout in self.scouts:
        snapshots.append(scout.snapshot())

    if self.surveyor:
        snapshots.append(self.surveyor.snapshot())

    for snap in snapshots:
        events = self.investigator.ingest_snapshot(self.frame, snap)
        for ev in events:
            self.ledger.ingest(ev)

    # --------------------------------------------------
    # 3. SANDY’S LAW GATES (AUTHORITATIVE)
    # --------------------------------------------------
    self.ledger.recompute_gates()

    gates = self.ledger.gates  # <- THIS is the truth

    # --------------------------------------------------
    # 4. HIGHER BOTS (STRICTLY GATED)
    # --------------------------------------------------

    if gates["object_stable"]:
        self.concierge.propose(self.ledger.tail(200))

    if gates["symbol_ready"]:
        lang_events = self.language.ingest_proposals(
            self.concierge.proposals_tail
        )
        for le in lang_events:
            for ev in self.investigator.ingest_snapshot(self.frame, le):
                self.ledger.ingest(ev)

    if gates["structure_stable"]:
        self.architect.generate(self.reception.registry)

    if gates["manager_approved"]:
        self.builder.execute(self.architect.plans_tail())