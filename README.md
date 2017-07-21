hostel-huptainer
----------------
This program's purpose is to handle SIGHUP'ing docker container
processes that have a `org.eff.certbot.cert_cns` label value matching
the supplied string.

The name is a munging together of host, label, SIGHUP and Docker
container; with host coming from hostname, el being 2 letters from
label, hup being from SIGHUP and tainer being from container.

Installation
============
Installation of this program is quite easy, as it only has one external
dependency, and this program includes this dependency in its setup.py
file.

That said, there are 3 ways that you can install this program;

*  You can also install this program from a clone of the source
   repository, as so (remember, if you want to modify the source code
   without re-installing, pass the `-e` flag to PIP):

   `pip install .`

*  You can also use Docker to install/run this program. You can do this
   like so when grabbing from the Docker Hub:

   `docker pull jitsusama/hostel-huptainer`

*  Finally, you can build the image from a clone of the source
   repository like so:

   `docker build -t jitsusama/hostel-huptainer .`

Usage
=====
This program relies on the `CERTBOT_HOSTNAME` environment variable
being present upon invocation, as it's meant to be called somewhere
downstream of a certbot program engaging with a manual-auth-hook or
manual-cleanup-hook invocation.

I developed this program to be used in conjunction with the [lets-do-dns][1]
program. With this in mind, I envision this program primarily being
called by lets-do-dns via the `LETS_DO_POSTCMD` environment variable
being passed to it.

Here's an example of how you can use this program from the CLI directly
when you installed the program via PIP:

```bash
   CERTBOT_HOSTNAME=myhost.mydomain.com \
   hostel-huptainer
```

Here's an example of how you can use this program from the CLI via
certbot/lets-do-dns when you installed the program via PIP:

```bash
   DO_APIKEY=super-secret-key \
   DO_DOMAIN=mydomain.com \
   LETS_DO_POSTCMD=hostel-huptainer \
   certbot certonly --manual -d myhostname.mydomain.com \
       --preferred-challenges dns \
       --manual-auth-hook lets-do-dns \
       --manual-cleanup-hook lets-do-dns
```

Here's an example of how you can use this program from Docker when
you pulled the image from the Docker Hub:

```bash
   docker run -v "$(pwd)/my-cert-dir:/etc/letsencrypt" \
       -v "/var/run/docker.sock:/var/run/docker.sock" \
       -e "DO_APIKEY=super-secret-key" \
       -e "DO_DOMAIN=mydomain.com" \
       -e "LETS_DO_POSTCMD=hostel-huptainer" \
       jitsusama/hostel-huptainer \
       certonly --manual -d myhostname.mydomain.com \
           --preferred-challenges dns \
           --manual-auth-hook lets-do-dns \
           --manual-cleanup-hook lets-do-dns
```

Note:

In both of these circumstances, certbot would be providing the
`CERTBOT_HOSTNAME` environment variable based on the `-d`
hostname supplied via its invocation. The `lets-do-dns` program
is programmed such that it will only call the passed
`hostel-huptainer` program during the manual-cleanup-hook stage.

[1]: https://github.com/jitsusama/lets-do-dns
