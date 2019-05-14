# Builds an AMI on the basis of a specified commit, starting from nothing but git and the checked out commit,
# and leaving only checkout, compilation, and supervisor installation/start to install.py, which runs
# when we spin up an instance.

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


# Assumes we have git installed and the commit the AMI is based on checked out
if __name__ == '__main__':

    # Start by updating installed yum packages
    print 'Running yum update...'
    sys_call('yum -y update')

    # We have to do this so we can use npm with sudo
    sys_call('sudo ln -s /usr/local/bin/node /usr/bin/node', failokay=True)
    sys_call('sudo ln -s /usr/local/lib/node /usr/lib/node', failokay=True)
    sys_call('sudo ln -s /usr/local/bin/npm /usr/bin/npm', failokay=True)
    sys_call('sudo ln -s /usr/local/bin/node-waf /usr/bin/node-waf', failokay=True)

    # Install basic software and dependencies
    print 'Installing Node...'
    sys_call('sudo -u ec2-user git clone https://github.com/tj/n')
    sys_call('cd n; sudo make install')
    sys_call('cd n/bin; sudo ./n  10.15')
    sys_call('rm -rf n')

    print 'Installing other basic dependencies...'
    sys_call('sudo yum install make automake gcc gcc-c++ kernel-devel git-core ruby-devel -y')
    sys_call('sudo yum -y erase ntp*')
    sys_call('sudo yum -y install chrony')
    sys_call('sudo service chronyd start')
    sys_call('sudo chkconfig chronyd on')

    # Need this to use native postgres bindings
    sys_call('yum -y install postgresql-devel', failokay=True)

    # Global NPM dependencies
    sys_call('env PATH=$PATH NODE_PATH=$NODE_PATH npm install -g coffee-script@1.6.3')

    # Reassign links for coffeescript
    sys_call('sudo ln -s /usr/local/bin/coffee /usr/bin/coffee', failokay=True)
    print 'build_ami ran successfully'
