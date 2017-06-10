TODO
====

*  Handle reloading specific Docker container processes.

   The basic steps to do this being:

   #. Map the ``CERTBOT_HOSTNAME`` environment variable to a running
      Docker container(s).

      .. note:: Possibly using an image tag that contains the hostname.

   #. Trigger ``kill -HUP`` on the matching Docker container(s).
