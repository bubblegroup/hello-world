# Compiles and sets up supervisor. Designed to quickly spin up an instance on the basis of
# an AMI that does almost all the work.

import subprocess

def sys_call(args,cwd=None, failokay=False, async=False, hide_output=False):
    print 'running ' + args
    process = subprocess.Popen(args, cwd=cwd, shell=True, stdout=(subprocess.PIPE if hide_output else None), stderr=subprocess.STDOUT)
    ret = process.poll() if async else process.wait()
    if ret is not None and ret != 0:
        if hide_output:
            print process.stdout.read()
        if failokay:
            print ('warning, call failed: ' + args)
        else:
            raise Exception('call failed: ' + args)
    return process



if __name__ == '__main__':

    # NPM ci, retrying because sometimes it fails erroneously
    try:
        print '\n\nRunning npm ci\n\n'
        sys_call('sudo -u ec2-user env PATH=$PATH NODE_PATH=$NODE_PATH npm ci')
    except:
        print '\n\n\nnpm ci failed the first time, so retrying\n\n\n'
        sys_call('sudo -u ec2-user env PATH=$PATH NODE_PATH=$NODE_PATH npm ci')

    sys_call("sudo chown -R ec2-user /usr/local/")
    # Compile coffeescript
    sys_call('coffee -c ..')
    
    # Install supervisor
    print 'Installing & configuring supervisor...'
    sys_call('sudo pip install supervisor==3.1', failokay=True)
    sys_call('sudo ln -s /usr/local/bin/supervisord /usr/bin/supervisord', failokay=True)
    sys_call('sudo ln -s /usr/local/bin/supervisorctl /usr/bin/supervisorctl', failokay=True)

    # Configure superviosr with name and path of the program to run
    name = 'hello_world'
    command = 'node /home/ec2-user/hello-world/hello_world.js'
    directory = '/home/ec2-user/hello-world'
    sys_call('/usr/local/bin/echo_supervisord_conf > tmp')
    sys_call('cat >> tmp <<\'EOF\'\n\n[program:' + name + ']\ncommand=' + command + '\nenvironment=UV_THREADPOOL_SIZE=128\ndirectory=' + directory + '\n\nEOF')
    sys_call("echo '* soft nofile 1000000\n* hard nofile 1000000\n* soft nproc 1000000\n* hard nproc 1000000' | sudo tee /etc/security/limits.d/large.conf")
    sys_call('sudo su -c"mv tmp /etc/supervisord.conf"')

    # Create the autostart script
    commands = """
    # Start supervisor on startup
    sudo -u ec2-user -H sh -c "export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin; supervisord"

    # Map port 80 -> 8080
    sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
    # Map port 443 -> 8043
    sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8043

    # Modify tcp keepalive
    sudo sysctl -w net.ipv4.tcp_keepalive_time=10
    sudo sysctl -w net.ipv4.tcp_keepalive_intvl=5
    sudo sysctl -w net.ipv4.tcp_keepalive_probes=10
    """
    sys_call('cat > /tmp/autostart <<\'EOF\'\n' + commands + '\n\nEOF')
    sys_call('sudo su -c"cat /tmp/autostart >> /etc/rc.local"')
    sys_call('rm /tmp/autostart')

    # Since we aren't restarting the server, we need to do the stuff in the autostart script right away
    sys_call('sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080')
    sys_call('sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8043')
    sys_call('sudo sysctl -w net.ipv4.tcp_keepalive_time=10')
    sys_call('sudo sysctl -w net.ipv4.tcp_keepalive_intvl=5')
    sys_call('sudo sysctl -w net.ipv4.tcp_keepalive_probes=10')

    # Start supervisor
    print 'Starting supervisor...'
    sys_call('sudo -u ec2-user supervisord -c /etc/supervisord.conf')