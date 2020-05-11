class DeadDaemonException(Exception):
    def __str__(self):
        return "already dead daemon"

class DaemonNotProducingBlock(Exception):
    def __str__(self):
        return "daemon does not produce block"

class FinishedWithError(Exception):
    def __str__(self):
        return "process was finished with error"

class InvalidContractRunType(Exception):
    def __str__(self):
        return "invalid contract run type (valid only 'wasm', 'hash', 'name', or 'uref')"
