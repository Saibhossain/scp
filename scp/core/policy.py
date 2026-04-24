C_HIGH = "C_high"
C_LOW = "C_low"


class Policy:
    def __init__(self):
        self.rules = {
            "send_email": {C_HIGH},
            "write_db": {C_HIGH},
            "delete_file": {C_HIGH},
            "write_note": {C_HIGH, C_LOW},
            "summarize": {C_HIGH, C_LOW},
        }

    def allowed(self, op, label):
        return label in self.rules.get(op, set())