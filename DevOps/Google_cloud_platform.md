# Google Cloud Platform references
https://console.cloud.google.com
- **Note**: the browser shell doesn't work in Firefox; use Chrome.

## Set up VM Instance

Given a new project and being shared Gary's Into-hdp project for access to his VM...

1. Compute Engine > VM Instances > **CREATE INSTANCE**
    - Name: `hdp3a`
    - Region: `us-east4` (Northern Virginia)
    - Zone: `us-east4-c`

    ![Set name and zone](img/vmsetup-01a-region.png)
2. Machine configuration
    - General-purpose
    - Series: `N1`
    - Machine type: `Custom`, 6-8 cores, 39GB memory

    ![Create instance](img/vmsetup-01b-machine.png)
3. Boot disk
    - **Change**
    - **Custom images** > Show image from: `Into-hdp`
    - Image: `hdp3-into-1-hive-spark`
    - Boot disk type: `standard persistent disk`
    - Size (GB): `32` (depends on your usage)

    ![Boot disk](img/vmsetup-02-boot_disk.png)
4. Click to show more **Management, security, disks, networking, sole tenancy**
5. Management
    - Preemptibility: `On`

    ![Preemptibility](img/vmsetup-03-preemptibility.png)
6. Networking
    - Hostname: `hdp3.c.test`

    ![Hostname](img/vmsetup-04-hostname.png)
7. **Create**


---

## Starting up (after setup)
1. Select your own project (not Into-hdp, that's just for access to the VM image during setup)
2. Go to **Compute Engine > VM instances**, select `hdp3a`, and click **Start**

![Start up VM](img/vm-01-start.png)

3. (Windows/Mac) Start a cloud shell by clicking the icon in the upper right corner

![Start cloud shell](img/vm-02-cloud_shell.png)

4. Connect to the vm with one of the `gcloud` commands below
    * This step must be done in the browser cloud shell on macOS (and probably Windows),  but in Linux it can be run in any shell.
5. (Windows/Mac) To open Ambari dashboard, click the web preview button in the upper right of the console window, then **Preview on port 8080**
    * (Linux) go directly to `localhost:8080` in a browser (or whichever port you need)

![Web preview](img/vm-03-preview_port.png)

---

## Google Cloud Console

### Connecting to VM via SSH
```
$ gcloud compute ssh --ssh-flag="-L 8080:localhost:8080" --zone us-east4-c hdp3a
...
[dtork@hdp3 ~]$
```

#### For accessing other services as well

| Port | Use           |
|------|---------------|
| 8080 | Ambari        |
| 9995 | Zeppelin      |
| 9200 | Elasticsearch |
| 5601 | Kibana        |
| 8088 | YARN          |

```
$ gcloud compute ssh --ssh-flag="-L 8080:localhost:8080
-L 9995:localhost:9995
-L 9200:localhost:9200
-L 5601:localhost:5601" \
--zone us-east4-c hdp3a
...
[dtork@hdp3 ~]$
```

### Running various services/programs

#### General steps
1. root into application (to get `you@app $` prompt)
2. run application
3. exit app and login before attempting another

```
### HIVE ###
[dtork@hdp3 ~]$ sudo su - hive
[hive@hdp3 ~]$ hive
0: jdbc:hive2://hdp3.c.test:2181/default>
...
[hive@hdp3 ~]$ exit
logout
[dtork@hdp3 ~]$


### HDFS ###
[dtork@hdp3 ~]$ sudo su - hdfs
[hdfs@hdp3 ~]$ hdfs dfs -ls /
...

[hdfs@hdp3 ~]$ exit
logout
[dtork@hdp3 ~]$


### SPARK ###
[dtork@hdp3 ~]$ sudo su - spark
[spark@hdp3 ~]$ spark-shell
scala>
...
[spark@hdp3 ~]$ exit
logout
[dtork@hdp3 ~]$


### YARN ###
[dtork@hdp3 ~]$ sudo su - yarn
[yarn@hdp3 ~]$ yarn application -list
...
[yarn@hdp3 ~]$ exit
logout
[dtork@hdp3 ~]$


# etc.
```

## Ambari
For managing services (HDFS, Hive, Spark, Zeppelin, etc.)

1. ensure you've SSH'd into the VM (above)
2. On the console, use the Web Preview button for port 8080. It will open Ambari with a url like so:  
`https://8080-dot-11416846-dot-devshell.appspot.com/?authuser=0`  
but with a different number between the `dot`s
    * When asked for a login, use "admin" for both
3. Click `...` next to **Services** and choose **Start All**
    * ![Start All services](img/ambari-01-start_all.png)
4. Wait for services to start (should take about 6-7 minutes)
    * ![Background operations progress](img/ambari-02-progress.png)

## Other services on different ports
* replace `8080` in the URL above used to access Ambari with the port you want to preview.
* remove any junk at the end of the URL

### When finished
Remember to stop all services when you're done, then shut down the GCP VM instance

1. Click `...` next to **Services** and choose **Stop All**
2. Wait for services to stop (should take about 1:30)

## Zeppelin

1. Make sure you've specified port 9995 when you ssh'd in (see above)
2. Browse to: https://9995-dot-11416846-dot-devshell.appspot.com/?authuser=0

## Storage
* Better to store on HDFS, in the `/tmp/` dir
    - can also put it into the `/user/spark`, `/user/hive/`, `/user/zeppelin`
    folders for easier access from those programs
* copying: Cloud SCP is easier! G Cloud ssh
    - https://cloud.google.com/sdk/gcloud/reference/compute/scp
