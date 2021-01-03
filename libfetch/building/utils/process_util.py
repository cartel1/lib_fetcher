import subprocess


class ProcessUtil:

    @classmethod
    def exec_cmd_and_wait(cls, args, /, std_out=None, std_err=None):
        with subprocess.Popen(args, stdout=std_out, stderr=std_err, text=True) as proc:
            sout, serr = proc.communicate()

            return proc.poll(), sout, serr
