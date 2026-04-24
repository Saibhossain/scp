from scp.core.policy import C_LOW, C_HIGH


def compose_labels(labels):
    if C_LOW in labels:
        return C_LOW
    return C_HIGH