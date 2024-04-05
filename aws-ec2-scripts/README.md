# Automating pausing/resuming EC2 instances on AWS

This guide shows how to set up basic scripts for pausing and resuming EC2 instances on AWS from the local terminal, without needing to log into AWS website. The scripts allow you to:

* Start an existing EC2 instance from the terminal while automatically updating the IP address in the local ssh config file.
* Stop an existing EC2 instance from the terminal so that it can be resumed later.

## Installation

* In order to control AWS instances from the terminal, you need to have AWS's command line tool `aws-cli` installed. This can be most easily done using `apt` or `brew` (i.e. run `apt install aws-cli` or `brew install aws-cli`). After installation, you can check that `aws-cli` is installed properly by running: `aws --version`.

## Configuration

Next step is to set up the appropriate config parameters in order to use `aws-cli` to access your EC2 instances. In order to do this, you need to:

* Access your dashboard on the AWS website, go to the top right part with `user@account-id`, click the drop-down menu and select "Security credentials".
* Find the section "Access keys" and then click "Create access key".
* This will create an access key/secret access key pair - the secret key should be noted *immediately* as it is not accessible afterwards.
* The keys should be written within the aws config file on the local machine.
    * The easiest way to do this is to run `aws configure` which will display several prompts to enter the keys.
    * **Note**: You will need to set the appropriate region of the instance during the setup (e.g. `eu-west-1`).
    * Alternatively this can be done manually by creating file `~/.aws/config` with the line:
    ```
    # ~/.aws/config
    [default]
    region = your-region
    ```
    and `~/.aws/credentials` with the lines:
    ```
    # ~/.aws/credentials
    [default]
    aws_access_key_id = YOUR-ACCESS-KEY
    aws_secret_access_key = YOUR-SECRET-KEY
    ```

### Checking it works

In order to check everything is set-up correctly, you can run the following command that should list the names of all existing instances:
```
aws ec2 describe-instances --query "Reservations[].Instances[].Tags[].Value"
```
You can find more info about different commands [here](https://docs.aws.amazon.com/cli/latest/reference/ec2/).

## Scripts

Once set-up, you can refer `.aws_utility` containing the example scripts to start and stop EC2 instances using the client. The file contains two main `bash` functions: `start_ec2_instance` and `stop_ec2_instance`. In order to run them from the terminal, you might consider sourcing `.aws_utility` within your local `.profile` file by appending:
```
# Useful functions for using aws
if [ -f ~/.aws_utility ]; then
	source ~/.aws_utility
fi
```

#### Setting defaults

If you're mainly using one instance, it is useful to set your default instance name in `.aws_utility`. In addition, `start_ec2_instance` automatically sets the IP address of the EC2 instance in your local ssh config file whenever it is resumed, so you can set the default host name of the instance, as well as the path to your ssh config. This is done by changing the following lines in `.aws_utility`:
```
# Use this instance name if no arg passed
DEFAULT_NAME="your-default-instance-name"

# Use this host name in ssh config if no arg passed
DEFAULT_HOST_NAME="aws"

# Path to ssh config
CONFIG_PATH="your-home-path/.ssh/config"
```

The functions will then use the default values unless explicit arguments are passed.

#### Important note for MacOS users!

The script assumes using GNU `sed` command. However, MacOS systems come with BSD version of `sed` that likely won't work with the script. In this case, you can install the GNU version by running `brew install gsed` and changing `sed` to `gsed` in the script.

#### Usage

##### `start_ec2_instance`

The function takes two optional arguments `instance_name` and `host_name`, which are otherwise set to the default values. It then tries to find an existing instance with the name `instance_name`, resumes it, and tries to update your local ssh config file (as set in `CONFIG_PATH`) with the new IP address. The function updates the IP address by finding a block within the config:
```
Host host_name
  HostName instance-ip-address
  ...
```
and changes the `instance-ip-address` value to the new IP address, where `host_name` is either the default value or the second argument passed to the function. If your ssh config is set up differently this might not work correctly.

##### `stop_ec2_instance`

The function takes one optional argument `instance_name`, otherwise using the default value. It tries to find an existing EC2 instance with the given name, and pause it.

#### `get_ec2_ip`

The function takes one optional argument `instance-name`, otherwise using the default value. It prints the current IP address of the instance if set.
