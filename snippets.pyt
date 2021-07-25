# def exec_cmd(self, cmd):
#     """ subprocess utility """
#     self.process = Popen(cmd, stdout=PIPE, shell=True)
#     self.stdout, self.stderr = self.process.communicate()
#     self.stdout = self.stdout.decode('utf-8') if self.stdout else None
#     self.stderr = self.stderr.decode('utf-8') if self.stderr else None
#     return self.process.returncode, self.stdout, self.stderr



# Token should be uploaded to object storage and reuse
# self.token_file = os.getcwd()+os.sep+".token"
# if os.path.isfile(self.token_file):
#     rc, stdout, stderr = self.exec_cmd("find "+ os.getcwd() + " -mmin -60 -name '.token' -type f ")
#     if stdout:
#         with open(self.token_file) as _token:
#             self.token = _token.read()
#             if self.token:
#                 logger.info(f"Using token from {self.token_file} ")
#                 return self.token
