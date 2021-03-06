# Handy Shell Snippets

### Wait for a tcp port

Wait for a tcp port is open and accepting connections.
You may want to combine this with a
[timeout](/{{ site.uprefix }}/basic/timeout) and with a
[fail fast](/{{ site.uprefix }}/basic/setup-and-tear-down).

```shell
$ wait_port() {
>     while ! nc -z 127.0.0.1 $1 >/dev/null 2>&1; do sleep 0.5; done
> }

$ wait_port 80  # byexample: +fail-fast +timeout=5              +skip
```

> Ignore the ``+skip`` option.

If instead you want to pick a free port do something like this:

```shell
$ free_port() {
>   for port in {1500..65000}; do netstat -tan | grep -q ":$port " || echo "Port $port" && break; done
> }

$ free_port     # byexample: +fail-fast
Port <port>
```

Like before you may want to combine this with a
[fail fast](/{{ site.uprefix }}/basic/setup-and-tear-down) option and you
can use the
[capture and paste](/{{ site.uprefix }}/basic/capture-and-paste) functionality
to save and use the port later without parsing the output yourself.

### Lock a file

Use ``flock`` to synchronize your programs and avoid a race condition.

Combine this with a
[fail fast](/{{ site.uprefix }}/basic/setup-and-tear-down) to fail quickly
if the lock cannot be obtained and with a
[skip](/{{ site.uprefix }}/basic/setup-and-tear-down) to make your that
you unlock the file at the end:

```shell
$ # try to get the lock, fail fast if we cannot
$ exec {fd}>>test/ds/f && flock -n $fd || echo "Lock failed"  # byexample: +fail-fast

$ # your code here

$ # release the lock, do not skip these steps to avoid deadlocks
$ flock -u $lockfd              # byexample: -skip +pass
$ exec {lockfd}>&-              # byexample: -skip +pass
$ rm -f test/ds/f               # byexample: -skip +pass
```

### Keep tracking a log

You have a program that logs something of you interest *asynchronously*.

You want to check it but you don't want to do a simple ``cat``
because, by the time you do the ``cat``, the your program may not had
change to log.

The solution is to use ``tail -f`` (or ``tailf``) to keep track of
the log file *in the background*, run your program and bring the ``tail``
back to the foreground to do the check.

<!--
# create and wipe the log
$ > test/ds/some.log
-->

Here we do the first part using
[+stop-on-silence](/{{ site.uprefix }}/languages/shell.md) to send it
to the background:

```shell
$ tail -f test/ds/some.log      # byexample: +stop-on-silence
```

The we run the asynchronous command (here you put *your* command)

```shell
$ (sleep 0.5 ; echo "very important message!" >> test/ds/some.log) &
[<job-id>] <pid>
```

And finally, we bring back the ``tail`` and check. We extend the
[timeout](/{{ site.uprefix }}/basic/timeout)
to give the ``echo`` an opportunity to complete and log.

```shell
$ fg %1                         # byexample: +stop-on-timeout +timeout=1
tail -f test/ds/some.log
very important message!
```

> Did you notice the difference between ``+stop-on-silence`` and
> ``+stop-on-timeout``? The former sends the program to the background
> if ``byexample`` does not detect any output from it after a small
> fraction of time (aka silence). The latter does the same but when
> the timeout is over.

Because ``fg %1`` will never end we *need* to
send it the background again and not fail with a timeout.

To finish it, we can kill it like any other process. You typically
do not want to [skip](/{{ site.uprefix }}/basic/setup-and-tear-down) this.

```shell
$ kill %% ; fg ; wait       # byexample: -skip
tail -f test/ds/some.log
Terminated
```
