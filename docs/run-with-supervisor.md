# Run with supervisor

You will need one supervisor file per each radio station.
The target is save 24h radio and save 30 minute chunks to Google Cloud Storage.

This is an example to use in ` /etc/supervisor/conf.d/yaasr-RADIONAME.conf`
We assume you have the `google-cloud-storage-credential.json` file at `/home/USER/yaasr` folder

```ini
[program:yaasr-RADIONAME]
command=yaasr compress-and-google-store --stream RADIONAME --bucket_name BUCKET_NAME --google-credentials /home/USER/yaasr/google-cloud-storage-credential.json
directory=/home/USER/yaasr
user=USER
autostart=true
autorestart=true
stdout_logfile=/var/log/yaasr-RADIONAME.log
stderr_logfile=/var/log/yaasr-RADIONAME.log
```

The command could be changed to fit your needs.

You can also create the supervisor files automatically using `yaasr supervisor ALL` or `yaasr supervisor stream-name`
