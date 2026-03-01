class LivenessAnalysis:

    def __init__(self, cfg):
        self.cfg = cfg
        self.live_in = {}
        self.live_out = {}
        self.use = {}
        self.defs = {}

    # =====================================================
    # ENTRY
    # =====================================================

    def compute(self):

        self._compute_use_def()
        self._compute_liveness()

        return self.live_in, self.live_out

    # =====================================================
    # USE / DEF
    # =====================================================

    def _compute_use_def(self):

        for block in self.cfg.blocks:

            use = set()
            defs = set()

            for instr in block.instructions:

                # Collect definitions
                if hasattr(instr, "target"):
                    defs.add(instr.target)

                # Collect uses
                for attr in ["left", "right", "value"]:
                    if hasattr(instr, attr):
                        val = getattr(instr, attr)
                        if isinstance(val, str) and val not in defs:
                            use.add(val)

                if hasattr(instr, "args"):
                    for arg in instr.args:
                        if isinstance(arg, str) and arg not in defs:
                            use.add(arg)

                if hasattr(instr, "sources"):  # phi
                    for var in instr.sources.values():
                        if var not in defs:
                            use.add(var)

            self.use[block] = use
            self.defs[block] = defs

    # =====================================================
    # LIVENESS
    # =====================================================

    def _compute_liveness(self):

        for block in self.cfg.blocks:
            self.live_in[block] = set()
            self.live_out[block] = set()

        changed = True

        while changed:
            changed = False

            for block in reversed(self.cfg.blocks):

                old_in = self.live_in[block].copy()
                old_out = self.live_out[block].copy()

                # OUT[B] = union of IN of successors
                new_out = set()
                for succ in block.successors:
                    new_out |= self.live_in[succ]

                self.live_out[block] = new_out

                # IN[B] = USE[B] ∪ (OUT[B] - DEF[B])
                self.live_in[block] = (
                    self.use[block] |
                    (self.live_out[block] - self.defs[block])
                )

                if old_in != self.live_in[block] or old_out != self.live_out[block]:
                    changed = True