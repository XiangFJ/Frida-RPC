cd /root/Desktop/supervisor-conf;
/root/.pyenv/shims/supervisorctl stop frida_api;
/root/.pyenv/shims/python /root/Desktop/FridaRpc/run_tester.py;
/root/.pyenv/shims/supervisorctl start frida_api
