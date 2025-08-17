# The following class is required for any extension we create.
from burp import IBurpExtender
# The following 2 are for Intruder payload generator.
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList

import random

# Define the following class extending the following 2 classes as arguments.
class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        # This method is used to register our class for Intruder to be aware of payload generation.
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        return

    # Returns the name of the payload generator.
    def getGeneratorName(self):
        return 'PYTHON2 Payload Generator'

    # Receives the attack parameter and and return an instance of the "IIntruderPayloadGenerator".
    # Note that it is now called "PFuzzer".
    def createNewInstance(self, attack):
        return PFuzzer(self, attack)

class PFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender = extender
        self.helpers = extender._helpers
        self._attack = attack
        # The 2 vaiables inform Burp whether we've finished fuzzing.
        self.max_payloads = 10
        self.num_iterations = 0

        return

    # Checks whether we've reached the macimum number of fuzzing iterations.
    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    # Responsible for the fuzzing process
    def getNextPayload(self, current_payload):
        # The 'current_payload' variable arrives as a byte array, so we convert it using the following:
        payload = "".join(chr(x) for x in current_payload)
        # We then pass it to the fuzing method 'mutate_payload'.
        payload = self.mutate_payload(payload)
        self.num_iterations += 1
        return payload

    def reset(self):
        self.num_iterations = 0
        return

    # This is the fuzzing method, the core of fuzzing.
    def mutate_payload(self, original_payload):
        # Pick a simple mutatir or even call an external script.
        picker = random.randint(1, 3)

        # Select a random offset in the payload to mutate.
        offset = random.randint(0, len(original_payload) - 1)
        # Take the payload and split it into 2 random chunks, front and back.
        front, back = original_payload[:offset], original_payload[offset:]

        # Then choose a random mutator:
        # 3/1 Random offset insert a SQL injection attempt by adding single quote at the end of front chunk.
        if picker == 1:
            front += "'"

        # 3/2 Jam an XSS attempt in the end of front junk.
        elif picker == 2:
            front += "<script>alert('PYTHON2!');</script>"

        # 3/3 Select a random chunk from the original and repeat it a random number of times.
        # Then add the result to the end of the 'front' chunk.
        elif picker == 3:
            chunk_length = random.randint(0, len(back) - 1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]
        # Add the 'back' chunk to the altered 'front' chunk to complete the mutated payload.
        return front + back
