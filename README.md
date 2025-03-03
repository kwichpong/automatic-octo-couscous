# automatic-octo-couscous

The file named getAWSMetadata.py is the Python source code to query AWS EC2 metadata as per the LSEG coding challenge.

To retrieve the EC2 metadata, a reviewer can type the following command on the EC2 servers where you want to extract the metadata.
> python3 getAWSEC2MetaData.py, and then the source code will output the JSON formatted of all EC2’s metadata that this sourcecode resided.  <Screen Recording - 1 Get All EC2 Metadata - is the sample of usage that I tested this source code> 

In case the reviewer would like to query the specific key from EC2 metadata (Bonus Point of the assignment), you can type
> python3 getAWSEC2MetaData.py --key=<specific key name>, and then the source code will throw the specific metadata key in JSON format like the screenshot-2
