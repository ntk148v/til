# Reset the ACL system

Source: <https://developer.hashicorp.com/consul/tutorials/security/access-control-troubleshoot#reset-the-acl-system>

If you encounter issues that are unresolvable, or misplace the bootstrap token, you can reset the ACL system by updating index. First, find the leader by `curl`'ing the `/v1/status/leader` endpoint on any node. ACL reset must be performed on the leader.

```shell
curl 172.17.0.1:8500/v1/status/leader
```

In this example, you can verify that the leader is at IP 172.17.0.3. The following commands need to be run on that server.

Re-run the bootstrap command to get the index number.

```shell
consul acl bootstrap

Failed ACL bootstrapping: Unexpected response code: 403 (Permission denied: ACL bootstrap no longer allowed (reset index: 13))
```

Then write the reset index into the bootstrap reset file: (here the reset index is 13):

```shell
echo 13 >> <data-directory>/acl-bootstrap-reset
```

After resetting the ACL system, you can initialize it again and recreate the bootstrap token.
