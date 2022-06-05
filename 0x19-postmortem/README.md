# POSTMORTEM

- Start time: 04/06/22 9:00 AM,
The wordpress page was returning a 500 status code, so the page was down for a 100% of the users.
Root cause: typo in a wordpress settings document.


The software team was monitoring the project at the time of release, and they found that it was not working. Also some users reported the problem.

The software team monitored running processes on the server using 'ps auxf' to see if any unwanted child processes were running in the background and preventing the server from responding.

After seeing that the processes looked fine, the team used 'strace' on some process IDs, including those for apache2 (the web server hosting the wordpress page).
The trace on one of the apache2 processes showed an infinite loop of system calls, so they looked at the second apache2 process, which was calling the accept4() system call and hanging.

After perusing all the errors returned by strace, the team saw that one of them mentioned that a file did not exist: the file that apache2 was trying to access seemed to end in '.phpp', which is not a common extension for a file.

The files in the /var/www/html/ directory were examined one by one, using Vim's pattern matching to try to locate the erroneous .phpp file extension. It was located in the wp-settings.php file. (Line 137, require_once( ABSPATH . WPINC . '/class-wp-locale.php' );).

The final p of the line was removed.

A Puppet manifest was written to automate the bug fix.

Addition
In short, a typo. The WordPress application encountered a critical error in wp-settings.php while trying to load the class-wp-locale.phpp file. The correct file name, located in the wp-content directory of the app folder, was class-wp-locale.php.

The patch involved a simple typo fix, removing the final p.

Prevention
This outage was not a web server error, but an application error. To prevent such cuts from advancing, note the following.

Test the app before you deploy it. This error would have arisen and could have been fixed sooner if the app had been tested.

To fix this bug, a Puppet manifest was written: 0-strace_is_your_friend.pp, which will perform the fix for any identical bugs should they occur in the future. The manifest replaces any phpp extensions in the /var/www/html/wp-settings.php file with php.

 - End time: 04/06/22 12:00 AM
