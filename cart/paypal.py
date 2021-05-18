import sys

#from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client = None
        self.client_id = "AW2ZLXfxKaa7yvJHbCADDdNniKGHMvk6fp_C2_5OnS8eMGWmU5oxftwzdHgldQ8M0FciQNswK70cgWpz"
        self.client_secret = "EPCs7Sn-YXnY9FOzt6YiM4ydAn-CHdYWev-jlzLPk5qrrJgnT72IKD11pETHCzOfbfqTtvBxCahi03kr"
        #self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        #self.client = PayPalHttpClient(self.environment)
