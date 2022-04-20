#!/usr/bin/env bash
# Let’s practice using Puppet to make changes to our configuration file
include stdlib
file_line { 'Declare identity file':
  path    => '/etc/ssh/ssh_config',
  line    => '    IdentityFile ~/.ssh/scholl',
  replace => true,
}

file_line { 'Turn off passwd auth':
  path    => '/etc/ssh/ssh_config',
  line    => '    PasswordAuthentication no',
  replace => true,
}
